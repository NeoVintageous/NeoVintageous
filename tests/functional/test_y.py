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


class Test_y(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_v(self):
        self.eq('x|ab|x', 'v_y', 'n_x|abx')
        self.assertRegister('"ab')
        self.assertRegister('0ab')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')
        self.eq('|fizz| |buzz|', 'v_y', 'n_|fizz |buzz')
        self.assertRegistersEqual('"0', ['fizz', 'buzz'])
        self.eq('a\n|fizz\n|b\n|buzz\n|c', 'v_y', 'n_a\n|fizz\nb\n|buzz\nc')
        self.assertRegistersEqual('"0', ['fizz\n', 'buzz\n'])
        self.assertRegistersEmpty('-1')

    def test_s(self):
        self.eq('x|ab|x', 's_y', 'n_x|abx')
        self.assertRegistersEqual('"0', 'ab')
        self.assertRegistersEmpty('-1')
        self.eq('|fizz| |buzz|', 's_y', 'n_|fizz |buzz')
        self.assertRegistersEqual('"0', ['fizz', 'buzz'])

    def test_v_y_should_not_capture_newline(self):
        self.eq('x|ab|\nx', 'v_y', 'n_x|ab\nx')
        self.assertRegister('"ab')
        self.assertRegister('0ab')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_v_y_should_capture_newline(self):
        self.eq('x|ab\n|x', 'v_y', 'n_x|ab\nx')
        self.assertRegister('"ab\n')
        self.assertRegister('0ab\n')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_yiw(self):
        self.eq('x wo|rd x', 'yiw', 'x |word x')
        self.assertRegister('"word')
        self.assertRegister('0word')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_yib(self):
        self.eq('(wo|rd)', 'yi(', '(|word)')
        self.eq('(wo|rd)', 'yi)', '(|word)')
        self.eq('(wo|rd)', 'yib', '(|word)')
        self.assertRegisters('"0', 'word')
        self.assertRegistersEmpty('-1')

        self.eq('(\nwo|rd\n)', 'yi(', '(\n|word\n)')
        self.eq('(\nwo|rd\n)', 'yi)', '(\n|word\n)')
        self.eq('(\nwo|rd\n)', 'yib', '(\n|word\n)')
        self.assertLinewiseRegisters('"0', 'word\n')
        self.assertRegistersEmpty('-1')

    def test_ydollar(self):
        self.eq('x a|b x', 'y$', 'x a|b x')
        self.assertRegister('"b x')
        self.assertRegister('0b x')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_ydollar_should_not_include_eol_newline(self):
        self.eq('x a|b x\n', 'y$', 'x a|b x\n')
        self.assertRegister('"b x')
        self.assertRegister('0b x')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_yy(self):
        self.eq('one\nt|wo\nthree', 'yy', 'one\nt|wo\nthree')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('0two\n', linewise=True)
        self.eq('o|ne', 'yy', 'o|ne')
        self.assertRegister('"one\n', linewise=True)
        self.assertRegister('0one\n', linewise=True)
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_yy_with_count(self):
        self.eq('x\n|1\n2\n3\nx\n', '3yy', 'x\n|1\n2\n3\nx\n')
        self.assertRegister('"1\n2\n3\n', linewise=True)
        self.assertRegister('01\n2\n3\n', linewise=True)
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_yy_empty_line(self):
        self.eq('\n\n|\n\n', 'yy', '\n\n|\n\n')
        self.assertRegister('"\n', linewise=True)
        self.assertRegister('0\n', linewise=True)
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_V(self):
        self.eq('x\n|abc\n|y', 'V_y', 'n_x\n|abc\ny')
        self.assertRegister('"abc\n', linewise=True)
        self.assertRegister('0abc\n', linewise=True)
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')
        self.eq('a\n|fizz\n|b\n|buzz\n|c', 'V_y', 'n_a\n|fizz\nb\n|buzz\nc')
        self.assertRegistersEqual('"0', ['fizz\n', 'buzz\n'], linewise=True)
        self.assertRegistersEmpty('-1')
