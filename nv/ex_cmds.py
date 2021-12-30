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
import sys
import traceback

from sublime import DIALOG_CANCEL
from sublime import DIALOG_YES
from sublime import ENCODED_POSITION
from sublime import FORCE_GROUP
from sublime import LITERAL
from sublime import Region
from sublime import find_resources
from sublime import load_resource
from sublime import set_timeout
from sublime import yes_no_cancel_dialog

from NeoVintageous.nv import shell
from NeoVintageous.nv import variables
from NeoVintageous.nv.cmdline import CmdlineOutput
from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.parser import parse_command_line
from NeoVintageous.nv.ex.parser import resolve_address
from NeoVintageous.nv.goto import goto_line
from NeoVintageous.nv.history import history
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.options import set_option
from NeoVintageous.nv.options import toggle_option
from NeoVintageous.nv.polyfill import is_file_read_only
from NeoVintageous.nv.polyfill import is_view_read_only
from NeoVintageous.nv.polyfill import save
from NeoVintageous.nv.polyfill import spell_add
from NeoVintageous.nv.polyfill import spell_undo
from NeoVintageous.nv.polyfill import view_find
from NeoVintageous.nv.polyfill import view_find_all_in_range
from NeoVintageous.nv.polyfill import view_to_region
from NeoVintageous.nv.registers import registers_get_all
from NeoVintageous.nv.registers import registers_set
from NeoVintageous.nv.search import clear_search_highlighting
from NeoVintageous.nv.search import is_smartcase_pattern
from NeoVintageous.nv.settings import get_cmdline_cwd
from NeoVintageous.nv.settings import get_ex_global_last_pattern
from NeoVintageous.nv.settings import get_ex_shell_last_command
from NeoVintageous.nv.settings import get_ex_substitute_last_pattern
from NeoVintageous.nv.settings import get_ex_substitute_last_replacement
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import reset_setting
from NeoVintageous.nv.settings import set_cmdline_cwd
from NeoVintageous.nv.settings import set_ex_global_last_pattern
from NeoVintageous.nv.settings import set_ex_shell_last_command
from NeoVintageous.nv.settings import set_ex_substitute_last_pattern
from NeoVintageous.nv.settings import set_ex_substitute_last_replacement
from NeoVintageous.nv.settings import set_setting
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.utils import adding_regions
from NeoVintageous.nv.utils import has_dirty_buffers
from NeoVintageous.nv.utils import has_newline_at_eof
from NeoVintageous.nv.utils import next_non_blank
from NeoVintageous.nv.utils import regions_transformer
from NeoVintageous.nv.utils import row_at
from NeoVintageous.nv.utils import set_selection
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.window import window_buffer_control
from NeoVintageous.nv.window import window_control
from NeoVintageous.nv.window import window_quit_view
from NeoVintageous.nv.window import window_tab_control


_log = logging.getLogger(__name__)


def _init_cwd(f, *args, **kwargs):
    @wraps(f)
    def inner(*args, **kwargs) -> None:
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


def ex_bfirst(window, **kwargs) -> None:
    window_buffer_control(window, action='first')


def ex_blast(window, **kwargs) -> None:
    window_buffer_control(window, action='last')


def ex_bnext(window, **kwargs) -> None:
    window_buffer_control(window, action='next')


def ex_bprevious(window, **kwargs) -> None:
    window_buffer_control(window, action='previous')


def ex_browse(window, view, **kwargs) -> None:
    window.run_command('prompt_open_file', {'initial_directory': get_cmdline_cwd()})


def ex_buffer(window, index: int = None, **kwargs) -> None:
    if index is None:
        return

    window_buffer_control(window, 'goto', index)
    if index != window.active_view().id():
        ui_bell('E86: Buffer %s does not exist' % index)


def ex_buffers(window, **kwargs) -> None:
    def _format_buffer_line(view) -> str:
        path = view.file_name()
        if path:
            parent, leaf = os.path.split(path)
            path = os.path.join(os.path.basename(parent), leaf)
        else:
            path = view.name() or '[No Name]'

        current_indicator = '%' if view.id() == window.active_view().id() else ' '
        readonly_indicator = '=' if is_view_read_only(view) else ' '
        modified_indicator = '+' if view.is_dirty() else ' '

        active_group_view = window.active_view_in_group(window.get_view_index(view)[0])
        visibility_indicator = 'a' if active_group_view and view.id() == active_group_view.id() else 'h'

        return '%5d %s%s%s%s "%s"' % (
            view.id(),
            current_indicator,
            visibility_indicator,
            readonly_indicator,
            modified_indicator,
            path
        )

    output = CmdlineOutput(window)
    output.write("\n".join([_format_buffer_line(view) for view in window.views()]))
    output.show()


