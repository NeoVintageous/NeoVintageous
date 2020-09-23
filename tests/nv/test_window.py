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


from NeoVintageous.tests import unittest

from NeoVintageous.nv.window import _layout_group_height
from NeoVintageous.nv.window import _layout_group_width
from NeoVintageous.nv.window import _layout_groups_equal
from NeoVintageous.nv.window import window_control

# +-+-+
# |0|1|
# | +-+
# | |2|
# +-+-+
LAYOUT_CELLS_3_VARIANT_1 = {
    'cols': [0.0, 0.5, 1.0],
    'rows': [0.0, 0.5, 1.0],
    'cells': [[0, 0, 1, 2], [1, 0, 2, 1], [1, 1, 2, 2]]}

# +-+-+
# |0|1|
# +-+-+
# | |2|
# | +-+
# | |3|
# +-+-+
LAYOUT_CELLS_4_VARIANT_1 = {
    'cols': [0.0, 0.5, 1.0],
    'rows': [0.0, 0.33, 0.66, 1.0],
    'cells': [[0, 0, 1, 3], [1, 0, 2, 1], [1, 1, 2, 2], [1, 2, 2, 3]]}

# +-+-+
# |0|1|
# | +-+
# | |2|
# +-+ |
# |4| |
# +-+ |
# |3| |
# +-+-+
LAYOUT_CELLS_5_VARIANT_1 = {
    'cols': [0.0, 0.5, 1.0],
    'rows': [0.0, 0.25, 0.5, 0.75, 1.0],
    'cells': [[0, 0, 1, 2], [1, 0, 2, 1], [1, 1, 2, 4], [0, 3, 1, 4], [0, 2, 1, 3]]}

# +-------+
# |0      |
# +-+-+-+-+
# |1|2|3|4|
# +-+-+-+-+
LAYOUT_CELLS_5_VARIANT_2 = {
    'cols': [0.0, 0.5, 0.75, 0.875, 1.0],
    'rows': [0.0, 0.5, 1.0],
    'cells': [[0, 0, 4, 1], [0, 1, 1, 2], [1, 1, 2, 2], [2, 1, 3, 2], [3, 1, 4, 2]]}

LAYOUT_COLS_2 = {
    'cols': [0.0, 0.5, 1.0],
    'rows': [0.0, 1.0],
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]}

LAYOUT_COLS_2_LEFT_SMALL = {
    'cols': [0.0, 0.025, 1.0],
    'rows': [0.0, 1.0],
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]}

LAYOUT_COLS_2_RIGHT_SMALL = {
    'cols': [0.0, 0.7, 1.0],
    'rows': [0.0, 1.0],
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]}

LAYOUT_COLS_3 = {
    'cols': [0.0, 0.33, 0.66, 1.0],
    'rows': [0.0, 1.0],
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]]}

LAYOUT_EMPTY = {
    'cols': [],
    'rows': [],
    'cells': []}  # type: dict

LAYOUT_GRID_4 = {
    'cols': [0.0, 0.5, 1.0],
    'rows': [0.0, 0.5, 1.0],
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [0, 1, 1, 2], [1, 1, 2, 2]]}

LAYOUT_ROWS_2 = {
    'cols': [0.0, 1.0],
    'rows': [0.0, 0.5, 1.0],
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2]]}

LAYOUT_ROWS_2_ABOVE_SMALL = {
    'cols': [0.0, 1.0],
    'rows': [0.0, 0.23782383419689118, 1.0],
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2]]}

LAYOUT_ROWS_2_BELOW_SMALL = {
    'cols': [0.0, 1.0],
    'rows': [0.0, 0.83782383419689118, 1.0],
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2]]}

LAYOUT_ROWS_3 = {
    'cols': [0.0, 1.0],
    'rows': [0.0, 0.33, 0.66, 1.0],
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2], [0, 2, 1, 3]]}

LAYOUT_SINGLE = {
    'cols': [0.0, 1.0],
    'rows': [0.0, 1.0],
    'cells': [[0, 0, 1, 1]]}


