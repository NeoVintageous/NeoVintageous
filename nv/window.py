# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from sublime import ENCODED_POSITION

from NeoVintageous.nv.polyfill import close_pane_if_empty
from NeoVintageous.nv.polyfill import goto_definition_side_by_side
from NeoVintageous.nv.polyfill import has_dirty_buffers
from NeoVintageous.nv.polyfill import make_all_groups_same_size
from NeoVintageous.nv.polyfill import set_selection
from NeoVintageous.nv.registers import get_alternate_file_register
from NeoVintageous.nv.settings import get_cmdline_cwd
from NeoVintageous.nv.settings import get_exit_when_quitting_last_window
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.utils import clone_file
from NeoVintageous.nv.utils import create_pane
from NeoVintageous.nv.vim import status_message


_LAYOUT_SINGLE_CELL = {
    'cells': [[0, 0, 1, 1]],
    'cols': [0.0, 1.0],
    'rows': [0.0, 1.0]
}

_LAYOUT_TWO_COLUMN = {
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1]],
    'rows': [0.0, 1.0],
    'cols': [0.0, 0.5, 1.0]
}

_LAYOUT_THREE_COLUMN = {
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]],
    'rows': [0.0, 1.0],
    'cols': [0.0, 0.33, 0.66, 1.0]
}

_LAYOUT_TWO_ROW = {
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2]],
    'rows': [0.0, 0.5, 1.0],
    'cols': [0.0, 1.0]
}

_LAYOUT_THREE_ROW = {
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2], [0, 2, 1, 3]],
    'rows': [0.0, 0.33, 0.66, 1.0],
    'cols': [0.0, 1.0]
}


def _layout_group_height(layout, group: int, height: int = None) -> dict:
    """Set current group highest (default: highest possible)."""
    row_count = len(layout['rows'])
    if row_count < 3:
        # The layout only has one column so there is no work to do because the
        # height is already as high as possible.
        return layout

    cell = layout['cells'][group]

    y1 = cell[1]
    y2 = cell[3]

    if y1 == 0 and y2 == (row_count - 1):
        # The group cell is already as high as possible.
        return layout

    # The minimal width that other windows will be resize to (accounts for some
    # tab size which is why it is greater than the min_width equivalent in the
    # _layout_group_width function). TODO In Vim I think the setting
    # 'winminheight' is used as the min width. The default in Vim for that
    # setting is 1.
    min_height = 0.057

    rows = []
    rows.append(0.0)
    for i in range(1, row_count - 1):
        if y1 >= i:
            rows.append(0.0 + (min_height * i))
        else:
            rows.append(1.0 - (min_height * (row_count - i - 1)))
    rows.append(1.0)

    layout['rows'] = rows

    return layout


def _layout_group_width(layout, group: int, width: int = None) -> dict:
    """Set current group width (default: widest possible)."""
    col_count = len(layout['cols'])

    # The layout only has one row so there is no work to do because the width is
    # already as wide as possible.
    if col_count < 3:
        return layout

    cell = layout['cells'][group]

    x1 = cell[0]
    x2 = cell[2]

    # The group cell is already as wide as possible.
    if x1 == 0 and x2 == (col_count - 1):
        return layout

    # The minimal width that other windows will be resize to. TODO In Vim I
    # think the setting 'winminwidth' is used as the min width. The default in
    # Vim for that setting is 20.
    min_width = 0.02

    cols = []
    cols.append(0.0)
    for i in range(1, col_count - 1):
        if x1 >= i:
            cols.append(0.0 + (min_width * i))
        else:
            cols.append(1.0 - (min_width * (col_count - i - 1)))
    cols.append(1.0)

    layout['cols'] = cols

    return layout


