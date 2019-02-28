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
import logging
import os
import re
import stat
import subprocess
import sys

from sublime import DIALOG_CANCEL
from sublime import DIALOG_YES
from sublime import ENCODED_POSITION
from sublime import find_resources
from sublime import FORCE_GROUP
from sublime import LITERAL
from sublime import load_resource
from sublime import MONOSPACE_FONT
from sublime import platform
from sublime import Region
from sublime import set_timeout
from sublime import yes_no_cancel_dialog

from NeoVintageous.nv import shell
from NeoVintageous.nv import variables
from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.parser import parse_command_line
from NeoVintageous.nv.ex.parser import parse_command_line_address
from NeoVintageous.nv.goto import goto_line
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.state import State
from NeoVintageous.nv.ui import ui_blink
from NeoVintageous.nv.vi import utils
from NeoVintageous.nv.vi.search import find_all_in_range
from NeoVintageous.nv.vi.settings import get_cmdline_cwd
from NeoVintageous.nv.vi.settings import set_cmdline_cwd
from NeoVintageous.nv.vi.settings import set_global
from NeoVintageous.nv.vi.settings import set_local
from NeoVintageous.nv.vi.utils import adding_regions
from NeoVintageous.nv.vi.utils import first_sel
from NeoVintageous.nv.vi.utils import has_dirty_buffers
from NeoVintageous.nv.vi.utils import next_non_blank
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vi.utils import resolve_insertion_point_at_b
from NeoVintageous.nv.vi.utils import row_at
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.window import window_buffer_control
from NeoVintageous.nv.window import window_control
from NeoVintageous.nv.window import window_tab_control


_log = logging.getLogger(__name__)


def _init_cwd(f, *args, **kwargs):
    @wraps(f)
    def inner(*args, **kwargs):
        view = kwargs.get('view')
        if not view:
            raise RuntimeError('view is required')

        original_cwd = os.getcwd()
        _log.debug('original cwd: %s', original_cwd)

        try:
            cmdline_cwd = get_cmdline_cwd()
            _log.debug('cmdline cwd: %s', cmdline_cwd)

            if cmdline_cwd and os.path.isdir(cmdline_cwd):
                _log.debug('changing cwd to %s from %s', cmdline_cwd, original_cwd)
                os.chdir(cmdline_cwd)

            f(*args, **kwargs)
        finally:
            if os.path.isdir(original_cwd):
                _log.debug('resetting cwd to %s', original_cwd)
                os.chdir(original_cwd)

    return inner


def _set_next_sel(view, data):
    # TODO [review] Should this overwrite "ex_data": For example it may contain things like the "prev_sel".
    view.settings().set('ex_data', {'next_sel': data})


def _serialize_deserialize(f, *args, **kwargs):

    @wraps(f)
    def inner(*args, **kwargs):
        view = kwargs.get('view')
        if not view:
            raise RuntimeError('view is required')

        # Serialize previous selection.

        sels = [(r.a, r.b) for r in list(view.sel())]
        view.settings().set('ex_data', {'prev_sel': sels})

        f(*args, **kwargs)

        # Deserialise and apply next selection.

        ex_data = view.settings().get('ex_data')
        if 'next_sel' in ex_data:
            next_sel = ex_data['next_sel']
        else:
            next_sel = []

        if next_sel:
            view.sel().clear()
            view.sel().add_all([Region(b) for (a, b) in next_sel])

        # Return to enter normal mode.
        # TODO [review] State dependency
        state = State(view)
        # TODO [review] enter normal mode dependency
        state.enter_normal_mode()
        enter_normal_mode(view, None)

    return inner


def ex_bfirst(window, **kwargs):
    window_buffer_control(window, action='first')


def ex_blast(window, **kwargs):
    window_buffer_control(window, action='last')


def ex_bnext(window, **kwargs):
    window_buffer_control(window, action='next')


def ex_bprevious(window, **kwargs):
    window_buffer_control(window, action='previous')


def ex_browse(window, view, **kwargs):
    window.run_command('prompt_open_file', {
        'initial_directory': get_cmdline_cwd()
    })


def ex_buffers(window, **kwargs):
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


def ex_cd(view, path=None, **kwargs):
    if not path:
        path = os.path.expanduser('~')
    elif path == '%:h':
        fname = view.file_name()
        if fname:
            path = os.path.dirname(fname)
    else:
        path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))

    if not os.path.isdir(path):
        return status_message("E344: Can't find directory \"%s\" in cdpath" % path)

    set_cmdline_cwd(path)
    status_message(path)