class TestSetLayoutGroupSize(unittest.TestCase):

    def test_height(self):
        # Negative tests: layouts with no rows shouldn't change.
        self.assertEqual(LAYOUT_SINGLE, _layout_group_height(LAYOUT_SINGLE.copy(), group=0))
        self.assertEqual(LAYOUT_COLS_2, _layout_group_height(LAYOUT_COLS_2.copy(), group=0))
        self.assertEqual(LAYOUT_COLS_2, _layout_group_height(LAYOUT_COLS_2.copy(), group=1))
        self.assertEqual(LAYOUT_COLS_3, _layout_group_height(LAYOUT_COLS_3.copy(), group=0))
        self.assertEqual(LAYOUT_COLS_3, _layout_group_height(LAYOUT_COLS_3.copy(), group=1))
        self.assertEqual(LAYOUT_COLS_3, _layout_group_height(LAYOUT_COLS_3.copy(), group=2))

        # Rows: 2
        expected = LAYOUT_ROWS_2.copy()
        expected['rows'] = [0.0, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_2.copy(), group=0))
        expected['rows'] = [0.0, 0.057, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_2.copy(), group=1))

        # Rows: 2 (above small)
        expected = LAYOUT_ROWS_2_ABOVE_SMALL.copy()
        expected['rows'] = [0.0, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_2_ABOVE_SMALL.copy(), group=0))
        expected['rows'] = [0.0, 0.057, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_2_ABOVE_SMALL.copy(), group=1))

        # Rows: 2 (already correct layout)
        expected = LAYOUT_ROWS_2.copy()
        expected['rows'] = [0.0, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(expected.copy(), group=0))
        expected['rows'] = [0.0, 0.057, 1.0]
        self.assertEqual(expected, _layout_group_height(expected.copy(), group=1))

        # Rows: 3
        expected = LAYOUT_ROWS_3.copy()
        expected['rows'] = [0.0, 0.886, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_3.copy(), group=0))
        expected['rows'] = [0.0, 0.057, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_3.copy(), group=1))
        expected['rows'] = [0.0, 0.057, 0.114, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_ROWS_3.copy(), group=2))

        # Rows: 3 (already correct layout)
        expected = LAYOUT_ROWS_3.copy()
        expected['rows'] = [0.0, 0.886, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(expected.copy(), group=0))

        # Grid: 4
        expected = LAYOUT_GRID_4.copy()
        expected['rows'] = [0.0, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_GRID_4.copy(), group=0))
        self.assertEqual(expected, _layout_group_height(LAYOUT_GRID_4.copy(), group=1))
        expected['rows'] = [0.0, 0.057, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_GRID_4.copy(), group=2))
        self.assertEqual(expected, _layout_group_height(LAYOUT_GRID_4.copy(), group=3))

        # Cells: 3
        expected = LAYOUT_CELLS_3_VARIANT_1.copy()
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_3_VARIANT_1.copy(), group=0))
        expected['rows'] = [0.0, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_3_VARIANT_1.copy(), group=1))
        expected['rows'] = [0.0, 0.057, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_3_VARIANT_1.copy(), group=2))

        # Cells: 5 (variant 1)
        expected = LAYOUT_CELLS_5_VARIANT_1.copy()
        expected['rows'] = [0.0, 0.829, 0.886, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_1.copy(), group=0))
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_1.copy(), group=1))
        expected['rows'] = [0.0, 0.057, 0.886, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_1.copy(), group=2))
        expected['rows'] = [0.0, 0.057, 0.114, 0.171, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_1.copy(), group=3))
        expected['rows'] = [0.0, 0.057, 0.114, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_1.copy(), group=4))

        # Cells: 5 (variant 2)
        expected = LAYOUT_CELLS_5_VARIANT_2.copy()
        expected['rows'] = [0.0, 0.943, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_2.copy(), group=0))
        expected['rows'] = [0.0, 0.057, 1.0]
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_2.copy(), group=1))
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_2.copy(), group=2))
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_2.copy(), group=3))
        self.assertEqual(expected, _layout_group_height(LAYOUT_CELLS_5_VARIANT_2.copy(), group=4))

    def test_width(self):
        # Negative tests: layouts with no columns shouldn't change.
        self.assertEqual(LAYOUT_SINGLE, _layout_group_width(LAYOUT_SINGLE.copy(), group=0))
        self.assertEqual(LAYOUT_ROWS_2, _layout_group_width(LAYOUT_ROWS_2.copy(), group=0))
        self.assertEqual(LAYOUT_ROWS_2, _layout_group_width(LAYOUT_ROWS_2.copy(), group=1))
        self.assertEqual(LAYOUT_ROWS_3, _layout_group_width(LAYOUT_ROWS_3.copy(), group=0))
        self.assertEqual(LAYOUT_ROWS_3, _layout_group_width(LAYOUT_ROWS_3.copy(), group=1))
        self.assertEqual(LAYOUT_ROWS_3, _layout_group_width(LAYOUT_ROWS_3.copy(), group=2))

        # Columns: 2
        expected = LAYOUT_COLS_2.copy()
        expected['cols'] = [0.0, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_2.copy(), group=0))
        expected['cols'] = [0.0, 0.02, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_2.copy(), group=1))

        # Columns: 2 (left small)
        expected = LAYOUT_COLS_2_LEFT_SMALL.copy()
        expected['cols'] = [0.0, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_2_LEFT_SMALL.copy(), group=0))
        expected['cols'] = [0.0, 0.02, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_2_LEFT_SMALL.copy(), group=1))

        # Columns: 2 (already correct layout)
        expected = LAYOUT_COLS_2.copy()
        expected['cols'] = [0.0, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(expected.copy(), group=0))
        expected['cols'] = [0.0, 0.02, 1.0]
        self.assertEqual(expected, _layout_group_width(expected.copy(), group=1))

        # Columns: 3
        expected = LAYOUT_COLS_3.copy()
        expected['cols'] = [0.0, 0.96, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_3.copy(), group=0))
        expected['cols'] = [0.0, 0.02, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_3.copy(), group=1))
        expected['cols'] = [0.0, 0.02, 0.04, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_COLS_3.copy(), group=2))

        # Columns: 3 (already correct layout)
        expected = LAYOUT_COLS_3.copy()
        expected['cols'] = [0.0, 0.96, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(expected.copy(), group=0))

        # Grid: 4
        expected = LAYOUT_GRID_4.copy()
        expected['cols'] = [0.0, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_GRID_4.copy(), group=0))
        self.assertEqual(expected, _layout_group_width(LAYOUT_GRID_4.copy(), group=2))
        expected['cols'] = [0.0, 0.02, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_GRID_4.copy(), group=1))
        self.assertEqual(expected, _layout_group_width(LAYOUT_GRID_4.copy(), group=3))

        # Cells: 3
        expected = LAYOUT_CELLS_3_VARIANT_1.copy()
        expected['cols'] = [0.0, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_3_VARIANT_1.copy(), group=0))
        expected['cols'] = [0.0, 0.02, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_3_VARIANT_1.copy(), group=1))
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_3_VARIANT_1.copy(), group=2))

        # Cells: 5 (variant 1)
        expected = LAYOUT_CELLS_5_VARIANT_1.copy()
        expected['cols'] = [0.0, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_1.copy(), group=0))
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_1.copy(), group=3))
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_1.copy(), group=4))
        expected['cols'] = [0.0, 0.02, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_1.copy(), group=1))
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_1.copy(), group=2))

        # Cells: 5 (variant 2)
        expected = LAYOUT_CELLS_5_VARIANT_2.copy()
        expected['cols'] = [0.0, 0.5, 0.75, 0.875, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_2.copy(), group=0))
        expected['cols'] = [0.0, 0.94, 0.96, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_2.copy(), group=1))
        expected['cols'] = [0.0, 0.02, 0.96, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_2.copy(), group=2))
        expected['cols'] = [0.0, 0.02, 0.04, 0.98, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_2.copy(), group=3))
        expected['cols'] = [0.0, 0.02, 0.04, 0.06, 1.0]
        self.assertEqual(expected, _layout_group_width(LAYOUT_CELLS_5_VARIANT_2.copy(), group=4))


