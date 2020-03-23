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

from NeoVintageous.nv.vi.search import reverse_find_wrapping


class Test_reverse_find_wrapping(unittest.ViewTestCase):

    def test_reverse_find_wrapping(self):
        self.normal('fizz buzz | one two three')
        self.assertIsNone(reverse_find_wrapping(self.view, 'foo', 3, self.view.size()))
        self.assertIsNone(reverse_find_wrapping(self.view, 'foo', 15, self.view.size()))
        self.assertEqual(reverse_find_wrapping(self.view, 'buzz', 10, self.view.size()), self.Region(5, 9))
        self.assertEqual(reverse_find_wrapping(self.view, 'zz', 10, self.view.size()), self.Region(7, 9))
