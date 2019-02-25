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

    def test_v_sort(self):
        self.eq('9\n|7\n3\n5|\n1', ":'<,'>sort", 'n_9\n|3\n5\n7\n1')
        self.eq('9\n|7\n    3\n5|\n1', ":'<,'>sort", 'n_9\n    |3\n5\n7\n1')
