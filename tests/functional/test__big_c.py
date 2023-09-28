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


class Test_C(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)

    def test_C(self):
        self.eq('one\n|two\nthree', 'C', 'i_one\n|\nthree')
        self.eq('one\nt|wo\nthree', 'C', 'i_one\nt|\nthree')
        self.assertRegister('"wo')
        self.assertRegister('-wo')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_C_with_count(self):
        self.eq('x\nfi|zz\nbuzz\ny', '2C', 'i_x\nfi|\ny')
        self.eq('x\nfi|zz\nbuzz\nfizz\nbuzz\ny', '3C', 'i_x\nfi|\nbuzz\ny')
        self.eq('x\nfi|zz\nbuzz\n1\n2', '9C', 'i_x\nfi|')

    def test_C_multiple_selections(self):
        self.eq('x\n|1\n|2\n|3\nx\n|4\nx', 'C', 'i_x\n|\n|\n|\nx\n|\nx')
        self.assertRegister('"', ['1', '2', '3', '4'])
        self.assertRegister('-', ['1', '2', '3', '4'])
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_C_multiple_selections_empty_lines(self):
        self.eq('x\n|1\n|\n|3\nx\n|\nx', 'C', 'i_x\n|\n|\n|\nx\n|\nx')

    def test_v_C(self):
        self.eq('one\n|two\n|three', 'v_C', 'i_one\n|three')
        self.assertLinewiseRegister('"two\n')
        self.assertLinewiseRegister('1two\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_V(self):
        self.eq('one\n|two\n|three', 'V_C', 'i_one\n|three')
        self.assertLinewiseRegister('"two\n')
        self.assertLinewiseRegister('1two\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_C_to_default_register(self):
        self.normal('f|izz\n')
        self.feed('C')
        self.assertInsert('f|\n')
        self.assertRegister('"izz')
        self.assertRegister('-izz')

    def test_C_to_register(self):
        self.normal('f|izz\n')
        self.feed('"')
        self.feed('a')
        self.feed('C')
        self.assertInsert('f|\n')
        self.assertRegister('"izz')
        self.assertRegister('aizz')
        self.assertRegisterEmpty('-')
