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


class TestUnimpaired(unittest.FunctionalTestCase):

    def test_blank_down(self):
        self.eq('aaa\nbb|b\nccc', '] ', 'aaa\n|bbb\n\nccc')
        self.eq('aaa\n    bb|b\nccc', '] ', 'aaa\n    |bbb\n\nccc')
        self.eq('aaa\nbb|b\nccc', '2] ', 'aaa\n|bbb\n\n\nccc')
        self.eq('aaa\nbb|b\nccc', '5] ', 'aaa\n|bbb\n\n\n\n\n\nccc')
        self.eq('aaa\nbb|b\nccc', '5] ', 'aaa\n|bbb\n\n\n\n\n\nccc')
        self.eq('aaa\n    bb|b\nccc', '5] ', 'aaa\n    |bbb\n\n\n\n\n\nccc')

    def test_blank_up(self):
        self.eq('aaa\nbb|b\nccc', '[ ', 'aaa\n\n|bbb\nccc')
        self.eq('aaa\n    bb|b\nccc', '[ ', 'aaa\n\n    |bbb\nccc')
        self.eq('aaa\nbb|b\nccc', '3[ ', 'aaa\n\n\n\n|bbb\nccc')
        self.eq('aaa\n    bb|b\nccc', '3[ ', 'aaa\n\n\n\n    |bbb\nccc')

    def test_move_down(self):
        self.eq('111\n22|2\n333\n444', ']e', '111\n333\n22|2\n444')
        self.eq('111\n22|2\n333\n444\n555\n666\n777\n888', '5]e', '111\n333\n444\n555\n666\n777\n22|2\n888')

    def test_move_up(self):
        self.eq('111\n222\n33|3\n444', '[e', '111\n33|3\n222\n444')
        self.eq('111\n222\n333\n444\n555\n666\n77|7\n888', '3[e', '111\n222\n333\n77|7\n444\n555\n666\n888')