def ex_close(window, forceit=False, **kwargs):
    window_control(window, 'c', close_if_last=forceit),


@_serialize_deserialize
def ex_copy(view, edit, address, line_range, **kwargs):
    # Copy the lines given by [range] to below the line given by {address}.
    def _calculate_address(address):
        # TODO: must calc only the first line ref?
        # TODO [refactor] parsing the address
        calculated = parse_command_line_address(address)
        if calculated is None:
            return None

        # TODO Refactor and remove assertions
        assert calculated.command is None, 'bad address'
        assert calculated.line_range.separator is None, 'bad address'

        return calculated.line_range

    try:
        unresolved = _calculate_address(address)
    except Exception:
        return status_message("E14: Invalid address")

    if unresolved is None:
        return status_message("E14: Invalid address")

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
    _set_next_sel(view, [(cursor_dest, cursor_dest)])


# TODO [refactor] into window module
def ex_cquit(window, **kwargs):
    window.run_command('exit')


@_serialize_deserialize
def ex_delete(view, edit, register, line_range, **kwargs):
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
    _set_next_sel(view, [(r.a, r.a)])


def ex_double_ampersand(view, edit, flags, count, line_range, **kwargs):
    ex_substitute(view=view, edit=edit, flags=flags, count=count, line_range=line_range, **kwargs)


@_init_cwd
def ex_edit(window, view, file_name=None, forceit=False, **kwargs):
    if file_name:
        file_name = os.path.expanduser(os.path.expandvars(file_name))

        if view.is_dirty() and not forceit:
            return status_message("E37: No write since last change")

        if os.path.isdir(file_name):
            # TODO In Vim, trying to edit a directory opens a file-manager.
            return status_message('"%s" is a directory', file_name)

        if not os.path.isabs(file_name):
            cwd = get_cmdline_cwd()
            if not os.path.isdir(cwd):
                return status_message("could not find a current working directory")

            file_name = os.path.join(cwd, file_name)

        window.open_file(file_name)

        if not os.path.exists(file_name):
            parent = os.path.dirname(file_name)
            if parent and not os.path.exists(parent):
                msg = '"{}" [New DIRECTORY]'.format(file_name)
            else:
                msg = '"{}" [New File]'.format(os.path.basename(file_name))

            # Give Sublime Text some time to load the new view.
            set_timeout(lambda: status_message(msg), 150)
    else:
        if forceit or not view.is_dirty():
            return view.run_command('revert')

        if view.is_dirty():
            return status_message("E37: No write since last change")

        status_message("E37: No write since last change")


# TODO [refactor] into window module
def ex_exit(window, view, **kwargs):
    if view.is_dirty():
        window.run_command('save')

    window.run_command('close')

    if len(window.views()) == 0:
        window.run_command('exit')


def ex_file(view, **kwargs):
    if view.file_name():
        fname = view.file_name()
    else:
        fname = '[No Name]'

    attrs = ''
    if view.is_read_only():
        attrs = 'readonly'

    if view.is_dirty():
        attrs = 'Modified'

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
        msg += " %d line%s --%d%%--" % (lines, ('s' if lines > 1 else ''), int(percent))

    status_message('%s' % msg)


_ex_global_most_recent_pat = None


# At the time of writing, the only command that supports :global is the
# "print" command e.g. print all lines matching \d+ into new buffer:
#   :%global/\d+/print
def ex_global(window, view, pattern, cmd, line_range, **kwargs):
    if line_range.is_empty:
        global_range = Region(0, view.size())
    else:
        global_range = line_range.resolve(view)

    global _ex_global_most_recent_pat
    if pattern:
        _ex_global_most_recent_pat = pattern
    else:
        pattern = _ex_global_most_recent_pat

    if not cmd:
        cmd = 'print'

    cmd = parse_command_line(cmd).command

    try:
        matches = find_all_in_range(view, pattern, global_range.begin(), global_range.end())
    except Exception as e:
        return status_message("(global): %s ... in pattern '%s'" % (str(e), pattern))

    # The cooperates_with_global attribute indicates if the command supports
    # the :global command. This is special flag, because all ex commands
    # don't yet support a global_lines argument. See TokenOfCommand. At time
    # of writing, the only command that supports the global_lines argument
    # is the "print" command e.g. print all lines matching \d+ into new
    # buffer: ":%global/\d+/print".
    if not matches or not cmd.cooperates_with_global:
        return status_message("command does not support :global")

    matches = [view.full_line(r.begin()) for r in matches]
    matches = [[r.a, r.b] for r in matches]

    cmd.params['global_lines'] = matches

    do_ex_command(window, cmd.target, cmd.params)