def _close_all_other_views(window) -> None:
    """Make the active view the only one on the screen.

    All other views are closed, unless they are modified.

    Modified views are merged into active group. Modified views
    are not removed, so changes cannot get lost.
    """
    active_view = window.active_view()
    if not active_view:
        return

    views = window.views()
    if len(views) > 1:
        # NOTE The non-active *unmodified* views are closed first and then the
        # groups. This effectivly collapses unmodified views into the same group as
        # the active view. Looping over the groups and closing views won't work.

        # Close all other unmodified views.
        for view in views:
            if view != active_view and not view.is_dirty():
                view.close()

    # Close inactive panes.
    active_group = window.active_group()
    for group in range(window.num_groups()):
        if group != active_group:
            # The "close_pane" command will not close views, instead it moves
            # views into the first or next pane. If the pane is the last
            # remaining pane and it has views, the pane is not closed.
            window.run_command('close_pane', {'group': group})


def _close_view(window, forceit: bool = False, close_if_last: bool = True, **kwargs) -> None:
    """Close view.

    Close pane if empty.

    If {forceit} is True the view is closed and the buffer contents are lost.

    If {close_if_last} is False and it is the only view left, it is not closed.
    """
    if close_pane_if_empty(window):
        return

    if not close_if_last and len(window.views()) < 2:
        return

    view = window.active_view()
    if not view:
        return

    if forceit:
        view.set_scratch(True)

    if view.is_dirty():
        buffer_name = view.file_name()
        if buffer_name is None:
            buffer_name = '[No Name]'

        status_message('No write since last change for buffer "%s"' % buffer_name)
        return

    view.close()

    if close_pane_if_empty(window):
        return


def _close_active_view(window, close_if_last=False) -> None:
    _close_view(window, close_if_last=close_if_last)


def window_quit_view(window, **kwargs) -> None:
    # Need to get the setting before quitting the the view because if closing the
    # last view there may not be a view to get the setting from.
    exit_when_quitting_last_window = get_exit_when_quitting_last_window(window.active_view())

    _close_view(window, **kwargs)

    if len(window.views()) == 0 and exit_when_quitting_last_window:
        window.run_command('close')


def window_quit_views(window, forceit: bool = False, **kwargs) -> None:
    if forceit:
        for view in window.views():
            if view.is_dirty():
                view.set_scratch(True)
    elif has_dirty_buffers(window):
        status_message("E37: No write since last change")
        return

    window.run_command('close_all')
    window.run_command('exit')


def _exchange_views(window, view_a, view_b) -> None:
    if not view_a or not view_b:
        return

    view_a_index = window.get_view_index(view_a)
    view_b_index = window.get_view_index(view_b)

    window.set_view_index(view_a, view_b_index[0], view_b_index[1])
    window.set_view_index(view_b, view_a_index[0], view_a_index[1])


def _exchange_view(window, other_view) -> None:
    _exchange_views(window, window.active_view(), other_view)


def _exchange_view_by_count(window, count: int = 1) -> None:
    """Exchange view with previous one.

    Without {count}: Exchange current view with the view in the
    next group.  If there is no next group, exchange with the view
    in the previous group.
    With {count}: Exchange current view with the view in Nth group
    (first group is 1).  The cursor is put in the other view.
    When vertical and horizontal group splits are mixed, the
    exchange is done in the row or column of groups that the
    current view is in.
    """
    if window.num_groups() < 2:
        return

    active_group_num = window.active_group()
    if (active_group_num + 1) < window.num_groups():
        other_group_num = active_group_num + 1
    else:
        other_group_num = active_group_num - 1

    other_view = window.active_view_in_group(other_group_num)

    _exchange_view(window, other_view)


def _move_active_view_to_far_left(window) -> None:
    """Move the current view to be at the far left.

    Using the full height of the view.

    Example of moving window (a=active).

    Currently only supports 2 row or 2 column layouts.
     ____________                    _________________
    |   0   |__1_|                  |    |   1   |  2 |
    |_______|__2a|                  |    |_______|__ _|
    |  3 | 4|  5 | move far left    | 0a |  3 | 4|  5 |
    |____|__|____|                  |    |____|__|____|
    |______6_____|                  |____|______6_____|

    """
    if window.num_groups() != 2:
        return

    if window.active_group() != 0:
        _exchange_view(window, window.active_view_in_group(0))
        window.focus_group(0)

    window.set_layout(_LAYOUT_TWO_COLUMN)
    make_all_groups_same_size(window)


