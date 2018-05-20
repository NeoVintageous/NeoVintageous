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


class Test_0(unittest.FunctionalTestCase):

    def test_0(self):
        self.eq('|abc', '0', '|abc')
        self.eq('a|bc', '0', '|abc')
        self.eq('ab|c', '0', '|abc')
        self.eq('x\n|ab\nx', '0', 'x\n|ab\nx')
        self.eq('x\na|b\nx', '0', 'x\n|ab\nx')
        self.eq('x\nab|\nx', '0', 'x\n|ab\nx')

    def test_v_0(self):
        self.eq('x\nab|c|d\nx', 'v_0', 'x\n|abc|d\nx')
        self.eq('x\na|bc|d\nx', 'v_0', 'x\n|ab|cd\nx')
        self.eq('x\n|abcd|\nx', 'v_0', 'x\n|a|bcd\nx')

    def test_v_0_multiline(self):
        self.eq('x|a\nabc|d\nx', 'v_0', 'x|a\na|bcd\nx')
