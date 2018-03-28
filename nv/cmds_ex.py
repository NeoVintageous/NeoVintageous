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


from functools import wraps
import inspect
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

    @wraps(f)
    def inner(*args, **kwargs):
        view = kwargs.get('view', None)
        if not view:
            window = kwargs.get('window', None)
            if window:
                view = window.active_view()

            if not view:
                try:
                    view = args[0].view
                except AttributeError:
                    try:
                        view = args[0].window.active_view()
                    except AttributeError:
                        view = args[0].active_view()

        # TODO [review] State dependency
        state = State(view)

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


def _set_next_selection(view, data):
    view.settings().set('ex_data', {'next_sel': data})


def _serialize_deserialize(f, *args, **kwargs):

    @wraps(f)
    def inner(*args, **kwargs):
        # TODO [refactor]
        view = kwargs.get('view', None)
        if not view:
            window = kwargs.get('window', None)
            if window:
                view = window.active_view()
            else:
                if len(args) > 0:
                    window = args[0]
                    view = window.active_view()

        #
        # Serialize
        #

        sels = [(r.a, r.b) for r in list(view.sel())]
        view.settings().set('ex_data', {'prev_sel': sels})

        f(*args, **kwargs)

        #
        # Set selection
        #

        # Deserialise
        ex_data = view.settings().get('ex_data')
        if 'next_sel' in ex_data:
            next_sel = ex_data['next_sel']
        else:
            next_sel = []

        if next_sel:
            print('adding next selection: ', next_sel)
            view.sel().clear()
            view.sel().add_all([Region(b) for (a, b) in next_sel])

        #
        # Set mode
        #

        # TODO [review] State dependency
        state = State(view)
        state.enter_normal_mode()
        # TODO [review] enter normal mode depedendency
        view.run_command('_enter_normal_mode')

    return inner


# TODO [refactor] into _nv_cmdline non-interactive command
class _nv_run_ex_text_cmd(TextCommand):
    def run(self, edit, name, command_line, *args, **kwargs):
        _log.debug('_nv_run_ex_text_cmd -> %s with %s %s in %s %s', name, args, kwargs, self.view.id(), self.view.file_name())  # noqa: E501

        parsed = parse_command_line(command_line)
        module = sys.modules[__name__]
        ex_cmd = getattr(module, name, None)
        parsed.command.params.update(kwargs)

        if ex_cmd:
            ex_cmd(
                view=self.view,
                edit=edit,
                line_range=parsed.line_range,
                **parsed.command.params
            )


def do_ex_command(window, name, args=None):
    _log.debug('do ex command -> %s %s', name, args)

    name = name.title().replace('_', '')
    if not name.startswith('Ex'):
        name = 'Ex' + name

    if args is None:
        args = {'command_line': name[2:].lower()}
    elif 'command_line' not in args:
        args['command_line'] = name[2:].lower()

    module = sys.modules[__name__]
    ex_cmd = getattr(module, name, None)

    if not ex_cmd:
        raise RuntimeError('unknown ex cmd {}'.format(name))

    if not inspect.isfunction(ex_cmd):
        raise RuntimeError('unknown ex cmd type {}'.format(ex_cmd))

    requires_edit_object = False
    for p in inspect.signature(ex_cmd).parameters:
        if p == 'edit':
            requires_edit_object = True
            break

    if requires_edit_object:
        # Text commands need edit tokens and they can only be created by
        # Sublime Text commands, so we need to wrap the command in a ST text
        # command.
        _log.debug('run ex command as a text command %s %s', name, args)
        args['name'] = name
        window.run_command('_nv_run_ex_text_cmd', args)
        _log.debug('finished ex text command')
    else:

        parsed = parse_command_line(args['command_line'])
        params = parsed.command.params
        params.update(args)

        view = window.active_view()
        if view:
            params['view'] = view

        # We don't want the ex commands using this.
        if 'command_line' in params:
            del params['command_line']

        # Passed directly to command.
        if 'forceit' in params:
            del params['forceit']

        _log.debug('run ex command as window command %s %s', name, params)

        ex_cmd(
            window=window,
            line_range=parsed.line_range,
            forceit=(args['forceit'] if 'forceit' in args else parsed.command.forced),
            **params
        )

        _log.debug('finished ex window command')


def ExGoto(window, view, line_range, *args, **kwargs):
    r = line_range.resolve(view)
    line_nr = row_at(view, r.a) + 1

    # TODO [review] State dependency
    state = State(view)

    # TODO [review] enter normal mode depedendency
    window.run_command('_enter_normal_mode', {'mode': state.mode})
    state.enter_normal_mode()

    jumplist_update(view)
    window.run_command('_vi_go_to_line', {'line': line_nr, 'mode': state.mode})
    jumplist_update(view)
    view.show(view.sel()[0])


_ex_help_tags_cache = {}