_ex_help_tags_cache = {}


def ex_help(window, subject=None, forceit=False, **kwargs):
    if not subject:
        subject = 'help.txt'

        if forceit:
            return status_message("E478: Don't panic!")

    if not _ex_help_tags_cache:
        _log.debug('initializing help tags...')

        tags_resources = [r for r in find_resources(
            'tags') if r.startswith('Packages/NeoVintageous/res/doc/tags')]

        if not tags_resources:
            return status_message('tags file not found')

        tags_matcher = re.compile('^([^\\s]+)\\s+([^\\s]+)\\s+(.+)$')
        tags_resource = load_resource(tags_resources[0])
        for line in tags_resource.split('\n'):
            if line:
                match = tags_matcher.match(line)
                if match:
                    _ex_help_tags_cache[match.group(1)] = (match.group(2), match.group(3))

        _log.debug('finished initializing help tags')

    if subject not in _ex_help_tags_cache:

        # Basic hueristic to find nearest relevant help e.g. `help ctrl-k`
        # will look for "ctrl-k", "c_ctrl-k", "i_ctrl-k", etc. Another
        # example is `:help copy` will look for "copy" then ":copy".
        # Also checks lowercase variants e.g. ctrl-k", "c_ctrl-k, etc., and
        # uppercase variants e.g. CTRL-K", "C_CTRL-K, etc.

        subject_candidates = (
            subject,
            re.sub('ctrl-([a-zA-Z])', lambda m: 'CTRL-' + m.group(1).upper(), subject),
            subject.lower(),
            subject.upper(),
        )

        found = False
        for p in ('', ':', 'c_', 'i_', 'v_', '-', '/'):
            for s in subject_candidates:
                _subject = p + s
                if _subject in _ex_help_tags_cache:
                    subject = _subject
                    found = True

            if found:
                break

        if not found:
            return status_message('E149: Sorry, no help for %s' % subject)

    tag = _ex_help_tags_cache[subject]

    doc_resources = [r for r in find_resources(
        tag[0]) if r.startswith('Packages/NeoVintageous/res/doc/')]

    if not doc_resources:
        return status_message('Sorry, help file "%s" not found' % tag[0])

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

    # Fixes #420 show() doesn't work properly when the Sublime Text
    # animation_enabled is true, which the default in Sublime.
    xy = view.text_to_layout(view.text_point(view.rowcol(c_pt)[0], 0))
    view.set_viewport_position(xy)


def ex_let(name, value, **kwargs):
    variables.set(name, value)


@_serialize_deserialize
def ex_move(view, edit, address, line_range, **kwargs):
    # Move the lines given by [range] to below the line given by {address}.
    if address is None:
        return status_message("E14: Invalid address")

    source = line_range.resolve(view)
    if any(s.contains(source) for s in view.sel()):
        return status_message("E134: Move lines into themselves")

    # TODO [refactor] is parsing the address necessary, if yes, create a parse_address function
    parsed_address_command = parse_command_line_address(address).line_range
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
        _set_next_sel(view, [[destination.a, destination.b]])
        return

    view.insert(edit, destination.end(), text)
    view.erase(edit, source)
    _set_next_sel(view, [[destination.a, destination.a]])


# TODO [refactor] into window module
@_init_cwd
def ex_new(window, **kwargs):
    window.run_command('new_file')


def ex_nnoremap(lhs=None, rhs=None, **kwargs):
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(NORMAL, lhs, rhs)


def ex_noremap(lhs=None, rhs=None, **kwargs):
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(NORMAL, lhs, rhs)
    mappings_add(OPERATOR_PENDING, lhs, rhs)
    mappings_add(VISUAL, lhs, rhs)
    mappings_add(VISUAL_BLOCK, lhs, rhs)
    mappings_add(VISUAL_LINE, lhs, rhs)


def ex_nunmap(lhs, **kwargs):
    try:
        mappings_remove(NORMAL, lhs)
    except KeyError:
        status_message('Mapping not found')


# TODO Unify with CTRL-W CTRL-O
def ex_only(window, view, forceit=False, **kwargs):
    if not forceit and has_dirty_buffers(window):
        return status_message("E445: Other window contains changes")

    current_id = view.id()
    for view in window.views():
        if view.id() == current_id:
            continue

        if view.is_dirty():
            view.set_scratch(True)

        view.close()


