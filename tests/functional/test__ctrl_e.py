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


class Test_ctrl_e(unittest.FunctionalTestCase):

    def test_v(self):
        self.eq('1\nfi|zz\nbu|zz\n3\n4', 'v_<C-e>', '1\nfi|zz\nbu|zz\n3\n4')

    def test_V(self):
        self.eq('1\n|fizz\nbuzz\n|3\n4', 'V_<C-e>', '1\n|fizz\nbuzz\n|3\n4')