def ExHelp(window, subject=None, forceit=False, *args, **kwargs):
    if not subject:
        subject = 'help.txt'

        if forceit:
            return message("E478: Don't panic!")

    subject = subject.lower()

    if not _ex_help_tags_cache:
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
                _ex_help_tags_cache[match.group(1).lower()] = (match.group(2), match.group(3))

        console_message('finished initializing help tags')

    if subject not in _ex_help_tags_cache:
        # Basic hueristic to find nearest relevant help e.g. `help ctrl-k`
        # will look for "ctrl-k", "c_ctrl-k", "i_ctrl-k", etc. Another
        # example is `:help copy` will look for "copy" then ":copy".
        found = False
        for m in (':', 'c_', 'i_', 'v_', '-', '/'):
            _subject = m + subject
            if _subject in _ex_help_tags_cache:
                found = True
                subject = _subject

        if not found:
            return message('E149: Sorry, no help for %s' % subject)

    tag = _ex_help_tags_cache[subject]

    doc_resources = [r for r in find_resources(
        tag[0]) if r.startswith('Packages/NeoVintageous/res/doc/')]

    if not doc_resources:
        return message('Sorry, help file "%s" not found' % tag[0])

    def window_find_open_view(window, name):
        for view in window.views():
            if view.name() == name:
                return view

    help_view_name = '%s [vim help]' % (tag[0])
    view = window_find_open_view(window, help_view_name)
    if view:
        window.focus_view(view)
    else:
        view = window.new_file()
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


_ex_shell_last_command = None


@_changing_cd
def ExShellOut(view, edit, cmd, line_range, *args, **kwargs):
    global _ex_shell_last_command

    if cmd == '!':
        if not _ex_shell_last_command:
            return status_message('E34: No previous command')

        cmd = _ex_shell_last_command

    # TODO: store only successful commands.
    _ex_shell_last_command = cmd

    try:
        if not line_range.is_empty:
            shell.filter_thru_shell(
                view=view,
                edit=edit,
                regions=[line_range.resolve(view)],
                cmd=cmd
            )
        else:
            output = shell.run_and_read(view, cmd)
            output_view = view.window().create_output_panel('vi_out')
            output_view.settings().set("line_numbers", False)
            output_view.settings().set("gutter", False)
            output_view.settings().set("scroll_past_end", False)
            output_view = view.window().create_output_panel('vi_out')
            output_view.run_command('append', {'characters': output, 'force': True, 'scroll_to_end': True})
            view.window().run_command("show_panel", {"panel": "output.vi_out"})
    except NotImplementedError:
        message('not implemented')


# TODO [refactor] shell commands to use common os nv.ex.shell commands
# This command starts a shell. When the shell exits (after the "exit" command)
# you return to Sublime Text. The name for the shell command comes from:
# * VintageousEx_linux_terminal setting on Linux
# * VintageousEx_osx_terminal setting on OSX
# The shell is opened at the active view directory. Sublime Text keeps a virtual
# current directory that most of the time will be out of sync with the actual
# current directory. The virtual current directory is always set to the current
# view's directory, but it isn't accessible through the API.
@_changing_cd
def ExShell(view, *args, **kwargs):

    def _open_shell(command):
        return subprocess.Popen(command, cwd=os.getcwd())

    if platform() == 'linux':
        term = view.settings().get('VintageousEx_linux_terminal')
        term = term or os.environ.get('COLORTERM') or os.environ.get('TERM')
        if not term:
            return message('terminal not found')

        try:
            _open_shell([term, '-e', 'bash']).wait()
        except Exception as e:
            return message('error executing command through shell {}'.format(e))

    elif platform() == 'osx':
        term = view.settings().get('VintageousEx_osx_terminal')
        term = term or os.environ.get('COLORTERM') or os.environ.get('TERM')
        if not term:
            return message('terminal not found')

        try:
            _open_shell([term, '-e', 'bash']).wait()
        except Exception as e:
            return message('error executing command through shell {}'.format(e))

    elif platform() == 'windows':
        _open_shell(['cmd.exe', '/k']).wait()
    else:
        message('not implemented')


