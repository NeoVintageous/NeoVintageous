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


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected msg')

TESTS = (
    test_data('abc aaa100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc\nabc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc\nabc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 8), (0, 8)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa110bbb abc\nabc aaa110bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10}, 'abc aaa-90bbb abc\nabc aaa-90bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 0), (0, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc', [[(0, 8), (0, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc\nabc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc\nabc aaa-110bbb abc', ''),  # noqa: E241,E501

    test_data('abc aaa100bbb abc\nabc aaa100bbb abc', [[(0, 8), (0, 8)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa90bbb abc\nabc aaa90bbb abc', ''),  # noqa: E241,E501
    test_data('abc aaa-100bbb abc\nabc aaa-100bbb abc', [[(0, 0), (0, 0)], [(1, 8), (1, 8)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 10, 'subtract': True}, 'abc aaa-110bbb abc\nabc aaa-110bbb abc', ''),  # noqa: E241,E501
)


class Test__nv_vi_ctrl_x(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('nv_vi_modify_numbers', data.cmd_params)

            self.assertEqual(data.expected, self.content(), "[{0}] {1}".format(i, data.msg))