def ex_onoremap(lhs=None, rhs=None, **kwargs):
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(OPERATOR_PENDING, lhs, rhs)


def ex_ounmap(lhs, **kwargs):
    try:
        mappings_remove(OPERATOR_PENDING, lhs)
    except KeyError:
        status_message('Mapping not found')


def ex_print(window, view, flags, line_range, global_lines=None, **kwargs):
    if view.size() == 0:
        return status_message("E749: empty buffer")

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


@_init_cwd
def ex_pwd(**kwargs):
    status_message(os.getcwd())


# TODO [refactor] into window module
def ex_qall(window, forceit=False, **kwargs):
    if forceit:
        for view in window.views():
            if view.is_dirty():
                view.set_scratch(True)
    elif has_dirty_buffers(window):
        return status_message('there are unsaved changes!')

    window.run_command('close_all')
    window.run_command('exit')


# TODO [refactor] into window module
def ex_quit(window, view, forceit=False, **kwargs):
    if forceit:
        view.set_scratch(True)

    if view.is_dirty() and not forceit:
        return status_message("E37: No write since last change")

    if not view.file_name() and not forceit:
        return status_message("E32: No file name")

    window.run_command('close')

    if len(window.views()) == 0:
        return window.run_command('close')

    if not window.views_in_group(window.active_group()):
        ex_unvsplit(window=window, view=view, forceit=forceit, **kwargs)


# TODO [review] This command looks unused
# TODO [refactor] shell commands to use common os nv.ex.shell commands
@_init_cwd
def ex_read(view, edit, cmd, line_range, **kwargs):
    r = line_range.resolve(view)
    target_point = min(r.end(), view.size())

    if cmd:
        if platform() == 'linux':
            # TODO: make shell command configurable.
            shell_cmd = view.settings().get('linux_shell')
            shell_cmd = shell_cmd or os.path.expandvars("$SHELL")
            if not shell_cmd:
                return status_message('no shell found')

            try:
                p = subprocess.Popen([shell_cmd, '-c', cmd], stdout=subprocess.PIPE)
            except Exception as e:
                return status_message('error executing command through shell {}'.format(e))

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
            return status_message('not implemented')
    else:
        # Read a file into the current view.
        # According to Vim's help, :r should read the current file's content
        # if no file name is given, but Vim doesn't do that.
        # TODO: implement reading a file into the buffer.
        return status_message('not implemented')


def ex_registers(window, view, **kwargs):
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

                # The splitlines function will remove any trailing newlines. We
                # need to append one if splitlines() removed a trailing one.
                if len(''.join(lines)) < len(v[0]):
                    value += '^J'

                items.append('"{}   {}'.format(k, _truncate(value, 78)))

    def on_done(idx):
        if idx == -1:
            return

        state.registers['"'] = [list(state.registers.to_dict().values())[idx]]

    if items:
        window.show_quick_panel(sorted(items), on_done, flags=MONOSPACE_FONT)


def ex_set(view, option, value, **kwargs):
    if option.endswith('?'):
        return status_message('not implemented')

    try:
        set_global(view, option, value)
    except (KeyError, ValueError):
        status_message('E518: Unknown option: ' + option)


def ex_setlocal(view, option, value, **kwargs):
    if option.endswith('?'):
        return status_message('not implemented')

    try:
        set_local(view, option, value)
    except (KeyError, ValueError):
        status_message('E518: Unknown option: ' + option)


# TODO [refactor] shell commands to use common os nv.ex.shell commands
# This command starts a shell. When the shell exits (after the "exit" command)
# you return to Sublime Text. The name for the shell command comes from:
# * VintageousEx_linux_terminal setting on Linux
# * VintageousEx_osx_terminal setting on OSX
# The shell is opened at the active view directory. Sublime Text keeps a virtual
# current directory that most of the time will be out of sync with the actual
# current directory. The virtual current directory is always set to the current
# view's directory, but it isn't accessible through the API.
@_init_cwd
def ex_shell(view, **kwargs):

    def _open_shell(command):
        return subprocess.Popen(command, cwd=os.getcwd())

    if platform() == 'linux':
        term = view.settings().get('VintageousEx_linux_terminal')
        term = term or os.environ.get('COLORTERM') or os.environ.get('TERM')
        if not term:
            return status_message('terminal not found')

        try:
            _open_shell([term, '-e', 'bash']).wait()
        except Exception as e:
            return status_message('error executing command through shell {}'.format(e))

    elif platform() == 'osx':
        term = view.settings().get('VintageousEx_osx_terminal')
        term = term or os.environ.get('COLORTERM') or os.environ.get('TERM')
        if not term:
            return status_message('terminal not found')

        try:
            _open_shell([term, '-e', 'bash']).wait()
        except Exception as e:
            return status_message('error executing command through shell {}'.format(e))

    elif platform() == 'windows':
        _open_shell(['cmd.exe', '/k']).wait()
    else:
        status_message('not implemented')