def _expand_to_realpath(path: str) -> str:
    expanded_user = os.path.expanduser(path)
    expanded_vars = os.path.expandvars(expanded_user)

    return os.path.realpath(expanded_vars)


@_init_cwd
def ex_cd(view, path=None, **kwargs) -> None:
    if not path:
        path = os.path.expanduser('~')
    elif path == '%:h':
        fname = view.file_name()
        if fname:
            path = os.path.dirname(fname)
    else:
        path = _expand_to_realpath(path)

    if not os.path.isdir(path):
        return status_message("E344: Can't find directory \"%s\" in cdpath" % path)

    set_cmdline_cwd(path)
    status_message(path)


def ex_close(window, forceit: bool = False, **kwargs) -> None:
    window_control(window, 'c', close_if_last=forceit)


def ex_copy(view, edit, line_range: RangeNode, address=None, **kwargs) -> None:
    if address is None:
        return status_message("E14: Invalid address")

    source = line_range.resolve(view)

    destination = resolve_address(view, address)
    if destination == Region(-1):
        destination_pt = 0
    else:
        destination_pt = view.text_point(row_at(view, destination.begin()) + 1, 0)

    text = view.substr(source)

    if destination_pt >= view.size() and not has_newline_at_eof(view):
        destination_pt = view.size()
        text = '\n' + text[:-1]

    view.insert(edit, destination_pt, text)

    new_sel = view.line(destination_pt + len(text) - 1).begin()

    set_selection(view, new_sel)
    enter_normal_mode(view)


def ex_cquit(window, **kwargs) -> None:
    window.run_command('exit')


def ex_delete(view, edit, register: str, line_range: RangeNode, global_lines=None, **kwargs) -> None:
    try:
        r = line_range.resolve(view)
    except ValueError as e:
        ui_bell(str(e))
        return

    if r == Region(-1, -1):
        r = view.full_line(0)

    rs = [r]

    # If :global called us, ignore the parsed range.
    if global_lines:
        rs = [Region(a, b) for (a, b) in global_lines]

    def _select(view, regions: list, register: str) -> None:
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

            registers_set(view, register, [text])

    # Save stuff to be deleted in register
    if global_lines:
        _select(view, [Region(r.a, r.b - 1) for r in rs], register)
    else:
        _select(view, [Region(r.a, r.b) for r in rs], register)

    # Build regions to be selected after deletion
    deleted_so_far = 0
    new_sel_pos = []
    for r in rs:
        new_sel_pos.append(r.a - deleted_so_far)
        size_of_region = r.b - r.a
        deleted_so_far += size_of_region

    # Delete
    for r in reversed(rs):
        view.erase(edit, r)

    new_sel = view.sel()[-1].b

    set_selection(view, new_sel)
    enter_normal_mode(view)


def ex_double_ampersand(view, edit, flags, count: int, line_range: RangeNode, **kwargs) -> None:
    ex_substitute(view=view, edit=edit, flags=flags, count=count, line_range=line_range, **kwargs)


@_init_cwd
def ex_edit(window, view, file_name: str = None, forceit: bool = False, **kwargs) -> None:
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


def ex_exit(window, view, **kwargs) -> None:
    _do_write(view)

    window.run_command('close')

    if len(window.views()) == 0:
        window.run_command('exit')


def ex_file(view, **kwargs) -> None:
    msg = '"{}"'.format(view.file_name() if view.file_name() else '[No Name]')

    if view.is_read_only():
        msg += " [readonly]"
    elif view.is_dirty():
        msg += " [Modified]"

    if view.size() > 0:
        line_count = view.rowcol(view.size())[0] + 1
        cursor_line_number = view.rowcol(view.sel()[0].b)[0] + 1

        if cursor_line_number < line_count:
            cursor_line_as_percent = int(round(round(100 / line_count, 2) * cursor_line_number, 2))
        else:
            cursor_line_as_percent = 100

        msg += " %d line%s --%d%%--" % (line_count, ('s' if line_count > 1 else ''), cursor_line_as_percent)
    else:
        msg += ' --No lines in buffer--'

    status_message('%s' % msg)


