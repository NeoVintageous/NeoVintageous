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
    test_data('    abc',                   [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 1}, 'abc',               'failed in {0}'),  # noqa: E241,E501
    test_data('        abc',               [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 1}, '    abc',           'failed in {0}'),  # noqa: E241,E501
    test_data('    abc\n    abc',          [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 2}, 'abc\nabc',          'failed in {0}'),  # noqa: E241,E501
    test_data('    abc\n    abc\n    abc', [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 3}, 'abc\nabc\nabc',     'failed in {0}'),  # noqa: E241,E501
    test_data('    abc\n    abc\n    abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL, 'count': 1}, 'abc\nabc\n    abc', 'failed in {0}'),  # noqa: E241,E501
)


class Test__nv_vi_double_antilambda(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('nv_vi_less_than_less_than', data.cmd_params)

            self.assertEqual(data.expected, self.content(), "[{0}] {1}".format(i, data.msg).format(i))
