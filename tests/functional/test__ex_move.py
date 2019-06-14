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

    def test_n(self):
        self.eq('a\n|b\nc', ':move 0', '|b\na\nc')
        self.eq('a\n|b\nc', ':move 1', 'a\n|b\nc')
        self.eq('a\n|b\nc', ':move 2', 'a\n|b\nc')
        self.eq('a\n|b\nc', ':move 3', 'a\nc\n|b')

        self.eq('a\n|b\nc', ':move2', 'a\n|b\nc')

        self.eq('a\n|b\nc', ':m 2', 'a\n|b\nc')
        self.eq('a\n|b\nc', ':m2', 'a\n|b\nc')

        self.eq('a\n|b\nc\n', ':move 0', '|b\na\nc\n')
        self.eq('a\n|b\nc\n', ':move 1', 'a\n|b\nc\n')
        self.eq('a\n|b\nc\n', ':move 2', 'a\n|b\nc\n')
        self.eq('a\n|b\nc\n', ':move 3', 'a\nc\n|b\n')

        self.eq('a\nb\nc\n|x', ':move 0', '|x\na\nb\nc\n')
        self.eq('a\nb\nc\n|x', ':move 1', 'a\n|x\nb\nc\n')
        self.eq('a\nb\nc\n|x', ':move 2', 'a\nb\n|x\nc\n')

        self.eq('a\nb\nc\n|x\n', ':move 0', '|x\na\nb\nc\n')
        self.eq('a\nb\nc\n|x\n', ':move 1', 'a\n|x\nb\nc\n')
        self.eq('a\nb\nc\n|x\n', ':move 2', 'a\nb\n|x\nc\n')

        self.eq('a\nb\n|x\nc', ':move 0', '|x\na\nb\nc')
        self.eq('a\nb\n|x\nc', ':move 1', 'a\n|x\nb\nc')

        self.eq('a\nb\n|x\nc\n', ':move 0', '|x\na\nb\nc\n')
        self.eq('a\nb\n|x\nc\n', ':move 1', 'a\n|x\nb\nc\n')

        self.eq('1\n|fizz\nbuzz\n4\n', ':move 1', '1\n|fizz\nbuzz\n4\n')

        self.eq('abc\n|xxx\nabc\nabc', ':move 2', 'abc\n|xxx\nabc\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move 3', 'abc\nabc\n|xxx\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move0', '|xxx\nabc\nabc\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move3', 'abc\nabc\n|xxx\nabc')
        self.eq('abc\n|xxx\nabc\nabc', ':move4', 'abc\nabc\nabc\n|xxx')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':move0', '|xxx\nabc\nxxx\nabc\nabc')
        self.eq('abc\n|xxx\nxxx\nabc\nabc', ':move4', 'abc\nxxx\nabc\n|xxx\nabc')

        self.eq('111\n|222\n333\n444\n555', ':move5', '111\n333\n444\n555\n|222')
        self.eq('111\n|222\n333\n444\n\n555', ':move5', '111\n333\n444\n\n|222\n555')
        self.eq('111\n|222\n333\n\n444', ':move4', '111\n333\n\n|222\n444')

        self.eq('1\n|buzz\nfizz\n4\n', ':move .+1', '1\nfizz\n|buzz\n4\n')
        self.eq('1\n|buzz\nfizzer\n4\n', ':move .+1', '1\nfizzer\n|buzz\n4\n')
        self.eq('1\n|buzzer\nfizz\n4\n', ':move .+1', '1\nfizz\n|buzzer\n4\n')

        self.eq('1\nbuzz\n|fizz\n4\n', ':move .-2', '1\n|fizz\nbuzz\n4\n')
        self.eq('1\nbuzz\n|fizzer\n4\n', ':move .-2', '1\n|fizzer\nbuzz\n4\n')
        self.eq('1\nbuzzer\n|fizz\n4\n', ':move .-2', '1\n|fizz\nbuzzer\n4\n')

    def test_v(self):
        self.eq('abc\n|x|xx\nabc\nabc', ":'<,'>move 3", 'n_abc\nabc\n|xxx\nabc')
        self.eq('abc\n|x|xx\nabc\nabc', ":'<,'>move3", 'n_abc\nabc\n|xxx\nabc')

        self.eq('abc\n|x|xx\nabc\nabc', ":'<,'>m 3", 'n_abc\nabc\n|xxx\nabc')
        self.eq('abc\n|x|xx\nabc\nabc', ":'<,'>m3", 'n_abc\nabc\n|xxx\nabc')

    @unittest.mock_status_message()
    def test_cannot_move_lines_into_themselves(self):
        self.eq('|1\n2\n3\n|4', ':\'<,\'>move 2', 'v_|1\n2\n3\n|4')
        self.assertStatusMessage('E134: Move lines into themselves')

    @unittest.mock_status_message()
    def test_invalid_address(self):
        self.eq('1\n|buzz\nfizz\n4\n', ':move', '1\n|buzz\nfizz\n4\n')
        self.assertStatusMessage('E14: Invalid address')
