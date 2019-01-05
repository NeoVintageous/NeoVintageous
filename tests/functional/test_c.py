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


class Test_c(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_ce(self):
        self.eq('one |two three', 'ce', 'i_one | three')
        self.eq('one t|wo three', 'ce', 'i_one t| three')
        self.assertRegister('"', 'wo')
        self.assertRegister('-', 'wo')
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_cw(self):
        self.eq('one |two three', 'cw', 'i_one | three')
        self.eq('one t|wo three', 'cw', 'i_one t| three')
        self.assertRegister('"', 'wo')
        self.assertRegister('-', 'wo')
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_c__dollar(self):
        self.eq('one |two three', 'c$', 'i_one |')
        self.eq('one t|wo three', 'c$', 'i_one t|')
        self.assertRegister('"', 'wo three')
        self.assertRegister('-', 'wo three')
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_cc(self):
        self.eq('|aaa\nbbb\nccc', 'cc', 'i_|\nbbb\nccc')
        self.eq('aaa\nbb|b\nccc', 'cc', 'i_aaa\n|\nccc')
        self.eq('aaa\nbbb\n|ccc', 'cc', 'i_aaa\nbbb\n|')
        self.assertRegister('"', 'ccc\n')
        self.assertRegister('-', None)
        self.assertRegister('0', None)
        self.assertRegister('1', 'ccc\n')
        self.assertRegister('2', 'bbb\n')
        self.assertRegister('3', 'aaa\n')

    def test_cc_should_not_strip_preceding_whitespace(self):
        self.eq('    |one', 'cc', 'i_    |')
        self.eq('one\n  tw|o\nthree\n', 'cc', 'i_one\n  |\nthree\n')

    def test_cc_last_line(self):
        self.eq('1\ntw|o', 'cc', 'i_1\n|')
        self.eq('1\ntw|o\n', 'cc', 'i_1\n|\n')

    def test_ci__quote(self):
        self.eq('"1|23"', 'ci"', 'i_"|"')
        self.assertRegister('"', '123')
        self.assertRegister('-', '123')
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_ci__quote_multi_sel(self):
        self.eq('x"1|23"y\ni"ab|c"j\n', 'ci"', 'i_x"|"y\ni"|"j\n')
        self.assertRegister('"', ['123', 'abc'])
        self.assertRegister('-', ['123', 'abc'])
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_ci__quote__empty_should_not_fill_registers(self):
        self.eq('"|"', 'ci"', 'i_"|"')
        self.assertRegister('"', None)
        self.assertRegister('-', None)
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_ci__quote__multi_sels_empty_should_not_fill_registers(self):
        self.eq('"|"\n"|"', 'ci"', 'i_"|"\n"|"')
        self.assertRegister('"', None)
        self.assertRegister('-', None)
        self.assertRegister('0', None)
        self.assertRegister('1', None)
