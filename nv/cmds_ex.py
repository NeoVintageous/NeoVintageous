# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import stat
import subprocess
import sys

from sublime import ENCODED_POSITION
from sublime import find_resources
from sublime import FORCE_GROUP
from sublime import LITERAL
from sublime import load_resource
from sublime import MONOSPACE_FONT
from sublime import ok_cancel_dialog
from sublime import platform
from sublime import Region
from sublime import set_timeout
from sublime_plugin import TextCommand

from NeoVintageous.nv import shell
from NeoVintageous.nv import variables
from NeoVintageous.nv.ex.parser import parse_command_line
from NeoVintageous.nv.jumplist import jumplist_update
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.state import State
from NeoVintageous.nv.ui import ui_blink
from NeoVintageous.nv.vi import abbrev
from NeoVintageous.nv.vi import utils
from NeoVintageous.nv.vi.core import ViCommandMixin
from NeoVintageous.nv.vi.search import find_all_in_range
from NeoVintageous.nv.vi.settings import set_global
from NeoVintageous.nv.vi.settings import set_local
from NeoVintageous.nv.vi.utils import adding_regions
from NeoVintageous.nv.vi.utils import first_sel
from NeoVintageous.nv.vi.utils import has_dirty_buffers
from NeoVintageous.nv.vi.utils import resolve_insertion_point_at_b
from NeoVintageous.nv.vi.utils import row_at
from NeoVintageous.nv.vim import console_message
from NeoVintageous.nv.vim import get_logger
from NeoVintageous.nv.vim import message
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.window import window_split
from NeoVintageous.nv.window import window_tab_control
from NeoVintageous.nv.window import WindowAPI

__all__ = [
    '_nv_run_ex_text_cmd'
]

_log = get_logger(__name__)


def _changing_cd(f, *args, **kwargs):
    def inner(*args, **kwargs):
        try:
            state = State(args[0].view)
        except AttributeError:
            state = State(args[0].window.active_view())

        old = os.getcwd()
        try:
            # FIXME: Under some circumstances, like when switching projects to
            # a file whose _cmdline_cd has not been set, _cmdline_cd might
            # return 'None'. In such cases, change to the actual current
            # directory as a last measure. (We should probably fix this anyway).
            os.chdir(state.settings.vi['_cmdline_cd'] or old)
            f(*args, **kwargs)
        finally:
            os.chdir(old)

    return inner


class _ExWindowCommand:
    def __init__(self, window):
        self.window = window


class _ExTextCommand:
    def __init__(self, view):
        self.view = view


# TODO [refactor] into a decorator
class _ExTextCommandBase(_ExTextCommand):

    def _serialize_sel(self):
        sels = [(r.a, r.b) for r in list(self.view.sel())]
        self.view.settings().set('ex_data', {'prev_sel': sels})

    def _deserialize_sel(self, name='next_sel'):
        return self.view.settings().get('ex_data')[name] or []

    def _set_sel(self):
        sel = self._deserialize_sel()
        self.view.sel().clear()
        self.view.sel().add_all([Region(b) for (a, b) in sel])

    # TODO [refactor] into module function so dependencies on this class can be removed
    def set_next_sel(self, data):
        self.view.settings().set('ex_data', {'next_sel': data})

    def _set_mode(self):
        state = State(self.view)
        state.enter_normal_mode()
        self.view.run_command('_enter_normal_mode')

    def run(self, edit, *args, **kwargs):
        self._serialize_sel()
        self._run(edit, *args, **kwargs)
        self._set_sel()
        self._set_mode()


# TODO [refactor] into _nv_cmdline non-interactive command
class _nv_run_ex_text_cmd(TextCommand):
    def run(self, edit, name, command_line, *args, **kwargs):
        _log.debug('_nv_run_ex_text_cmd -> %s with %s %s in %s %s', name, args, kwargs, self.view.id(), self.view.file_name())  # noqa: E501

        module = sys.modules[__name__]
        ex_cmd = getattr(module, name, None)
        parsed = parse_command_line(command_line)

        try:
            ex_cmd(self.view).run(
                edit=edit,
                line_range=parsed.line_range,
                forceit=parsed.command.forced,
                **parsed.command.params
            )
        except TypeError:
            raise  # TODO e.g. possible exception 'TypeError'> run() missing 1 required positional argument: 'name'  # noqa: E501


# TODO [refactor]
def do_ex_command(window, name, args=None):
    _log.debug('do ex command -> %s %s', name, args)

    name = name.title().replace('_', '')
    if not name.startswith('Ex'):
        name = 'Ex' + name

    if args is None:
        args = {'command_line': name[2:].lower()}

    module = sys.modules[__name__]
    ex_cmd = getattr(module, name, None)

    if ex_cmd:
        _log.debug('prepared ex command -> %s %s %s', name, args, ex_cmd)

        if issubclass(ex_cmd, _ExWindowCommand):
            parsed = parse_command_line(args['command_line'])

            # We don't want the ex commands using this.
            del args['command_line']

            args.update(parsed.command.params)

            try:
                ex_cmd(window).run(
                    line_range=parsed.line_range,
                    forceit=parsed.command.forced,
                    **args
                )
            except TypeError:
                raise  # TODO e.g. possible exception 'TypeError'> run() missing 1 required positional argument: 'name'  # noqa: E501

        elif issubclass(ex_cmd, _ExTextCommand):
            # Text commands need edit tokens and they can only be created by
            # Sublime Text commands, so we need to wrap the command in a ST text
            # command.
            args['name'] = name
            window.run_command('_nv_run_ex_text_cmd', args)
        else:
            raise RuntimeError('unknown ex cmd type {}'.format(ex_cmd))
    else:
        raise RuntimeError('unknown ex cmd {}'.format(name))


class ExGoto(_ExWindowCommand, ViCommandMixin):

    def run(self, line_range, *args, **kwargs):
        r = line_range.resolve(self._view)
        line_nr = row_at(self._view, r.a) + 1

        # TODO: .enter_normal_mode has access to self.state.mode
        self.enter_normal_mode(mode=self.state.mode)
        self.state.enter_normal_mode()

        jumplist_update(self.window.active_view())
        self.window.run_command('_vi_go_to_line', {'line': line_nr, 'mode': self.state.mode})
        jumplist_update(self.window.active_view())
        self._view.show(self._view.sel()[0])