def ex_global(window, view, pattern: str, line_range: RangeNode, cmd='print', **kwargs) -> None:
    if not pattern:
        pattern = get_ex_global_last_pattern()
        if not pattern:
            return status_message('E35: No previous regular expression')

    cmd = parse_command_line(cmd).command
    # The cooperates_with_global flag indicates if a command supports :global.
    if not cmd.cooperates_with_global:
        return status_message('command "%s" does not support :global', cmd.target)

    # The default line specifier for most commands is the cursor position, but
    # the commands :write and :global have the whole file (1,$) as default.
    if line_range.is_empty:
        region = view_to_region(view)
    else:
        region = line_range.resolve(view)

    matches = view_find_all_in_range(view, pattern, region.a, region.b - 1)
    if not matches:
        return status_message('Pattern not found: %s', pattern)

    matches = [view.full_line(r.begin()) for r in matches]
    matches = [[r.a, r.b] for r in matches]

    # Handle `:g!`/`:global!`
    # The `!` is translated into `kwargs['forceit'] == True` and means we should
    # pick all lines _not_ matching the pattern.
    if kwargs.get('forceit', False):
        inv_pos = region.a
        new_matches = []
        for a, b in matches:
            new_matches.append([inv_pos, a])
            inv_pos = b
        new_matches.append([inv_pos, region.b])
        matches = new_matches

    cmd.params['global_lines'] = matches

    do_ex_command(window, cmd.target, cmd.params)
    set_ex_global_last_pattern(pattern)


_help_tags_cache = {}  # type: dict


def ex_help(window, subject: str = None, forceit: bool = False, **kwargs) -> None:
    if not subject:
        subject = 'help.txt'

        if forceit:
            status_message("E478: Don't panic!")
            return

    if not _help_tags_cache:
        tags_matcher = re.compile('^([^\\s]+)\\s+([^\\s]+)\\s+(.+)$')
        for line in load_resource('Packages/NeoVintageous/res/doc/tags').split('\n'):
            if line:
                match = tags_matcher.match(line)
                if match:
                    _help_tags_cache[match.group(1)] = (match.group(2), match.group(3))

    subject = subject.rstrip()

    # Recognize a few exceptions e.g. some strings that contain '*' with "star",
    # "|" with "bar" and '"' with "quote".
    subject_replacements = {
        "*": "star",
        "g*": "gstar",
        "[*": "[star",
        "]*": "]star",
        "/*": "/star",
        "/\\*": "/\\star",
        "\"*": "quotestar",
        "**": "starstar",
        "/|": "/bar",
        "/\\|": "/\\bar",
        '|': 'bar',
        '"': 'quote'
    }

    try:
        subject = subject_replacements[subject]
    except KeyError:
        pass

    if subject not in _help_tags_cache:

        # Basic hueristic to find nearest relevant help e.g. `help ctrl-k` will
        # look for "ctrl-k", "c_ctrl-k", "i_ctrl-k", etc. Another example is
        # `:help copy` will look for "copy" then ":copy". Also checks lowercase
        # variants e.g. ctrl-k", "c_ctrl-k, etc., and uppercase variants e.g.
        # CTRL-K", "C_CTRL-K, etc.

        subject_candidates = [subject]

        if subject.lower() not in subject_candidates:
            subject_candidates.append(subject.lower())

        if subject.upper() not in subject_candidates:
            subject_candidates.append(subject.upper())

        ctrl_key = re.sub('ctrl-([a-zA-Z])', lambda m: 'CTRL-' + m.group(1).upper(), subject)
        if ctrl_key not in subject_candidates:
            subject_candidates.append(ctrl_key)

        found = False
        for p in ('', ':', 'c_', 'i_', 'v_', '-', '/'):
            for s in subject_candidates:
                _subject = p + s
                if _subject in _help_tags_cache:
                    subject = _subject
                    found = True
                    break

            if found:
                break

    try:
        help_file, help_tag = _help_tags_cache[subject]
    except KeyError:
        status_message('E149: Sorry, no help for %s' % subject)
        return

    help_file_resource = 'Packages/NeoVintageous/res/doc/' + help_file

    # TODO There must be a better way to test for the existence of a resource.
    doc_resources = [r for r in find_resources(help_file) if r.startswith('Packages/NeoVintageous/res/doc/')]
    if not doc_resources:
        # This should only happen if the help "tags" file is out of date.
        status_message('Sorry, help file "%s" not found' % help_file)
        return

    def _window_find_open_view(window, name: str):
        for view in window.views():
            if view.name() == name:
                return view

    help_view_name = '%s [vim help]' % (help_file)
    view = _window_find_open_view(window, help_view_name)
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
        view.run_command('nv_view', {'action': 'insert', 'text': load_resource(help_file_resource)})
        view.set_read_only(True)

    # Format the tag so that we can
    # do a literal search rather
    # than regular expression.
    tag_region = view_find(view, help_tag.lstrip('/').replace('\\/', '/').replace('\\\\', '\\'), 0, LITERAL)
    if not tag_region:
        # This should only happen if the help "tags" file is out of date.
        tag_region = Region(0)

    # Add one point so that the cursor is
    # on the tag rather than the tag
    # punctuation star character.
    c_pt = tag_region.begin() + 1

    set_selection(view, c_pt)
    view.show(c_pt, False)

    # Fixes #420 show() doesn't work properly when the Sublime Text
    # animation_enabled is true, which the default in Sublime.
    xy = view.text_to_layout(view.text_point(view.rowcol(c_pt)[0], 0))
    view.set_viewport_position(xy)


