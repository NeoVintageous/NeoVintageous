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


class Test_y(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_v_y(self):
        self.eq('x|ab|x', 'v_y', 'n_x|abx')
        self.assertRegister('"', 'ab')
        self.assertRegister('0', 'ab')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_v_y_should_not_capture_newline(self):
        self.eq('x|ab|\nx', 'v_y', 'n_x|ab\nx')
        self.assertRegister('"', 'ab')
        self.assertRegister('0', 'ab')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_v_y_should_capture_newline(self):
        self.eq('x|ab\n|x', 'v_y', 'n_x|ab\nx')
        self.assertRegister('"', 'ab\n')
        self.assertRegister('0', 'ab\n')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_yiw(self):
        self.eq('x wo|rd x', 'yiw', 'x |word x')
        self.assertRegister('"', 'word')
        self.assertRegister('0', 'word')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_ydollar(self):
        self.eq('x a|b x', 'y$', 'x a|b x')
        self.assertRegister('"', 'b x')
        self.assertRegister('0', 'b x')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_ydollar_should_not_include_eol_newline(self):
        self.eq('x a|b x\n', 'y$', 'x a|b x\n')
        self.assertRegister('"', 'b x')
        self.assertRegister('0', 'b x')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_yy(self):
        self.eq('one\nt|wo\nthree', 'yy', 'one\nt|wo\nthree')
        self.assertRegister('"', 'two\n')
        self.assertRegister('0', 'two\n')
        self.eq('o|ne', 'yy', 'o|ne')
        self.assertRegister('"', 'one\n')
        self.assertRegister('0', 'one\n')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_yy_with_count(self):
        self.eq('x\n|1\n2\n3\nx\n', '3yy', 'x\n|1\n2\n3\nx\n')
        self.assertRegister('"', '1\n2\n3\n')
        self.assertRegister('0', '1\n2\n3\n')
        self.assertRegister('1', None)
        self.assertRegister('-', None)

    def test_yy_empty_line(self):
        self.eq('\n\n|\n\n', 'yy', '\n\n|\n\n')
        self.assertRegister('"', '\n')
        self.assertRegister('0', '\n')
        self.assertRegister('1', None)
        self.assertRegister('-', None)
