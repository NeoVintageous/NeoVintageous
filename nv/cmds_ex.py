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
from sublime_plugin import WindowCommand

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
from NeoVintageous.nv.vi.core import ViCommandMixin as WindowCommandMixin
from NeoVintageous.nv.vi.search import find_all_in_range
from NeoVintageous.nv.vi.settings import set_global
from NeoVintageous.nv.vi.settings import set_local
from NeoVintageous.nv.vi.utils import adding_regions
from NeoVintageous.nv.vi.utils import first_sel
from NeoVintageous.nv.vi.utils import has_dirty_buffers
from NeoVintageous.nv.vi.utils import resolve_insertion_point_at_b
from NeoVintageous.nv.vi.utils import row_at
from NeoVintageous.nv.vim import console_message
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
    'ExAbbreviate',
    'ExBrowse',
    'ExCdCommand',
    'ExCddCommand',
    'ExClose',
    'ExCopy',
    'ExCquit',
    'ExDelete',
    'ExDoubleAmpersand',
    'ExEdit',
    'ExExit',
    'ExFile',
    'ExGlobal',
    'ExGoto',
    'ExHelp',
    'ExLet',
    'ExMove',
    'ExNew',
    'ExNnoremap',
    'ExNoremap',
    'ExNunmap',
    'ExOnly',
    'ExOnoremap',
    'ExOunmap',
    'ExPrint',
    'ExPrintWorkingDir',
    'ExPromptSelectOpenFile',
    'ExQuitAllCommand',
    'ExQuitCommand',
    'ExReadShellOut',
    'ExRegisters',
    'ExSet',
    'ExSetLocal',
    'ExShell',
    'ExShellOut',
    'ExSnoremap',
    'ExSplit',
    'ExSubstitute',
    'ExSunmap',
    'ExTabfirstCommand',
    'ExTablastCommand',
    'ExTabnextCommand',
    'ExTabonlyCommand',
    'ExTabprevCommand',
    'ExUnabbreviate',
    'ExUnmap',
    'ExUnvsplit',
    'ExVnoremap',
    'ExVsplit',
    'ExVunmap',
    'ExWriteAll',
    'ExWriteAndQuitAll',
    'ExWriteAndQuitCommand',
    'ExWriteFile',
    'ExYank'
]


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


class ExTextCommandBase(TextCommand):

    def serialize_sel(self):
        sels = [(r.a, r.b) for r in list(self.view.sel())]
        self.view.settings().set('ex_data', {'prev_sel': sels})

    def deserialize_sel(self, name='next_sel'):
        return self.view.settings().get('ex_data')[name] or []

    def set_sel(self):
        sel = self.deserialize_sel()
        self.view.sel().clear()
        self.view.sel().add_all([Region(b) for (a, b) in sel])

    def set_next_sel(self, data):
        self.view.settings().set('ex_data', {'next_sel': data})

    def set_mode(self):
        state = State(self.view)
        state.enter_normal_mode()
        self.view.run_command('_enter_normal_mode')

    def run(self, edit, *args, **kwargs):
        self.serialize_sel()
        self.run_ex_command(edit, *args, **kwargs)
        self.set_sel()
        self.set_mode()


class ExGoto(WindowCommand, WindowCommandMixin):

    def run(self, command_line):
        if not command_line:
            # No-op: user issues ':'.
            return

        parsed = parse_command_line(command_line)

        r = parsed.line_range.resolve(self._view)
        line_nr = row_at(self._view, r.a) + 1

        # TODO: .enter_normal_mode has access to self.state.mode
        self.enter_normal_mode(mode=self.state.mode)
        self.state.enter_normal_mode()

        jumplist_update(self.window.active_view())
        self.window.run_command('_vi_go_to_line', {'line': line_nr, 'mode': self.state.mode})
        jumplist_update(self.window.active_view())
        self._view.show(self._view.sel()[0])


