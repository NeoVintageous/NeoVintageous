from sublime import Region

from NeoVintageous.lib import nvim


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


def _set_layout_group_height(layout, group, height=None):
    # Set current group highest (default: highest possible).
    #
    # TODO implement set to {height}, currently sets to default highest possible
    #
    # Args:
    #   :layout (dict):
    #   :group (int):
    #   :height (int, optional): Defaults to highest possible.
    #
    # Returns:
    #   dict

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
    # _set_layout_group_width function).
    # TODO In Vim I think the setting 'winminheight' is used as the min width.
    # The default in Vim for that setting is 1.
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


def _set_layout_group_width(layout, group, width=None):
    # Set current group width (default: widest possible).
    #
    # TODO implement set to {width}, currently sets to default widest possible
    #
    # Args:
    #   :layout (dict):
    #   :group (int):
    #   :width (int, optional): Defaults to widest possible.
    #
    # Returns:
    #   dict

    col_count = len(layout['cols'])
    if col_count < 3:
        # The layout only has one row so there is no work to do because the
        # width is already as wide as possible.
        return layout

    cell = layout['cells'][group]

    x1 = cell[0]
    x2 = cell[2]

    if x1 == 0 and x2 == (col_count - 1):
        # The group cell is already as wide as possible.
        return layout

    # The minimal width that other windows will be resize to.
    # TODO In Vim I think the setting 'winminwidth' is used as the min width.
    # The default in Vim for that setting is 20.
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


# TODO could implement settings similar to vim
# window resizing e.g. 'winheight', 'winwidth',
# 'winfixheight', and 'winfixwidth'
def _set_layout_groups_size_equal(layout):
    # Make all groups (almost) equally high and wide.
    #
    # Uses 'winheight' and 'winwidth' for the current window.  Windows with
    # 'winfixheight' set keep their height and windows with 'winfixwidth' set
    # keep their width.
    cell_count = len(layout['cells'])
    col_count = len(layout['cols'])
    row_count = len(layout['rows'])

    if col_count == 2 and row_count == 2:
        return layout

    if cell_count == 4 and col_count == 3 and row_count == 3:
        # Special case for Grid with 4 cells. Works around
        # some complicated layout issues.
        return {
            'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [0, 1, 1, 2], [1, 1, 2, 2]],
            'cols': [0.0, 0.5, 1.0],
            'rows': [0.0, 0.5, 1.0]
        }

    def equalise(count):
        size = round(1.0 / (count - 1), 2)
        vals = [0.0]
        for i in range(1, count - 1):
            vals.append(round(size * i, 2))
        vals.append(1.0)
        return vals

    if col_count > 2:
        layout['cols'] = equalise(col_count)

    if row_count > 2:
        layout['rows'] = equalise(row_count)

    return layout


