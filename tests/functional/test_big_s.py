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


class Test_S(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_S(self):
        self.eq('|', 'S', 'i_|')
        self.eq('|aaa\nbbb\nccc', 'S', 'i_|\nbbb\nccc')
        self.eq('aaa\nbb|b\nccc', 'S', 'i_aaa\n|\nccc')
        self.eq('aaa\nbbb\n|ccc', 'S', 'i_aaa\nbbb\n|')
        self.assertRegister('"', 'ccc\n')
        self.assertRegister('-', None)
        self.assertRegister('0', None)
        self.assertRegister('1', 'ccc\n')
        self.assertRegister('2', 'bbb\n')
        self.assertRegister('3', 'aaa\n')

    def test_S_should_not_strip_preceding_whitespace(self):
        self.eq('    |one', 'S', 'i_    |')

    def test_S_last_line(self):
        self.eq('1\ntw|o', 'S', 'i_1\n|')
        self.eq('1\ntw|o\n', 'S', 'i_1\n|\n')
