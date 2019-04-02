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


class Test_minus(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('1\n2\n|3', 'n_-', '1\n|2\n3')
        self.eq('1\n    fizz\n|3', 'n_-', '1\n    |fizz\n3')
        self.eq('1\n2\n3\n4\n5\n|6\n7', 'n_4-', '1\n|2\n3\n4\n5\n6\n7')

    def test_v(self):
        self.eq('1\n    fizz\n3\n4\n5\nf|izz bu|zz\n7', 'v_4-', 'r_1\n    |fizz\n3\n4\n5\nfi|zz buzz\n7')