# TODO Refactor into descrete functional api instead of a class
class WindowAPI():

    def __init__(self, window):
        self.window = window

    # TODO could implement settings similar to vim "hidden" and "autowrite"
    def close_all_other_views(self):
        """
        Make the current view the only one on the screen.

        All other views are closed.

        Modified views are merged into current group. Modified views
        are not removed, so changes cannot get lost.
        """
        current_group_num = self.window.active_group()
        current_view = self.window.active_view()

        if not current_view:
            return

        views = self.window.views()

        if len(views) == 1:
            return

        # Note: the views are closed and then the groups. Looping
        # over the groups and closing the views in that group and
        # then closing the group won't work.

        # close other unmodified views
        for view in views:
            if view != current_view and not view.is_dirty():
                view.close()

        # close other groups
        for i in range(self.window.num_groups()):
            if i != current_group_num:
                # TODO is this the best way to close a group
                self.window.run_command('close_pane', {'group': i})

    def quit_current_view(self, exit_sublime_if_last=False):
        self._close_current_view(do_not_close_if_last=False)
        if exit_sublime_if_last:
            if len(self.window.views()) == 0:
                self.window.run_command('close')

    def close_current_view(self, do_not_close_if_last=True):
        self._close_current_view(do_not_close_if_last)

    def _close_current_view(self, do_not_close_if_last):
        """
        Close current view.

        If {do_not_close_if_last} then this command fails when there is only one
        view on screen. Modified views are not removed, so changes cannot get
        lost.

        If it's not a file on disk and contains only whitespace then it is
        closed.
        """
        views_in_group = self.window.views_in_group(self.window.active_group())
        if len(views_in_group) == 0:
            self.window.run_command('destroy_pane', {'direction': 'self'})
            return

        current_view = self.window.active_view()
        if not current_view:
            return

        # If it's not a file on disk and contains only whitespace then close it
        if not current_view.file_name() and current_view.substr(Region(0, current_view.size())).strip() == '':
            current_view.set_scratch(True)
            current_view.close()
            views_in_group = self.window.views_in_group(self.window.active_group())
            if len(views_in_group) == 0:
                self.window.run_command('destroy_pane', {'direction': 'self'})
            return

        if do_not_close_if_last and len(self.window.views()) < 2:
            nvim.status_message('cannot close last view')
            return

        if current_view.is_dirty():
            dirty_buffer_message = 'No write since last change'
            if current_view.file_name() is not None:
                dirty_buffer_message += ' for buffer "%s"' % current_view.file_name()

            nvim.status_message(dirty_buffer_message)
            return

        current_view.close()

        views_in_group = self.window.views_in_group(self.window.active_group())
        if len(views_in_group) == 0:
            self.window.run_command('destroy_pane', {'direction': 'self'})
            return

    # TODO implement count
    # TODO implement exchange when vertical and horizontal group splits
    def exchange_current_view_with_view_in_next_or_previous_group(self, count=1):
        """
        Exchange view with previous one.

        Without {count}: Exchange current view with the view in the
        next group.  If there is no next group, exchange with the view
        in the previous group.
        With {count}: Exchange current view with the view in Nth group
        (first group is 1).  The cursor is put in the other view.
        When vertical and horizontal group splits are mixed, the
        exchange is done in the row or column of groups that the
        current view is in.
        """
        if self.window.num_groups() < 2:
            return

        active_group_num = self.window.active_group()
        if (active_group_num + 1) < self.window.num_groups():
            other_group_num = active_group_num + 1
        else:
            other_group_num = active_group_num - 1

        other_view = self.window.active_view_in_group(other_group_num)

        self._exchange_current_view(other_view)

    def _exchange_view(self, view_a, view_b):

        if not view_a:
            return

        if not view_b:
            return

        view_a_index = self.window.get_view_index(view_a)
        view_b_index = self.window.get_view_index(view_b)

        self.window.set_view_index(view_a, view_b_index[0], view_b_index[1])
        self.window.set_view_index(view_b, view_a_index[0], view_a_index[1])

    def _exchange_current_view(self, other_view):
        self._exchange_view(self.window.active_view(), other_view)

    def move_current_view_to_far_left(self):
        """
        Move the current view to be at the far left, using the full height of the view.

        Example of moving window (a=active)
         ____________                    _________________
        |   0   |__1_|                  |    |   1   |  2 |
        |_______|__2a|                  |    |_______|__ _|
        |  3 | 4|  5 | move far left    | 0a |  3 | 4|  5 |
        |____|__|____|                  |    |____|__|____|
        |______6_____|                  |____|______6_____|

        Currently only supports 2 row or 2 column layouts.

        """
        if self.window.num_groups() > 2:
            # TODO not implemented yet
            return

        if self.window.num_groups() < 2:
            # no work to do
            return

        if self.window.active_group() != 0:
            # view index needs updating
            self._exchange_current_view(self.window.active_view_in_group(0))
            self.window.focus_group(0)

        self.window.set_layout(_LAYOUT_TWO_COLUMN)
        self.resize_groups_almost_equally()

    def move_current_view_to_far_right(self):
        """
        Move the current view to be at the far right, using the full height of the view.

        Currently only supports 2 row or 2 column layouts.
        """
        if self.window.num_groups() > 2:
            # TODO not implemented yet
            return

        if self.window.num_groups() < 2:
            # no work to do
            return

        if self.window.active_group() != 1:
            # view index needs updating
            self._exchange_current_view(self.window.active_view_in_group(1))
            self.window.focus_group(1)

        self.window.set_layout(_LAYOUT_TWO_COLUMN)
        self.resize_groups_almost_equally()

    def move_current_view_to_very_bottom(self):
        """
        Move the current view to be at the very bottom, using the full width of the view.

        Currently only supports 2 row or 2 column layouts.
        """
        if self.window.num_groups() > 2:
            # TODO not implemented yet
            return

        if self.window.num_groups() < 2:
            # no work to do
            return

        if self.window.active_group() != 1:
            # view index needs updating
            self._exchange_current_view(self.window.active_view_in_group(1))
            self.window.focus_group(1)

        self.window.set_layout(_LAYOUT_TWO_ROW)
        self.resize_groups_almost_equally()

    def move_current_view_to_very_top(self):
        """
        Move the current view to be at the very top, using the full width of the view.

        Currently only supports 2 row or 2 column layouts.
        """
        if self.window.num_groups() > 2:
            # TODO not implemented yet
            return

        if self.window.num_groups() < 2:
            # no work to do
            return

        if self.window.active_group() != 0:
            # view index needs updating
            self._exchange_current_view(self.window.active_view_in_group(0))
            self.window.focus_group(0)

        self.window.set_layout(_LAYOUT_TWO_ROW)
        self.resize_groups_almost_equally()

    def move_group_focus_to_nth_above_current_one(self, n=1):
        """
        Move cursor to Nth group above current one.

        Uses the cursor position to select between alternatives.
        """
        self._move_group_focus_to_nth_in_direction_of_current_one('above', n)

    def move_group_focus_to_nth_below_current_one(self, n=1):
        """
        Move cursor to Nth group below current one.

        Uses the cursor position to select between alternatives.
        """
        self._move_group_focus_to_nth_in_direction_of_current_one('below', n)

    def move_group_focus_to_nth_left_of_current_one(self, n=1):
        """
        Move cursor to Nth group left of current one.

        Uses the cursor position to select between alternatives.
        """
        self._move_group_focus_to_nth_in_direction_of_current_one('left', n)

    def move_group_focus_to_nth_right_of_current_one(self, n=1):
        """
        Move cursor to Nth group right of current one.

        Uses the cursor position to select between alternatives.
        """
        self._move_group_focus_to_nth_in_direction_of_current_one('right', n)

    def move_group_focus_to_bottom_right(self):
        self.window.focus_group(self.window.num_groups() - 1)

    def move_group_focus_to_top_left(self):
        self.window.focus_group(0)

    def _move_group_focus_to_nth_in_direction_of_current_one(self, direction, n=1):
        nth_group_number = self._get_nth_group_number_in_direction_of_current_one(direction, n)
        if nth_group_number is None:
            return
        self.window.focus_group(nth_group_number)

    # TODO implement cursor position to select between alternatives
    def _get_nth_group_number_in_direction_of_current_one(self, direction, n):
        """
        Retrieve group number in given direction.

        :param direction:
            A string, one of "above", "below", "left", or "right".
        :param n:
            An integer.
        Uses the cursor position to select between alternatives.
        Returns None if there are no groups in {direction}.
        Returns the group number furthest in {direction} if {n}
        is more than the number of groups in {direction}.
        """
        layout = self.window.layout()

        if (direction == 'left' or direction == 'right') and len(layout['cols']) < 3:
            return None

        if (direction == 'below' or direction == 'above') and len(layout['rows']) < 3:
            return None

        current_cell = layout['cells'][self.window.active_group()]
        current_cell_x1 = current_cell[0]
        current_cell_y1 = current_cell[1]
        current_cell_x2 = current_cell[2]
        current_cell_y2 = current_cell[3]

        cell_group_candidates = {}
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

        direction_count = n - 1

        if direction_count >= len(cell_group_candidate_indexes):
            group_nums = cell_group_candidates[cell_group_candidate_indexes.pop()]
        else:
            group_nums = cell_group_candidates[cell_group_candidate_indexes[direction_count]]

        group_num = group_nums[0]

        return group_num

    def set_current_group_height_to_n(self, n=None):
        # Set current group height to N (default: highest possible).
        #
        # TODO implement set to n, currently sets to default highest possible
        #
        # Args:
        #   :n (int):
        return self.window.set_layout(
            _set_layout_group_height(
                self.window.layout(),
                self.window.active_group(),
                n))

    def set_current_group_width_to_n(self, n=None):
        # Set current group width to N (default: widest possible)
        #
        # TODO implement set to n, currently sets to default widest possible
        #
        # Args:
        #   :n (int):
        return self.window.set_layout(
            _set_layout_group_width(
                self.window.layout(),
                self.window.active_group(),
                n))

    # TODO decrease_current_group_height_by_n()
    def decrease_current_group_height_by_n(self, n=1):
        pass

    # TODO decrease_current_group_width_by_n()
    def decrease_current_group_width_by_n(self, n=1):
        pass

    # TODO increase_current_group_height_by_n()
    def increase_current_group_height_by_n(self, n=1):
        pass

    # TODO increase_current_group_width_by_n()
    def increase_current_group_width_by_n(self, n=1):
        pass

    def resize_groups_almost_equally(self):
        # Make all groups (almost) equally high and wide.
        #
        # Uses 'winheight' and 'winwidth' for the current window.  Windows with
        # 'winfixheight' set keep their height and windows with 'winfixwidth'
        # set keep their width.
        #
        # TODO could implement settings similar to vim window resizing e.g.
        # 'winheight', 'winwidth', 'winfixheight', and 'winfixwidth'
        return self.window.set_layout(
            _set_layout_groups_size_equal(
                self.window.layout()))

    def split_current_view_in_two(self, n=None):
        """
        Split current view in two.

        The result is two viewports on the same file.  Make new view N high
        (default is to use half the height of the current window).  Rduces the
        current view height to create room (and others, if the 'equalalways'
        option is set, 'eadirection' isn't "hor", and one of the is higher than
        the current or the new view).
        """
        self.window.run_command('create_pane', {'direction': 'down'})
        self.window.run_command('clone_file_to_pane', {'direction': 'down'})

    def split_current_view_in_two_vertically(self, n=None):
        self.window.run_command('create_pane', {'direction': 'right'})
        self.window.run_command('clone_file_to_pane', {'direction': 'right'})

    def split_with_new_file(self, n=None):
        """
        Create a new group and start editing an empty file in it.

        Make new group N high (default is to use half the existing height).
        Reduces the current group height to create room (and others, if the
        'equalalways' option is set and 'eadirection' isn't "hor").
        """
        self.window.run_command('create_pane', {'direction': 'down', 'give_focus': True})