# TODO [review] This command looks unused
# TODO [refactor] shell commands to use common os nv.ex.shell commands
@_changing_cd
def ExRead(view, edit, cmd, line_range, *args, **kwargs):
    r = line_range.resolve(view)
    target_point = min(r.end(), view.size())

    if cmd:
        if platform() == 'linux':
            # TODO: make shell command configurable.
            shell_cmd = view.settings().get('linux_shell')
            shell_cmd = shell_cmd or os.path.expandvars("$SHELL")
            if not shell_cmd:
                return message('no shell found')

            try:
                p = subprocess.Popen([shell_cmd, '-c', cmd], stdout=subprocess.PIPE)
            except Exception as e:
                return message('error executing command through shell {}'.format(e))

            view.insert(edit, target_point, p.communicate()[0][:-1].decode('utf-8').strip() + '\n')

        elif platform() == 'windows':
            # TODO [refactor] shell commands to use common os nv.ex.shell commands
            from NeoVintageous.nv.shell_windows import get_oem_cp
            from NeoVintageous.nv.shell_windows import get_startup_info
            p = subprocess.Popen(['cmd.exe', '/C', cmd],
                                 stdout=subprocess.PIPE,
                                 startupinfo=get_startup_info())
            cp = 'cp' + get_oem_cp()
            rv = p.communicate()[0].decode(cp)[:-2].strip()
            view.insert(edit, target_point, rv.strip() + '\n')

        else:
            return message('not implemented')
    else:
        # Read a file into the current view.
        # According to Vim's help, :r should read the current file's content
        # if no file name is given, but Vim doesn't do that.
        # TODO: implement reading a file into the buffer.
        return message('not implemented')


def ExPromptSelectOpenFile(window, *args, **kwargs):
    def _get_view_info(view):
        path = view.file_name()
        if path:
            parent, leaf = os.path.split(path)
            parent = os.path.basename(parent)
            path = os.path.join(parent, leaf)
        else:
            path = view.name() or str(view.buffer_id())
            leaf = view.name() or 'untitled'

        status = []
        if not view.file_name():
            status.append("t")
        if view.is_dirty():
            status.append("*")
        if view.is_read_only():
            status.append("r")

        if status:
            leaf += ' (%s)' % ', '.join(status)

        return [leaf, path]

    file_names = [_get_view_info(view) for view in window.views()]
    view_ids = [view.id() for view in window.views()]

    def on_done(index):
        if index == -1:
            return

        sought_id = view_ids[index]
        for view in window.views():
            # TODO: Start looking in current group.
            if view.id() == sought_id:
                window.focus_view(view)

    window.show_quick_panel(file_names, on_done)


def ExNoremap(keys, command, *args, **kwargs):
    if not (keys and command):
        # TODO [refactor] Instead of calling status_message(), raise a
        # NotImplemented exception instead, and let the command runner handle
        # it. All other commands should do the same in cases like this.
        return status_message('Listing key mappings is not implemented')

    mappings_add(NORMAL, keys, command)
    mappings_add(OPERATOR_PENDING, keys, command)
    mappings_add(VISUAL, keys, command)
    mappings_add(VISUAL_BLOCK, keys, command)
    mappings_add(VISUAL_LINE, keys, command)


def ExUnmap(keys, *args, **kwargs):
    try:
        mappings_remove(NORMAL, keys)
        mappings_remove(OPERATOR_PENDING, keys)
        mappings_remove(VISUAL, keys)
        mappings_remove(VISUAL_BLOCK, keys)
        mappings_remove(VISUAL_LINE, keys)
    except KeyError:
        status_message('Mapping not found')


def ExNnoremap(keys, command, *args, **kwargs):
    if not (keys and command):
        return status_message('Listing key mappings is not implemented')

    mappings_add(NORMAL, keys, command)


def ExNunmap(keys, *args, **kwargs):
    try:
        mappings_remove(NORMAL, keys)
    except KeyError:
        status_message('Mapping not found')


def ExOnoremap(keys, command, *args, **kwargs):
    if not (keys and command):
        return status_message('Listing key mappings is not implemented')

    mappings_add(OPERATOR_PENDING, keys, command)


def ExOunmap(keys, *args, **kwargs):
    try:
        mappings_remove(OPERATOR_PENDING, keys)
    except KeyError:
        status_message('Mapping not found')


def ExSnoremap(keys, command, *args, **kwargs):
    if not (keys and command):
        return status_message('Listing key mappings is not implemented')

    mappings_add(SELECT, keys, command)


def ExSunmap(keys, *args, **kwargs):
    try:
        mappings_remove(SELECT, keys)
    except KeyError:
        status_message('Mapping not found')


def ExVnoremap(keys, command, *args, **kwargs):
    if not (keys and command):
        return status_message('Listing key mappings is not implemented')

    mappings_add(VISUAL, keys, command)
    mappings_add(VISUAL_BLOCK, keys, command)
    mappings_add(VISUAL_LINE, keys, command)


def ExVunmap(keys, *args, **kwargs):
    try:
        mappings_remove(VISUAL, keys)
        mappings_remove(VISUAL_BLOCK, keys)
        mappings_remove(VISUAL_LINE, keys)
    except KeyError:
        status_message('Mapping not found')


# TODO [review] Looks broken or not implemented properly
def ExAbbreviate(window, short=None, full=None, *args, **kwargs):
    if short is None and full is None:
        def _show_abbreviations():
            abbrevs = ['{0} --> {1}'.format(item['trigger'], item['contents']) for item in abbrev.Store().get_all()]
            window.show_quick_panel(abbrevs, None, flags=MONOSPACE_FONT)

        return _show_abbreviations()

    if not (short and full):
        return message(':abbreviate not fully implemented')

    abbrev.Store().set(short, full)