class TestResizeGroupsAlmostEqually(unittest.TestCase):

    def test_size(self):
        # Negative tests: layouts with no rows or columns shouldn't change.
        self.assertEqual(LAYOUT_SINGLE, _layout_groups_equal(LAYOUT_SINGLE.copy()))

        # Negative tests: layouts that are already equally sized shouldn't change
        self.assertEqual(LAYOUT_COLS_2, _layout_groups_equal(LAYOUT_COLS_2.copy()))
        self.assertEqual(LAYOUT_COLS_3, _layout_groups_equal(LAYOUT_COLS_3.copy()))
        self.assertEqual(LAYOUT_ROWS_2, _layout_groups_equal(LAYOUT_ROWS_2.copy()))
        self.assertEqual(LAYOUT_ROWS_3, _layout_groups_equal(LAYOUT_ROWS_3.copy()))
        self.assertEqual(LAYOUT_GRID_4, _layout_groups_equal(LAYOUT_GRID_4.copy()))
        self.assertEqual(LAYOUT_CELLS_3_VARIANT_1, _layout_groups_equal(LAYOUT_CELLS_3_VARIANT_1.copy()))

        # Columns: 2
        self.assertEqual(LAYOUT_COLS_2, _layout_groups_equal(LAYOUT_COLS_2_LEFT_SMALL.copy()))
        self.assertEqual(LAYOUT_COLS_2, _layout_groups_equal(LAYOUT_COLS_2_RIGHT_SMALL.copy()))

        # Rows: 2
        self.assertEqual(LAYOUT_ROWS_2, _layout_groups_equal(LAYOUT_ROWS_2_ABOVE_SMALL.copy()))
        self.assertEqual(LAYOUT_ROWS_2, _layout_groups_equal(LAYOUT_ROWS_2_BELOW_SMALL.copy()))

        # Grid: 4
        expected = LAYOUT_GRID_4.copy()
        layout = LAYOUT_GRID_4.copy()
        layout['cols'] = [0.0, 0.3, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))
        layout['cols'] = [0.0, 0.9, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))
        layout['rows'] = [0.0, 0.6, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))
        layout['rows'] = [0.0, 0.2, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))

        # Cells: 3 (variant 1)
        expected = LAYOUT_CELLS_3_VARIANT_1.copy()
        layout = LAYOUT_CELLS_3_VARIANT_1.copy()
        layout['cols'] = [0.0, 0.3, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))
        layout['cols'] = [0.0, 0.8, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))
        layout['rows'] = [0.0, 0.4, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout.copy()))

        # Cells: 4 (variant 1)
        expected = LAYOUT_CELLS_4_VARIANT_1.copy()
        layout = LAYOUT_CELLS_4_VARIANT_1.copy()
        layout['rows'] = [0.0, 0.5, 0.75, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout))
        layout['rows'] = [0.0, 0.7, 0.8, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout))
        layout['cols'] = [0.0, 0.2, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout))
        layout['cols'] = [0.0, 0.33, 1.0]
        self.assertEqual(expected, _layout_groups_equal(layout))


