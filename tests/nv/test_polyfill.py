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

from NeoVintageous.nv.polyfill import view_find
from NeoVintageous.nv.polyfill import view_find_in_range


class TestViewFind(unittest.ViewTestCase):

    def test_match(self):
        self.normal('|fizz buzz')
        self.assertRegion(view_find(self.view, 'f', 0), (0, 1))
        self.assertRegion(view_find(self.view, 'z', 0), (2, 3))
        self.assertRegion(view_find(self.view, 'z', 5), (7, 8))
        self.assertRegion(view_find(self.view, '\\s', 0), (4, 5))

    def test_no_match(self):
        self.normal('|fizz buzz')
        self.assertIsNone(view_find(self.view, 'x', 0))
        self.assertIsNone(view_find(self.view, 'f', 1))

    def test_zero_length_match(self):
        self.normal('|fizz buzz\nfizz')
        self.assertRegion(view_find(self.view, '^', 0), (0, 0))
        self.assertRegion(view_find(self.view, '^', 1), (10, 10))


class TestViewFindInRange(unittest.ViewTestCase):

    def test_match(self):
        self.normal('|fizz buzz')
        self.assertRegion(view_find_in_range(self.view, 'i', 1, 6), (1, 2))
        self.assertRegion(view_find_in_range(self.view, 'z', 1, 6), (2, 3))
        self.assertRegion(view_find_in_range(self.view, 'b', 1, 6), (5, 6))

    def test_no_match(self):
        self.normal('|fizz buzz')
        self.assertIsNone(view_find_in_range(self.view, 'x', 0, 9))
        self.assertIsNone(view_find_in_range(self.view, 'u', 1, 6))
