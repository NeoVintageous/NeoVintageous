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

    def test_D(self):
        self.eq('12|34', 'D', '1|2')
        self.eq('12|34\n', 'D', '1|2\n')
        self.eq('12|34\nx', 'D', '1|2\nx')

    def test_v_D(self):
        self.eq('1|23|4', 'v_D', 'n_|')
        self.eq('x\n1|2\n34\n5|6\ny', 'v_D', 'n_x\n|y')
        self.eq('x\n12|34\n5|678\ny', 'v_D', 'n_x\n|y')

    def test_v_D_should_put_cursor_on_first_no_ws_char(self):
        self.eq('x\n1|2\n34\n5|6\n    y', 'v_D', 'n_x\n    |y')