class MockView():
    pass


class MockWindow():

    def __init__(self):
        self.index_data = {}  # type: dict
        self._active_group_num = 0

    def set_layout(self, layout):
        self.layout_data = layout

    def layout(self):
        return self.layout_data

    def active_group(self):
        return self._active_group_num

    def focus_group(self, num):
        self._active_group_num = num

    def num_groups(self):
        return len(self.layout_data['cells'])

    def active_view(self):
        return MockView()

    def active_view_in_group(self, group_num):
        pass

    def set_view_index(self, view, group_num, group_index):
        pass


LAYOUT_EMPTY_COLS_AND_ROWS = {
    'cols': [],
    'rows': []
}  # type: dict

LAYOUT_FOOBAR_COLS_AND_ROWS = {
    'cols': [1.0],
    'rows': [1.0]
}

LAYOUT_SINGLE_CELL = {
    'cells': [[0, 0, 1, 1]],
    'cols': [0.0, 1.0], 'rows': [0.0, 1.0]
}

LAYOUT_TWO_COLUMN = {
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1]],
    'rows': [0.0, 1.0], 'cols': [0.0, 0.5, 1.0]
}

LAYOUT_THREE_COLUMN = {
    'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]],
    'rows': [0.0, 1.0], 'cols': [0.0, 0.33, 0.66, 1.0]
}

