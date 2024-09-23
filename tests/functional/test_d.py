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
from NeoVintageous.tests.text_object_targets import all_one_line_targets


class Test_d(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_dB(self):
        self.eq('fizz bu.,!;|zz', 'dB', 'fizz |zz')
        self.assertRegisters('"-', 'bu.,!;')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dB_noop(self):
        self.eq('|', 'dB', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_de(self):
        self.eq('one t|wo three', 'de', 'one t| three')
        self.assertRegisters('"-', 'wo')
        self.assertRegistersEmpty('01')
        self.eq('x\n|\nbuzz\nfizz', 'de', 'x\n|fizz')

    @unittest.mock_bell()
    def test_de_noop(self):
        self.eq('|', 'de', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dE(self):
        self.eq('one t|wo three', 'dE', 'one t| three')
        self.assertRegisters('"-', 'wo')
        self.assertRegistersEmpty('01')

    def test_df(self):
        self.eq('|a = 1', 'df=', '| 1')
        self.assertRegisters('"-', 'a =')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_df_noop(self):
        self.eq('0|x2345', 'dfx', '0|x2345')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dF(self):
        self.eq('0x23|a5', 'dFx', '0|a5')
        self.assertRegisters('"-', 'x23')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dF_noop(self):
        self.eq('0123|x5', 'dFx', '0123|x5')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dt(self):
        self.eq('0|a23x5', 'dtx', '0|x5')
        self.assertRegisters('"-', 'a23')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dt_noop(self):
        self.eq('0|x2345', 'dtx', '0|x2345')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dT(self):
        self.eq('0x23|a5', 'dTx', '0x|a5')
        self.assertRegisters('"-', '23')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dT_noop(self):
        self.eq('012x|a5', 'dTx', '012x|a5')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_dw(self):
        self.eq('one t|wo three', 'dw', 'one t|three')
        self.assertRegisters('"-', 'wo ')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_dw_noop(self):
        self.eq('|', 'dw', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_diw(self):
        self.eq('a fi|zz.b', 'diw', 'a |.b')
        self.eq('a .|..b', 'diw', 'a |b')

    @unittest.expectedFailure
    def test_diw_issue_748_01(self):
        self.eq('a fi|zz b', 'diw', 'a | b')

    @unittest.expectedFailure
    def test_diw_issue_748_02(self):
        self.eq('a fi|zz    b', 'diw', 'a |    b')

    def test_daw(self):
        self.eq('a fi|zz b', 'daw', 'a |b')
        self.eq('a fi|zz    b', 'daw', 'a |b')
        self.eq('a fi|zz.b', 'daw', 'a|.b')
        self.eq('a    fi|zz.b', 'daw', 'a|.b')
        self.eq('\n\n|\n\n\n', 'daw', '\n\n|\n\n')

    def test_d__dollar(self):
        self.eq('one t|wo three', 'd$', 'one |t')
        self.assertRegisters('"-', 'wo three')
        self.assertRegistersEmpty('01')

    @unittest.mock_bell()
    def test_d__dollar_noop(self):
        self.eq('|', 'd$', '|')
        self.assertRegistersEmpty('"-01')
        self.assertBell()

    def test_d_underscore(self):
        self.eq('| 12\n 56', 'd_', ' |56')
        self.assertRegisters('"1', ' 12\n')
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
        self.assertLinewiseRegister('"two\n')
        self.assertLinewiseRegister('1two\n')
        self.assertLinewiseRegister('2two\n')
        self.assertLinewiseRegister('3one two three\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_dd_puts_cursor_on_first_non_blank(self):
        self.eq('one\n|two\n    three', 'dd', 'one\n    |three')

    def test_dd_last_line(self):
        self.eq('1\n2\n|3', 'dd', '1\n|2')
        self.eq('1\n2\n3\n|', 'dd', '1\n2\n|3')
        self.eq('1\n2\n|3\n', 'dd', '1\n2\n|')

    def test_di__one_line_targets(self):
        for t in all_one_line_targets:
            self.eq('{0}|{0}'.format(t), 'di' + t, '{0}|{0}'.format(t))
            self.eq('x{0}fi|zz{0}x'.format(t), 'di' + t, 'x{0}|{0}x'.format(t))
            self.assertRegister('"fizz')
            self.assertRegister('-fizz')
            self.assertRegisterEmpty('0')
            self.assertRegisterEmpty('1')

    def test_da__quote__or__slash__or__underscore(self):
        for t in all_one_line_targets:
            self.eq('{0}|{0}'.format(t), 'da' + t, '|')
            self.eq('x{0}fi|zz{0}y'.format(t), 'da' + t, 'x|y')
            self.assertRegister('"{0}fizz{0}'.format(t))
            self.assertRegister('-{0}fizz{0}'.format(t))
            self.assertRegisterEmpty('0')
            self.assertRegisterEmpty('1')

    def test_v(self):
        self.eq('x\nfi|zz bu|zz\ny', 'v_d', 'n_x\nfi|zz\ny')

    def test_s(self):
        self.eq('x\nfi|zz bu|zz\ny', 's_d', 'n_x\nfi|zz\ny')
        self.eq('f|iz|z\nf|iz|z\nf|iz|z\nfizz', 's_d', 'n_f|z\nf|z\nf|z\nfizz')

    def test_V_d_visual_line_sets_linewise_register(self):
        self.eq('x\n|abc\n|y', 'V_d', 'n_x\n|y')
        self.assertLinewiseRegister('"abc\n')
        self.assertLinewiseRegister('1abc\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_V_d_puts_cursors_on_first_non_blank(self):
        self.eq('    x\n|    a\n    b\n|    y\n', 'V_d', 'n_    x\n    |y\n')
        self.assertLinewiseRegister('"    a\n    b\n')
        self.assertLinewiseRegister('1    a\n    b\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_b(self):
        self.eq('fixyzzz\nbu|xyz|zz\nfi|xyz|zz\nbu|xyz|zz\nfixyzzz\n', 'b_d', 'n_fixyzzz\nbuzz\nfizz\nbu|zz\nfixyzzz\n')

    def test_dw_to_default_register(self):
        self.normal('f|izz buzz')
        self.feed('dw')
        self.assertNormal('f|buzz')
        self.assertRegister('"izz ')
        self.assertRegister('-izz ')

    def test_dw_to_register(self):
        self.normal('f|izz buzz')
        self.feed('"')
        self.feed('a')
        self.feed('dw')
        self.assertNormal('f|buzz')
        self.assertRegister('"izz ')
        self.assertRegister('aizz ')
        self.assertRegisterEmpty('-')

    def test_dw_with_motion_count(self):
        self.normal('1|11 222 333 444 555 666 777 888')
        self.feed('d')
        self.feed('2w')
        self.assertNormal('1|333 444 555 666 777 888')

    def test_dw_operator_count_and_motion_count_should_multiply(self):
        self.normal('1|11 222 333 444 555 666 777 888')
        self.feed('2d')
        self.feed('3w')
        self.assertNormal('1|777 888')
