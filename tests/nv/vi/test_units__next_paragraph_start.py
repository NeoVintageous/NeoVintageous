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

from NeoVintageous.nv.vi.units import next_paragraph_start


class Test_next_paragraph_start(unittest.ViewTestCase):

    def test_next_paragraph_start_empty(self):
        self.normal('')
        self.assertEqual(0, next_paragraph_start(self.view, 0))

    def test_next_paragraph_start(self):
        self.normal('1\n\n4\n\n789\n\n2\n')
        self.assertEqual(2, next_paragraph_start(self.view, 0))
        self.assertEqual(5, next_paragraph_start(self.view, 2))
        self.assertEqual(10, next_paragraph_start(self.view, 5))
        self.assertEqual(13, next_paragraph_start(self.view, 10))
        self.assertEqual(13, next_paragraph_start(self.view, 13))

    def test_next_paragraph_start_count(self):
        self.normal('1\n\n4\n\n789\n\n2\n')
        self.assertEqual(10, next_paragraph_start(self.view, 0, count=3))
        self.assertEqual(13, next_paragraph_start(self.view, 10, count=3))

    def test_next_paragraph_start_empty_lines(self):
        self.normal('1\n\n\n\n6\n\n\n\n1\n')
        self.assertEqual(2, next_paragraph_start(self.view, 0))
        self.assertEqual(7, next_paragraph_start(self.view, 2))
        self.assertEqual(12, next_paragraph_start(self.view, 7))

    def test_next_paragraph_start_puts_cursor_on_eof_char(self):
        self.normal('1\nxxx')
        self.assertEqual(4, next_paragraph_start(self.view, 0))
        self.assertEqual(4, next_paragraph_start(self.view, 2))
        self.assertEqual(4, next_paragraph_start(self.view, 4))
