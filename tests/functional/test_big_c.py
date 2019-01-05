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


class Test_C(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_C(self):
        self.eq('one\n|two\nthree', 'C', 'i_one\n|\nthree')
        self.eq('one\nt|wo\nthree', 'C', 'i_one\nt|\nthree')
        self.assertRegister('"', 'wo')
        self.assertRegister('-', 'wo')
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_C_multiple_selections(self):
        self.eq('x\n|1\n|2\n|3\nx\n|4\nx', 'C', 'i_x\n|\n|\n|\nx\n|\nx')
        self.assertRegister('"', ['1', '2', '3', '4'])
        self.assertRegister('-', ['1', '2', '3', '4'])
        self.assertRegister('0', None)
        self.assertRegister('1', None)

    def test_C_multiple_selections_empty_lines(self):
        self.eq('x\n|1\n|\n|3\nx\n|\nx', 'C', 'i_x\n|\n|\n|\nx\n|\nx')
