# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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
        self.assertRegisters('"0', 'ab')
        self.assertRegistersEmpty('-1')
        self.eq('|fizz| |buzz|', 'v_y', 'n_|fizz |buzz')
        self.assertRegisters('"0', ['fizz', 'buzz'])
        self.eq('a\n|fizz\n|b\n|buzz\n|c', 'v_y', 'n_a\n|fizz\nb\n|buzz\nc')
        self.assertRegisters('"0', ['fizz\n', 'buzz\n'])
        self.assertRegistersEmpty('-1a')
        self.resetRegisters()
        self.eq('x|ab|x', 'v_"ay', 'n_x|abx')
        self.assertRegisters('"a', 'ab')
        self.assertRegistersEmpty('-01')
        self.resetRegisters()
        self.eq('x\nfi|zz\nbu|zz\ny', 'v_y', 'n_x\nfi|zz\nbuzz\ny')
        self.assertRegisters('"0', 'zz\nbu')
        self.assertRegistersEmpty('-1')
        self.resetRegisters()
        self.eq('x|ab|x', 'v_"by', 'n_x|abx')
        self.assertRegisters('"b', 'ab')
        self.assertRegistersEmpty('-01')
        self.resetRegisters()
        self.eq('x|cd|x', 'v_"2y', 'n_x|cdx')
        self.assertRegisters('"2', 'cd')
        self.assertRegistersEmpty('-0')
        self.assertClipboardEmpty()

    def test_v_Y(self):
        self.eq('x\nfizz |buzz\nfizz| buzz\nx', 'v_Y', 'n_x\nfizz buzz\nfiz|z buzz\nx')
        self.assertLinewiseRegisters('"0', 'fizz buzz\nfizz buzz\n')
        self.assertRegistersEmpty('-1')

    def test_s(self):
        self.eq('x|ab|x', 's_y', 'n_x|abx')
        self.assertRegisters('"0', 'ab')
        self.assertRegistersEmpty('-1')
        self.eq('|fizz| |buzz|', 's_y', 'n_|fizz |buzz')
        self.assertRegisters('"0', ['fizz', 'buzz'])

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
        self.eq('x fiz|z x', 'yiw', 'x |fizz x')
        self.assertRegisters('"0', 'fizz', '1-')
        self.eq('x    x', 'yiw', 'x    |x')

    def test_yaw(self):
        self.eq('x wo|rd x', 'yaw', 'x |word x')
        self.assertRegisters('"0', 'word ', '1-')
        self.eq('x fi|zz    x', 'yaw', 'x |fizz    x')
        self.assertRegisters('"0', 'fizz    ', '1-')

    @unittest.expectedFailure
    def test_yaw_issue_748_01(self):
        self.eq('x    fi|zz.x', 'yaw', 'x|    fizz.x')

    def test_y_into_readonly_registers(self):
        self.eq('x fi|zz x', '"xyiw', 'x |fizz x')
        self.assertRegisters('"x', 'fizz', '01-')
        self.eq('x bu|zz x', '"_yiw', 'x |buzz x')
        self.assertRegisters('"x', 'fizz', '01-')
        self.eq('x bu|zz x', '"%yiw', 'x |buzz x')
        self.assertRegisters('"x', 'fizz', '01-')
        self.eq('x bu|zz x', '"#yiw', 'x |buzz x')
        self.assertRegisters('"x', 'fizz', '01-')
        self.eq('x bu|zz x', '".yiw', 'x |buzz x')
        self.assertRegisters('"x', 'fizz', '01-')
        self.eq('x bu|zz x', '":yiw', 'x |buzz x')
        self.assertRegisters('"x', 'fizz', '01-')
        self.eq('b|uz|z', 'v_"_y', 'n_b|uzz')
        self.assertRegisters('"x', 'fizz', '01-')
        self.assertClipboardEmpty()

    def test_y_into_clipboard(self):
        self.eq('f|iz|z', 'v_"*y', 'n_f|izz')
        self.assertRegisters('"', 'iz', '01-')
        self.assertClipboard('iz')
        self.eq('b|uz|z', 'v_"+y', 'n_b|uzz')
        self.assertRegisters('"', 'uz', '01-')
        self.assertClipboard('uz')
        self.set_setting('use_sys_clipboard', True)
        self.eq('f|iz|z', 'v_"xy', 'n_f|izz')
        self.assertRegisters('"x', 'iz', '01-')
        self.assertClipboard('iz')
        self.set_setting('use_sys_clipboard', False)
        self.eq('b|ab|z', 'v_"xy', 'n_b|abz')
        self.assertRegisters('"x', 'ab', '01-')
        self.assertClipboard('iz')

    def test_yk(self):
        self.eq('fiz\nbuz\n|bish\nbosh\n', 'yk', 'fiz\n|buz\nbish\nbosh\n')
        self.assertLinewiseRegisters('"0', 'buz\nbish\n', '1-')
        self.eq('fiz\nbuz\nbish\n|bosh\n', '2yk', 'fiz\n|buz\nbish\nbosh\n')
        self.assertLinewiseRegisters('"0', 'buz\nbish\nbosh\n', '1-')

    def test_yj(self):
        self.eq('fiz\n|buz\nbish\nbosh\n', 'yj', 'fiz\n|buz\nbish\nbosh\n')
        self.assertLinewiseRegisters('"0', 'buz\nbish\n', '1-')
        self.eq('fiz\n|buz\nbish\nbosh\n', '2yj', 'fiz\n|buz\nbish\nbosh\n')
        self.assertLinewiseRegisters('"0', 'buz\nbish\nbosh\n', '1-')
        self.eq('|fiz\nbuz\nbish\nbosh\n', '3yj', '|fiz\nbuz\nbish\nbosh\n')
        self.assertLinewiseRegisters('"0', 'fiz\nbuz\nbish\nbosh\n', '1-')

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
        self.assertLinewiseRegister('"two\n')
        self.assertLinewiseRegister('0two\n')
        self.eq('o|ne', 'yy', 'o|ne')
        self.assertLinewiseRegister('"one\n')
        self.assertLinewiseRegister('0one\n')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')
        self.resetRegisters()
        self.eq('one\nt|wo\nthree', '"byy', 'one\nt|wo\nthree')
        self.assertLinewiseRegisters('"b', 'two\n')
        self.assertRegistersEmpty('-01')
        self.eq('two\nthr|ee\nfour', '"Byy', 'two\nthr|ee\nfour')
        self.assertLinewiseRegisters('"b', 'two\nthree\n')
        self.resetRegisters()
        self.eq('one\nt|wo\nthree', '"2yy', 'one\nt|wo\nthree')
        self.assertLinewiseRegisters('"2', 'two\n')
        self.assertRegistersEmpty('-01')
        self.assertClipboardEmpty()

    def test_yy_with_count(self):
        self.eq('x\n|1\n2\n3\nx\n', '3yy', 'x\n|1\n2\n3\nx\n')
        self.assertLinewiseRegister('"1\n2\n3\n')
        self.assertLinewiseRegister('01\n2\n3\n')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_yy_empty_line(self):
        self.eq('\n\n|\n\n', 'yy', '\n\n|\n\n')
        self.assertLinewiseRegister('"\n')
        self.assertLinewiseRegister('0\n')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_V(self):
        self.eq('x\n|abc\n|y', 'V_y', 'n_x\n|abc\ny')
        self.assertLinewiseRegister('"abc\n')
        self.assertLinewiseRegister('0abc\n')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')
        self.eq('a\n|fizz\n|b\n|buzz\n|c', 'V_y', 'n_a\n|fizz\nb\n|buzz\nc')
        self.assertLinewiseRegisters('"0', ['fizz\n', 'buzz\n'])
        self.assertRegistersEmpty('-1')

    def test_visual_block_cursor_should_move_to_beggining_of_selection(self):
        # Forward/down visual block.
        self.eq('fi|zz bu|zz\nfizz buzz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('fi|zz bu|zz\nfi|zz bu|zz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('fi|zz bu|zz\nfi|zz bu|zz\nfi|zz bu|zz\n', 'b_y', 'n_fi|zz buzz\nfizz buzz\nfizz buzz\n')

        # Reverse/down visual block.
        self.eq('r_fi|zz bu|zz\nfizz buzz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('r_fi|zz bu|zz\nfi|zz bu|zz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('r_fi|zz bu|zz\nfi|zz bu|zz\nfi|zz bu|zz\n', 'b_y', 'n_fi|zz buzz\nfizz buzz\nfizz buzz\n')

        # Foward/up visual block
        self.eq('u_fi|zz bu|zz\nfizz buzz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('u_fi|zz bu|zz\nfi|zz bu|zz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('u_fi|zz bu|zz\nfi|zz bu|zz\nfi|zz bu|zz\n', 'b_y', 'n_fi|zz buzz\nfizz buzz\nfizz buzz\n')

        # Reverse/up visual block
        self.eq('r_u_fi|zz bu|zz\nfizz buzz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('r_u_fi|zz bu|zz\nfi|zz bu|zz', 'b_y', 'n_fi|zz buzz\nfizz buzz')
        self.eq('r_u_fi|zz bu|zz\nfi|zz bu|zz\nfi|zz bu|zz\n', 'b_y', 'n_fi|zz buzz\nfizz buzz\nfizz buzz\n')

    def test_issue_739_nested_braces(self):
        self.eq(' { nested |{    targets    } } ', 'yi{', ' { nested {    |targets    } } ')
        self.resetRegisters()
        self.eq(' { nested |{    targets    } } ', 'ya{', ' { nested |{    targets    } } ')
