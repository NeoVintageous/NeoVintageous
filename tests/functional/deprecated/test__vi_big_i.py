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


def second_sel(self):
    return self.view.sel()[1]


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')

TESTS = (
    test_data('abc',           [[(0, 0), (0, 2)]],                   {'mode': unittest.INTERNAL_NORMAL}, [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 1)], [(1, 1), (1, 1)]], {'mode': unittest.INTERNAL_NORMAL}, [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 1)], [(1, 1), (1, 1)]], {'mode': unittest.INTERNAL_NORMAL}, [(1, 0), (1, 0)], second_sel, ''),  # noqa: E241,E501
    test_data('abc',           [[(0, 0), (0, 2)]],                   {'mode': unittest.VISUAL},           [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 2)], [(1, 1), (1, 2)]], {'mode': unittest.VISUAL},           [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 2)], [(1, 1), (1, 2)]], {'mode': unittest.VISUAL},           [(1, 0), (1, 0)], second_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc\nabc', [[(0, 0), (1, 4)]],                   {'mode': unittest.VISUAL_LINE},      [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc\nabc', [[(1, 0), (2, 4)]],                   {'mode': unittest.VISUAL_LINE},      [(1, 0), (1, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 2), (0, 3)], [(1, 2), (1, 3)]], {'mode': unittest.VISUAL_BLOCK},     [(0, 2), (0, 2)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 2), (0, 3)], [(1, 2), (1, 3)]], {'mode': unittest.VISUAL_BLOCK},     [(1, 2), (1, 2)], second_sel, ''),  # noqa: E241,E501
)


class Test__nv_vi_big_i(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('nv_vi_big_i', data.cmd_params)
            actual = data.actual_func(self)

            self.assertEqual(self._R(*data.expected), actual, "[{0}] {1}".format(i, data.msg))