def _move_active_view_to_far_right(window) -> None:
    """Move the current view to be at the far right, using the full height of the view."""
    if window.num_groups() != 2:
        return

    if window.active_group() != 1:
        _exchange_view(window, window.active_view_in_group(1))
        window.focus_group(1)

    window.set_layout(_LAYOUT_TWO_COLUMN)
    make_all_groups_same_size(window)


def _move_active_view_to_very_bottom(window) -> None:
    """Move the current view to be at the very bottom, using the full width of the view."""
    if window.num_groups() != 2:
        return

    if window.active_group() != 1:
        _exchange_view(window, window.active_view_in_group(1))
        window.focus_group(1)

    window.set_layout(_LAYOUT_TWO_ROW)
    make_all_groups_same_size(window)


def _move_active_view_to_very_top(window) -> None:
    """Move the current view to be at the very top, using the full width of the view."""
    if window.num_groups() != 2:
        return

    if window.active_group() != 0:
        _exchange_view(window, window.active_view_in_group(0))
        window.focus_group(0)

    window.set_layout(_LAYOUT_TWO_ROW)
    make_all_groups_same_size(window)


def _get_group(window, direction: str, count: int):
    """Retrieve group number in given direction.

    :param direction:
        A string, one of "above", "below", "left", or "right".
    :param count:
        An integer.
    Uses the cursor position to select between alternatives.
    Returns None if there are no groups in {direction}.
    Returns the group number furthest in {direction} if
    {count} is more than the number of groups in {direction}.
    """
    layout = window.layout()

    if (direction == 'left' or direction == 'right') and len(layout['cols']) < 3:
        return None

    if (direction == 'below' or direction == 'above') and len(layout['rows']) < 3:
        return None

    current_cell = layout['cells'][window.active_group()]
    current_cell_x1 = current_cell[0]
    current_cell_y1 = current_cell[1]
    current_cell_x2 = current_cell[2]
    current_cell_y2 = current_cell[3]

    cell_group_candidates = {}  # type: dict
    for group_num, cell in enumerate(layout['cells']):
        cell_x1 = cell[0]
        cell_y1 = cell[1]
        cell_x2 = cell[2]
        cell_y2 = cell[3]

        if direction == 'below':
            if cell_x1 < current_cell_x2 and cell_x2 > current_cell_x1 and cell_y1 >= current_cell_y2:
                if cell_y1 not in cell_group_candidates:
                    cell_group_candidates[cell_y1] = []
                cell_group_candidates[cell_y1].append(group_num)
        elif direction == 'above':
            if cell_x1 < current_cell_x2 and cell_x2 > current_cell_x1 and cell_y2 <= current_cell_y1:
                if cell_y2 not in cell_group_candidates:
                    cell_group_candidates[cell_y2] = []
                cell_group_candidates[cell_y2].append(group_num)
        elif direction == 'right':
            if cell_y1 < current_cell_y2 and cell_y2 > current_cell_y1 and cell_x1 >= current_cell_x2:
                if cell_x1 not in cell_group_candidates:
                    cell_group_candidates[cell_x1] = []
                cell_group_candidates[cell_x1].append(group_num)
        elif direction == 'left':
            if cell_y1 < current_cell_y2 and cell_y2 > current_cell_y1 and cell_x2 <= current_cell_x1:
                if cell_x1 not in cell_group_candidates:
                    cell_group_candidates[cell_x1] = []
                cell_group_candidates[cell_x1].append(group_num)

    if len(cell_group_candidates) == 0:
        return None

    cell_group_candidate_indexes = list(cell_group_candidates)

    if direction == 'above' or direction == 'left':
        cell_group_candidate_indexes.reverse()
    else:
        cell_group_candidate_indexes.sort()

    direction_count = count - 1

    if direction_count >= len(cell_group_candidate_indexes):
        group_nums = cell_group_candidates[cell_group_candidate_indexes.pop()]
    else:
        group_nums = cell_group_candidates[cell_group_candidate_indexes[direction_count]]

    group_num = group_nums[0]

    return group_num


