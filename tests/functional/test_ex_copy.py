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


class Test_ex_copy(unittest.FunctionalTestCase):

    def test_copy(self):
        self.eq('a\n|b\nc\n', ':copy 0', '|b\na\nb\nc\n')
        self.eq('a\n|b\nc\n', ':copy 1', 'a\n|b\nb\nc\n')
        self.eq('a\n|b\nc\n', ':copy 2', 'a\nb\n|b\nc\n')
        self.eq('a\n|b\nc\n', ':%copy 0', 'a\nb\n|c\na\nb\nc\n')
        self.eq('a\n|b\nc\n', ':%copy 2', 'a\nb\na\nb\n|c\nc\n')
        self.eq('abc\n|xxx\nabc\nabc', ':copy3', 'abc\nxxx\nabc\n|xxx\nabc')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':.,.+1copy4', 'abc\nxxx\nxxx\nabc\nxxx\n|xxx\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':copy4', 'abc\nxxx\nabc\nabc\n|xxx')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':.,.+1copy5', 'abc\nxxx\nxxx\nabc\nabc\nxxx\n|xxx')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':.,.+1copy0', 'xxx\n|xxx\nabc\nxxx\nxxx\nabc\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':copy0', '|xxx\nabc\nxxx\nabc\nabc')
        self.eq('abc\n|xxx\nabc\n\nabc', ':copy4', 'abc\nxxx\nabc\n\n|xxx\nabc')
        self.eq('abc\n|xxx\nxxx\nabc\n\nabc', ':.,.+1copy5', 'abc\nxxx\nxxx\nabc\n\nxxx\n|xxx\nabc')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':.,.+1copy2', 'abc\nxxx\nxxx\n|xxx\nxxx\nabc\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':copy2', 'abc\nxxx\n|xxx\nabc\nabc')
        self.eq('|abc', ':copy 1,10', '|abc')
        self.eq('abc\n|xxx\nabc\nabc', ':copy 3', 'abc\nxxx\nabc\n|xxx\nabc')
