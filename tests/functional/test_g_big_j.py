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


class Test_gJ(unittest.FunctionalTestCase):

    def test_gJ(self):
        self.eq('|aaa\nbbb', 'gJ', 'aaa|bbb')
        self.eq('|aaa\nbbb', '1gJ', 'aaa|bbb')
        self.eq('|aaa\nbbb', '2gJ', 'aaa|bbb')
        self.eq('|aaa\nbbb', '9gJ', 'aaa|bbb')
        self.eq('|aaa\nbbb\nccc', 'gJ', 'aaa|bbb\nccc')
        self.eq('|aaa\nbbb\nccc', '1gJ', 'aaa|bbb\nccc')
        self.eq('|aaa\nbbb\nccc', '2gJ', 'aaa|bbb\nccc')
        self.eq('|aaa\nbbb\nccc', '3gJ', 'aaa|bbbccc'),  # TODO Fix: cursor position is incorrect
        self.eq('|aaa\nbbb\nccc', '9gJ', 'aaa|bbbccc'),  # TODO Fix: cursor position is incorrect
        self.eq('|aaa\n    bbb', 'gJ', 'aaa|    bbb')
        self.eq('|aaa\n    bbb', '1gJ', 'aaa|    bbb')
        self.eq('|aaa\n    bbb', '2gJ', 'aaa|    bbb')
        self.eq('|aaa\n    bbb', '9gJ', 'aaa|    bbb')