# https://vimhelp.appspot.com/help.txt.html
class ExHelp(_ExWindowCommand, ViCommandMixin):

    _tags_cache = {}

    def run(self, subject=None, forceit=False, *args, **kwargs):
        if not subject:
            subject = 'help.txt'

            if forceit:
                return message("E478: Don't panic!")

        subject = subject.lower()

        if not self._tags_cache:
            console_message('initializing help tags...')

            tags_resources = [r for r in find_resources(
                'tags') if r.startswith('Packages/NeoVintageous/res/doc/tags')]

            if not tags_resources:
                return message('tags file not found')

            tags_matcher = re.compile('^([^\\s]+)\\s+([^\\s]+)\\s+(.+)$')
            tags_resource = load_resource(tags_resources[0])
            for line in tags_resource.split('\n'):
                if line:
                    match = tags_matcher.match(line)
                    self._tags_cache[match.group(1).lower()] = (match.group(2), match.group(3))

            console_message('finished initializing help tags')

        if subject not in self._tags_cache:
            # Basic hueristic to find nearest relevant help e.g. `help ctrl-k`
            # will look for "ctrl-k", "c_ctrl-k", "i_ctrl-k", etc. Another
            # example is `:help copy` will look for "copy" then ":copy".
            found = False
            for m in (':', 'c_', 'i_', 'v_', '-', '/'):
                _subject = m + subject
                if _subject in self._tags_cache:
                    found = True
                    subject = _subject

            if not found:
                return message('E149: Sorry, no help for %s' % subject)

        tag = self._tags_cache[subject]

        doc_resources = [r for r in find_resources(
            tag[0]) if r.startswith('Packages/NeoVintageous/res/doc/')]

        if not doc_resources:
            return message('Sorry, help file "%s" not found' % tag[0])

        def window_find_open_view(window, name):
            for view in self.window.views():
                if view.name() == name:
                    return view

        help_view_name = '%s [vim help]' % (tag[0])
        view = window_find_open_view(self.window, help_view_name)
        if view:
            self.window.focus_view(view)

        if not view:
            view = self.window.new_file()
            view.set_scratch(True)
            view.set_name(help_view_name)

            settings = view.settings()
            settings.set('auto_complete', False)
            settings.set('auto_indent', False)
            settings.set('auto_match_enabled', False)
            settings.set('draw_centered', False)
            settings.set('draw_indent_guides', False)
            settings.set('line_numbers', False)
            settings.set('match_selection', False)
            settings.set('rulers', [])
            settings.set('scroll_past_end', False)
            settings.set('smart_indent', False)
            settings.set('tab_size', 8)
            settings.set('translate_tabs_to_spaces', False)
            settings.set('trim_automatic_white_space', False)
            settings.set('word_wrap', False)

            view.assign_syntax('Packages/NeoVintageous/res/Help.sublime-syntax')
            view.run_command('insert', {'characters': load_resource(doc_resources[0])})
            view.set_read_only(True)

        # Format the tag so that we can
        # do a literal search rather
        # than regular expression.
        tag_region = view.find(tag[1].lstrip('/'), 0, LITERAL)

        # Add one point so that the cursor is
        # on the tag rather than the tag
        # punctuation star character.
        c_pt = tag_region.begin() + 1

        view.sel().clear()
        view.sel().add(c_pt)
        view.show(c_pt, False)


# https://vimhelp.appspot.com/various.txt.html#:%21
# https://vimhelp.appspot.com/various.txt.html#:%21%21
class ExShellOut(_ExTextCommand):
    _last_command = None

    @_changing_cd
    def run(self, edit, cmd, line_range, *args, **kwargs):
        if cmd == '!':
            if not self._last_command:
                return status_message('no previous command')

            cmd = self._last_command

        # TODO: store only successful commands.
        self._last_command = cmd

        try:
            if not line_range.is_empty:
                shell.filter_thru_shell(
                    view=self.view,
                    edit=edit,
                    regions=[line_range.resolve(self.view)],
                    cmd=cmd
                )
            else:
                # TODO Read output into output panel.
                out = shell.run_and_read(self.view, cmd)

                output_view = self.view.window().create_output_panel('vi_out')
                output_view.settings().set("line_numbers", False)
                output_view.settings().set("gutter", False)
                output_view.settings().set("scroll_past_end", False)
                output_view = self.view.window().create_output_panel('vi_out')
                output_view.run_command('append', {'characters': out,
                                                   'force': True,
                                                   'scroll_to_end': True})
                self.view.window().run_command("show_panel", {"panel": "output.vi_out"})
        except NotImplementedError:
            message('not implemented')


# TODO [refactor] shell commands to use common os nv.ex.shell commands
class ExShell(_ExWindowCommand, ViCommandMixin):

    # This command starts a shell. When the shell exits (after the "exit"
    # command) you return to Sublime Text. The name for the shell command comes
    # from:
    # * VintageousEx_linux_terminal setting on Linux
    # * VintageousEx_osx_terminal setting on OSX
    # The shell is opened at the active view directory. Sublime Text keeps a
    # virtual current directory that most of the time will be out of sync with
    # the actual current directory. The virtual current directory is always set
    # to the current view's directory, but it isn't accessible through the API.

    @_changing_cd
    def run(self, *args, **kwargs):

        if platform() == 'linux':
            term = self._view.settings().get('VintageousEx_linux_terminal')
            term = term or os.environ.get('COLORTERM') or os.environ.get('TERM')
            if not term:
                return message('terminal not found')

            try:
                self._open_shell([term, '-e', 'bash']).wait()
            except Exception as e:
                return message('error executing command through shell {}'.format(e))

        elif platform() == 'osx':
            term = self._view.settings().get('VintageousEx_osx_terminal')
            term = term or os.environ.get('COLORTERM') or os.environ.get('TERM')
            if not term:
                return message('terminal not found')

            try:
                self._open_shell([term, '-e', 'bash']).wait()
            except Exception as e:
                return message('error executing command through shell {}'.format(e))

        elif platform() == 'windows':
            self._open_shell(['cmd.exe', '/k']).wait()
        else:
            message('not implemented')

    def _open_shell(self, command):
        return subprocess.Popen(command, cwd=os.getcwd())