def ex_history(window, name: str = 'all', **kwargs) -> None:
    output = CmdlineOutput(window)
    output.write(history(name))
    output.show()


def ex_inoremap(lhs: str = None, rhs: str = None, **kwargs) -> None:
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(INSERT, lhs, rhs)


def ex_let(name, value, **kwargs) -> None:
    variables.set(name, re.sub('^(?:"|\')(.*)(?:"|\')$', '\\1', value))


def ex_move(view, edit, line_range: RangeNode, address: str = None, **kwargs) -> None:
    if address is None:
        return status_message("E14: Invalid address")

    source = line_range.resolve(view)
    if any(s.contains(source) for s in view.sel()):
        return status_message("E134: Move lines into themselves")

    destination = resolve_address(view, address)
    if destination == source:
        return

    if destination == Region(-1):
        destination = Region(0)

    text = view.substr(source)
    new_sel = destination.end() - source.size()

    if destination.end() >= view.size() and not has_newline_at_eof(view):
        text = '\n' + text.rstrip()
        new_sel += 1

    if destination.end() <= source.begin():
        if not text.endswith('\n'):
            text += '\n'

        new_sel = destination.b

        view.erase(edit, source)
        view.insert(edit, destination.end(), text)
    else:
        view.insert(edit, destination.end(), text)
        view.erase(edit, source)

    set_selection(view, new_sel)
    enter_normal_mode(view)


@_init_cwd
def ex_new(window, **kwargs) -> None:
    window.run_command('new_file')


def ex_nnoremap(lhs: str = None, rhs: str = None, **kwargs) -> None:
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(NORMAL, lhs, rhs)


def ex_nohlsearch(view, **kwargs) -> None:
    clear_search_highlighting(view)


def ex_noremap(lhs: str = None, rhs: str = None, **kwargs) -> None:
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(NORMAL, lhs, rhs)
    mappings_add(OPERATOR_PENDING, lhs, rhs)
    mappings_add(VISUAL, lhs, rhs)
    mappings_add(VISUAL_BLOCK, lhs, rhs)
    mappings_add(VISUAL_LINE, lhs, rhs)


def ex_nunmap(lhs: str, **kwargs) -> None:
    try:
        mappings_remove(NORMAL, lhs)
    except KeyError:
        status_message('E31: No such mapping')


# TODO Unify with CTRL-W CTRL-O
def ex_only(window, view, forceit: bool = False, **kwargs) -> None:
    if not forceit and has_dirty_buffers(window):
        status_message("E445: Other window contains changes")
        return

    current_id = view.id()
    for view in window.views():
        if view.id() == current_id:
            continue

        if view.is_dirty():
            view.set_scratch(True)

        view.close()


