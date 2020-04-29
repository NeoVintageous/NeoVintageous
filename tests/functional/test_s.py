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


class Test_s(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('enable_sneak', False)

    def test_n(self):
        self.eq('|', 's', 'i_|')
        self.eq('a|bc', 's', 'i_a|c')
        self.eq('a|bc\n', 's', 'i_a|c\n')
        self.eq('a|bcde\nf\n', '3s', 'i_a|e\nf\n')
        self.assertRegister('"bcd')
        self.assertRegister('-bcd')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_n_should_not_delete_past_the_eol(self):
        self.eq('a|bc\n456789', '5s', 'i_a|\n456789')

    def test_v(self):
        self.eq('a|bc|d', 'v_s', 'i_a|d')
        self.assertRegister('"bc')
        self.assertRegister('-bc')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_v_multiline(self):
        self.eq('ab|12\n34|cd', 'v_s', 'i_ab|cd')
        self.eq('ab|12\n34\n56|cd\n', 'v_s', 'i_ab|cd\n')
        self.assertRegister('"12\n34\n56')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertRegister('112\n34\n56')
        self.assertRegister('212\n34')

    def test_l(self):
        self.eq('x\n|ab\n|y', 'V_s', 'i_x\n|\ny')
        self.eq('x\n|ab\ncd\n|y\n', 'V_s', 'i_x\n|\ny\n')
        self.assertLinewiseRegister('"ab\ncd\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertLinewiseRegister('1ab\ncd\n')
        self.assertLinewiseRegister('2ab\n')

    def test_V_empty_lines(self):
        self.eq('\n|\n\n|\n', 'V_s', 'i_\n|\n\n')
        self.assertLinewiseRegister('"\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertLinewiseRegister('1\n')

    def test_s(self):
        self.eq('a|fizz|b', 's_s', 'i_a|b')