# https://vimhelp.appspot.com/insert.txt.html#:r
# TODO [review] This command looks unused
# TODO [refactor] shell commands to use common os nv.ex.shell commands
class ExRead(_ExTextCommand):

    @_changing_cd
    def run(self, edit, cmd, line_range, *args, **kwargs):
        r = line_range.resolve(self.view)
        target_point = min(r.end(), self.view.size())

        if cmd:
            if platform() == 'linux':
                # TODO: make shell command configurable.
                shell_cmd = self.view.settings().get('linux_shell')
                shell_cmd = shell_cmd or os.path.expandvars("$SHELL")
                if not shell_cmd:
                    return message('no shell found')

                try:
                    p = subprocess.Popen([shell_cmd, '-c', cmd], stdout=subprocess.PIPE)
                except Exception as e:
                    return message('error executing command through shell {}'.format(e))

                self.view.insert(edit, target_point, p.communicate()[0][:-1].decode('utf-8').strip() + '\n')

            elif platform() == 'windows':
                # TODO [refactor] shell commands to use common os nv.ex.shell commands
                from NeoVintageous.nv.shell_windows import get_oem_cp
                from NeoVintageous.nv.shell_windows import get_startup_info
                p = subprocess.Popen(['cmd.exe', '/C', cmd],
                                     stdout=subprocess.PIPE,
                                     startupinfo=get_startup_info())
                cp = 'cp' + get_oem_cp()
                rv = p.communicate()[0].decode(cp)[:-2].strip()
                self.view.insert(edit, target_point, rv.strip() + '\n')

            else:
                return message('not implemented')
        else:
            # Read a file into the current view.
            # According to Vim's help, :r should read the current file's content
            # if no file name is given, but Vim doesn't do that.
            # TODO: implement reading a file into the buffer.
            return message('not implemented')


# https://vimhelp.appspot.com/windows.txt.html#:ls
class ExPromptSelectOpenFile(_ExWindowCommand):

    def run(self, *args, **kwargs):
        self.file_names = [self._get_view_info(view) for view in self.window.views()]
        self.view_ids = [view.id() for view in self.window.views()]
        self.window.show_quick_panel(self.file_names, self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        sought_id = self.view_ids[index]
        for view in self.window.views():
            # TODO: Start looking in current group.
            if view.id() == sought_id:
                self.window.focus_view(view)

    def _get_view_info(self, v):
        path = v.file_name()
        if path:
            parent, leaf = os.path.split(path)
            parent = os.path.basename(parent)
            path = os.path.join(parent, leaf)
        else:
            path = v.name() or str(v.buffer_id())
            leaf = v.name() or 'untitled'

        status = []
        if not v.file_name():
            status.append("t")
        if v.is_dirty():
            status.append("*")
        if v.is_read_only():
            status.append("r")

        if status:
            leaf += ' (%s)' % ', '.join(status)

        return [leaf, path]


# TODO All the map related commands can probably be refactored into one command
# with a parameter that detimines what action to take.
# https://vimhelp.appspot.com/map.txt.html#:noremap
class ExNoremap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, command, *args, **kwargs):
        if not (keys and command):

            # TODO [refactor] Instead of calling status_message(), raise a
            # NotImplemented exception instead, and let the command runner
            # handle it. All other commands should do the same in cases like
            # this.

            return status_message('Listing key mappings is not implemented')

        # TODO The mappings functions are not used much. Generally, they are
        # used in ex map related commands, and in the rc file. As such, the
        # module is good candidate for refactoring into a descrete module like
        # the rc module e.g. mappings.add(), mappings.remove(), etc.

        # TODO The mappings functions could probably accept a list of modes.

        mappings_add(NORMAL, keys, command)
        mappings_add(OPERATOR_PENDING, keys, command)
        mappings_add(VISUAL, keys, command)
        mappings_add(VISUAL_BLOCK, keys, command)
        mappings_add(VISUAL_LINE, keys, command)


