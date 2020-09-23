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


test_data = namedtuple('test_data', 'cmd initial_text regions cmd_params expected actual_func msg')
region_data = namedtuple('region_data', 'regions')

TESTS_INTERNAL_NORMAL = (
    # NORMAL mode
    test_data(cmd='nv_vi_dollar', initial_text='abc\nabc\n', regions=[[(0, 0), (0, 0)]], cmd_params={'mode': unittest.NORMAL},  # noqa: E241,E501
              expected=region_data([(0, 2), (0, 2)]), actual_func=first_sel, msg=''),

    test_data(cmd='nv_vi_dollar', initial_text=('abc\n' * 10), regions=[[(0, 0), (0, 0)]], cmd_params={'mode': unittest.NORMAL, 'count': 5},  # noqa: E241,E501
              expected=region_data([18, 18]), actual_func=first_sel, msg=''),

    test_data(cmd='nv_vi_dollar', initial_text=('abc\n\nabc\n'), regions=[[4, 4]], cmd_params={'mode': unittest.NORMAL, 'count': 1},  # noqa: E241,E501
              expected=region_data([4, 4]), actual_func=first_sel, msg='should not move on empty line'),

    # VISUAL mode
    test_data(cmd='nv_vi_dollar', initial_text='abc\nabc\n', regions=[[0, 1]], cmd_params={'mode': unittest.VISUAL},  # noqa: E241,E501
              expected=region_data([0, 4]), actual_func=first_sel, msg=''),

    test_data(cmd='nv_vi_dollar', initial_text=('abc\n' * 10), regions=[[0, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 5},  # noqa: E241,E501
              expected=region_data([0, 20]), actual_func=first_sel, msg=''),

    test_data(cmd='nv_vi_dollar', initial_text=('abc\n\nabc\n'), regions=[[4, 5]], cmd_params={'mode': unittest.VISUAL, 'count': 1},  # noqa: E241,E501
              expected=region_data([4, 5]), actual_func=first_sel, msg=''),

    test_data(cmd='nv_vi_dollar', initial_text=('abc\nabc\n'), regions=[[6, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 1},  # noqa: E241,E501
              expected=region_data([6, 3]), actual_func=first_sel, msg='can move in visual mode with reversed sel no cross over'),  # noqa: E241,E501

    test_data(cmd='nv_vi_dollar', initial_text=('abc\nabc\n'), regions=[[3, 2]], cmd_params={'mode': unittest.VISUAL, 'count': 1},  # noqa: E241,E501
              expected=region_data([2, 4]), actual_func=first_sel, msg='can move in visual mode with reversed sel at eol'),  # noqa: E241,E501

    test_data(cmd='nv_vi_dollar', initial_text=('abc\nabc\n'), regions=[[5, 4]], cmd_params={'mode': unittest.VISUAL, 'count': 2},  # noqa: E241,E501
              expected=region_data([4, 8]), actual_func=first_sel, msg='can move in visual mode with revesed sel cross over'),  # noqa: E241,E501

    test_data(cmd='nv_vi_dollar', initial_text=('abc\nabc\nabc\n'), regions=[[0, 4]], cmd_params={'mode': unittest.VISUAL_LINE, 'count': 1},  # noqa: E241,E501
              expected=region_data([0, 4]), actual_func=first_sel, msg='can move in visual mode with revesed sel cross over'),  # noqa: E241,E501

    test_data(cmd='nv_vi_dollar', initial_text='abc\nabc\n', regions=[[0, 0]], cmd_params={'mode': unittest.INTERNAL_NORMAL},  # noqa: E241,E501
              expected=region_data([0, 3]), actual_func=first_sel, msg=''),

    test_data(cmd='nv_vi_dollar', initial_text='abc\nabc\nabc\nabc\n', regions=[[0, 0]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 3},  # noqa: E241,E501
              expected=region_data([0, 12]), actual_func=first_sel, msg=''),
)


TESTS = TESTS_INTERNAL_NORMAL


class Test__nv_vi_dollar(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command(data.cmd, data.cmd_params)

            msg = "failed at test index {0} {1}".format(i, data.msg)
            actual = data.actual_func(self)

            if isinstance(data.expected, region_data):
                self.assertEqual(self._R(*data.expected.regions), actual, msg)
            else:
                self.assertEqual(data.expected, actual, msg)
