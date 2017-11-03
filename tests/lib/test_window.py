import unittest

from NeoVintageous.lib.window import WindowAPI


class MockView():
    pass


class MockWindow():

    def __init__(self):
        self.index_data = {}

    def set_layout(self, layout):
        self.layout_data = layout

    def layout(self):
        return self.layout_data

    def active_group(self):
        return self.active_group_num

    def focus_group(self, num):
        self.active_group_num = num

    def num_groups(self):
        return len(self.layout_data['cells'])

    def active_view(self):
        return MockView()

    def set_view_index(self, view, group_num, group_index):
        pass


LAYOUT_EMPTY_COLS_AND_ROWS = {
    'cols': [],
    'rows': []
}

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


class TestSublimeWindowApi(unittest.TestCase):

    def setUp(self):
        self.window = MockWindow()
        self.api = WindowAPI(self.window)

    def test_nth_group_number_in_direction_of_current_one(self):

        providers = [
            {
                'layout': LAYOUT_FOOBAR_COLS_AND_ROWS,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]}  # FIXME # noqa: E501
                ]
            },
            {
                'layout': LAYOUT_EMPTY_COLS_AND_ROWS,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]}  # FIXME # noqa: E501
                ]
            },
            {
                'layout': LAYOUT_SINGLE_CELL,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': None, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]}  # FIXME # noqa: E501
                ]
            },
            {
                'layout': LAYOUT_TWO_COLUMN,
                'tests': [
                    {'active_group': 0, 'left': None, 'right': 1, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]},  # FIXME # noqa: E501
                    {'active_group': 1, 'left': 0, 'right': None, 'below': None, 'above': None, 'count': [1, 2, 3, 4, 5]}  # FIXME # noqa: E501
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
                    {'active_group': 0, 'left': None, 'right': None, 'below': 1, 'above': None, 'count': [1, 2, 3, 4, 5]},  # FIXME # noqa: E501
                    {'active_group': 1, 'left': None, 'right': None, 'below': None, 'above': 0, 'count': [1, 2, 3, 4, 5]}  # FIXME # noqa: E501
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
            {
                'layout': LAYOUT_COMPLICATED,
                'tests': [

                    # Note: at time of writing the implementation does not take into account the
                    # position of the cursor when moving from one view to another. For example,
                    # take the follow layout:
                    #  ___ ___
                    # | a | c |
                    # |___| c |
                    # | b | c |
                    # |___|_c_|
                    #
                    # Regardless of where the cursor in view "c", moving left currently always
                    # goes to the topmost view, in the case above "a".

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
                    {'active_group': 6, 'left': None, 'right': None, 'below': None, 'above': 0, 'count': [2]},

                    # { 'active_group': 6, 'left': None, 'right': None, 'below': None, 'above': 0, 'count': [3]}
                    # TODO select alternative based on cursor position; above should be == 1
                ]
            }
        ]

        for provider in providers:
            self.window.set_layout(provider['layout'])
            for test in provider['tests']:
                self.window.active_group_num = test['active_group']
                for direction in ['left', 'right', 'below', 'above']:
                    for count in test['count']:
                        self.assertEqual(
                            test[direction],
                            self.api._get_nth_group_number_in_direction_of_current_one(direction, count)
                        )
