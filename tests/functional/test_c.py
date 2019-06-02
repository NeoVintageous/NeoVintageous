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


class Test_c(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('vintageous_use_sys_clipboard', False)

    def test_c0(self):
        self.eq('1\nfi|zz\n2', 'c0', 'i_1\n|zz\n2')
        self.assertRegistersEqual('"-', 'fi')
        self.assertRegistersEmpty('01')

    def test_ce(self):
        self.eq('one |two three', 'ce', 'i_one | three')
        self.eq('one t|wo three', 'ce', 'i_one t| three')
        self.assertRegister('"wo')
        self.assertRegister('-wo')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_v(self):
        self.eq('fi|zz bu|zz', 'v_c', 'i_fi|zz')
        self.eq('r_fi|zz bu|zz', 'v_c', 'i_fi|zz')
        self.eq('r_fi|   |zz', 'v_c', 'i_fi|zz')

    def test_s(self):
        self.eq('fi|zz bu|zz', 's_c', 'i_fi|zz')

    def test_cb(self):
        self.eq('x fizz|buzz x', 'cb', 'i_x |buzz x')
        self.assertRegister('"fizz')
        self.assertRegister('-fizz')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_cw(self):
        self.eq('one |two three', 'cw', 'i_one | three')
        self.eq('one t|wo three', 'cw', 'i_one t| three')
        self.assertRegister('"wo')
        self.assertRegister('-wo')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')
        self.eq('one t|wo\nthree four', '2cw', 'i_one t| four')
        self.eq('one |two\nthree four', '2cw', 'i_one | four')
        self.eq('one |two\nthree\nfour', '2cw', 'i_one |\nfour')

    def test_caw(self):
        self.eq('a fi|zz b', 'caw', 'i_a | b')
        self.eq('1\na fi|zz b\n3', 'caw', 'i_1\na | b\n3')
        self.eq('one t|wo\nthree four', '2caw', 'i_one | four')
        self.eq('one t|wo\nthree\nfour', '2caw', 'i_one|\nfour')
        self.eq('one |two\nthree\nfour', '2caw', 'i_one|\nfour')
        self.eq('one |two\nthree\nfour', '2caw', 'i_one|\nfour')
        self.eq('one |two\nthree four', '2caw', 'i_one | four')

    def test_c__dollar(self):
        self.eq('one |two three', 'c$', 'i_one |')
        self.eq('one t|wo three', 'c$', 'i_one t|')
        self.assertRegister('"wo three')
        self.assertRegister('-wo three')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_cc(self):
        self.eq('\n\n|\n\n', 'cc', 'i_\n\n|\n\n')
        self.eq('|aaa\nbbb\nccc', 'cc', 'i_|\nbbb\nccc')
        self.eq('aaa\nbb|b\nccc', 'cc', 'i_aaa\n|\nccc')
        self.eq('aaa\nbbb\n|ccc', 'cc', 'i_aaa\nbbb\n|')
        self.assertRegister('"ccc\n', linewise=True)
        self.assertRegister('1ccc\n', linewise=True)
        self.assertRegister('2bbb\n', linewise=True)
        self.assertRegister('3aaa\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_cc_should_not_strip_preceding_whitespace(self):
        self.eq('    |one', 'cc', 'i_    |')
        self.eq('one\n  tw|o\nthree\n', 'cc', 'i_one\n  |\nthree\n')

    def test_cc_last_line(self):
        self.eq('1\ntw|o', 'cc', 'i_1\n|')
        self.eq('1\ntw|o\n', 'cc', 'i_1\n|\n')

    def test_ci__quote(self):
        self.eq('"|"', 'ci"', 'i_"|"')
        self.eq('"1|23"', 'ci"', 'i_"|"')
        self.assertRegister('"123')
        self.assertRegister('-123')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_ci__quote_multi_sel(self):
        self.eq('x"1|23"y\ni"ab|c"j\n', 'ci"', 'i_x"|"y\ni"|"j\n')
        self.assertRegister('"', ['123', 'abc'])
        self.assertRegister('-', ['123', 'abc'])
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_ci__quote__empty_should_not_fill_registers(self):
        self.eq('"|"', 'ci"', 'i_"|"')
        self.assertRegisterEmpty('"')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_ci__quote__multi_sels_empty_should_not_fill_registers(self):
        self.eq('"|"\n"|"', 'ci"', 'i_"|"\n"|"')
        self.assertRegisterEmpty('"')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_c_visual_line_sets_linewise_register(self):
        self.eq('x\n|abc\n|y', 'V_c', 'i_x\n|y')
        self.assertRegister('"abc\n', linewise=True)
        self.assertRegister('1abc\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_c_(self):
        self.eq('1\nfi|zz\n2\n3', 'c_', 'i_1\n|\n2\n3')
        self.eq('1\n    fi|zz\n2\n3', 'c_', 'i_1\n|\n2\n3')