# TODO [review] Looks broken or not implemented properly
def ExUnabbreviate(lhs, *args, **kwargs):
    if lhs:
        return

    abbrev.Store().erase(lhs)


@_changing_cd
def ExPwd(*args, **kwargs):
    status_message(os.getcwd())


@_changing_cd
def ExWrite(window, view, file_name, cmd, forceit, line_range, *args, **kwargs):
    # TODO [refactor] Should params should used keys compatible with **kwargs? (review other commands too) # noqa: E501
    options = kwargs.get('++')
    appends = kwargs.get('>>')

    if options:
        return message('++opt isn\'t implemented for :write')

    if cmd:
        return message('!cmd not implememted for :write')

    if not view:
        return

    def _check_is_readonly(fname):
        # type: (str) -> bool
        if not fname:
            return False

        try:
            return (stat.S_IMODE(os.stat(fname).st_mode) & stat.S_IWUSR != stat.S_IWUSR)
        except FileNotFoundError:
            return False

        return False

    if appends:
        def _do_append_to_file(view, file_name, forceit, line_range):
            r = None
            if line_range.is_empty:
                # If the user didn't provide any range data, Vim writes whe whole buffer.
                r = Region(0, view.size())
            else:
                r = line_range.resolve(view)

            if not forceit and not os.path.exists(file_name):
                return message("E212: Can't open file for writing: %s" % file_name)

            try:
                with open(file_name, 'at') as f:
                    text = view.substr(r)
                    f.write(text)

                # TODO: make this `show_info` instead.
                return status_message('Appended to ' + os.path.abspath(file_name))

            except IOError as e:
                return message('could not write file {}'.format(str(e)))

        def _do_append(view, file_name, forceit, line_range):
            if file_name:
                return _do_append_to_file(view, file_name, forceit, line_range)

            r = None
            if line_range.is_empty:
                # If the user didn't provide any range data, Vim appends whe whole buffer.
                r = Region(0, view.size())
            else:
                r = line_range.resolve(view)

            text = view.substr(r)
            text = text if text.startswith('\n') else '\n' + text

            location = resolve_insertion_point_at_b(first_sel(view))

            view.run_command('append', {'characters': text})

            utils.replace_sel(view, Region(view.line(location).a))

            # TODO [review] State dependency
            state = State(view)

            # TODO [review] enter normal mode depedendency
            window.run_command('_enter_normal_mode', {'mode': state.mode})
            state.enter_normal_mode()

        return _do_append(view, file_name, forceit, line_range)

    if cmd:
        return message('!cmd isn\'t implemented for :write')

    if file_name:
        def _do_write(window, view, file_name, forceit, line_range):
            fname = file_name

            if not forceit:
                if os.path.exists(fname):
                    ui_blink()

                    return message("E13: File exists (add ! to override)")

                if _check_is_readonly(fname):
                    ui_blink()

                    return message("E45: 'readonly' option is set (add ! to override)")

            region = None
            if line_range.is_empty:
                # If the user didn't provide any range data, Vim writes whe whole buffer.
                region = Region(0, view.size())
            else:
                region = line_range.resolve(view)

            assert region is not None, "range cannot be None"

            try:
                expanded_path = os.path.expandvars(os.path.expanduser(fname))
                expanded_path = os.path.abspath(expanded_path)
                with open(expanded_path, 'wt') as f:
                    text = view.substr(region)
                    f.write(text)

                # FIXME: Does this do what we think it does?
                view.retarget(expanded_path)
                window.run_command('save')

            except IOError as e:
                # TODO: Add logging.
                return message("E212: Can't open file for writing: {}".format(fname))

        return _do_write(window, view, file_name, forceit, line_range)

    if not view.file_name():
        return message("E32: No file name")

    read_only = (_check_is_readonly(view.file_name()) or view.is_read_only())

    if read_only and not forceit:
        ui_blink()

        return message("E45: 'readonly' option is set (add ! to override)")

    window.run_command('save')


@_changing_cd
def ExWall(window, forceit=False, *args, **kwargs):
    # TODO read-only views don't get properly saved.
    for v in (v for v in window.views() if v.file_name()):
        if v.is_read_only() and not forceit:
            continue

        v.run_command('save')


def ExFile(view, *args, **kwargs):
    if view.file_name():
        fname = view.file_name()
    else:
        fname = 'untitled'

    attrs = ''
    if view.is_read_only():
        attrs = 'readonly'

    if view.is_dirty():
        attrs = 'modified'

    lines = 'no lines in the buffer'
    if view.rowcol(view.size())[0]:
        lines = view.rowcol(view.size())[0] + 1

    # fixme: doesn't calculate the buffer's % correctly
    if not isinstance(lines, str):
        vr = view.visible_region()
        start_row, end_row = view.rowcol(vr.begin())[0], view.rowcol(vr.end())[0]
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


