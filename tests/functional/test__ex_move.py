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


class Test_ex_move(unittest.FunctionalTestCase):

    def test_move(self):
        self.eq('a\n|b\nc\n', ':move 0', '|b\na\nc\n')
        self.eq('a\n|b\nc\n', ':move 1', '|a\nb\nc\n')
        self.eq('a\n|b\nc\n', ':move 2', 'a\n|b\nc\n')
        self.eq('a\n|b\nc\n', ':move 3', 'a\nc\n|\nb')
        self.eq('aaa\n|xxx\nxxx\naaa\n\naaa', ':move5', 'aaa\nxxx\naaa\n\nxx|x\naaa')
        self.eq('aaa\n|xxx\nxxx\naaa\naaa', ':move5', 'aaa\nxxx\naaa\naaa\n|xxx')
        self.eq('abc\n|xxx\nabc\n\nabc', ':move4', 'abc\nabc\n\nxx|x\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move 2', 'abc\n|xxx\nabc\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move 3', 'abc\nabc\n|xxx\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move0', '|xxx\nabc\nabc\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move3', 'abc\nabc\n|xxx\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move4', 'abc\nabc\nabc\n|xxx')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':move0', '|xxx\nabc\nxxx\nabc\nabc')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':move4', 'abc\nxxx\nabc\n|xxx\nabc')

    def test_v_move(self):
        self.eq('abc\n|x|xx\nabc\nabc', ":'<,'>move3", 'n_abc\nabc\n|xxx\nabc')

    @unittest.mock_status_message()
    def test_cannot_move_lines_into_themselves(self):
        self.eq('|1\n2\n3\n|4', ':\'<,\'>move 2', 'n_1\n2\n3\n|4')
        self.assertStatusMessage('E134: Move lines into themselves')