LAYOUT_TWO_ROW = {
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2]],
    'cols': [0.0, 1.0], 'rows': [0.0, 0.5, 1.0]
}

LAYOUT_THREE_ROW = {
    'cols': [0.0, 1.0],
    'cells': [[0, 0, 1, 1], [0, 1, 1, 2], [0, 2, 1, 3]], 'rows': [0.0, 0.33, 0.66, 1.0]
}

LAYOUT_FOUR_CELL_GRID = {
    'rows': [0.0, 0.5, 1.0],
    'cols': [0.0, 0.5, 1.0], 'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [0, 1, 1, 2], [1, 1, 2, 2]]
}

#  ____________
# |   0   |__1_|
# |_______|__2_|
# |  3 | 4|  5 |
# |____|__|____|
# |_____6______|
#
LAYOUT_COMPLICATED = {
    'rows': [0.0, 0.2, 0.4, 0.75, 1.0],
    'cols': [0.0, 0.4, 0.5, 1.0],
    'cells': [[0, 0, 2, 2], [2, 0, 3, 1], [2, 1, 3, 2], [0, 2, 1, 3], [1, 2, 2, 3], [2, 2, 3, 3], [0, 3, 3, 4]]
}


class TestWindowActionControl(unittest.TestCase):

    def setUp(self):
        self.window = MockWindow()

    def test_window_control_b(self):
        self.window.set_layout(LAYOUT_FOUR_CELL_GRID)
        window_control(self.window, 'b')
        self.assertEqual(3, self.window.active_group())

    def test_window_control_t(self):
        self.window.set_layout(LAYOUT_FOUR_CELL_GRID)
        window_control(self.window, 't')
        self.assertEqual(0, self.window.active_group())