@_serialize_deserialize
def ExMove(view, edit, address, line_range, *args, **kwargs):
    # Move the lines given by [range] to below the line given by {address}.
    if address is None:
        return message("E14: Invalid address")

    source = line_range.resolve(view)
    if any(s.contains(source) for s in view.sel()):
        return message("E134: Move lines into themselves")

    # TODO [refactor] is parsing the address necessary, if yes, create a parse_address function
    parsed_address_command = parse_command_line(address).line_range
    destination = parsed_address_command.resolve(view)
    if destination == source:
        return

    text = view.substr(source)
    if destination.end() >= view.size():
        text = '\n' + text.rstrip()

    if destination == Region(-1):
        destination = Region(0)

    if destination.end() < source.begin():
        view.erase(edit, source)
        view.insert(edit, destination.end(), text)
        _set_next_selection(view, [[destination.a, destination.b]])
        return

    view.insert(edit, destination.end(), text)
    view.erase(edit, source)
    _set_next_selection(view, [[destination.a, destination.a]])


@_serialize_deserialize
def ExCopy(view, edit, address, line_range, *args, **kwargs):
    # Copy the lines given by [range] to below the line given by {address}.
    def _calculate_address(address):
        # TODO: must calc only the first line ref?
        # TODO [refactor] parsing the address
        calculated = parse_command_line(address)
        if calculated is None:
            return None

        # TODO Refactor and remove assertions
        assert calculated.command is None, 'bad address'
        assert calculated.line_range.separator is None, 'bad address'

        return calculated.line_range

    try:
        unresolved = _calculate_address(address)
    except Exception:
        return message("E14: Invalid address")

    if unresolved is None:
        return message("E14: Invalid address")

    # TODO: how do we signal row 0?
    target_region = unresolved.resolve(view)

    if target_region == Region(-1, -1):
        address = 0
    else:
        row = utils.row_at(view, target_region.begin()) + 1
        address = view.text_point(row, 0)

    source = line_range.resolve(view)
    text = view.substr(source)

    if address >= view.size():
        address = view.size()
        text = '\n' + text[:-1]

    view.insert(edit, address, text)

    cursor_dest = view.line(address + len(text) - 1).begin()
    _set_next_selection(view, [(cursor_dest, cursor_dest)])


# TODO Unify with CTRL-W CTRL-O
def ExOnly(window, view, forceit=False, *args, **kwargs):
    if not forceit and has_dirty_buffers(window):
        return message("E445: Other window contains changes")

    current_id = view.id()
    for view in window.views():
        if view.id() == current_id:
            continue

        if view.is_dirty():
            view.set_scratch(True)

        view.close()


def ExDoubleAmpersand(view, edit, flags, count, line_range, *args, **kwargs):
    ExSubstitute(view=view, edit=edit, flags=flags, count=count, line_range=line_range, *args, **kwargs)


_ex_substitute_last_pattern = None
_ex_substitute_last_replacement = ''