_ex_shell_last_command = None


@_init_cwd
def ex_shell_out(view, edit, cmd, line_range, **kwargs):
    global _ex_shell_last_command

    if cmd == '!':
        if not _ex_shell_last_command:
            return status_message('E34: No previous command')

        cmd = _ex_shell_last_command

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

        # TODO: store only successful commands.
        _ex_shell_last_command = cmd
    except NotImplementedError:
        status_message('not implemented')


def ex_snoremap(lhs=None, rhs=None, **kwargs):
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(SELECT, lhs, rhs)


def ex_sort(view, options='', **kwargs):
    case_sensitive = True if 'i' not in options else False

    view.run_command('sort_lines', {'case_sensitive': case_sensitive})

    if 'u' in options:
        view.run_command('permute_lines', {'operation': 'unique'})

    def f(view, s):
        return Region(next_non_blank(view, s.begin()))

    regions_transformer(view, f)
    enter_normal_mode(view, None)


def ex_split(window, file=None, **kwargs):
    window_control(window, 's', file=file)


_ex_substitute_last_pattern = None
_ex_substitute_last_replacement = ''


def ex_substitute(view, edit, line_range, pattern=None, replacement='', flags=None, count=1, **kwargs):
    global _ex_substitute_last_pattern, _ex_substitute_last_replacement

    if flags is None:
        flags = []

    # Repeat last substitute with same search
    # pattern and substitute string, but
    # without the same flags.
    if not pattern:
        pattern = _ex_substitute_last_pattern
        if not pattern:
            return status_message('E33: No previous substitute regular expression')

        replacement = _ex_substitute_last_replacement

    if replacement is None:
        return status_message('No substitute replacement string')

    _ex_substitute_last_pattern = pattern
    _ex_substitute_last_replacement = replacement

    computed_flags = re.MULTILINE
    computed_flags |= re.IGNORECASE if ('i' in flags) else 0

    try:
        compiled_pattern = re.compile(pattern, flags=computed_flags)
    except Exception as e:
        return status_message('[regex error]: {} ... in pattern {}'.format((str(e), pattern)))

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
                    response = yes_no_cancel_dialog('Replace with "%s"?' % replacement)
                    if response == DIALOG_CANCEL:
                        break

                    if response == DIALOG_YES:
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

    enter_normal_mode(view, None)


def ex_sunmap(lhs, **kwargs):
    try:
        mappings_remove(SELECT, lhs)
    except KeyError:
        status_message('Mapping not found')


def ex_tabclose(window, **kwargs):
    window_tab_control(window, action='close')


def ex_tabfirst(window, **kwargs):
    window_tab_control(window, action='first')


def ex_tablast(window, **kwargs):
    window_tab_control(window, action='last')


def ex_tabnext(window, **kwargs):
    window_tab_control(window, action='next')


def ex_tabonly(window, **kwargs):
    window_tab_control(window, action='only')


def ex_tabprevious(window, **kwargs):
    window_tab_control(window, action='previous')


def ex_unmap(lhs, **kwargs):
    try:
        mappings_remove(NORMAL, lhs)
        mappings_remove(OPERATOR_PENDING, lhs)
        mappings_remove(VISUAL, lhs)
        mappings_remove(VISUAL_BLOCK, lhs)
        mappings_remove(VISUAL_LINE, lhs)
    except KeyError:
        status_message('Mapping not found')


# TODO [review] Either remove or refactor into window module. Preferably remove, because there should be standard commands that can achieve the same thing.  # noqa: E501
# Non-standard Vim :unvsplit command
def ex_unvsplit(window, **kwargs):
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


def ex_vnoremap(lhs=None, rhs=None, **kwargs):
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(VISUAL, lhs, rhs)
    mappings_add(VISUAL_BLOCK, lhs, rhs)
    mappings_add(VISUAL_LINE, lhs, rhs)


