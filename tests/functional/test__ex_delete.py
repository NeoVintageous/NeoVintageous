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


class Test_ex_delete(unittest.FunctionalTestCase):

    def test_delete(self):
        self.eq('abc\n|xxx\nabc\nabc', ':delete', 'abc\n|abc\nabc')
        self.eq('abc\nabc\nabc\n|xxx', ':4delete', 'abc\nabc\nabc\n|')
        self.eq('abc\nabc\nabc\n|xxx\n', ':delete', 'abc\nabc\nabc\n|')
        self.eq('xxx\n|abc\nabc\nabc', ':0delete', '|abc\nabc\nabc')
        self.eq('abc\n|abc\n\nabc', ':3delete', 'abc\nabc\n|abc')
        self.eq('|abc\nxxx\nxxx\nabc\nabc', ':2,3delete', 'abc\n|abc\nabc')
        self.eq('|abc\nxxx\nxxx\nxxx\nabc\nabc', ':2,4delete', 'abc\n|abc\nabc')
        self.eq('|abc\n\n\n\nabc\nabc', ':2,4delete', 'abc\n|abc\nabc')
        self.eq('abc\nxxx\nabc\n|abc', ':2,4delete', 'abc\n|')
        self.eq('abc\n|xxx\nabc\nabc', ':2delete', 'abc\n|abc\nabc')

    def test_v_delete(self):
        self.eq('1\n2|2\n33\n4|4\n5\n', ":'<,'>delete", 'n_1\n|5\n')
