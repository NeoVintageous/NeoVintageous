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


class Test_D(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('12|34', 'D', '1|2')
        self.eq('12|34\n', 'D', '1|2\n')
        self.eq('12|34\nx', 'D', '1|2\nx')
        self.assertRegisters('"-', '34', '01')

    def test_n_with_count(self):
        self.eq('111\n|222\n333\n444', '2D', '111\n|\n444')
        self.eq('111\n|222\n333\n444\n5\n6\n7\n8', '3D', '111\n|\n5\n6\n7\n8')
        self.eq('111\n|2\n3\n4\n55555', '9D', '111\n|')

    def test_v(self):
        self.eq('1|23|4', 'v_D', 'n_|')
        self.eq('x\n1|2\n34\n5|6\ny', 'v_D', 'n_x\n|y')
        self.eq('x\n12|34\n5|678\ny', 'v_D', 'n_x\n|y')
        self.assertLinewiseRegister('"1234\n5678\n')
        self.assertRegistersEmpty('-0')
        self.assertLinewiseRegister('11234\n5678\n')
        self.assertLinewiseRegister('212\n34\n56\n')
        self.assertLinewiseRegister('31234\n')
        self.eq('x\n1|2\n34\n5|6\n    y', 'v_D', 'n_x\n    |y')

    def test_D_to_default_register(self):
        self.normal('f|izz\n')
        self.feed('D')
        self.assertNormal('|f\n')
        self.assertRegister('"izz')
        self.assertRegister('-izz')

    def test_D_to_register(self):
        self.normal('f|izz\n')
        self.feed('"')
        self.feed('a')
        self.feed('D')
        self.assertNormal('|f\n')
        self.assertRegister('"izz')
        self.assertRegister('aizz')
        self.assertRegisterEmpty('-')