# TODO [refactor] into window module
# TODO Refactor like ExSplit
def ex_vsplit(window, view, file=None, **kwargs):
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
        return status_message('Can\'t create more groups')

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


def ex_vunmap(lhs, **kwargs):
    try:
        mappings_remove(VISUAL, lhs)
        mappings_remove(VISUAL_BLOCK, lhs)
        mappings_remove(VISUAL_LINE, lhs)
    except KeyError:
        status_message('Mapping not found')


@_init_cwd
def ex_wall(window, forceit=False, **kwargs):
    # TODO read-only views don't get properly saved.
    for v in (v for v in window.views() if v.file_name()):
        if v.is_read_only() and not forceit:
            continue

        v.run_command('save')


# TODO [refactor] into window module
def ex_wq(window, view, forceit=False, **kwargs):
    if forceit:
        # TODO raise not implemented exception and make the command runner handle it.
        return status_message('not implemented')

    if view.is_read_only():
        return status_message("can't write a read-only buffer")

    if not view.file_name():
        return status_message("can't save a file without name")

    window.run_command('save')

    ex_quit(window=window, view=view, forceit=forceit, **kwargs)


def ex_wqall(window, **kwargs):
    if not all(view.file_name() for view in window.views()):
        ui_blink()

        return status_message("E32: No file name")

    if any(view.is_read_only() for view in window.views()):
        ui_blink()

        return status_message("E45: 'readonly' option is set (add ! to override)")

    window.run_command('save_all')

    # TODO Remove assert statements
    assert not any(view.is_dirty() for view in window.views())

    window.run_command('close_all')
    window.run_command('exit')


@_init_cwd
def ex_write(window, view, file_name, cmd, line_range, forceit=False, **kwargs):
    options = kwargs.get('++')
    appends = kwargs.get('>>')

    if options:
        return status_message('++opt isn\'t implemented for :write')

    if cmd:
        return status_message('!cmd not implememted for :write')

    if not view:
        return

    def _check_is_readonly(fname):
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
                return status_message("E212: Can't open file for writing: %s" % file_name)

            try:
                with open(file_name, 'at') as f:
                    text = view.substr(r)
                    f.write(text)

                # TODO: make this `show_info` instead.
                return status_message('Appended to ' + os.path.abspath(file_name))

            except IOError as e:
                return status_message('could not write file {}'.format(str(e)))

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
            enter_normal_mode(window, state.mode)
            state.enter_normal_mode()

        return _do_append(view, file_name, forceit, line_range)

    if cmd:
        return status_message('!cmd isn\'t implemented for :write')

    if file_name:
        def _do_write(window, view, file_name, forceit, line_range):
            fname = file_name

            if not forceit:
                if os.path.exists(fname):
                    ui_blink()

                    return status_message("E13: File exists (add ! to override)")

                if _check_is_readonly(fname):
                    ui_blink()

                    return status_message("E45: 'readonly' option is set (add ! to override)")

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

                view.retarget(expanded_path)
                window.run_command('save')

            except IOError:
                return status_message("E212: Can't open file for writing: {}".format(fname))

        return _do_write(window, view, file_name, forceit, line_range)

    if not view.file_name():
        return status_message("E32: No file name")

    read_only = (_check_is_readonly(view.file_name()) or view.is_read_only())

    if read_only and not forceit:
        ui_blink()

        return status_message("E45: 'readonly' option is set (add ! to override)")

    window.run_command('save')


def ex_yank(view, register, line_range, **kwargs):
    line_range = line_range.resolve(view)

    if not register:
        register = '"'

    text = view.substr(line_range)

    state = State(view)
    state.registers[register] = [text]

    if register == '"':
        state.registers['0'] = [text]


# Default ex command. See :h [range].
def _default_ex_cmd(window, view, line_range, **kwargs):
    _log.debug('default ex cmd %s %s', line_range, kwargs)

    line = row_at(view, line_range.resolve(view).a) + 1

    # TODO [review] State dependency
    state = State(view)
    enter_normal_mode(window, state.mode)
    state.enter_normal_mode()
    goto_line(view, line, state.mode)


def _get_ex_cmd(name):
    ex_cmd = getattr(sys.modules[__name__], 'ex_' + name, None)

    if not ex_cmd:
        raise RuntimeError("unknown ex cmd '{}'".format(name))

    # TODO Do we really need this check?
    if not inspect.isfunction(ex_cmd):
        raise RuntimeError("unknown ex cmd type '{}'".format(name))

    return ex_cmd


