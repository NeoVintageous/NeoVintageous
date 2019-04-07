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


class Test_d(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_dB(self):
        self.eq('fizz bu.,!;|zz', 'dB', 'fizz |zz')
        self.assertRegistersEqual('"-', 'bu.,!;')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dB_noop(self):
        self.eq('|', 'dB', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_de(self):
        self.eq('one t|wo three', 'de', 'one t| three')
        self.assertRegistersEqual('"-', 'wo')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_de_noop(self):
        self.eq('|', 'de', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_df(self):
        self.eq('|a = 1', 'df=', '| 1')
        self.assertRegistersEqual('"-', 'a =')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_df_noop(self):
        self.eq('0|x2345', 'dfx', '0|x2345')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dF(self):
        self.eq('0x23|a5', 'dFx', '0|a5')
        self.assertRegistersEqual('"-', 'x23')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dF_noop(self):
        self.eq('0123|x5', 'dFx', '0123|x5')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dt(self):
        self.eq('0|a23x5', 'dtx', '0|x5')
        self.assertRegistersEqual('"-', 'a23')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dt_noop(self):
        self.eq('0|x2345', 'dtx', '0|x2345')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dT(self):
        self.eq('0x23|a5', 'dTx', 'r_0x|a5')
        self.assertRegistersEqual('"-', '23')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dT_noop(self):
        self.eq('012x|a5', 'dTx', '012x|a5')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dw(self):
        self.eq('one t|wo three', 'dw', 'one t|three')
        self.assertRegistersEqual('"-', 'wo ')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dw_noop(self):
        self.eq('|', 'dw', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_d__dollar(self):
        self.eq('one t|wo three', 'd$', 'one |t')
        self.assertRegistersEqual('"-', 'wo three')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_d__dollar_noop(self):
        self.eq('|', 'd$', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_d_underscore(self):
        self.eq('| 12\n 56', 'd_', ' |56')
        self.assertRegistersEqual('"1', ' 12\n')
        self.assertRegistersEmpty('-0')

    @unittest.mock_bell()
    def test_d_underscore_noop(self):
        self.eq('|', 'd_', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dd(self):
        self.eq('one |two three', 'dd', '|')
        self.eq('one\n|two\nthree', 'dd', 'one\n|three')
        self.eq('one\ntwo|\nthree', 'dd', 'one\n|three')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('1two\n', linewise=True)
        self.assertRegister('2two\n', linewise=True)
        self.assertRegister('3one two three\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_dd_puts_cursor_on_first_non_blank(self):
        self.eq('one\n|two\n    three', 'dd', 'one\n    |three')

    def test_dd_last_line(self):
        self.eq('1\n2\n|3', 'dd', '1\n|2')
        self.eq('1\n2\n3\n|', 'dd', '1\n2\n|3')
        self.eq('1\n2\n|3\n', 'dd', '1\n2\n|')

    def test_d_visual_line_sets_linewise_register(self):
        self.eq('x\n|abc\n|y', 'l_d', 'n_x\n|y')
        self.assertRegister('"abc\n', linewise=True)
        self.assertRegister('1abc\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_l_d_puts_cursors_on_first_non_blank(self):
        self.eq('    x\n|    a\n    b\n|    y\n', 'l_d', 'n_    x\n    |y\n')
        self.assertRegister('"    a\n    b\n', linewise=True)
        self.assertRegister('1    a\n    b\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