def _focus_group(window, direction: str, count: int = 1) -> None:
    nth_group_number = _get_group(window, direction, count)
    if nth_group_number is None:
        return

    # If the cursor is not visible in the view we are moving to, then move the
    # cursor to the top of the visible area of the view (instead of scrolling
    # the view to show the cursor). This prevents the view we are moving to
    # suddenly scrolling, which can be unexpected and is arguably bad UX. The
    # functionaility now works closer to how Vim works. The main difference in
    # Vim is that the cursor never leaves the  visible areas in the first place,
    # it just doesn't happen e.g. when you scroll with the mouse in Vim, Vim
    # moves the cursor along with the scrolling visible area so the cursor is
    # always visible, it never disappears from the visible areas.

    view = window.active_view_in_group(nth_group_number)
    if view:
        visible_region = view.visible_region()
        if not view.visible_region().contains(view.sel()[0]):
            set_selection(view, visible_region.begin())

    window.focus_group(nth_group_number)


def _focus_group_above(window, count: int = 1) -> None:
    """Move cursor to Nth group above current one."""
    _focus_group(window, 'above', count)


def _focus_group_below(window, count: int = 1) -> None:
    """Move cursor to Nth group below current one."""
    _focus_group(window, 'below', count)


def _focus_group_left(window, count: int = 1) -> None:
    """Move cursor to Nth group left of current one."""
    _focus_group(window, 'left', count)


def _focus_group_right(window, count: int = 1) -> None:
    """Move cursor to Nth group right of current one."""
    _focus_group(window, 'right', count)


def _focus_group_top_left(window) -> None:
    window.focus_group(0)


def _focus_group_bottom_right(window) -> None:
    window.focus_group(window.num_groups() - 1)


def _set_group_height(window, height: int = None) -> None:
    """Set current group height (default: highest possible)."""
    return window.set_layout(
        _layout_group_height(window.layout(), window.active_group(), height)
    )


def _set_group_width(window, width: int = None) -> None:
    """Set current group width (default: widest possible)."""
    return window.set_layout(
        _layout_group_width(window.layout(), window.active_group(), width)
    )


def _decrease_group_height(window, count: int = 1) -> None:
    pass


def _decrease_group_width(window, count: int = 1) -> None:
    pass


def _increase_group_height(window, count: int = 1) -> None:
    pass


def _increase_group_width(window, count: int = 1) -> None:
    pass


def _split(window, file: str = None) -> None:
    if file:
        create_pane(window, 'down', file)
    else:
        clone_file(window, 'down')


def _vsplit(window, file: str = None) -> None:
    if file:
        create_pane(window, 'right', file)
    else:
        clone_file(window, 'right')


def _new(window, file: str = None) -> None:
    create_pane(window, 'down', file)


def vnew(window, file: str = None) -> None:
    create_pane(window, 'right', file)


def _split_alternate(window):
    alternate_file = get_alternate_file_register()
    if not alternate_file:
        ui_bell('E23: No alternate file')
        return

    create_pane(window, 'down', alternate_file)


def open_alternate_file(window) -> None:
    alternate_file = get_alternate_file_register()
    if not alternate_file:
        ui_bell('E23: No alternate file')
        return

    window.open_file(alternate_file)


def window_buffer_control(window, action: str, count: int = 1) -> None:
    if action in ('next', 'previous'):
        views = window.views()
        active_view = window.active_view()
        active_index = views.index(active_view)
        view_count = len(views)

        if action == 'next':
            index = (active_index + count) % view_count
        else:
            index = (active_index + view_count - count) % view_count

        window.focus_view(views[index])

    elif action == 'first':
        window.focus_group(0)
        window.run_command('select_by_index', {'index': 0})

    elif action == 'goto':
        goto_id = int(count)
        for view in window.views():
            if view.id() == goto_id:
                window.focus_view(view)

    elif action == 'last':
        window.focus_group(window.num_groups() - 1)
        index = len(window.views_in_group(window.num_groups() - 1)) - 1
        window.run_command('select_by_index', {'index': index})

    else:
        raise ValueError('unknown buffer control action: %s' % action)


