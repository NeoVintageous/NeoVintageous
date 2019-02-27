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


class Test_ex_sort(unittest.FunctionalTestCase):

    def test_sort(self):
        self.eq('d\nb\n|c\na', ':sort', 'a\nb\n|c\nd')

    def test_sort_options(self):
        self.eq('1\n1\n2\n|3\n2\n4', ':sort u', '1\n|2\n3\n4')
        self.eq('|a\nA\nB\nb', ':sort i', '|a\nA\nB\nb')
        self.eq('|b\nA\na\nB', ':sort i', '|A\na\nb\nB')
        self.eq('|b\na\nA\nB', ':sort i', '|a\nA\nb\nB')
        self.eq('|1\nb\n1\nb\na\nA\na\nB', ':sort iu', '|1\na\nA\nb\nB')

    def test_v_sort(self):
        self.eq('9\n|7\n3\n5|\n1', ":'<,'>sort", 'n_9\n|3\n5\n7\n1')
        self.eq('9\n|7\n    3\n5|\n1', ":'<,'>sort", 'n_9\n    |3\n5\n7\n1')
        self.eq('6\n7\n|1\nb\n1\nb\na\nA\na\nB|\n2\n3', ":'<,'>sort iu", 'n_6\n7\n|1\na\nA\nb\nB\n2\n3')
