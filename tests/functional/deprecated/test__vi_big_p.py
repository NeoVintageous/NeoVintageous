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

from NeoVintageous.nv.vi import registers


test_data = namedtuple('test_data', 'content regions in_register params expected msg')

TESTS = (
    # INTERNAL NORMAL MODE
    test_data(content='abc',
              regions=[[(0, 0), (0, 0)]],
              in_register=['xxx'], params={'mode': unittest.INTERNAL_NORMAL, 'count': 1},
              expected=('xxxabc', unittest.Region(2, 2)), msg='failed in {0}'),

    # INTERNAL NORMAL MODE - linewise
    test_data(content='abc',
              regions=[[(0, 0), (0, 0)]],
              in_register=['xxx\n'], params={'mode': unittest.INTERNAL_NORMAL, 'count': 1},
              expected=('xxx\nabc', unittest.Region(0, 0)), msg='failed in {0}'),

    # VISUAL MODE
    test_data(content='abc',
              regions=[[(0, 0), (0, 3)]],
              in_register=['xxx'], params={'mode': unittest.VISUAL, 'count': 1},
              expected=('xxx', unittest.Region(2, 2)), msg='failed in {0}'),

    # VISUAL MODE - linewise
    test_data(content='aaa bbb ccc',
              regions=[[(0, 4), (0, 7)]],
              in_register=['xxx\n'], params={'mode': unittest.VISUAL, 'count': 1},
              expected=('aaa xxx\n ccc', unittest.Region(6, 6)), msg='failed in {0}'),
)


class Test__vi_big_p(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.content)
            self.select([self._R(*region) for region in data.regions])

            self.view.settings().set('vintageous_use_sys_clipboard', False)
            registers._data['"'] = data.in_register
            registers._linewise['"'] = False

            self.view.run_command('_vi_big_p', data.params)

            msg = "[{0}] {1}".format(i, data.msg)
            self.assertEqual(data.expected[0], self.content(), msg.format(i))
            self.assertEqual(data.expected[1], self.view.sel()[0], msg.format(i))
