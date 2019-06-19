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


class Test_X(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'X', '|')
        self.eq('|\n', 'X', '|\n')
        self.eq('|a\n', 'X', '|a\n')
        self.eq('a|b', 'X', '|b')
        self.eq('a|b\n', 'X', '|b\n')
        self.eq('x\nab|cd', '5X', 'x\n|cd')
        self.eq('7654321|\n', '6X', '|7\n')
        self.assertLinewiseRegisters('"1', '654321\n')
        self.assertRegistersEmpty('-0')

    def test_v(self):
        self.eq('one\n|two\n|three', 'v_X', 'n_one\n|three')
        self.assertLinewiseRegisters('"1', 'two\n')
        self.eq('fi|zz\nbu|zz', 'v_X', 'n_|')
        self.assertLinewiseRegisters('"1', 'fizz\nbuzz\n')
        self.eq('1\nfi|zz\nbu|zz\n2\n3', 'v_X', 'n_1\n|2\n3')
        self.assertLinewiseRegisters('"1', 'fizz\nbuzz\n')
        self.eq('1\n\n|\n\n|\n\n2\n3', 'v_X', 'n_1\n\n|\n\n2\n3')
        self.assertLinewiseRegisters('"1', '\n\n\n')
        self.eq('|\n|', 'v_X', 'n_|\n')
        self.eq('r_|\n|', 'v_X', 'n_|\n')
        self.assertRegistersEmpty('-0')

    def test_V(self):
        self.eq('one\n|two\n|three', 'V_X', 'n_one\n|three')
        self.assertLinewiseRegisters('"1', 'two\n')
        self.assertRegistersEmpty('-0')