def window_tab_control(window, action: str, count: int = 1, index: int = None) -> None:
    view = window.active_view()
    if not view:
        return status_message('view not found')

    view_count = len(window.views_in_group(window.active_group()))
    group_index, view_index = window.get_view_index(view)

    if action == 'next':
        window.run_command('select_by_index', {'index': (view_index + count) % view_count})

    elif action == 'previous':
        window.run_command('select_by_index', {'index': (view_index + view_count - count) % view_count})

    elif action == 'last':
        window.run_command('select_by_index', {'index': view_count - 1})

    elif action == 'first':
        window.run_command('select_by_index', {'index': 0})

    elif action == 'goto':
        if index:
            window.run_command('select_by_index', {'index': index - 1})

    elif action == 'only':
        group_views = window.views_in_group(group_index)
        if any(view.is_dirty() for view in group_views):
            return status_message('E445: Other window contains changes')

        for group_view in group_views:
            if group_view.id() == view.id():
                continue

            window.focus_view(group_view)
            window_quit_view(window)

        window.focus_view(view)

    elif action == 'new':
        window.run_command('new_file')

    elif action == 'close':
        window.run_command('close_by_index', {'group': group_index, 'index': view_index})

    else:
        raise ValueError('unknown tab control action: %s' % action)


def window_control(window, action: str, mode=None, count: int = 1, register=None, **kwargs) -> None:
    if action == 'b':
        _focus_group_bottom_right(window)
    elif action == 'H':
        _move_active_view_to_far_left(window)
    elif action == 'J':
        _move_active_view_to_very_bottom(window)
    elif action == 'K':
        _move_active_view_to_very_top(window)
    elif action == 'L':
        _move_active_view_to_far_right(window)
    elif action == 'W':
        _focus_neighbouring_group(window, count, forward=False)
    elif action == 'c':
        _close_active_view(window, **kwargs)
    elif action == '=':
        make_all_groups_same_size(window)
    elif action == '>':
        _increase_group_width(window, count)
    elif action == 'h':
        _focus_group_left(window, count)
    elif action == 'j':
        _focus_group_below(window, count)
    elif action == 'k':
        _focus_group_above(window, count)
    elif action == 'l':
        _focus_group_right(window, count)
    elif action == '<':
        _decrease_group_width(window, count)
    elif action == '-':
        _decrease_group_height(window, count)
    elif action == 'n':
        _new(window, **kwargs)
    elif action == 'o':
        _close_all_other_views(window)
    elif action == '|':
        _set_group_width(window, count)
    elif action == '+':
        _increase_group_height(window, count)
    elif action == 'q':
        window_quit_view(window)
    elif action == 's':
        _split(window, **kwargs)
    elif action == 't':
        _focus_group_top_left(window)
    elif action == '_':
        _set_group_height(window, count)
    elif action == 'v':
        _vsplit(window, **kwargs)
    elif action == 'w':
        _focus_neighbouring_group(window, count)
    elif action == 'x':
        _exchange_view_by_count(window, count)
    elif action == ']':
        goto_definition_side_by_side(window)
    elif action == '^':
        _split_alternate(window)
    else:
        raise ValueError('unknown action')


def _focus_neighbouring_group(window, count: int, forward: bool = True) -> None:
    if count > 0:
        window.focus_group(min(count, window.num_groups()) - 1)
    else:
        window.run_command('focus_neighboring_group', {'forward': forward})


def window_open_file(window, file: str, row: int = None, col: int = None) -> bool:
    if not file:
        return False

    if not os.path.isabs(file):
        cwd = get_cmdline_cwd()

        if os.path.isdir(cwd):
            file = os.path.join(cwd, file)

    if not os.path.isfile(file):
        return False

    flags = 0
    if row:
        flags = ENCODED_POSITION
        file += ':' + str(row)
        file += ':' + str(col) if col else ''

    window.open_file(file, flags)

    return True
