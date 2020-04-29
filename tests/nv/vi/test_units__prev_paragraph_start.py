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

from NeoVintageous.nv.vi.units import prev_paragraph_start


class Test_prev_paragraph_start(unittest.ViewTestCase):

    def test_prev_paragraph_start_empty(self):
        self.normal('')
        self.assertEqual(0, prev_paragraph_start(self.view, 0))

    def test_prev_paragraph_start(self):
        self.normal('12\n45\n\n89\n12\n\n5\n7|8\n01\n\n45')
        self.assertEqual(13, prev_paragraph_start(self.view, 17))
        self.assertEqual(6, prev_paragraph_start(self.view, 13))
        self.assertEqual(0, prev_paragraph_start(self.view, 6))
        self.assertEqual(0, prev_paragraph_start(self.view, 0))

    def test_prev_paragraph_start_empty_lines(self):
        self.normal('1\n\n\n\n6\n8\n0\n\n\n\n567\n')
        self.assertEqual(13, prev_paragraph_start(self.view, 15))
        self.assertEqual(4, prev_paragraph_start(self.view, 13))
        self.assertEqual(0, prev_paragraph_start(self.view, 4))

    def test_prev_paragraph_start_count(self):
        self.normal('1\n\n4\n\n7\n\n0\n\n3\n')
        self.assertEqual(5, prev_paragraph_start(self.view, 14, count=3))
        self.assertEqual(0, prev_paragraph_start(self.view, 5, count=3))
