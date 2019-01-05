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


class Test_x(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_x_empty(self):
        self.eq('|', 'x', '|')
        self.eq('|\n', 'x', '|\n')
        self.eq('|a\n', 'x', '|\n')
        self.eq('a|xb\n', 'x', 'a|b\n')
        self.eq('a|123b\n', '3x', 'a|b\n')
        self.assertRegister('"', '123')
        self.assertRegister('-', '123')
        self.assertRegister('1', None)

    def test_x_should_be_noop_on_empty_lines(self):
        self.eq('\n\n|\n\n', 'x', '\n\n|\n\n')
        self.assertRegister('"', None)
        self.assertRegister('-', None)
        self.assertRegister('1', None)

    def test_x_multiple_selections(self):
        self.eq('a|xb|xc|xd', 'x', 'a|b|c|d')

    def test_v_x(self):
        self.eq('|a', 'v_x', 'n_|')
        self.eq('|a\n', 'v_x', 'n_|\n')
        self.eq('a|xb\n', 'v_x', 'n_a|b\n', 'should delete character')
        self.eq('a|xyz|b\n', 'v_x', 'n_a|b\n', 'should delete characters')
        self.assertRegister('"', 'xyz')
        self.assertRegister('-', 'xyz')
        self.assertRegister('1', None)

    def test_v_x_multiple_lines(self):
        self.eq('a\nb|x\ny|c\n', 'v_x', 'n_a\nb|c\n', 'should delete characters across multiple lines')
        self.eq('ab\n|xy\n|cd\n', 'v_x', 'n_ab\n|cd\n', 'should delete full line')
        self.eq('ab\n|x1\nx2\n|cd\n', 'v_x', 'n_ab\n|cd\n', 'should delete two full lines')
        self.eq('\n|\n\n|\n', 'v_x', 'n_\n|\n')
        self.assertRegister('"', '\n\n')
        self.assertRegister('-', None)
        self.assertRegister('1', '\n\n')
        self.assertRegister('2', 'x1\nx2\n')
        self.assertRegister('3', 'xy\n')
        self.assertRegister('4', 'x\ny')

    def test_v_x_multiple_selections(self):
        self.eq('a|xb|xc|xd', 'x', 'a|b|c|d', 'should work for multiple selection')
        self.eq('a|x1|b|x2|c|x3|d', 'v_x', 'n_a|b|c|d', 'should work for multiple selection')

    def test_l_x(self):
        self.eq('ab\n|xy\n|cd\n', 'l_x', 'n_ab\n|cd\n', 'should delete full line')
        self.eq('ab\n|x1\nx2\nx3\n|cd\n', 'l_x', 'n_ab\n|cd\n', 'should delete multiple full lines')
        self.assertRegister('"', 'x1\nx2\nx3\n')
        self.assertRegister('-', None)
        self.assertRegister('1', 'x1\nx2\nx3\n')
        self.assertRegister('2', 'xy\n')

    def test_l_x_empty_lines(self):
        self.eq('\n|\n\n|\n', 'l_x', 'n_\n|\n')
        self.assertRegister('"', '\n\n')
        self.assertRegister('-', None)
        self.assertRegister('1', '\n\n')

    def test_issue_263(self):
        self.eq('a\n|\nb', 'x', 'a\n|\nb')
        self.eq('a\n\n|\n\nb', 'x', 'a\n\n|\n\nb')
