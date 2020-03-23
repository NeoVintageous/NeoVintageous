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

from NeoVintageous.nv.vi.text_objects import get_closest_tag


class Test_get_closest_tag(unittest.ViewTestCase):

    def test_get_closest_tag(self):
        self.normal('ab')
        self.assertEqual(None, get_closest_tag(self.view, 0))
        self.assertEqual(None, get_closest_tag(self.view, 1))
        self.assertEqual(None, get_closest_tag(self.view, 2))

        self.normal('<p>x<i>ab</i></p>')
        self.assertEqual(self.Region(0, 3), get_closest_tag(self.view, 0))
        self.assertEqual(self.Region(0, 3), get_closest_tag(self.view, 1))
        self.assertEqual(self.Region(0, 3), get_closest_tag(self.view, 2))
        self.assertEqual(self.Region(0, 3), get_closest_tag(self.view, 3))
        self.assertEqual(self.Region(4, 7), get_closest_tag(self.view, 4))
        self.assertEqual(self.Region(4, 7), get_closest_tag(self.view, 5))
        self.assertEqual(self.Region(4, 7), get_closest_tag(self.view, 6))
        self.assertEqual(self.Region(4, 7), get_closest_tag(self.view, 7))
        self.assertEqual(self.Region(4, 7), get_closest_tag(self.view, 8))
        self.assertEqual(self.Region(9, 13), get_closest_tag(self.view, 9))
