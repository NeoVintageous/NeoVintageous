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


class Test_D(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_D(self):
        self.eq('12|34', 'D', '1|2')
        self.eq('12|34\n', 'D', '1|2\n')
        self.eq('12|34\nx', 'D', '1|2\nx')
        self.assertRegister('"34')
        self.assertRegister('-34')
        self.assertRegisterIsNone('0')
        self.assertRegisterIsNone('1')

    def test_v_D(self):
        self.eq('1|23|4', 'v_D', 'n_|')
        self.eq('x\n1|2\n34\n5|6\ny', 'v_D', 'n_x\n|y')
        self.eq('x\n12|34\n5|678\ny', 'v_D', 'n_x\n|y')
        self.assertRegister('"1234\n5678\n', linewise=True)
        self.assertRegisterIsNone('-')
        self.assertRegisterIsNone('0')
        self.assertRegister('11234\n5678\n', linewise=True)
        self.assertRegister('212\n34\n56\n', linewise=True)
        self.assertRegister('31234\n', linewise=True)

    def test_v_D_should_put_cursor_on_first_no_ws_char(self):
        self.eq('x\n1|2\n34\n5|6\n    y', 'v_D', 'n_x\n    |y')
