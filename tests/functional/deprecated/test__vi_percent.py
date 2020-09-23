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

from collections import namedtuple

from NeoVintageous.tests import unittest


def first_sel(self):
    return self.view.sel()[0]


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')

TESTS = (
    test_data('abc (abc) abc', [[(0, 6), (0, 7)]], {'mode': unittest.VISUAL},           [(0, 7), (0, 4)], first_sel, 'visual not on bracket A'),  # noqa: E241,E501
    test_data('abc (abc) abc', [[(0, 7), (0, 6)]], {'mode': unittest.VISUAL},           [(0, 7), (0, 4)], first_sel, 'visual not on bracket B'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 0), (0, 2)]], {'mode': unittest.VISUAL},           [(0, 0), (0, 4)], first_sel, 'visual right A'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 1), (0, 2)]], {'mode': unittest.VISUAL},           [(0, 1), (0, 4)], first_sel, 'visual right B'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 5), (0, 3)]], {'mode': unittest.VISUAL},           [(0, 5), (0, 1)], first_sel, 'visual left A'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 4), (0, 3)]], {'mode': unittest.VISUAL},           [(0, 4), (0, 1)], first_sel, 'visual left B'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 2), (0, 4)]], {'mode': unittest.VISUAL},           [(0, 3), (0, 1)], first_sel, 'visual right->left A'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 3), (0, 4)]], {'mode': unittest.VISUAL},           [(0, 4), (0, 1)], first_sel, 'visual right->left B'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 3), (0, 1)]], {'mode': unittest.VISUAL},           [(0, 2), (0, 4)], first_sel, 'visual left->right A'),  # noqa: E241,E501
    test_data('0(2)4',         [[(0, 2), (0, 1)]], {'mode': unittest.VISUAL},           [(0, 1), (0, 4)], first_sel, 'visual left->right B'),  # noqa: E241,E501
    test_data('()',            [[(0, 0), (0, 1)]], {'mode': unittest.VISUAL},           [(0, 0), (0, 2)], first_sel, 'visual off by one right'),  # noqa: E241,E501
    test_data('()',            [[(0, 2), (0, 1)]], {'mode': unittest.VISUAL},           [(0, 2), (0, 0)], first_sel, 'visual off by one left'),  # noqa: E241,E501
    test_data('()',            [[(0, 1), (0, 2)]], {'mode': unittest.VISUAL},           [(0, 2), (0, 0)], first_sel, 'visual off by one right->left'),  # noqa: E241,E501
    test_data('()',            [[(0, 1), (0, 0)]], {'mode': unittest.VISUAL},           [(0, 0), (0, 2)], first_sel, 'visual off by one left->right'),  # noqa: E241,E501
    test_data('abc (abc) abc', [[(0, 6), (0, 6)]], {'mode': unittest.INTERNAL_NORMAL},  [(0, 7), (0, 4)], first_sel, ''),  # noqa: E241,E501
    test_data('abc (abc) abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL},  [(0, 9), (0, 4)], first_sel, ''),  # noqa: E241,E501
    test_data('abc (abc) abc', [[(0, 4), (0, 4)]], {'mode': unittest.INTERNAL_NORMAL},  [(0, 4), (0, 9)], first_sel, ''),  # noqa: E241,E501
    test_data('abc (abc) abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL},  [(0, 0), (0, 9)], first_sel, ''),  # noqa: E241,E501
)


class Test__nv_vi_percent(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.view.sel().clear()

            self.write(data.initial_text)
            for region in data.regions:
                self.select(self._R(*region))

            self.view.run_command('nv_vi_percent', data.cmd_params)

            msg = "[{0}] {1}".format(i, data.msg)
            actual = data.actual_func(self)
            self.assertEqual(self._R(*data.expected), actual, msg)