# This function is used by the command **_nv_ex_cmd_edit_wrap**. The
# **_nv_ex_cmd_edit_wrap** command is required to wrap ex commands that need a
# Sublime Text edit token. Edit tokens can only be obtained from a TextCommand.
# Some ex commands don't need an edit token, those commands don't need to be
# wrapped by a text command.
#
# Arguments belonging to this function are underscored to avoid collisions with
# the ex command args in kwargs.
def do_ex_cmd_edit_wrap(self, edit, _name=None, _line=None, **kwargs):
    _log.debug('do ex cmd edit wrap _name=%s _line=%s kwargs=%s', _name, _line, kwargs)

    if _name:
        ex_cmd = _get_ex_cmd(_name)
        args = kwargs

        window = self.view.window()
        if window:
            args['window'] = window

        # TODO [review] This function is wrapped by a Sublime Text command (see
        # above), which means objects like the RangeNode() can't be passed
        # through. For the moment it just defaults to an empty RangeNode.

        # TODO [review] Ex commands could probably make the line_range optional.

        ex_cmd(view=self.view, edit=edit, line_range=RangeNode(), **args)

    elif _line:
        cmdline = parse_command_line(_line[1:])
        ex_cmd = _get_ex_cmd(cmdline.command.target)

        args = cmdline.command.params
        if 'forceit' not in args:
            args['forceit'] = cmdline.command.forced

        args.update(kwargs)

        window = self.view.window()
        if window:
            args['window'] = window

        ex_cmd(view=self.view, edit=edit, line_range=cmdline.line_range, **args)

    else:
        raise RuntimeError('_name or _line is required')


def do_ex_command(window, name, args=None):
    # type: (...) -> None
    #
    # Execute ex commands by name with arguments.
    #
    # Args:
    #   window (sublime.Window):
    #   name (str):
    #   args (dict[str, [bool|int|str|dict]]):
    #
    # This is the preferred api to use when calling ex commands, because it does
    # several sanity checks e.g. ensures the ex command receives a valid view or
    # edit object (if it required one).
    #
    # >>> do_ex_command(window, 'help', {'subject': 'neovintageous'})
    #
    # This is roughly equivalent to running the cmdline command:
    #
    #     :help neovintageous
    #
    # Or calling the ex command explicitly (though you should prefer to use this
    # api):
    #
    #   ex_help(window=window, subject='neovintageous')
    #
    # To see what arguments are available for an ex command, read the relevant
    # ex command function signature: the commands are located in this module and
    # are prefixed with "ex_" e.g. ex_help(...), ex_write(...).
    #
    # If you need to call an ex command as a string value rather than by name
    # and arguments (though you should prefer to use this api), see the
    # do_ex_cmdline() function.

    _log.debug('do ex command %s %s', name, args)

    if args is None:
        args = {}

    ex_cmd = _get_ex_cmd(name)

    if 'edit' in inspect.signature(ex_cmd).parameters:
        args['_name'] = name

        return window.run_command('_nv_ex_cmd_edit_wrap', args)

    view = window.active_view()
    if view:
        args['view'] = view

    _log.debug('execute ex command: %s %s', name, args)

    # TODO [review] This function is wrapped by a Sublime Text command (see
    # above), which means objects like the RangeNode() can't be passed through.
    # For the moment it just defaults to an empty RangeNode.

    # TODO [review] Ex commands could probably make the line_range optional.

    ex_cmd(window=window, line_range=RangeNode(), **args)


def _parse_user_cmdline(line):
    re_cmd = '[A-Z][a-zA-Z_]*'
    re_arg_name = '[a-zA-Z_]+'
    re_arg_value = '[a-zA-Z0-9\\.\n\t@_-]+'

    match = re.match('^\\:(?P<cmd>' + re_cmd + ')(?P<args>(?:\\s' + re_arg_name + '=' + re_arg_value + ')+)?$', line)
    if not match:
        return None

    command = match.groupdict()

    # TODO Refactor coerce to underscore.
    cmd = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', command['cmd'])
    cmd = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', cmd)
    cmd = cmd.replace("-", "_")
    cmd = cmd.lower()

    command['cmd'] = cmd

    if command['args']:
        argsv = re.findall('\\s(?P<name>' + re_arg_name + ')=(?P<value>' + re_arg_value + ')', command['args'])
        if argsv:
            args = {}
            for name, value in argsv:
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                elif re.match('^(?:-)?[0-9]+$', value):
                    value = int(value)
                elif re.match('^(?:-)?(?:[0-9]+\\.)[0-9]+$', value):
                    value = float(value)

                args[name] = value

            if args:
                command['args'] = args

    return command


