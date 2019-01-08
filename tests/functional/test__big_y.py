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


class Test_Y(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_Y(self):
        self.eq('one\nt|wo\nthree', 'Y', 'one\nt|wo\nthree')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('0two\n', linewise=True)
        self.eq('o|ne', 'Y', 'o|ne')
        self.assertRegister('"', 'one\n', linewise=True)
        self.assertRegister('0', 'one\n', linewise=True)
        self.assertRegisterIsNone('1')
        self.assertRegisterIsNone('-')