# TODO [refactor] Rename param "search_term" -> "pattern"
def ExSubstitute(view, edit, line_range, search_term=None, replacement='', flags=0, count=1, *args, **kwargs):
    pattern = search_term

    global _ex_substitute_last_pattern, _ex_substitute_last_replacement

    # Repeat last :substitute with same search pattern and substitute string,
    # but without the same flags.
    if not pattern:
        pattern = _ex_substitute_last_pattern
        if not pattern:
            return status_message('E33: No previous substitute regular expression')

        replacement = _ex_substitute_last_replacement

    if not pattern:
        return status_message('No substitute regular expression')

    if replacement is None:
        return status_message('No substitute replacement string')

    _ex_substitute_last_pattern = pattern
    _ex_substitute_last_replacement = replacement

    computed_flags = re.MULTILINE
    computed_flags |= re.IGNORECASE if ('i' in flags) else 0

    try:
        compiled_pattern = re.compile(pattern, flags=computed_flags)
    except Exception as e:
        return message('[regex error]: {} ... in pattern {}'.format((str(e), pattern)))

    target_region = line_range.resolve(view)
    if target_region.empty():
        return status_message('E486: Pattern not found: {}'.format(pattern))

    replace_count = 0 if (flags and 'g' in flags) else 1

    if 'c' in flags:

        def _replace_confirming(view, edit, pattern, compiled_pattern,
                                replacement, replace_count, target_region):

            last_row = row_at(view, target_region.b - 1)
            start = target_region.begin()

            while True:
                if start >= view.size():
                    break

                match = view.find(pattern, start)

                # no match or match out of range -- stop
                if (match == Region(-1)) or (row_at(view, match.a) > last_row):
                    view.show(first_sel(view).begin())
                    return

                size_before = view.size()

                with adding_regions(view, 's_confirm', [match], 'comment'):
                    view.show(match.a, True)
                    if ok_cancel_dialog("Confirm replacement?"):
                        text = view.substr(match)
                        substituted = re.sub(compiled_pattern, replacement, text, count=replace_count)
                        view.replace(edit, match, substituted)

                start = match.b + (view.size() - size_before) + 1

        return _replace_confirming(view, edit, pattern, compiled_pattern, replacement, replace_count, target_region)

    lines = view.lines(target_region)
    if not lines:
        return status_message('E486: Pattern not found: {}'.format(pattern))

    new_lines = []
    dirty = False
    for line in lines:
        line_str = view.substr(line)
        new_line_str = re.sub(compiled_pattern, replacement, line_str, count=replace_count)
        new_lines.append(new_line_str)
        if new_line_str != line_str:
            dirty = True

    new_region_text = '\n'.join(new_lines)
    if view.size() > line.end():
        new_region_text += '\n'

    if not dirty:
        return status_message('E486: Pattern not found: {}'.format(pattern))

    # Reposition cursor before replacing target region so that the cursor
    # will auto adjust in sync with the replacement.
    view.sel().clear()
    view.sel().add(line.begin())

    view.replace(edit, target_region, new_region_text)

    # TODO Refactor set position cursor after operation into reusable api.
    # Put cursor on first non-whitespace char of current line.
    line = view.line(view.sel()[0].b)
    if line.size() > 0:
        pt = view.find('^\\s*', line.begin()).end()
        view.sel().clear()
        view.sel().add(pt)

    # TODO [review] enter normal mode depedendency
    view.run_command('_enter_normal_mode')


@_serialize_deserialize
def ExDelete(view, edit, register, line_range, *args, **kwargs):
    r = line_range.resolve(view)
    if r == Region(-1, -1):
        r = view.full_line(0)

    def _select(view, regions, register):
        view.sel().clear()
        to_store = []
        for r in regions:
            view.sel().add(r)
            if register:
                to_store.append(view.substr(view.full_line(r)))

        if register:
            text = ''.join(to_store)
            if not text.endswith('\n'):
                text = text + '\n'

            state = State(view)
            state.registers[register] = [text]

    _select(view, [r], register)
    view.erase(edit, r)
    _set_next_selection(view, [(r.a, r.a)])


_ex_global_most_recent_pat = None


# At the time of writing, the only command that supports :global is the
# "print" command e.g. print all lines matching \d+ into new buffer:
#   :%global/\d+/print
# TODO [refactor] Rename "subcommand" -> "cmd"
def ExGlobal(window, view, pattern, subcommand, line_range, *args, **kwargs):
    if line_range.is_empty:
        global_range = Region(0, view.size())
    else:
        global_range = line_range.resolve(view)

    global _ex_global_most_recent_pat
    if pattern:
        _ex_global_most_recent_pat = pattern
    else:
        pattern = _ex_global_most_recent_pat

    if not subcommand:
        subcommand = 'print'

    parsed_subcommand = parse_command_line(subcommand).command

    try:
        matches = find_all_in_range(view, pattern, global_range.begin(), global_range.end())
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

    matches = [view.full_line(r.begin()) for r in matches]
    matches = [[r.a, r.b] for r in matches]

    parsed_subcommand.params['global_lines'] = matches

    do_ex_command(window, parsed_subcommand.target_command, parsed_subcommand.params)


def ExPrint(window, view, flags, line_range, global_lines=None, *args, **kwargs):
    if view.size() == 0:
        return message("E749: empty buffer")

    def _get_lines(view, parsed_range, global_lines):
        # If :global called us, ignore the parsed range.
        if global_lines:
            return [(view.substr(Region(a, b)), row_at(view, a)) for (a, b) in global_lines]

        to_display = []
        for line in view.lines(parsed_range):
            text = view.substr(line)
            to_display.append((text, row_at(view, line.begin())))

        return to_display

    lines = _get_lines(view, line_range.resolve(view), global_lines)

    display = window.new_file()
    display.set_scratch(True)

    if 'l' in flags:
        display.settings().set('draw_white_space', 'all')

    for i, (text, row) in enumerate(lines):
        characters = ''
        if '#' in flags:
            characters = "{} {}".format(row, text).lstrip()
        else:
            characters = text.lstrip()

        if not global_lines:
            if i < len(lines) - 1:
                characters += '\n'

        display.run_command('append', {'characters': characters})


# TODO [refactor] into window module
def ExClose(window, forceit=False, *args, **kwargs):
    WindowAPI(window).close_current_view(not forceit)