def do_ex_cmdline(window, line):
    # type: (...) -> None
    #
    # Execute ex command as a string (what a user would enter at the cmdline).
    #
    # Args:
    #   window (sublime.Window):
    #   line (str):
    #
    # The line MUST begin with a colon:
    #
    # >>> do_ex_cmdline(window, ':help neovintageous')
    #
    # This is roughly equivalent to executing the command via the preferred api:
    #
    # >>> do_ex_command(window, 'help', {'subject': 'neovintageous'})
    #
    # Commands MUST not begin with an underscore. This would be invalid:
    #
    # >>> do_ex_cmdline(window, ':_help neovintageous')
    #
    # User Sublime Text commands are supported by starting the command name with
    # an **uppercase letter**. This is to avoid confusion with built-in Ex
    # commands. The command name is coerced to snake_case before executing:
    #
    # >>> do_ex_cmdline(window, ':CommandName')
    #
    # Is roughly equivalant to:
    #
    # >>> sublime.active_window().run('command_name')
    #
    # Arguments are accepted in basic use-cases. Values true and false are
    # converted to boolean, and digits are converted to integers. Examples:
    #
    # >>> do_ex_cmdline(window, ':CommandName str=fizz bool=true int=42')
    #
    # Is roughly equivalant to:
    #
    # >>> sublime.active_window().run('command_name', {'str': 'fizz', 'bool': True, 'int': 42})

    _log.debug('do ex cmdline >>>%s<<<', line)

    if len(line) < 2:
        raise RuntimeError('cmdline must be at least 2 characters long and begin a colon')

    if line[0] != ':':
        raise RuntimeError('cmdline must start with a colon')

    if line[1].isupper():
        # Run user command. User commands begin with an uppercase letter.
        user_command = _parse_user_cmdline(line)
        if not user_command:
            return status_message('invalid command')

        _log.debug('execute user ex command: %s', user_command)

        return window.run_command(user_command['cmd'], user_command['args'])

    try:
        cmdline = parse_command_line(line[1:])
    except Exception as e:
        return status_message(str(e))

    if not cmdline.command:
        # Do default ex command. The default ex command is not associated with
        # any ex command. See :h [range].
        view = window.active_view()
        if not view:
            raise RuntimeError('an active view is required for default ex cmd')

        if not cmdline.line_range:
            return status_message('invalid command')

        return _default_ex_cmd(window=window, view=view, line_range=cmdline.line_range)

    ex_cmd = _get_ex_cmd(cmdline.command.target)

    # TODO [review] Objects like the RangeNode() can't be passed through Sublime Text  commands, command args only accept simple data types, which is why we send the line which will be parsed again by the wrapper command. Ideally we wouldn't need to parse the line again.  # noqa: E501
    if 'edit' in inspect.signature(ex_cmd).parameters:
        return window.run_command('_nv_ex_cmd_edit_wrap', {'_line': line})

    args = cmdline.command.params

    view = window.active_view()
    if view:
        args['view'] = view

    _log.debug('execute ex command: %s %s', cmdline.command.target, args)

    ex_cmd(window=window, line_range=cmdline.line_range, forceit=cmdline.command.forced, **args)


# TODO [refactor] Into do_ex_cmdline() with a param to indicate user cmdline? e.g do_ex_cmdline(window, line, interactive=True).  # noqa: E501
def do_ex_user_cmdline(window, line):
    # type: (...) -> None
    #
    # Execute an interactive ex command (what a user would use in a mapping).
    #
    # Args:
    #   window (Window):
    #   line (str):
    #
    # This is almost equivalent to do_ex_cmdline(), except:
    #
    # * If the line is equal to a colon then the cmdline is invoked with no
    #   initial text (this is as though the user pressed colon).
    #
    # * If the line does not end with <CR> then the cmdline is invoked with the
    #   line set as the initial text.
    #
    # Otherwise the trailing <CR> is stripped and the line passed to
    # do_ex_cmdline().

    _log.debug('do ex user cmdline >>>%s<<<', line)

    if line.endswith('<CR>'):
        do_ex_cmdline(window, line[:-4])
    else:
        if ':' == line:
            return window.run_command('_nv_cmdline')
        elif line[0] != ':':
            raise RuntimeError('user cmdline must begin with a colon')

        return window.run_command('_nv_cmdline', args={'initial_text': line})
