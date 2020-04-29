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

from sublime import LITERAL

from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.search import find_all_in_range


class Test_find_all_in_range(unittest.ViewTestCase):

    def test_find_one(self):
        self.write('abc')
        self.assertEqual(find_all_in_range(self.view, 'a', 0, self.view.size(), LITERAL), [self.Region(0, 1)])
        self.assertEqual(find_all_in_range(self.view, 'b', 0, self.view.size(), LITERAL), [self.Region(1, 2)])
        self.assertEqual(find_all_in_range(self.view, 'c', 0, self.view.size(), LITERAL), [self.Region(2, 3)])
        self.assertEqual(find_all_in_range(self.view, 'x', 0, self.view.size(), LITERAL), [])
        self.assertEqual(find_all_in_range(self.view, 'a', 1, self.view.size(), LITERAL), [])
        self.assertEqual(find_all_in_range(self.view, 'b', 1, self.view.size(), LITERAL), [self.Region(1, 2)])
        self.assertEqual(find_all_in_range(self.view, 'b', 2, self.view.size(), LITERAL), [])
        self.assertEqual(find_all_in_range(self.view, 'c', 2, self.view.size(), LITERAL), [self.Region(2, 3)])

    def test_find_many(self):
        self.write('abc abc abc')
        self.assertEqual(find_all_in_range(self.view, 'x', 0, self.view.size()), [])
        self.assertEqual(find_all_in_range(self.view, 'a', 0, self.view.size()), [
            self.Region(0, 1),
            self.Region(4, 5),
            self.Region(8, 9)
        ])
        self.assertEqual(find_all_in_range(self.view, 'c', 0, self.view.size()), [
            self.Region(2, 3),
            self.Region(6, 7),
            self.Region(10, 11)
        ])
        self.assertEqual(find_all_in_range(self.view, 'b', 0, 7), [
            self.Region(1, 2),
            self.Region(5, 6)
        ])
