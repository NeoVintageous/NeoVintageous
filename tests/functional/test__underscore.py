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


class Test__(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('| 123\n 678', 'n_2_', ' 123\n |678')
        self.eq(' 1|23\n 678', 'n_2_', ' 123\n |678')
        self.eq('| 123\n 678', 'n_2_', ' 123\n |678')
        self.eq('  2|a4', 'n__', '  |2a4')
        self.eq(' | 234', 'n_2_', '  |234')

    def test_v(self):
        self.eq('| 12|3\n 678', 'v_2_', '| 123\n 6|78')
        self.eq('r_| 12|3\n 678', 'v_2_', ' 1|23\n 6|78')
        self.eq('| 12|3\n 678', 'v_2_', '| 123\n 6|78')
        self.eq('r_  2|ba|5', 'v__', 'r_  |2ba|5')
        self.eq('  2|ab|5', 'v__', 'r_  |2a|b5')
        self.eq('r_|  |2345', 'v__', ' | 2|345')
        self.eq('|  |2345', 'v__', '|  2|345')
        self.eq(' | 23b|5', 'v__', ' | 2|3b5')
        self.eq('r_ | 23a|5', 'v__', 'r_  |23a|5')
        self.eq('| 123\n| 678', 'v__', '| 1|23\n 678')
        self.eq('r_ 123|\n 67|8', 'v__', 'r_ |123\n 67|8')
        self.eq(' 1|23\n 67|8', 'v__', ' 1|23\n 6|78')
        self.eq('r_ 1|23\n 67|8', 'v__', 'r_ |123\n 67|8')
        self.eq('|f|', 'v__', '|f|')
        self.eq('r_|r|', 'v__', '|r|')

    def test_d(self):
        self.eq('| 12\n 56', 'd_', ' |56')
        self.eq(' 1|2\n 56', 'd_', ' |56')
        self.eq(' 12\n 5|6', 'd_', ' 12\n|')
        self.eq(' 1|23\n 678\n bcd', '2d_', ' |bcd')
        self.eq(' 123\n 6|78\n bcd', '3d_', ' 123\n|')