def ex_onoremap(lhs: str = None, rhs: str = None, **kwargs) -> None:
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(OPERATOR_PENDING, lhs, rhs)


def ex_ounmap(lhs: str, **kwargs) -> None:
    try:
        mappings_remove(OPERATOR_PENDING, lhs)
    except KeyError:
        status_message('E31: No such mapping')


def ex_print(window, view, line_range: RangeNode, flags: list = None, global_lines=None, **kwargs) -> None:
    if view.size() == 0:
        return status_message("E749: empty buffer")

    if flags is None:
        flags = []

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
def ex_pwd(**kwargs) -> None:
    status_message(os.getcwd())


def ex_qall(window, forceit: bool = False, **kwargs) -> None:
    if forceit:
        for view in window.views():
            if view.is_dirty():
                view.set_scratch(True)
    elif has_dirty_buffers(window):
        status_message("E37: No write since last change")
        return

    window.run_command('close_all')
    window.run_command('exit')


def ex_quit(**kwargs) -> None:
    window_quit_view(**kwargs)


@_init_cwd
def ex_read(view, edit, line_range: RangeNode, cmd: str = None, file_name: str = None, **kwargs) -> None:
    if cmd:
        content = shell.read(view, cmd).strip()
        if content:
            insertion_pt = line_range.resolve(view).end()
            view.insert(edit, insertion_pt, content + '\n')
            set_selection(view, view.line(insertion_pt + len(content)).a)

    # TODO :read [name] According to Vim's help :read should read the current
    # file's content *if no file is given* but Vim doesn't seem to do that.
    elif file_name:
        ui_bell(':read [file] is not yet implemeneted; please open an issue')


def ex_registers(window, view, **kwargs) -> None:
    def _truncate(string: str, truncate_at: int) -> str:
        if len(string) > truncate_at:
            return string[0:truncate_at] + ' ...'

        return string

    items = []
    registers = registers_get_all(view).items()
    for k, v in registers:
        if v:
            multiple_values = []

            for part in v:
                lines = part.splitlines()
                # ^J indicates a newline
                part_value = '^J'.join(lines)

                # The splitlines function will remove any trailing newlines. We
                # need to append one if splitlines() removed a trailing one.
                if len(''.join(lines)) < len(v[0]):
                    part_value += '^J'

                multiple_values.append(part_value)

            # ^V indicates a visual block
            items.append('"{}   {}'.format(k, _truncate('^V'.join(multiple_values), 120)))

    items.sort()
    items.insert(0, '--- Registers ---')
    output = CmdlineOutput(window)
    output.write("\n".join(items))
    output.show()


def ex_set(option: str, value, **kwargs) -> None:
    view = kwargs.get('view', None)
    if not view:
        return

    try:
        if option.endswith('?'):
            name = option[:-1]
            value = get_option(view, name)

            if value is True:
                msg = name
            elif value is False:
                msg = 'no' + name
            else:
                msg = '%s=%s' % (name, value)

            status_message('%s', msg)
        elif option.endswith('!'):
            toggle_option(view, option[:-1])
        elif option.startswith('inv'):
            toggle_option(view, option[3:])
        else:
            set_option(view, option, value)

    except KeyError:
        status_message('E518: Unknown option: ' + option)
    except ValueError as e:
        status_message(str(e))


def ex_setlocal(**kwargs) -> None:
    ex_set(**kwargs)


@_init_cwd
def ex_shell(view, **kwargs) -> None:
    shell.open(view)


def ex_silent(window, view, command: str = None, **kwargs) -> None:
    if not command:
        return

    set_setting(view, 'shell_silent', True)
    do_ex_cmdline(window, ':' + command)
    reset_setting(view, 'shell_silent')


@_init_cwd
def ex_shell_out(view, edit, cmd: str, line_range: RangeNode, **kwargs) -> None:
    if cmd == '!':
        cmd = get_ex_shell_last_command()
        if not cmd:
            return status_message('E34: No previous command')

    if '%' in cmd:
        file_name = view.file_name()
        if not file_name:
            return status_message('E499: Empty file name for \'%\' or \'#\', only works with ":p:h"')

        cmd = cmd.replace('%', file_name)

    try:
        if not line_range.is_empty:
            shell.filter_thru_shell(
                view=view,
                edit=edit,
                regions=[line_range.resolve(view)],
                cmd=cmd
            )
        else:
            cmdline_output = CmdlineOutput(view.window())
            cmdline_output.write(shell.read(view, cmd))
            if not get_setting(view, 'shell_silent'):
                cmdline_output.show()

        # TODO: store only successful commands.
        set_ex_shell_last_command(cmd)
    except Exception:  # pragma: no cover
        traceback.print_exc()