# TODO [refactor] into window module
def ExQuit(window, view, forceit=False, *args, **kwargs):
    if forceit:
        view.set_scratch(True)

    if view.is_dirty() and not forceit:
        return message("E37: No write since last change")

    if not view.file_name() and not forceit:
        return message("E32: No file name")

    window.run_command('close')

    if len(window.views()) == 0:
        return window.run_command('close')

    if not window.views_in_group(window.active_group()):
        ExUnvsplit(window=window, view=view, forceit=forceit, *args, **kwargs)


# TODO [refactor] into window module
def ExQall(window, forceit=False, *args, **kwargs):
    if forceit:
        for view in window.views():
            if view.is_dirty():
                view.set_scratch(True)
    elif has_dirty_buffers(window):
        # TODO [review] [easypick] status message
        return status_message('there are unsaved changes!')

    window.run_command('close_all')
    window.run_command('exit')


# TODO [refactor] into window module
def ExWq(window, view, forceit=False, *args, **kwargs):
    if forceit:
        # TODO raise not implemented exception and make the command runner handle it.
        return message('not implemented')

    if view.is_read_only():
        return status_message("can't write a read-only buffer")

    if not view.file_name():
        return status_message("can't save a file without name")

    window.run_command('save')

    ExQuit(window=window, view=view, forceit=forceit, *args, **kwargs)


def ExBrowse(window, view, *args, **kwargs):
    # TODO [review] State dependency
    state = State(view)

    window.run_command('prompt_open_file', {
        'initial_directory': state.settings.vi['_cmdline_cd']
    })


@_changing_cd
def ExEdit(window, view, file_name, cmd, forceit=False, *args, **kwargs):
    # TODO [refactor] file_name_arg
    file_name_arg = file_name
    if file_name_arg:
        file_name = os.path.expanduser(os.path.expandvars(file_name_arg))

        if view.is_dirty() and not forceit:
            return message("E37: No write since last change")

        if os.path.isdir(file_name):
            # TODO :edit Open a file-manager in a buffer
            return message('Cannot open directory')

        def get_file_path():
            file_name = view.file_name()
            if file_name:
                file_dir = os.path.dirname(file_name)
                if os.path.isdir(file_dir):
                    return file_dir

                # TODO [review] State dependency
                state = State(view)

                file_dir = state.settings.vi['_cmdline_cd']
                if os.path.isdir(file_dir):
                    return file_dir

        if not os.path.isabs(file_name):
            file_path = get_file_path()
            if file_path:
                file_name = os.path.join(file_path, file_name)
            else:
                return message("could not find a parent directory")

        window.open_file(file_name)

        if not os.path.exists(file_name):
            parent = os.path.dirname(file_name)
            if parent and not os.path.exists(parent):
                msg = '"{}" [New DIRECTORY]'.format(file_name_arg)
            else:
                msg = '"{}" [New File]'.format(os.path.basename(file_name))

            # Give ST some time to load the new view.
            set_timeout(lambda: status_message(msg), 150)

        return

    if forceit or not view.is_dirty():
        view.run_command('revert')
        return

    if view.is_dirty():
        return message("E37: No write since last change")

    message("E37: No write since last change")


# TODO [refactor] into window module
def ExCquit(window, *args, **kwargs):
    window.run_command('exit')


# TODO [refactor] into window module
def ExExit(window, view, *args, **kwargs):
    if view.is_dirty():
        window.run_command('save')

    window.run_command('close')

    if len(window.views()) == 0:
        window.run_command('exit')


def ExRegisters(window, view, *args, **kwargs):
    def _truncate(string, truncate_at):
        if len(string) > truncate_at:
            return string[0:truncate_at] + ' ...'

        return string

    # TODO [review] State dependency
    state = State(view)

    items = []
    for k, v in state.registers.to_dict().items():
        if v:
            if len(v) > 0 and v[0]:
                lines = v[0].splitlines()
                value = '^J'.join(lines)

                # The splitlines function will remove a final newline, if
                # present. So joining the lines with the join-line indicator
                # (^J) may be missing a final join-line indicator.
                if len(''.join(lines)) < len(v[0]):
                    value += '^J'

                items.append('"{}   {}'.format(k, _truncate(value, 78)))

    def on_done(idx):
        if idx == -1:
            return

        state.registers['"'] = [list(state.registers.to_dict().values())[idx]]

    if items:
        window.show_quick_panel(sorted(items), on_done, flags=MONOSPACE_FONT)


# TODO [refactor] into window module
@_changing_cd
def ExNew(window, *args, **kwargs):
    window.run_command('new_file')


def ExYank(view, register, line_range, *args, **kwargs):
    line_range = line_range.resolve(view)

    if not register:
        register = '"'

    text = view.substr(line_range)

    state = State(view)
    state.registers[register] = [text]

    if register == '"':
        state.registers['0'] = [text]


def ExTabnext(window, *args, **kwargs):
    window_tab_control(window, command='next')