# https://vimhelp.appspot.com/map.txt.html#:unmap
class ExUnmap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, *args, **kwargs):
        try:
            mappings_remove(NORMAL, keys)
            mappings_remove(OPERATOR_PENDING, keys)
            mappings_remove(VISUAL, keys)
            mappings_remove(VISUAL_BLOCK, keys)
            mappings_remove(VISUAL_LINE, keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:nnoremap
class ExNnoremap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, command, *args, **kwargs):
        if not (keys and command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(NORMAL, keys, command)


# https://vimhelp.appspot.com/map.txt.html#:nunmap
class ExNunmap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, *args, **kwargs):
        try:
            mappings_remove(NORMAL, keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:onoremap
class ExOnoremap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, command, *args, **kwargs):
        if not (keys and command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(OPERATOR_PENDING, keys, command)


# https://vimhelp.appspot.com/map.txt.html#:ounmap
class ExOunmap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, *args, **kwargs):
        try:
            mappings_remove(OPERATOR_PENDING, keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:snoremap
class ExSnoremap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, command, *args, **kwargs):
        if not (keys and command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(SELECT, keys, command)


# https://vimhelp.appspot.com/map.txt.html#:sunmap
class ExSunmap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, *args, **kwargs):
        try:
            mappings_remove(SELECT, keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:vnoremap
class ExVnoremap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, command, *args, **kwargs):
        if not (keys and command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(VISUAL, keys, command)
        mappings_add(VISUAL_BLOCK, keys, command)
        mappings_add(VISUAL_LINE, keys, command)


# https://vimhelp.appspot.com/map.txt.html#:vunmap
class ExVunmap(_ExWindowCommand, ViCommandMixin):

    def run(self, keys, *args, **kwargs):
        try:
            mappings_remove(VISUAL, keys)
            mappings_remove(VISUAL_BLOCK, keys)
            mappings_remove(VISUAL_LINE, keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:abbreviate
class ExAbbreviate(_ExWindowCommand, ViCommandMixin):

    def run(self, short=None, full=None, *args, **kwargs):
        if short is None and full is None:
            self.show_abbreviations()
            return

        if not (short and full):
            return message(':abbreviate not fully implemented')

        abbrev.Store().set(short, full)

    def show_abbreviations(self):
        abbrevs = ['{0} --> {1}'.format(item['trigger'], item['contents']) for item in abbrev.Store().get_all()]
        self.window.show_quick_panel(abbrevs, None, flags=MONOSPACE_FONT)


# https://vimhelp.appspot.com/map.txt.html#:unabbreviate
class ExUnabbreviate(_ExWindowCommand, ViCommandMixin):

    def run(self, lhs, *args, **kwargs):
        if lhs:
            return

        abbrev.Store().erase(lhs)


# TODO [review] Is ViCommandMixin required for this command? Review all other commands too.
# https://vimhelp.appspot.com/editing.txt.html#:pwd
class ExPwd(_ExWindowCommand, ViCommandMixin):

    @_changing_cd
    def run(self, *args, **kwargs):
        status_message(os.getcwd())


# https://vimhelp.appspot.com/editing.txt.html#:write
class ExWrite(_ExWindowCommand, ViCommandMixin):

    @_changing_cd
    def run(self, file_name, cmd, forceit, line_range, *args, **kwargs):

        # TODO [refactor] params should used keys compatible with **kwargs, see do_ex_command(). Review other scanners too. # noqa: E501
        options = kwargs.get('++')
        appends = kwargs.get('>>')

        if options:
            return message('++opt isn\'t implemented for :write')

        if cmd:
            return message('!cmd not implememted for :write')

        if not self._view:
            return

        if appends:
            self.do_append(file_name, forceit, line_range)
            return

        if cmd:
            return message('!cmd isn\'t implemented for :write')

        if file_name:
            self.do_write(file_name, forceit, line_range)
            return

        if not self._view.file_name():
            return message("E32: No file name")

        read_only = (self.check_is_readonly(self._view.file_name()) or self._view.is_read_only())

        if read_only and not forceit:
            ui_blink()

            return message("E45: 'readonly' option is set (add ! to override)")

        self.window.run_command('save')

    def check_is_readonly(self, fname):
        """
        Return `True` if @fname is read-only on the filesystem.

        @fname
          Path to a file.
        """
        if not fname:
            return

        try:
            mode = os.stat(fname)
            read_only = (stat.S_IMODE(mode.st_mode) & stat.S_IWUSR != stat.S_IWUSR)
        except FileNotFoundError:
            return

        return read_only

    def do_append(self, file_name, forceit, line_range):
        if file_name:
            self.do_append_to_file(file_name, forceit, line_range)
            return

        r = None
        if line_range.is_empty:
            # If the user didn't provide any range data, Vim appends whe whole buffer.
            r = Region(0, self._view.size())
        else:
            r = line_range.resolve(self._view)

        text = self._view.substr(r)
        text = text if text.startswith('\n') else '\n' + text

        location = resolve_insertion_point_at_b(first_sel(self._view))

        self._view.run_command('append', {'characters': text})

        utils.replace_sel(self._view, Region(self._view.line(location).a))

        self.enter_normal_mode(mode=self.state.mode)
        self.state.enter_normal_mode()

    def do_append_to_file(self, file_name, forceit, line_range):
        r = None
        if line_range.is_empty:
            # If the user didn't provide any range data, Vim writes whe whole buffer.
            r = Region(0, self._view.size())
        else:
            r = line_range.resolve(self._view)

        if not forceit and not os.path.exists(file_name):
            return message("E212: Can't open file for writing: %s" % file_name)

        try:
            with open(file_name, 'at') as f:
                text = self._view.substr(r)
                f.write(text)

            # TODO: make this `show_info` instead.
            return status_message('Appended to ' + os.path.abspath(file_name))

        except IOError as e:
            return message('could not write file {}'.format(str(e)))

    def do_write(self, file_name, forceit, line_range):
        fname = file_name

        if not forceit:
            if os.path.exists(fname):
                ui_blink()

                return message("E13: File exists (add ! to override)")

            if self.check_is_readonly(fname):
                ui_blink()

                return message("E45: 'readonly' option is set (add ! to override)")

        region = None
        if line_range.is_empty:
            # If the user didn't provide any range data, Vim writes whe whole buffer.
            region = Region(0, self._view.size())
        else:
            region = line_range.resolve(self._view)

        assert region is not None, "range cannot be None"

        try:
            expanded_path = os.path.expandvars(os.path.expanduser(fname))
            expanded_path = os.path.abspath(expanded_path)
            with open(expanded_path, 'wt') as f:
                text = self._view.substr(region)
                f.write(text)

            # FIXME: Does this do what we think it does?
            self._view.retarget(expanded_path)
            self.window.run_command('save')

        except IOError as e:
            # TODO: Add logging.
            return message("E212: Can't open file for writing: {}".format(fname))


# https://vimhelp.appspot.com/editing.txt.html#:wa
class ExWall(_ExWindowCommand, ViCommandMixin):

    @_changing_cd
    def run(self, forceit=False, *args, **kwargs):
        # TODO read-only views don't get properly saved.
        for v in (v for v in self.window.views() if v.file_name()):
            if v.is_read_only() and not forceit:
                continue

            v.run_command('save')


# https://vimhelp.appspot.com/editing.txt.html#:file
class ExFile(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        if self._view.file_name():
            fname = self._view.file_name()
        else:
            fname = 'untitled'

        attrs = ''
        if self._view.is_read_only():
            attrs = 'readonly'

        if self._view.is_dirty():
            attrs = 'modified'

        lines = 'no lines in the buffer'
        if self._view.rowcol(self._view.size())[0]:
            lines = self._view.rowcol(self._view.size())[0] + 1

        # fixme: doesn't calculate the buffer's % correctly
        if not isinstance(lines, str):
            vr = self._view.visible_region()
            start_row, end_row = self._view.rowcol(vr.begin())[0], self._view.rowcol(vr.end())[0]
            mid = (start_row + end_row + 2) / 2
            percent = float(mid) / lines * 100.0

        msg = '"' + fname + '"'
        if attrs:
            msg += " [%s]" % attrs
        if isinstance(lines, str):
            msg += " -- %s --" % lines
        else:
            msg += " %d line(s) --%d%%--" % (lines, int(percent))

        status_message('%s' % msg)


# https://vimhelp.appspot.com/change.txt.html#:move
class ExMove(_ExTextCommandBase):

    def _run(self, edit, address, line_range, *args, **kwargs):
        if address is None:
            return message("E14: Invalid address")

        source = line_range.resolve(self.view)
        if any(s.contains(source) for s in self.view.sel()):
            return message("E134: Move lines into themselves")

        # TODO [refactor] is parsing the address necessary, if yes, create a parse_address function
        parsed_address_command = parse_command_line(address).line_range
        destination = parsed_address_command.resolve(self.view)
        if destination == source:
            return

        text = self.view.substr(source)
        if destination.end() >= self.view.size():
            text = '\n' + text.rstrip()

        if destination == Region(-1):
            destination = Region(0)

        if destination.end() < source.begin():
            self.view.erase(edit, source)
            self.view.insert(edit, destination.end(), text)
            self.set_next_sel([[destination.a, destination.b]])
            return

        self.view.insert(edit, destination.end(), text)
        self.view.erase(edit, source)
        self.set_next_sel([[destination.a, destination.a]])


# https://vimhelp.appspot.com/change.txt.html#:copy
class ExCopy(_ExTextCommandBase):

    def _run(self, edit, address, line_range, *args, **kwargs):
        def calculate_address(address):
            # TODO: must calc only the first line ref?
            # TODO [refactor] parsing the address
            calculated = parse_command_line(address)
            if calculated is None:
                return None

            assert calculated.command is None, 'bad address'
            assert calculated.line_range.separator is None, 'bad address'

            return calculated.line_range

        try:
            unresolved = calculate_address(address)
        except Exception:
            return message("E14: Invalid address")

        if unresolved is None:
            return message("E14: Invalid address")

        # TODO: how do we signal row 0?
        target_region = unresolved.resolve(self.view)

        if target_region == Region(-1, -1):
            address = 0
        else:
            row = utils.row_at(self.view, target_region.begin()) + 1
            address = self.view.text_point(row, 0)

        source = line_range.resolve(self.view)
        text = self.view.substr(source)

        if address >= self.view.size():
            address = self.view.size()
            text = '\n' + text[:-1]

        self.view.insert(edit, address, text)

        cursor_dest = self.view.line(address + len(text) - 1).begin()
        self.set_next_sel([(cursor_dest, cursor_dest)])


# TODO Unify with CTRL-W CTRL-O
# https://vimhelp.appspot.com/windows.txt.html#:only
class ExOnly(_ExWindowCommand, ViCommandMixin):

    def run(self, forceit=False, *args, **kwargs):
        if not forceit and has_dirty_buffers(self.window):
            return message("E445: Other window contains changes")

        current_id = self._view.id()
        for view in self.window.views():
            if view.id() == current_id:
                continue

            if view.is_dirty():
                view.set_scratch(True)

            view.close()


# https://vimhelp.appspot.com/change.txt.html#:&&
class ExDoubleAmpersand(_ExWindowCommand, ViCommandMixin):

    def run(self, flags, count, line_range, *args, **kwargs):
        # TODO [review] don't use str(line_range) as the content will be unexpected
        new_command_line = '{0}substitute///{1} {2}'.format(
            str(line_range),
            ''.join(flags),
            count
        )

        do_ex_command(self.window, 'substitute', {'command_line': new_command_line.strip()})


# https://vimhelp.appspot.com/change.txt.html#:substitute
# TODO [enhancement] Implement count.
class ExSubstitute(_ExTextCommand):

    _last_pattern = None
    _last_flags = []
    _last_replacement = ''

    # TODO [refactor] Rename param "search_term" -> "pattern"
    def run(self, edit, search_term, replacement, flags, count, line_range, *args, **kwargs):
        pattern = search_term

        # :s
        if not pattern:
            pattern = ExSubstitute._last_pattern
            replacement = ExSubstitute._last_replacement
            # TODO: Don't we have to reuse the previous flags?
            flags = []

        if not pattern:
            return status_message('E33: No previous substitute regular expression')

        ExSubstitute._last_pattern = pattern
        ExSubstitute._last_replacement = replacement
        ExSubstitute._last_flags = flags

        computed_flags = re.MULTILINE
        computed_flags |= re.IGNORECASE if ('i' in flags) else 0

        try:
            compiled_pattern = re.compile(pattern, flags=computed_flags)
        except Exception as e:
            return message('[regex error]: {} ... in pattern {}'.format((str(e), pattern)))

        target_region = line_range.resolve(self.view)
        if target_region.empty():
            return status_message('E486: Pattern not found: {}'.format(pattern))

        replace_count = 0 if (flags and 'g' in flags) else 1

        if 'c' in flags:
            return self.replace_confirming(edit, pattern, compiled_pattern, replacement, replace_count, target_region)

        lines = self.view.lines(target_region)
        if not lines:
            return status_message('E486: Pattern not found: {}'.format(pattern))

        new_lines = []
        dirty = False
        for line in lines:
            line_str = self.view.substr(line)
            new_line_str = re.sub(compiled_pattern, replacement, line_str, count=replace_count)
            new_lines.append(new_line_str)
            if new_line_str != line_str:
                dirty = True

        new_region_text = '\n'.join(new_lines)
        if self.view.size() > line.end():
            new_region_text += '\n'

        if not dirty:
            return status_message('E486: Pattern not found: {}'.format(pattern))

        # Reposition cursor before replacing target region so that the cursor
        # will auto adjust in sync with the replacement.
        self.view.sel().clear()
        self.view.sel().add(line.begin())

        self.view.replace(edit, target_region, new_region_text)

        # TODO Refactor set position cursor after operation into reusable api.
        # Put cursor on first non-whitespace char of current line.
        line = self.view.line(self.view.sel()[0].b)
        if line.size() > 0:
            pt = self.view.find('^\\s*', line.begin()).end()
            self.view.sel().clear()
            self.view.sel().add(pt)

        self.view.run_command('_enter_normal_mode')

    def replace_confirming(self, edit, pattern, compiled_pattern, replacement,
                           replace_count, target_region):

        last_row = row_at(self.view, target_region.b - 1)
        start = target_region.begin()

        while True:
            if start >= self.view.size():
                break

            match = self.view.find(pattern, start)

            # no match or match out of range -- stop
            if (match == Region(-1)) or (row_at(self.view, match.a) > last_row):
                self.view.show(first_sel(self.view).begin())
                return

            size_before = self.view.size()

            with adding_regions(self.view, 's_confirm', [match], 'comment'):
                self.view.show(match.a, True)
                if ok_cancel_dialog("Confirm replacement?"):
                    text = self.view.substr(match)
                    substituted = re.sub(compiled_pattern, replacement, text, count=replace_count)
                    self.view.replace(edit, match, substituted)

            start = match.b + (self.view.size() - size_before) + 1


# https://vimhelp.appspot.com/change.txt.html#:delete
class ExDelete(_ExTextCommandBase):

    def select(self, regions, register):
        self.view.sel().clear()
        to_store = []
        for r in regions:
            self.view.sel().add(r)
            if register:
                to_store.append(self.view.substr(self.view.full_line(r)))

        if register:
            text = ''.join(to_store)
            if not text.endswith('\n'):
                text = text + '\n'

            state = State(self.view)
            state.registers[register] = [text]

    def _run(self, edit, register, line_range, *args, **kwargs):
        r = line_range.resolve(self.view)
        if r == Region(-1, -1):
            r = self.view.full_line(0)

        self.select([r], register)
        self.view.erase(edit, r)
        self.set_next_sel([(r.a, r.a)])


class ExGlobal(_ExWindowCommand, ViCommandMixin):

    # At the time of writing, the only command that supports :global is the
    # "print" command e.g. print all lines matching \d+ into new buffer:
    #
    #   :%global/\d+/print

    _most_recent_pat = None

    def run(self, pattern, subcommand, line_range, *args, **kwargs):
        if line_range.is_empty:
            global_range = Region(0, self._view.size())
        else:
            global_range = line_range.resolve(self._view)

        if pattern:
            ExGlobal._most_recent_pat = pattern
        else:
            pattern = ExGlobal._most_recent_pat

        if not subcommand:
            subcommand = 'print'

        parsed_subcommand = parse_command_line(subcommand).command

        try:
            matches = find_all_in_range(self._view, pattern, global_range.begin(), global_range.end())
        except Exception as e:
            return message("(global): %s ... in pattern '%s'" % (str(e), pattern))

        # The cooperates_with_global attribute indicates if the command supports
        # the :global command. This is special flag, because all ex commands
        # don't yet support a global_lines argument. See TokenOfCommand. At time
        # of writing, the only command that supports the global_lines argument
        # is the "print" command e.g. print all lines matching \d+ into new
        # buffer: ":%global/\d+/print".
        if not matches or not parsed_subcommand.cooperates_with_global:
            return message("command does not support :global")

        matches = [self._view.full_line(r.begin()) for r in matches]
        matches = [[r.a, r.b] for r in matches]

        do_ex_command(self.window, parsed_subcommand.target_command, {
            'command_line': str(parsed_subcommand),
            'global_lines': matches
        })


# https://vimhelp.appspot.com/various.txt.html#:print
class ExPrint(_ExWindowCommand, ViCommandMixin):

    def run(self, flags, line_range, global_lines=None, *args, **kwargs):
        if self._view.size() == 0:
            return message("E749: empty buffer")

        r = line_range.resolve(self._view)
        lines = self.get_lines(r, global_lines)

        display = self.window.new_file()
        display.set_scratch(True)

        if 'l' in flags:
            display.settings().set('draw_white_space', 'all')

        for (text, row) in lines:
            characters = ''
            if '#' in flags:
                characters = "{} {}".format(row, text).lstrip()
            else:
                characters = text.lstrip()

            display.run_command('append', {'characters': characters})

    def get_lines(self, parsed_range, global_lines):
        # FIXME: this is broken.
        # If :global called us, ignore the parsed range.
        if global_lines:
            return [(self._view.substr(Region(a, b)), row_at(self._view, a)) for (a, b) in global_lines]

        # FIXME This is broken.
        to_display = []
        for line in self._view.full_line(parsed_range):
            text = self._view.substr(line)
            to_display.append((text, row_at(self._view, line.begin())))

        return to_display


# TODO [refactor] into window module
# https://vimhelp.appspot.com/windows.txt.html#:close
class ExClose(_ExWindowCommand, ViCommandMixin):

    def run(self, forceit=False, *args, **kwargs):
        # TODO [refactor] WindowAPI.close_current_view() into a window.function
        WindowAPI(self.window).close_current_view(not forceit)


# TODO [refactor] into window module
# https://vimhelp.appspot.com/editing.txt.html#:q
class ExQuit(_ExWindowCommand, ViCommandMixin):

    def run(self, forceit=False, *args, **kwargs):
        view = self._view
        if forceit:
            view.set_scratch(True)

        if view.is_dirty() and not forceit:
            return message("E37: No write since last change")

        if not view.file_name() and not forceit:
            return message("E32: No file name")

        self.window.run_command('close')

        if len(self.window.views()) == 0:
            self.window.run_command('close')
            return

        # FIXME: Probably doesn't work as expected.

        # Close the current group if there aren't any views left in it.
        if not self.window.views_in_group(self.window.active_group()):
            do_ex_command(self.window, 'unvsplit')


# TODO [refactor] into window module
# https://vimhelp.appspot.com/editing.txt.html#:qa
class ExQall(_ExWindowCommand, ViCommandMixin):

    def run(self, forceit=False, *args, **kwargs):
        if forceit:
            for v in self.window.views():
                if v.is_dirty():
                    v.set_scratch(True)

        elif has_dirty_buffers(self.window):
            return status_message('there are unsaved changes!')

        self.window.run_command('close_all')
        self.window.run_command('exit')


# TODO [refactor] into window module
class ExWq(_ExWindowCommand, ViCommandMixin):

    def run(self, forceit=False, *args, **kwargs):
        if forceit:
            # TODO raise not implemented exception and make the command runner handle it.
            return message('not implemented')

        if self._view.is_read_only():
            return status_message("can't write a read-only buffer")

        if not self._view.file_name():
            return status_message("can't save a file without name")

        self.window.run_command('save')

        do_ex_command(self.window, 'quit')


# https://vimhelp.appspot.com/editing.txt.html#:browse
class ExBrowse(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        self.window.run_command('prompt_open_file', {
            'initial_directory': self.state.settings.vi['_cmdline_cd']
        })


# https://vimhelp.appspot.com/editing.txt.html#:edit
class ExEdit(_ExWindowCommand, ViCommandMixin):

    @_changing_cd
    def run(self, file_name, cmd, forceit=False, *args, **kwargs):
        # TODO [refactor] file_name_arg
        file_name_arg = file_name
        if file_name_arg:
            file_name = os.path.expanduser(os.path.expandvars(file_name_arg))

            if self._view.is_dirty() and not forceit:
                return message("E37: No write since last change")

            if os.path.isdir(file_name):
                # TODO :edit Open a file-manager in a buffer
                return message('Cannot open directory')

            def get_file_path():
                file_name = self._view.file_name()
                if file_name:
                    file_dir = os.path.dirname(file_name)
                    if os.path.isdir(file_dir):
                        return file_dir

                    file_dir = self.state.settings.vi['_cmdline_cd']
                    if os.path.isdir(file_dir):
                        return file_dir

            if not os.path.isabs(file_name):
                file_path = get_file_path()
                if file_path:
                    file_name = os.path.join(file_path, file_name)
                else:
                    return message("could not find a parent directory")

            self.window.open_file(file_name)

            if not os.path.exists(file_name):
                parent = os.path.dirname(file_name)
                if parent and not os.path.exists(parent):
                    msg = '"{}" [New DIRECTORY]'.format(file_name_arg)
                else:
                    msg = '"{}" [New File]'.format(os.path.basename(file_name))

                # Give ST some time to load the new view.
                set_timeout(lambda: status_message(msg), 150)

            return

        if forceit or not self._view.is_dirty():
            self._view.run_command('revert')
            return

        if self._view.is_dirty():
            return message("E37: No write since last change")

        message("E37: No write since last change")


# TODO [refactor] into window module
# https://vimhelp.appspot.com/quickfix.txt.html#:cquit
class ExCquit(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        self.window.run_command('exit')


# TODO [refactor] into window module
# https://vimhelp.appspot.com/editing.txt.html#:exit
class ExExit(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        if self._view.is_dirty():
            self.window.run_command('save')

        self.window.run_command('close')

        if len(self.window.views()) == 0:
            self.window.run_command('exit')


# https://vimhelp.appspot.com/change.txt.html#:registers
class ExRegisters(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        def truncate(string, truncate_at):
            if len(string) > truncate_at:
                return string[0:truncate_at] + ' ...'

            return string

        items = []
        for k, v in self.state.registers.to_dict().items():
            if v:
                if len(v) > 0 and v[0]:
                    lines = v[0].splitlines()
                    value = '^J'.join(lines)

                    # The splitlines function will remove a final newline, if
                    # present. So joining the lines with the join-line indicator
                    # (^J) may be missing a final join-line indicator.
                    if len(''.join(lines)) < len(v[0]):
                        value += '^J'

                    items.append('"{}   {}'.format(k, truncate(value, 78)))

        if items:
            self.window.show_quick_panel(sorted(items), self.on_done, flags=MONOSPACE_FONT)

    def on_done(self, idx):
        if idx == -1:
            return

        self.state.registers['"'] = [list(self.state.registers.to_dict().values())[idx]]


# TODO [refactor] into window module
# https://vimhelp.appspot.com/windows.txt.html#:new
class ExNew(_ExWindowCommand, ViCommandMixin):

    @_changing_cd
    def run(self, *args, **kwargs):
        self.window.run_command('new_file')


# https://vimhelp.appspot.com/windows.txt.html#:yank
class ExYank(_ExTextCommand):

    def run(self, edit, register, count, line_range, *args, **kwargs):
        line_range = line_range.resolve(self.view)

        if not register:
            register = '"'

        text = self.view.substr(line_range)

        state = State(self.view)
        state.registers[register] = [text]
        # TODO: o_O?
        if register == '"':
            state.registers['0'] = [text]


# TODO [refactor] All the "tab" related ex commands can probably be refactored into a single command with actions # noqa: E501


# https://vimhelp.appspot.com/tabpage.txt.html#:tabnext
class ExTabnext(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        # TODO [review] The window related command e.g window_tab_control(), are
        # not used often, at least some of them. Those that are only meant to be
        # used once or twice in the lifecycle of a request can probably be
        # refactored into a  descrete module e.g. windows.tab_control(...).
        window_tab_control(self.window, command='next')


# https://vimhelp.appspot.com/tabpage.txt.html#:tabprevious
class ExTabprevious(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        window_tab_control(self.window, command='prev')


# https://vimhelp.appspot.com/tabpage.txt.html#:tablast
class ExTablast(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        window_tab_control(self.window, command='last')


# https://vimhelp.appspot.com/tabpage.txt.html#:tabfirst
class ExTabfirst(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        window_tab_control(self.window, command='first')


# https://vimhelp.appspot.com/tabpage.txt.html#:tabonly
class ExTabonly(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        window_tab_control(self.window, command='only')


# https://vimhelp.appspot.com/editing.txt.html#:cd
class ExCd(_ExWindowCommand, ViCommandMixin):

    # XXX Currently behaves as on Unix systems for all platforms.

    @_changing_cd
    def run(self, path=None, forceit=False, *args, **kwargs):
        if self._view.is_dirty() and not forceit:
            return message("E37: No write since last change")

        if not path:
            self.state.settings.vi['_cmdline_cd'] = os.path.expanduser("~")

            return do_ex_command(self.window, 'pwd')

        # TODO: It seems there a few symbols that are always substituted when they represent a
        # filename. We should have a global method of substiting them.
        if path == '%:h':
            fname = self._view.file_name()
            if fname:
                self.state.settings.vi['_cmdline_cd'] = os.path.dirname(fname)

                do_ex_command(self.window, 'pwd')

            return

        path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
        if not os.path.exists(path):
            return message("E344: Can't find directory \"%s\" in cdpath" % path)

        self.state.settings.vi['_cmdline_cd'] = path

        do_ex_command(self.window, 'pwd')


class ExCdd(_ExWindowCommand, ViCommandMixin):

    # Non-standard command to change the current directory to the active view's
    # directory. In Sublime Text, the current directory doesn't follow the
    # active view, so it's convenient to be able to align both easily.
    # XXX: Is the above still true?
    # XXX: This command may be removed at any time.

    def run(self, forceit=False, *args, **kwargs):
        if self._view.is_dirty() and not forceit:
            return message("E37: No write since last change")

        path = os.path.dirname(self._view.file_name())

        try:
            self.state.settings.vi['_cmdline_cd'] = path
            status_message(path)
        except IOError:
            message("E344: Can't find directory \"%s\" in cdpath" % path)


# TODO [refactor] into window module
# TODO Refactor like ExSplit
# https://vimhelp.appspot.com/windows.txt.html#:vsplit
class ExVsplit(_ExWindowCommand, ViCommandMixin):

    _MAX_SPLITS = 4

    # TODO Refactor variable access into reusable function because it's also used by ExUnvsplit
    LAYOUT_DATA = {
        1: {"cells": [[0, 0, 1, 1]],
            "rows": [0.0, 1.0],
            "cols": [0.0, 1.0]},
        2: {"cells": [[0, 0, 1, 1], [1, 0, 2, 1]],
            "rows": [0.0, 1.0],
            "cols": [0.0, 0.5, 1.0]},
        3: {"cells": [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]],
            "rows": [0.0, 1.0],
            "cols": [0.0, 0.33, 0.66, 1.0]},
        4: {"cells": [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1], [3, 0, 4, 1]],
            "rows": [0.0, 1.0],
            "cols": [0.0, 0.25, 0.50, 0.75, 1.0]},
    }

    def run(self, file=None, *args, **kwargs):
        groups = self.window.num_groups()
        if groups >= ExVsplit._MAX_SPLITS:
            return message('Can\'t create more groups')

        old_view = self._view
        pos = ''
        current_file_name = None
        if old_view and old_view.file_name():
            pos = ':{0}:{1}'.format(*old_view.rowcol(old_view.sel()[0].b))
            current_file_name = old_view.file_name() + pos

        self.window.run_command('set_layout', ExVsplit.LAYOUT_DATA[groups + 1])

        if file:
            existing = self.window.find_open_file(file)
            pos = ''
            if existing:
                pos = ':{0}:{1}'.format(*existing.rowcol(existing.sel()[0].b))

            return self.open_file(file + pos)

        if current_file_name:
            self.open_file(current_file_name)
        else:
            self.window.new_file()

    def open_file(self, file):
        self.window.open_file(
            file,
            group=(self.window.num_groups() - 1),
            flags=(FORCE_GROUP | ENCODED_POSITION)
        )


# TODO Unify with <C-w>s
# https://vimhelp.appspot.com/windows.txt.html#:split
class ExSplit(_ExWindowCommand, ViCommandMixin):

    def run(self, file=None, *args, **kwargs):
        window_split(self.window, file)


# TODO [review] Either remove or refactor into window module. Preferably remove, because there should be standard commands that can achieve the same thing.  # noqa: E501
class ExUnvsplit(_ExWindowCommand, ViCommandMixin):

    # Non-standard Vim :unvsplit command

    def run(self, *args, **kwargs):
        groups = self.window.num_groups()
        if groups == 1:
            return status_message("can't delete more groups")

        # If we don't do this, cloned views will be moved to the previous group
        # and kept around. We want to close them instead.

        self.window.run_command('close')
        self.window.run_command('set_layout', ExVsplit.LAYOUT_DATA[groups - 1])


# https://vimhelp.appspot.com/options.txt.html#:setlocal
class ExSetlocal(_ExWindowCommand, ViCommandMixin):

    def run(self, option, value, *args, **kwargs):
        if option.endswith('?'):
            return message('not implemented')

        try:
            set_local(self._view, option, value)
        except KeyError:
            status_message('no such option')
        except ValueError:
            status_message('invalid value for option')


# https://vimhelp.appspot.com/options.txt.html#:set
class ExSet(_ExWindowCommand, ViCommandMixin):

    def run(self, option, value, *args, **kwargs):
        if option.endswith('?'):
            return message('not implemented')

        try:
            set_global(self._view, option, value)
        except KeyError:
            status_message('no such option')
        except ValueError:
            status_message('invalid value for option')


# https://vimhelp.appspot.com/eval.txt.html#:let
class ExLet(_ExWindowCommand, ViCommandMixin):

    def run(self, name, value, *args, **kwargs):
        variables.set(name, value)


# https://vimhelp.appspot.com/editing.txt.html#:wqall
class ExWqall(_ExWindowCommand, ViCommandMixin):

    def run(self, *args, **kwargs):
        if not all(v.file_name() for v in self.window.views()):
            ui_blink()

            return message("E32: No file name")

        if any(v.is_read_only() for v in self.window.views()):
            ui_blink()

            return message("E45: 'readonly' option is set (add ! to override)")

        self.window.run_command('save_all')

        # TODO Remove assert statements
        assert not any(v.is_dirty() for v in self.window.views())

        self.window.run_command('close_all')
        self.window.run_command('exit')