def ex_snoremap(lhs: str = None, rhs: str = None, **kwargs) -> None:
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(SELECT, lhs, rhs)


def ex_sort(view, options: str = '', **kwargs) -> None:
    case_sensitive = True if 'i' not in options else False

    view.run_command('mark_undo_groups_for_gluing')
    view.run_command('sort_lines', {'case_sensitive': case_sensitive})

    if 'u' in options:
        view.run_command('permute_lines', {'operation': 'unique'})

    def f(view, s: Region) -> Region:
        return Region(next_non_blank(view, s.begin()))

    regions_transformer(view, f)
    enter_normal_mode(view)
    view.show(view.sel()[-1], False)
    view.run_command('glue_marked_undo_groups')


def ex_split(window, file: str = None, **kwargs) -> None:
    window_control(window, 's', file=file)


def ex_spellgood(view, word: str, **kwargs) -> None:
    spell_add(view, word)


def ex_spellundo(word: str, **kwargs) -> None:
    spell_undo(word)


def ex_substitute(view, edit, line_range: RangeNode,
                  pattern: str = None, replacement: str = '', flags: list = None,
                  count: int = 1, **kwargs) -> None:
    if flags is None:
        flags = []

    # When no pattern is given then the the last search pattern and last
    # replacement is used. Note that the last used flags are not used.
    if not pattern:
        pattern = get_ex_substitute_last_pattern()
        replacement = get_ex_substitute_last_replacement()

    if not pattern:
        return status_message('E33: No previous substitute regular expression')

    if replacement is None:
        return status_message('No substitute replacement string')

    set_ex_substitute_last_pattern(pattern)
    set_ex_substitute_last_replacement(replacement)

    computed_flags = 0

    computed_flags |= re.MULTILINE

    if (get_option(view, 'ignorecase') or 'i' in flags) and 'I' not in flags:
        if not is_smartcase_pattern(view, pattern):
            computed_flags |= re.IGNORECASE

    try:
        compiled_pattern = re.compile(pattern, flags=computed_flags)
    except Exception as e:
        return status_message('[regex error]: {} ... in pattern {}'.format(str(e), pattern))

    target_region = line_range.resolve(view)
    if target_region.empty():
        return status_message('E486: Pattern not found: {}'.format(pattern))

    replace_count = 0 if (flags and 'g' in flags) else 1

    if 'c' in flags:

        def _replace_confirming(view, edit, pattern: str, compiled_pattern,
                                replacement: str, replace_count: int, target_region: Region) -> None:

            last_row = row_at(view, target_region.b - 1)
            start = target_region.begin()

            while True:
                if start >= view.size():
                    break

                match = view.find(pattern, start)

                # no match or match out of range -- stop
                if (match == Region(-1)) or (row_at(view, match.a) > last_row):
                    view.show(view.sel()[0].begin())
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
    set_selection(view, line.begin())

    view.replace(edit, target_region, new_region_text)

    # TODO Refactor set position cursor after operation into reusable api.
    # Put cursor on first non-whitespace char of current line.
    line = view.line(view.sel()[0].b)
    if line.size() > 0:
        set_selection(view, view.find('^\\s*', line.begin()).end())

    enter_normal_mode(view)


def ex_sunmap(lhs: str, **kwargs) -> None:
    try:
        mappings_remove(SELECT, lhs)
    except KeyError:
        status_message('E31: No such mapping')


def ex_tabclose(window, **kwargs) -> None:
    window_tab_control(window, action='close')


def ex_tabfirst(window, **kwargs) -> None:
    window_tab_control(window, action='first')


def ex_tablast(window, **kwargs) -> None:
    window_tab_control(window, action='last')


def ex_tabnext(window, **kwargs) -> None:
    window_tab_control(window, action='next')


def ex_tabonly(window, **kwargs) -> None:
    window_tab_control(window, action='only')


