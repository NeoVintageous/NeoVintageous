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


class TestSurround_S(unittest.FunctionalTestCase):

    def test_v_S(self):
        self.eq('|one| two three', 'v_S"', 'n_|"one" two three')
        self.eq('one |two| three', 'v_S"', 'n_one |"two" three')

    def test_v_S_multiple_selections(self):
        self.eq('x |hello| y |world| z', 'v_S"', 'n_x |"hello" y |"world" z')