# https://vimhelp.appspot.com/help.txt.html
class ExHelp(WindowCommand, WindowCommandMixin):

    _tags_cache = {}

    def run(self, command_line):
        parsed = parse_command_line(command_line)
        if not parsed:
            return

        subject = parsed.command.subject
        if not subject:
            if parsed.command.forced:
                return message("E478: Don't panic!")

            subject = 'help.txt'

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
class ExShellOut(TextCommand):
    _last_command = None

    @_changing_cd
    def run(self, edit, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)
        shell_cmd = parsed.command.command

        if shell_cmd == '!':
            if not self._last_command:
                return status_message('no previous command')

            shell_cmd = self._last_command

        # TODO: store only successful commands.
        self._last_command = shell_cmd

        try:
            if not parsed.line_range.is_empty:
                shell.filter_thru_shell(
                    view=self.view,
                    edit=edit,
                    regions=[parsed.line_range.resolve(self.view)],
                    cmd=shell_cmd
                )
            else:
                # TODO Read output into output panel.
                out = shell.run_and_read(self.view, shell_cmd)

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
class ExShell(WindowCommand, WindowCommandMixin):
    """
    This command starts a shell.

    When the shell exits (after the "exit" command) you return to Sublime Text.
    The name for the shell command comes from:

    * VintageousEx_linux_terminal setting on Linux
    * VintageousEx_osx_terminal setting on OSX

    The shell is opened at the active view directory. Sublime Text keeps a
    virtual current directory that most of the time will be out of sync with the
    actual current directory. The virtual current directory is always set to the
    current view's directory, but it isn't accessible through the API.
    """

    @_changing_cd
    def run(self, command_line=''):
        assert command_line, 'expected non-command line'
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
class ExReadShellOut(TextCommand):

    @_changing_cd
    def run(self, edit, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        r = parsed.line_range.resolve(self.view)
        target_point = min(r.end(), self.view.size())

        if parsed.command.command:
            if platform() == 'linux':
                # TODO: make shell command configurable.
                shell_cmd = self.view.settings().get('linux_shell')
                shell_cmd = shell_cmd or os.path.expandvars("$SHELL")
                if not shell_cmd:
                    return message('no shell found')

                try:
                    p = subprocess.Popen([shell_cmd, '-c', parsed.command.command], stdout=subprocess.PIPE)
                except Exception as e:
                    return message('error executing command through shell {}'.format(e))

                self.view.insert(edit, target_point, p.communicate()[0][:-1].decode('utf-8').strip() + '\n')

            elif platform() == 'windows':
                # TODO [refactor] shell commands to use common os nv.ex.shell commands
                from NeoVintageous.nv.shell_windows import get_oem_cp
                from NeoVintageous.nv.shell_windows import get_startup_info
                p = subprocess.Popen(['cmd.exe', '/C', parsed.command.command],
                                     stdout=subprocess.PIPE,
                                     startupinfo=get_startup_info())
                cp = 'cp' + get_oem_cp()
                rv = p.communicate()[0].decode(cp)[:-2].strip()
                self.view.insert(edit, target_point, rv.strip() + '\n')

            else:
                message('not implemented')
        else:
            # Read a file into the current view.
            # According to Vim's help, :r should read the current file's content
            # if no file name is given, but Vim doesn't do that.
            # TODO: implement reading a file into the buffer.
            return message('not implemented')


# https://vimhelp.appspot.com/windows.txt.html#:ls
class ExPromptSelectOpenFile(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
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


# https://vimhelp.appspot.com/map.txt.html#:noremap
class ExNoremap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        if not (parsed.command.keys and parsed.command.command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(NORMAL, parsed.command.keys, parsed.command.command)
        mappings_add(OPERATOR_PENDING, parsed.command.keys, parsed.command.command)
        mappings_add(VISUAL, parsed.command.keys, parsed.command.command)
        mappings_add(VISUAL_BLOCK, parsed.command.keys, parsed.command.command)
        mappings_add(VISUAL_LINE, parsed.command.keys, parsed.command.command)


# https://vimhelp.appspot.com/map.txt.html#:unmap
class ExUnmap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        try:
            mappings_remove(NORMAL, parsed.command.keys)
            mappings_remove(OPERATOR_PENDING, parsed.command.keys)
            mappings_remove(VISUAL, parsed.command.keys)
            mappings_remove(VISUAL_BLOCK, parsed.command.keys)
            mappings_remove(VISUAL_LINE, parsed.command.keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:nnoremap
class ExNnoremap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        if not (parsed.command.keys and parsed.command.command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(NORMAL, parsed.command.keys, parsed.command.command)


# https://vimhelp.appspot.com/map.txt.html#:nunmap
class ExNunmap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        try:
            mappings_remove(NORMAL, parsed.command.keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:onoremap
class ExOnoremap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        if not (parsed.command.keys and parsed.command.command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(OPERATOR_PENDING, parsed.command.keys, parsed.command.command)


# https://vimhelp.appspot.com/map.txt.html#:ounmap
class ExOunmap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        try:
            mappings_remove(OPERATOR_PENDING, parsed.command.keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:snoremap
class ExSnoremap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        if not (parsed.command.keys and parsed.command.command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(SELECT, parsed.command.keys, parsed.command.command)


# https://vimhelp.appspot.com/map.txt.html#:sunmap
class ExSunmap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        try:
            mappings_remove(SELECT, parsed.command.keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:vnoremap
class ExVnoremap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        if not (parsed.command.keys and parsed.command.command):
            return status_message('Listing key mappings is not implemented')

        mappings_add(VISUAL, parsed.command.keys, parsed.command.command)
        mappings_add(VISUAL_BLOCK, parsed.command.keys, parsed.command.command)
        mappings_add(VISUAL_LINE, parsed.command.keys, parsed.command.command)


# https://vimhelp.appspot.com/map.txt.html#:vunmap
class ExVunmap(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        try:
            mappings_remove(VISUAL, parsed.command.keys)
            mappings_remove(VISUAL_BLOCK, parsed.command.keys)
            mappings_remove(VISUAL_LINE, parsed.command.keys)
        except KeyError:
            status_message('Mapping not found')


# https://vimhelp.appspot.com/map.txt.html#:abbreviate
class ExAbbreviate(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        if not command_line:
            self.show_abbreviations()
            return

        parsed = parse_command_line(command_line)

        if not (parsed.command.short and parsed.command.full):
            return message(':abbreviate not fully implemented')

        abbrev.Store().set(parsed.command.short, parsed.command.full)

    def show_abbreviations(self):
        abbrevs = ['{0} --> {1}'.format(item['trigger'], item['contents']) for item in abbrev.Store().get_all()]
        self.window.show_quick_panel(abbrevs, None, flags=MONOSPACE_FONT)


# https://vimhelp.appspot.com/map.txt.html#:unabbreviate
class ExUnabbreviate(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        if not parsed.command.short:
            return

        abbrev.Store().erase(parsed.command.short)


# https://vimhelp.appspot.com/editing.txt.html#:pwd
class ExPrintWorkingDir(WindowCommand, WindowCommandMixin):

    @_changing_cd
    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        status_message(os.getcwd())


# https://vimhelp.appspot.com/editing.txt.html#:write
class ExWriteFile(WindowCommand, WindowCommandMixin):

    @_changing_cd
    def run(self, command_line=''):
        if not command_line:
            raise ValueError('empty command line; that seems to be an error')

        parsed = parse_command_line(command_line)

        if parsed.command.options:
            return message('++opt isn\'t implemented for :write')

        if parsed.command.command:
            return message('!cmd not implememted for :write')

        if not self._view:
            return

        if parsed.command.appends:
            self.do_append(parsed)
            return

        if parsed.command.command:
            return message('!cmd isn\'t implemented for :write')

        if parsed.command.target_file:
            self.do_write(parsed)
            return

        if not self._view.file_name():
            return message("E32: No file name")

        read_only = (self.check_is_readonly(self._view.file_name()) or self._view.is_read_only())

        if read_only and not parsed.command.forced:
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

    def do_append(self, parsed_command):
        if parsed_command.command.target_file:
            self.do_append_to_file(parsed_command)
            return

        r = None
        if parsed_command.line_range.is_empty:
            # If the user didn't provide any range data, Vim appends whe whole buffer.
            r = Region(0, self._view.size())
        else:
            r = parsed_command.line_range.resolve(self._view)

        text = self._view.substr(r)
        text = text if text.startswith('\n') else '\n' + text

        location = resolve_insertion_point_at_b(first_sel(self._view))

        self._view.run_command('append', {'characters': text})

        utils.replace_sel(self._view, Region(self._view.line(location).a))

        self.enter_normal_mode(mode=self.state.mode)
        self.state.enter_normal_mode()

    def do_append_to_file(self, parsed_command):
        r = None
        if parsed_command.line_range.is_empty:
            # If the user didn't provide any range data, Vim writes whe whole buffer.
            r = Region(0, self._view.size())
        else:
            r = parsed_command.line_range.resolve(self._view)

        fname = parsed_command.command.target_file

        if not parsed_command.command.forced and not os.path.exists(fname):
            return message("E212: Can't open file for writing: %s" % fname)

        try:
            with open(fname, 'at') as f:
                text = self._view.substr(r)
                f.write(text)

            # TODO: make this `show_info` instead.
            return status_message('Appended to ' + os.path.abspath(fname))

        except IOError as e:
            return message('could not write file {}'.format(str(e)))

    def do_write(self, ex_command):
        fname = ex_command.command.target_file

        if not ex_command.command.forced:
            if os.path.exists(fname):
                ui_blink()

                return message("E13: File exists (add ! to override)")

            if self.check_is_readonly(fname):
                ui_blink()

                return message("E45: 'readonly' option is set (add ! to override)")

        region = None
        if ex_command.line_range.is_empty:
            # If the user didn't provide any range data, Vim writes whe whole buffer.
            region = Region(0, self._view.size())
        else:
            region = ex_command.line_range.resolve(self._view)

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
class ExWriteAll(WindowCommand, WindowCommandMixin):

    @_changing_cd
    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)
        forced = parsed.command.forced

        # TODO: read-only views don't get properly saved.
        for v in (v for v in self.window.views() if v.file_name()):
            if v.is_read_only() and not forced:
                continue

            v.run_command('save')


# https://vimhelp.appspot.com/editing.txt.html#:file
class ExFile(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        # XXX figure out what the right params are. vim's help seems to be
        # wrong
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
class ExMove(ExTextCommandBase):

    def run_ex_command(self, edit, command_line=''):
        assert command_line, 'expected non-empty command line'

        move_command = parse_command_line(command_line)
        if move_command.command.address is None:
            return message("E14: Invalid address")

        source = move_command.line_range.resolve(self.view)
        if any(s.contains(source) for s in self.view.sel()):
            return message("E134: Move lines into themselves")

        parsed_address_command = parse_command_line(move_command.command.address).line_range
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
class ExCopy(ExTextCommandBase):

    def run_ex_command(self, edit, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        def calculate_address(command):
            # TODO: must calc only the first line ref?
            calculated = parse_command_line(command.address)
            if calculated is None:
                return None

            assert calculated.command is None, 'bad address'
            assert calculated.line_range.separator is None, 'bad address'

            return calculated.line_range

        try:
            unresolved = calculate_address(parsed.command)
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

        source = parsed.line_range.resolve(self.view)
        text = self.view.substr(source)

        if address >= self.view.size():
            address = self.view.size()
            text = '\n' + text[:-1]

        self.view.insert(edit, address, text)

        cursor_dest = self.view.line(address + len(text) - 1).begin()
        self.set_next_sel([(cursor_dest, cursor_dest)])


# https://vimhelp.appspot.com/windows.txt.html#:only
class ExOnly(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):

        if not command_line:
            raise ValueError('empty command line; that seems wrong')

        parsed = parse_command_line(command_line)

        if not parsed.command.forced and has_dirty_buffers(self.window):
            return message("E445: Other window contains changes")

        current_id = self._view.id()

        for view in self.window.views():
            if view.id() == current_id:
                continue

            if view.is_dirty():
                view.set_scratch(True)

            view.close()


# https://vimhelp.appspot.com/change.txt.html#:&
class ExDoubleAmpersand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        new_command_line = '{0}substitute///{1} {2}'.format(
            str(parsed.line_range),
            ''.join(parsed.command.params['flags']),
            parsed.command.params['count'],
        )

        self.window.run_command('ex_substitute', {
            'command_line': new_command_line.strip()
        })


# https://vimhelp.appspot.com/change.txt.html#:substitute
# TODO [enhancement] Implement count.
class ExSubstitute(TextCommand):

    _last_pattern = None
    _last_flags = []
    _last_replacement = ''

    def run(self, edit, command_line=''):
        if not command_line:
            raise ValueError('no command line passed; that seems wrong')

        parsed = parse_command_line(command_line)
        pattern = parsed.command.pattern
        replacement = parsed.command.replacement
        flags = parsed.command.flags

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

        target_region = parsed.line_range.resolve(self.view)
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
class ExDelete(ExTextCommandBase):

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

    def run_ex_command(self, edit, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        r = parsed.line_range.resolve(self.view)

        if r == Region(-1, -1):
            r = self.view.full_line(0)

        self.select([r], parsed.command.params['register'])

        self.view.erase(edit, r)

        self.set_next_sel([(r.a, r.a)])


class ExGlobal(WindowCommand, WindowCommandMixin):
    """
    Global filters.

    :[range]g[lobal]/{pattern}/[cmd]
    :[range]g[lobal]!/{pattern}/[cmd]

    :global filters lines where a pattern matches and then applies the supplied
    action to all those lines. By default, :global searches all lines in the
    buffer. If you want to filter lines where a pattern does NOT match, add an
    exclamation point e.g. :g!/DON'T TOUCH THIS/delete.

    Some examples.

    This command deletes all lines between line 10 and line 20 where
    'FOO'matches: `:10,20g/FOO/delete`.

    This command replaces all instances of 'old' with 'NEW' in every line where
    'ABC' matches: `:g:ABC:s!old!NEW!g`.
    """

    _most_recent_pat = None

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command_line'
        parsed = parse_command_line(command_line)

        if parsed.line_range.is_empty:
            global_range = Region(0, self._view.size())
        else:
            global_range = parsed.line_range.resolve(self._view)

        pattern = parsed.command.pattern
        if pattern:
            ExGlobal._most_recent_pat = pattern
        else:
            pattern = ExGlobal._most_recent_pat

        subcommand = parsed.command.subcommand
        if not subcommand:
            subcommand = 'print'

        parsed_subcommand = parse_command_line(subcommand).command

        try:
            matches = find_all_in_range(self._view, pattern, global_range.begin(), global_range.end())
        except Exception as e:
            msg = "(global): %s ... in pattern '%s'" % (str(e), pattern)
            return message(msg)

        if not matches or not parsed_subcommand.cooperates_with_global:
            return

        matches = [self._view.full_line(r.begin()) for r in matches]
        matches = [[r.a, r.b] for r in matches]

        # Note: ex commands cooperating with :global must accept an additional
        # global_lines parameter.

        self.window.run_command(parsed_subcommand.target_command, {
            'command_line': str(parsed_subcommand),
            'global_lines': matches,
        })


# https://vimhelp.appspot.com/various.txt.html#:print
class ExPrint(WindowCommand, WindowCommandMixin):

    def run(self, command_line='', global_lines=None):
        assert command_line, 'expected non-empty command line'

        if self._view.size() == 0:
            return message("E749: empty buffer")

        parsed = parse_command_line(command_line)

        r = parsed.line_range.resolve(self._view)

        lines = self.get_lines(r, global_lines)

        display = self.window.new_file()
        display.set_scratch(True)

        if 'l' in parsed.command.flags:
            display.settings().set('draw_white_space', 'all')

        for (text, row) in lines:
            characters = ''
            if '#' in parsed.command.flags:
                characters = "{} {}".format(row, text).lstrip()
            else:
                characters = text.lstrip()
            display.run_command('append', {'characters': characters})

    def get_lines(self, parsed_range, global_lines):
        # FIXME: this is broken.
        # If :global called us, ignore the parsed range.
        if global_lines:
            return [(self._view.substr(Region(a, b)), row_at(self._view, a)) for (a, b) in global_lines]

        to_display = []
        for line in self._view.full_line(parsed_range):
            text = self._view.substr(line)
            to_display.append((text, row_at(self._view, line.begin())))
        return to_display


# https://vimhelp.appspot.com/windows.txt.html#:close
class ExClose(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        do_not_close_if_last = False if parsed.command.forced else True
        WindowAPI(self.window).close_current_view(do_not_close_if_last)


# https://vimhelp.appspot.com/editing.txt.html#:q
class ExQuitCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        quit_command = parse_command_line(command_line)

        view = self._view

        if quit_command.command.forced:
            view.set_scratch(True)

        if view.is_dirty() and not quit_command.command.forced:
            return message("E37: No write since last change")

        if not view.file_name() and not quit_command.command.forced:
            return message("E32: No file name")

        self.window.run_command('close')

        if len(self.window.views()) == 0:
            self.window.run_command('close')
            return

        # FIXME: Probably doesn't work as expected.
        # Close the current group if there aren't any views left in it.
        if not self.window.views_in_group(self.window.active_group()):
            self.window.run_command('ex_unvsplit')


# https://vimhelp.appspot.com/editing.txt.html#:qa
class ExQuitAllCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        if parsed.command.forced:
            for v in self.window.views():
                if v.is_dirty():
                    v.set_scratch(True)

        elif has_dirty_buffers(self.window):
            return status_message('there are unsaved changes!')

        self.window.run_command('close_all')
        self.window.run_command('exit')


class ExWriteAndQuitCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        # TODO: implement this
        if parsed.command.forced:
            return message('not implemented')

        if self._view.is_read_only():
            return status_message("can't write a read-only buffer")

        if not self._view.file_name():
            return status_message("can't save a file without name")

        self.window.run_command('save')
        self.window.run_command('ex_quit', {'command_line': 'quit'})


# https://vimhelp.appspot.com/editing.txt.html#:browse
class ExBrowse(WindowCommand, WindowCommandMixin):

    def run(self, command_line):
        assert command_line, 'expected a non-empty command line'

        self.window.run_command('prompt_open_file', {
            'initial_directory': self.state.settings.vi['_cmdline_cd']
        })


# https://vimhelp.appspot.com/editing.txt.html#:edit
class ExEdit(WindowCommand, WindowCommandMixin):

    @_changing_cd
    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        if parsed.command.file_name:
            file_name = os.path.expanduser(os.path.expandvars(parsed.command.file_name))

            if self._view.is_dirty() and not parsed.command.forced:
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
                    msg = '"{}" [New DIRECTORY]'.format(parsed.command.file_name)
                else:
                    msg = '"{}" [New File]'.format(os.path.basename(file_name))

                # Give ST some time to load the new view.
                set_timeout(lambda: status_message(msg), 150)

            return

        if parsed.command.forced or not self._view.is_dirty():
            self._view.run_command('revert')
            return

        if self._view.is_dirty():
            return message("E37: No write since last change")

        message("E37: No write since last change")


# https://vimhelp.appspot.com/quickfix.txt.html#:cquit
class ExCquit(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command_line'

        self.window.run_command('exit')


# https://vimhelp.appspot.com/editing.txt.html#:exit
class ExExit(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        if self._view.is_dirty():
            self.window.run_command('save')

        self.window.run_command('close')

        if len(self.window.views()) == 0:
            self.window.run_command('exit')


# https://vimhelp.appspot.com/change.txt.html#:registers
class ExRegisters(WindowCommand, WindowCommandMixin):

    def run(self, command_line):
        parse_command_line(command_line)

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


# https://vimhelp.appspot.com/windows.txt.html#:new
class ExNew(WindowCommand, WindowCommandMixin):

    @_changing_cd
    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        self.window.run_command('new_file')


# https://vimhelp.appspot.com/windows.txt.html#:yank
class ExYank(TextCommand):

    def run(self, edit, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        register = parsed.command.register
        line_range = parsed.line_range.resolve(self.view)

        if not register:
            register = '"'

        text = self.view.substr(line_range)

        state = State(self.view)
        state.registers[register] = [text]
        # TODO: o_O?
        if register == '"':
            state.registers['0'] = [text]


# https://vimhelp.appspot.com/tabpage.txt.html#:tabnext
class ExTabnextCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parse_command_line(command_line)
        window_tab_control(self.window, command='next')


# https://vimhelp.appspot.com/tabpage.txt.html#:tabprevious
class ExTabprevCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parse_command_line(command_line)
        window_tab_control(self.window, command='prev')


# https://vimhelp.appspot.com/tabpage.txt.html#:tablast
class ExTablastCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parse_command_line(command_line)
        window_tab_control(self.window, command='last')


# https://vimhelp.appspot.com/tabpage.txt.html#:tabfirst
class ExTabfirstCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parse_command_line(command_line)
        window_tab_control(self.window, command='first')


# https://vimhelp.appspot.com/tabpage.txt.html#:tabonly
class ExTabonlyCommand(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        window_tab_control(self.window, command='only', forced=parsed.command.forced)


# https://vimhelp.appspot.com/editing.txt.html#:cd
class ExCdCommand(WindowCommand, WindowCommandMixin):
    """
    Print or change the current directory.

    Without an argument behaves as in Unix for all platforms.
    """

    @_changing_cd
    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        if self._view.is_dirty() and not parsed.command.forced:
            return message("E37: No write since last change")

        if not parsed.command.path:
            self.state.settings.vi['_cmdline_cd'] = os.path.expanduser("~")
            self._view.run_command('ex_print_working_dir')
            return

        # TODO: It seems there a few symbols that are always substituted when they represent a
        # filename. We should have a global method of substiting them.
        if parsed.command.path == '%:h':
            fname = self._view.file_name()
            if fname:
                self.state.settings.vi['_cmdline_cd'] = os.path.dirname(fname)
                self._view.run_command('ex_print_working_dir')
            return

        path = os.path.realpath(os.path.expandvars(os.path.expanduser(parsed.command.path)))
        if not os.path.exists(path):
            return message("E344: Can't find directory \"%s\" in cdpath" % path)

        self.state.settings.vi['_cmdline_cd'] = path
        self._view.run_command('ex_print_working_dir')


class ExCddCommand(WindowCommand, WindowCommandMixin):
    """
    Ex Command (non-standard).

    :cdd[!]

    Non-standard command to change the current directory to the active
    view's directory.

    In Sublime Text, the current directory doesn't follow the active view, so
    it's convenient to be able to align both easily.

    XXX: Is the above still true?

    (This command may be removed at any time.)
    """

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        parsed = parse_command_line(command_line)

        if self._view.is_dirty() and not parsed.command.forced:
            return message("E37: No write since last change")

        path = os.path.dirname(self._view.file_name())

        try:
            self.state.settings.vi['_cmdline_cd'] = path
            status_message(path)
        except IOError:
            message("E344: Can't find directory \"%s\" in cdpath" % path)


# TODO Refactor like ExSplit
# https://vimhelp.appspot.com/windows.txt.html#:vsplit
class ExVsplit(WindowCommand, WindowCommandMixin):

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

    def run(self, command_line=''):
        parsed = parse_command_line(command_line)

        file = parsed.command.params['file']

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


# https://vimhelp.appspot.com/windows.txt.html#:split
class ExSplit(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        window_split(self.window, parse_command_line(command_line).command.params['file'])


class ExUnvsplit(WindowCommand, WindowCommandMixin):
    """Non-standard Vim :unvsplit command."""

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        groups = self.window.num_groups()
        if groups == 1:
            status_message('can\'t delete more groups')
            return

        # If we don't do this, cloned views will be moved to the previous group and kept around.
        # We want to close them instead.
        self.window.run_command('close')
        self.window.run_command('set_layout', ExVsplit.LAYOUT_DATA[groups - 1])


# https://vimhelp.appspot.com/options.txt.html#:setlocal
class ExSetLocal(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        option = parsed.command.option
        value = parsed.command.value

        if option.endswith('?'):
            return message('not implemented')

        try:
            set_local(self._view, option, value)
        except KeyError:
            status_message('no such option')
        except ValueError:
            status_message('invalid value for option')


# https://vimhelp.appspot.com/options.txt.html#:set
class ExSet(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)

        option = parsed.command.option
        value = parsed.command.value

        if option.endswith('?'):
            return message('not implemented')

        try:
            set_global(self._view, option, value)
        except KeyError:
            status_message('no such option')
        except ValueError:
            status_message('invalid value for option')


# https://vimhelp.appspot.com/eval.txt.html#:let
class ExLet(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'
        parsed = parse_command_line(command_line)
        variables.set(parsed.command.variable_name, parsed.command.variable_value)


# https://vimhelp.appspot.com/editing.txt.html#:wqall
class ExWriteAndQuitAll(WindowCommand, WindowCommandMixin):

    def run(self, command_line=''):
        assert command_line, 'expected non-empty command line'

        if not all(v.file_name() for v in self.window.views()):
            ui_blink()

            return message("E32: No file name")

        if any(v.is_read_only() for v in self.window.views()):
            ui_blink()

            return message("E45: 'readonly' option is set (add ! to override)")

        self.window.run_command('save_all')

        assert not any(v.is_dirty() for v in self.window.views())

        self.window.run_command('close_all')
        self.window.run_command('exit')