def ex_tabprevious(window, **kwargs) -> None:
    window_tab_control(window, action='previous')


def ex_unmap(lhs: str, **kwargs) -> None:
    for mode in (NORMAL, OPERATOR_PENDING, VISUAL, VISUAL_LINE, VISUAL_BLOCK):
        try:
            mappings_remove(mode, lhs)
        except KeyError:
            status_message('E31: No such mapping')


# TODO [review] Either remove or refactor into window module. Preferably remove, because there should be standard commands that can achieve the same thing.  # noqa: E501
# Non-standard Vim :unvsplit command
def ex_unvsplit(window, **kwargs) -> None:
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


def ex_vnoremap(lhs: str = None, rhs: str = None, **kwargs) -> None:
    if not (lhs and rhs):
        return status_message('Listing key mappings is not implemented')

    mappings_add(VISUAL, lhs, rhs)
    mappings_add(VISUAL_BLOCK, lhs, rhs)
    mappings_add(VISUAL_LINE, lhs, rhs)


# TODO Refactor like ExSplit
def ex_vsplit(window, view, file: str = None, **kwargs) -> None:
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

    def open_file(window, file: str) -> None:
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


def ex_vunmap(lhs: str, **kwargs) -> None:
    for mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
        try:
            mappings_remove(mode, lhs)
        except KeyError:
            status_message('E31: No such mapping')


def ex_wall(window, **kwargs) -> None:
    # a specific view is passed instead
    del kwargs['view']
    for view in window.views():
        ex_write(window=window, view=view, **kwargs)


@_init_cwd
def ex_wq(**kwargs) -> None:
    ex_write(**kwargs)
    ex_quit(**kwargs)


def ex_wqall(**kwargs) -> None:
    ex_wall(**kwargs)
    ex_qall(**kwargs)


@_init_cwd
def ex_write(window, view, file_name: str = None, line_range: RangeNode = None, forceit: bool = False, **kwargs) -> None:  # noqa: E501
    if kwargs.get('++') or kwargs.get('cmd'):
        status_message('argument not implemented')
        return

    if kwargs.get('>>'):
        if file_name:
            _do_write_append_file(view, file_name, forceit, line_range)
        else:
            _do_write_append(window, view, line_range)
    else:
        if file_name:
            _do_write_file(window, view, file_name, forceit, line_range)
        else:
            _do_write(view)


def _do_write(view) -> None:
    if not view.is_dirty():
        return

    if not view.file_name():
        ui_bell("E32: No file name")
        return

    if is_view_read_only(view):
        ui_bell("E45: 'readonly' option is set (add ! to override)")
        return

    save(view)


def _do_write_file(window, view, file_name: str, forceit: bool, line_range: RangeNode = None) -> None:
    if not forceit:
        if os.path.exists(file_name):
            ui_bell("E13: File exists (add ! to override)")
            return

        if is_file_read_only(file_name):
            ui_bell("E45: 'readonly' option is set (add ! to override)")
            return

    try:
        file_path = os.path.abspath(os.path.expandvars(os.path.expanduser(file_name)))
        with open(file_path, 'wt') as f:
            f.write(_get_write_buffer(view, line_range))

        view.retarget(file_path)
        save(window)
    except IOError:
        ui_bell("E212: Can't open file for writing: {}".format(file_name))


def _get_write_buffer(view, line_range: RangeNode = None) -> str:
    if line_range is None or line_range.is_empty:
        region = view_to_region(view)
    else:
        region = line_range.resolve(view)

    return view.substr(region)


def _do_write_append_file(view, file_name: str, forceit: bool, line_range: RangeNode = None) -> None:
    if not forceit and not os.path.exists(file_name):
        status_message("E212: Can't open file for writing: %s", file_name)
        return

    try:
        with open(file_name, 'at') as f:
            f.write(_get_write_buffer(view, line_range))

        status_message('Appended to %s' % os.path.abspath(file_name))
    except IOError as e:
        status_message('could not write file %s', str(e))


def _do_write_append(window, view, line_range: RangeNode = None) -> None:
    view.run_command('append', {'characters': _get_write_buffer(view, line_range)})
    save(view)
    enter_normal_mode(window, get_mode(view))


