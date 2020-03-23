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

from NeoVintageous.nv.vi.search import reverse_search_by_pt


class Test_reverse_search_by_pt(unittest.ViewTestCase):

    def test_found_literal_returns_region(self):
        self.write('abc')
        self.assertEqual(self.Region(0, 1), reverse_search_by_pt(self.view, 'a', start=0, end=3, flags=LITERAL))
        self.assertEqual(self.Region(1, 2), reverse_search_by_pt(self.view, 'b', start=0, end=3, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search_by_pt(self.view, 'c', start=0, end=3, flags=LITERAL))

    def test_literal_multiline(self):
        self.write('abc\ndef\nhij\ndef\nnop')
        self.assertEqual(reverse_search_by_pt(self.view, 'a', 0, self.view.size(), LITERAL), self.Region(0, 1))
        self.assertEqual(reverse_search_by_pt(self.view, 'b', 0, self.view.size(), LITERAL), self.Region(1, 2))
        self.assertEqual(reverse_search_by_pt(self.view, 'd', 0, self.view.size(), LITERAL), self.Region(12, 13))
        self.assertEqual(reverse_search_by_pt(self.view, 'd', 0, 11, LITERAL), self.Region(4, 5))
        self.assertEqual(reverse_search_by_pt(self.view, 'a', 1, self.view.size(), LITERAL), None)

    def test_literal_not_found_returns_none(self):
        self.write('abc')
        self.assertEqual(None, reverse_search_by_pt(self.view, 'x', start=0, end=3, flags=LITERAL))

    def test_literal_not_found_in_whitespace_returns_none(self):
        self.write(' ')
        self.assertEqual(None, reverse_search_by_pt(self.view, 'x', start=0, end=1, flags=LITERAL))

    def test_literal_start_position_is_characterwise(self):
        self.write('aaaxxx')
        self.assertEqual(self.Region(2, 3), reverse_search_by_pt(self.view, 'a', start=0, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search_by_pt(self.view, 'a', start=1, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search_by_pt(self.view, 'a', start=2, end=6, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=3, end=6, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=4, end=6, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=5, end=6, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=6, end=6, flags=LITERAL))

    def test_literal_end_position_is_characterwise(self):
        self.write('xxxaaa')
        self.assertEqual(self.Region(5, 6), reverse_search_by_pt(self.view, 'a', start=0, end=6, flags=LITERAL))
        self.assertEqual(self.Region(4, 5), reverse_search_by_pt(self.view, 'a', start=0, end=5, flags=LITERAL))
        self.assertEqual(self.Region(3, 4), reverse_search_by_pt(self.view, 'a', start=0, end=4, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=0, end=3, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=0, end=2, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=0, end=1, flags=LITERAL))
        self.assertEqual(None, reverse_search_by_pt(self.view, 'a', start=0, end=0, flags=LITERAL))

    def test_out_of_bounds(self):
        self.normal('ab|c def')
        self.assertEqual(reverse_search_by_pt(self.view, 'a', -4, self.view.size()), None)
        self.assertEqual(reverse_search_by_pt(self.view, 'a', 5, self.view.size() + 1), None)
