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


TESTS_NORMAL_SINGLE_SEL = (
    test_data(initial_text='abc',     regions=[[(0, 2), (0, 2)]], cmd_params={'mode': unittest.NORMAL},  expected=[(0, 0), (0, 0)], actual_func=first_sel,  msg=''),  # noqa: E241,E501
    test_data(initial_text='abc abc', regions=[[(0, 4), (0, 4)]], cmd_params={'mode': unittest.NORMAL},  expected=[(0, 0), (0, 0)], actual_func=first_sel,  msg=''),  # noqa: E241,E501
    test_data(initial_text='abc a',   regions=[[(0, 4), (0, 4)]], cmd_params={'mode': unittest.NORMAL},  expected=[(0, 0), (0, 0)], actual_func=first_sel,  msg=''),  # noqa: E241,E501
)

TESTS_VISUAL_SINGLE_SEL_START_LEN_1 = (
    test_data(initial_text='abc',   regions=[[(0, 2), (0, 3)]], cmd_params={'mode': unittest.VISUAL},  expected=[(0, 3), (0, 0)], actual_func=first_sel,  msg=''),  # noqa: E241,E501
    test_data(initial_text='abc a', regions=[[(0, 4), (0, 5)]], cmd_params={'mode': unittest.VISUAL},  expected=[(0, 5), (0, 0)], actual_func=first_sel,  msg=''),  # noqa: E241,E501
)

TESTS = TESTS_NORMAL_SINGLE_SEL + TESTS_VISUAL_SINGLE_SEL_START_LEN_1


class Test__nv_vi_b(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('nv_vi_b', data.cmd_params)
            actual = data.actual_func(self)

            self.assertEqual(self._R(*data.expected), actual, "failed at test index {0} {1}".format(i, data.msg))