class TestSublimeWindowApi(unittest.TestCase):

    def setUp(self):
        self.window = MockWindow()

    def test_nth_group_number_in_direction_of_current_one(self):

        providers = [
            {
                'layout': LAYOUT_FOOBAR_COLS_AND_ROWS,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]}  # noqa: E501
                ]
            },
            {
                'layout': LAYOUT_EMPTY_COLS_AND_ROWS,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': None, 'above': None,
                     'count': [1, 2, 3, 4, 5]}
                ]
            },
            {
                'layout': LAYOUT_SINGLE_CELL,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': None, 'above': None,
                     'count': [1, 2, 3, 4, 5]}
                ]
            },
            {
                'layout': LAYOUT_TWO_COLUMN,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': 1, 'below': None, 'above': None,
                     'count': [1, 2, 3, 4, 5]},
                    {'active_group': 1, 'left': 0, 'right': None, 'below': None, 'above': None,
                     'count': [1, 2, 3, 4, 5]}
                ]
            },
            {
                'layout': LAYOUT_THREE_COLUMN,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': 1, 'below': None, 'above': None, 'count': [1]},
                    {'active_group': 0, 'left': None, 'right': 2, 'below': None, 'above': None, 'count': [2, 3, 4, 5]},
                    {'active_group': 1, 'left': 0, 'right': 2, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]},
                    {'active_group': 2, 'left': 1, 'right': None, 'below': None, 'above': None, 'count': [1]},
                    {'active_group': 2, 'left': 0, 'right': None, 'below': None, 'above': None, 'count': [2, 3, 4, 5]}
                ]
            },
            {
                'layout': LAYOUT_TWO_ROW,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': 1, 'above': None,
                     'count': [1, 2, 3, 4, 5]},
                    {'active_group': 1, 'left': None, 'right': None, 'below': None, 'above': 0,
                     'count': [1, 2, 3, 4, 5]}
                ]
            },
            {
                'layout': LAYOUT_THREE_ROW,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': 1, 'above': None, 'count': [1]},
                    {'active_group': 0, 'left': None, 'right': None, 'below': 2, 'above': None, 'count': [2, 3, 4, 5]},
                    {'active_group': 1, 'left': None, 'right': None, 'below': 2, 'above': 0, 'count': [1, 2, 3, 4, 5]},
                    {'active_group': 2, 'left': None, 'right': None, 'below': None, 'above': 1, 'count': [1]},
                    {'active_group': 2, 'left': None, 'right': None, 'below': None, 'above': 0, 'count': [2, 3, 4, 5]}

                ]
            },
            {
                'layout': LAYOUT_FOUR_CELL_GRID,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': 1, 'below': 2, 'above': None, 'count': [1, 2, 3, 4, 5]},
                    {'active_group': 1, 'left': 0, 'right': None, 'below': 3, 'above': None, 'count': [1, 2, 3, 4, 5]},
                    {'active_group': 2, 'left': None, 'right': 3, 'below': None, 'above': 0, 'count': [1, 2, 3, 4, 5]},
                    {'active_group': 3, 'left': 2, 'right': None, 'below': None, 'above': 1, 'count': [1, 2, 3, 4, 5]}
                ]
            },

            # Test complicated layout
            #
            # Example of moving window
            #  ____________                   _________________
            # |   0   |__1_|                 |    |   1   |  2 |
            # |_______|__2a|                 |    |_______|__ _|
            # |  3 | 4|  5 | move 2 far left | 0a |  3 | 4|  5 |
            # |____|__|____|                 |    |____|__|____|
            # |______6_____|                 |____|______6_____|
            #
            #
            # Note: at time of writing the implementation does not take into
            # account the position of the cursor when moving from one view to
            # another. For example, take the follow layout:
            #        ___ ___
            #       | a | c |
            #       |___| c |
            #       | b | c |
            #       |___|_c_|
            #
            # Regardless of where the cursor in view "c", moving left currently
            # always goes to the topmost view, in the case above "a".
            {
                'layout': LAYOUT_COMPLICATED,
                'tests': [

                    {'active_group': 0, 'left': None, 'right': 1, 'below': 3, 'above': None, 'count': [1]},
                    {'active_group': 0, 'left': None, 'right': 1, 'below': 6, 'above': None, 'count': [2, 3, 4, 5]},

                    {'active_group': 1, 'left': 0, 'right': None, 'below': 2, 'above': None, 'count': [1]},
                    {'active_group': 1, 'left': 0, 'right': None, 'below': 5, 'above': None, 'count': [2]},
                    {'active_group': 1, 'left': 0, 'right': None, 'below': 6, 'above': None, 'count': [3, 4, 5]},

                    {'active_group': 2, 'left': 0, 'right': None, 'below': 5, 'above': 1, 'count': [1]},
                    {'active_group': 2, 'left': 0, 'right': None, 'below': 6, 'above': 1, 'count': [2, 3, 4, 5]},

                    {'active_group': 3, 'left': None, 'right': 4, 'below': 6, 'above': 0, 'count': [1]},
                    {'active_group': 3, 'left': None, 'right': 5, 'below': 6, 'above': 0, 'count': [2, 3, 4, 5]},

                    {'active_group': 4, 'left': 3, 'right': 5, 'below': 6, 'above': 0, 'count': [1]},
                    {'active_group': 4, 'left': 3, 'right': 5, 'below': 6, 'above': 0, 'count': [2, 3, 4, 5]},

                    {'active_group': 5, 'left': 4, 'right': None, 'below': 6, 'above': 2, 'count': [1]},
                    {'active_group': 5, 'left': 3, 'right': None, 'below': 6, 'above': 1, 'count': [2, 3, 4, 5]},

                    {'active_group': 6, 'left': None, 'right': None, 'below': None, 'above': 3, 'count': [1]},
                    {'active_group': 6, 'left': None, 'right': None, 'below': None, 'above': int(1 if unittest.is_py38() else 0), 'count': [2]}  # noqa: E501
                ]
            }
        ]  # type: list

        actions = {
            'left': 'h',
            'right': 'l',
            'above': 'k',
            'below': 'j',
        }

        for provider in providers:

            self.window.set_layout(provider['layout'])

            for test in provider['tests']:
                for direction in ['left', 'right', 'below', 'above']:
                    self.window.focus_group(test['active_group'])
                    for count in test['count']:

                        window_control(self.window, actions[direction], count)

                        expected = test[direction]
                        actual = self.window.active_group()

                        if actual == test['active_group']:
                            actual = None

                        self.assertEqual(expected, actual)