def ex_yank(view, register: str, line_range: RangeNode, **kwargs) -> None:
    if not register:
        register = '"'

    try:
        resolved = line_range.resolve(view)
    except ValueError as e:
        ui_bell(str(e))
        return

    text = view.substr(resolved)
    registers_set(view, register, [text])

    if register == '"':
        registers_set(view, '0', [text])


# Default ex command. See :h [range].
def _default_ex_cmd(window, view, line_range: RangeNode, **kwargs) -> None:
    _log.debug('default ex cmd %s %s', line_range, kwargs)
    line = row_at(view, line_range.resolve(view).a) + 1
    enter_normal_mode(window, get_mode(view))
    goto_line(view, get_mode(view), line)


def _get_ex_cmd(name: str):
    ex_cmd = getattr(sys.modules[__name__], 'ex_' + name, None)

    if not ex_cmd:
        raise RuntimeError("unknown ex cmd '{}'".format(name))

    # TODO Do we really need this check?
    if not inspect.isfunction(ex_cmd):
        raise RuntimeError("unknown ex cmd type '{}'".format(name))

    return ex_cmd


# This function is used by the command **nv_ex_cmd_edit_wrap**. The
# **nv_ex_cmd_edit_wrap** command is required to wrap ex commands that need a
# Sublime Text edit token. Edit tokens can only be obtained from a TextCommand.
# Some ex commands don't need an edit token, those commands don't need to be
# wrapped by a text command.
#
# Arguments belonging to this function are underscored to avoid collisions with
# the ex command args in kwargs.
def do_ex_cmd_edit_wrap(self, edit, _name: str = None, _line: str = None, **kwargs) -> None:
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


def do_ex_command(window, name: str, args=None) -> None:
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

        return window.run_command('nv_ex_cmd_edit_wrap', args)

    view = window.active_view()
    if view:
        args['view'] = view

    _log.debug('execute ex command: %s %s', name, args)

    # TODO [review] This function is wrapped by a Sublime Text command (see
    # above), which means objects like the RangeNode() can't be passed through.
    # For the moment it just defaults to an empty RangeNode.

    # TODO [review] Ex commands could probably make the line_range optional.

    ex_cmd(window=window, line_range=RangeNode(), **args)


def _parse_user_cmdline(line: str):
    commands = []
    for line in _split_cmdline_lines(line):
        command = _parse_user_cmdline_split(line)
        if command:
            commands.append(command)

    return commands


def _split_cmdline_lines(line: str) -> list:
    return re.split('\\<bar\\>', line, flags=re.IGNORECASE)


def _parse_user_cmdline_split(line: str):
    re_cmd = '[A-Z][a-zA-Z_]*'
    re_arg_name = '[a-zA-Z_][a-zA-Z0-9_]*'
    re_arg_value = '[a-zA-Z0-9\\:\\.,\n\t#@_-]+'

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


def do_ex_cmdline(window, line: str) -> None:
    # Execute ex command as a string (what a user would enter at the cmdline).
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
        user_commands = _parse_user_cmdline(line)
        if not user_commands:
            return status_message('invalid command')

        _log.debug('execute user ex command: %s', user_commands)

        for command in user_commands:
            window.run_command(command['cmd'], command['args'])

        return

    try:
        cmdline = parse_command_line(line[1:])
    except Exception as e:
        ui_bell(str(e))
        return

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
        return window.run_command('nv_ex_cmd_edit_wrap', {'_line': line})

    args = cmdline.command.params

    view = window.active_view()
    if view:
        args['view'] = view

    _log.debug('execute ex command: %s %s', cmdline.command.target, args)

    ex_cmd(window=window, line_range=cmdline.line_range, forceit=cmdline.command.forced, **args)


# TODO [refactor] Into do_ex_cmdline() with a param to indicate user cmdline? e.g do_ex_cmdline(window, line, interactive=True).  # noqa: E501
def do_ex_user_cmdline(window, line: str) -> None:
    # Execute an interactive ex command (what a user would use in a mapping).
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

    if line.lower().endswith('<cr>'):
        # Strips carriage return
        for line in _split_cmdline_lines(line[:-4]):
            do_ex_cmdline(window, line)
    else:
        if ':' == line:
            return window.run_command('nv_cmdline')
        elif line[0] != ':':
            raise RuntimeError('user cmdline must begin with a colon')

        return window.run_command('nv_cmdline', args={'initial_text': line})