def ExTabprevious(window, *args, **kwargs):
    window_tab_control(window, command='prev')


def ExTablast(window, *args, **kwargs):
    window_tab_control(window, command='last')


def ExTabfirst(window, *args, **kwargs):
    window_tab_control(window, command='first')


def ExTabonly(window, *args, **kwargs):
    window_tab_control(window, command='only')


@_changing_cd
def ExCd(window, view, path=None, forceit=False, *args, **kwargs):
    # XXX Currently behaves as on Unix systems for all platforms.
    if view.is_dirty() and not forceit:
        return message("E37: No write since last change")

    # TODO [review] State dependency
    state = State(view)

    if not path:
        state.settings.vi['_cmdline_cd'] = os.path.expanduser("~")

        return ExPwd(window=window, view=view, path=path, forceit=forceit, *args, **kwargs)

    # TODO: It seems there a few symbols that are always substituted when they represent a
    # filename. We should have a global method of substiting them.
    if path == '%:h':
        fname = view.file_name()
        if fname:
            state.settings.vi['_cmdline_cd'] = os.path.dirname(fname)

            ExPwd(window=window, view=view, path=path, forceit=forceit, *args, **kwargs)

        return

    path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
    if not os.path.exists(path):
        return message("E344: Can't find directory \"%s\" in cdpath" % path)

    state.settings.vi['_cmdline_cd'] = path

    ExPwd(window=window, view=view, path=path, forceit=forceit, *args, **kwargs)


# Non-standard command to change the current directory to the active view's
# directory. In Sublime Text, the current directory doesn't follow the
# active view, so it's convenient to be able to align both easily.
# XXX: Is the above still true?
# XXX: This command may be removed at any time.
def ExCdd(view, forceit=False, *args, **kwargs):
    if view.is_dirty() and not forceit:
        return message("E37: No write since last change")

    path = os.path.dirname(view.file_name())

    try:
        # TODO [review] State dependency
        state = State(view)

        state.settings.vi['_cmdline_cd'] = path
        status_message(path)
    except IOError:
        message("E344: Can't find directory \"%s\" in cdpath" % path)


# TODO [refactor] into window module
# TODO Refactor like ExSplit
def ExVsplit(window, view, file=None, *args, **kwargs):
    max_splits = 4

    layout_data = {
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

    groups = window.num_groups()
    if groups >= max_splits:
        return message('Can\'t create more groups')

    old_view = view
    pos = ''
    current_file_name = None
    if old_view and old_view.file_name():
        pos = ':{0}:{1}'.format(*old_view.rowcol(old_view.sel()[0].b))
        current_file_name = old_view.file_name() + pos

    window.run_command('set_layout', layout_data[groups + 1])

    def open_file(window, file):
        window.open_file(file, group=(window.num_groups() - 1), flags=(FORCE_GROUP | ENCODED_POSITION))

    if file:
        existing = window.find_open_file(file)
        pos = ''
        if existing:
            pos = ':{0}:{1}'.format(*existing.rowcol(existing.sel()[0].b))

        return open_file(window, file + pos)

    if current_file_name:
        open_file(window, current_file_name)
    else:
        window.new_file()


# TODO Unify with <C-w>s
def ExSplit(window, file=None, *args, **kwargs):
    window_split(window, file)


# TODO [review] Either remove or refactor into window module. Preferably remove, because there should be standard commands that can achieve the same thing.  # noqa: E501
# Non-standard Vim :unvsplit command
def ExUnvsplit(window, *args, **kwargs):
    groups = window.num_groups()
    if groups == 1:
        return status_message("can't delete more groups")

    # If we don't do this, cloned views will be moved to the previous group and
    # kept around. We want to close them instead.

    layout_data = {
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

    window.run_command('close')
    window.run_command('set_layout', layout_data[groups - 1])


def ExSetlocal(view, option, value, *args, **kwargs):
    if option.endswith('?'):
        return message('not implemented')

    try:
        set_local(view, option, value)
    except KeyError:
        status_message('no such option')
    except ValueError:
        status_message('invalid value for option')


def ExSet(view, option, value, *args, **kwargs):
    if option.endswith('?'):
        return message('not implemented')

    try:
        set_global(view, option, value)
    except KeyError:
        status_message('no such option')
    except ValueError:
        status_message('invalid value for option')


def ExLet(name, value, *args, **kwargs):
    variables.set(name, value)


def ExWqall(window, *args, **kwargs):
    if not all(view.file_name() for view in window.views()):
        ui_blink()

        return message("E32: No file name")

    if any(view.is_read_only() for view in window.views()):
        ui_blink()

        return message("E45: 'readonly' option is set (add ! to override)")

    window.run_command('save_all')

    # TODO Remove assert statements
    assert not any(view.is_dirty() for view in window.views())

    window.run_command('close_all')
    window.run_command('exit')
