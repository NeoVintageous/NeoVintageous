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
from NeoVintageous.nv.vi.search import find_wrapping
from NeoVintageous.nv.vi.search import reverse_find_wrapping
from NeoVintageous.nv.vi.search import reverse_search
from NeoVintageous.nv.vi.search import reverse_search_by_pt


class TestFindWrapping(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_can_wrap_around_buffer(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(15)
        self.assertEqual(self.Region(0, 3), find_wrapping(self.view, 'xxx', 15, self.view.size()))

    def test_fails_if_search_not_present(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(15)
        self.assertEqual(None, find_wrapping(self.view, 'yyy', 15, self.view.size()))

    def test_can_find_next_occurrence(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(4)
        self.assertEqual(self.Region(12, 15), find_wrapping(self.view, 'xxx', 4, self.view.size()))


class TestReverseFindWrapping(unittest.ViewTestCase):

    def test_reverse_find_wrapping(self):
        self.normal('fizz buzz | one two three')
        self.assertIsNone(reverse_find_wrapping(self.view, 'foo', 3, self.view.size()))
        self.assertIsNone(reverse_find_wrapping(self.view, 'foo', 15, self.view.size()))
        self.assertEqual(reverse_find_wrapping(self.view, 'buzz', 10, self.view.size()), self.Region(5, 9))
        self.assertEqual(reverse_find_wrapping(self.view, 'zz', 10, self.view.size()), self.Region(7, 9))


class TestReverseSearchByPt(unittest.ViewTestCase):

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


class TestReverseSearch(unittest.ViewTestCase):

    def test_found_literal_returns_region(self):
        self.write('abc')
        self.assertEqual(self.Region(0, 1), reverse_search(self.view, 'a', start=0, end=3, flags=LITERAL))
        self.assertEqual(self.Region(1, 2), reverse_search(self.view, 'b', start=0, end=3, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'c', start=0, end=3, flags=LITERAL))

    def test_literal_not_found_returns_none(self):
        self.write('abc')
        self.assertEqual(None, reverse_search(self.view, 'x', start=0, end=3, flags=LITERAL))

    def test_literal_not_found_in_whitespace_returns_none(self):
        self.write(' ')
        self.assertEqual(None, reverse_search(self.view, 'x', start=0, end=1, flags=LITERAL))

    def test_literal_start_position_is_linewise(self):
        self.write('aaaxxx')
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=0, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=1, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=2, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=3, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=4, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=5, end=6, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=6, end=6, flags=LITERAL))

    def test_literal_start_position_is_linewise_2(self):
        self.write('aaa\nxxx')
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=0, end=7, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=1, end=7, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=2, end=7, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search(self.view, 'a', start=3, end=7, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=4, end=7, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=5, end=7, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=6, end=7, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=7, end=7, flags=LITERAL))

    def test_literal_end_position_is_linewise(self):
        self.write('xxxaaa')
        self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=6, flags=LITERAL))
        self.assertEqual(self.Region(4, 5), reverse_search(self.view, 'a', start=0, end=5, flags=LITERAL))
        self.assertEqual(self.Region(3, 4), reverse_search(self.view, 'a', start=0, end=4, flags=LITERAL))

        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=3, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=2, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=1, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=0, flags=LITERAL))

        # XXX The current implementation of reverse_search() end position is not
        # technically not linewise. The start position *is* linewise. I don't
        # know if this is causing bugs or if internals depends on this
        # functionality, so "fixing it" and making it a true linewise search may
        # break things in unexpected ways. It needs reviewing. The way it should
        # probably work is to make the following tests pass:

        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=6, flags=LITERAL))
        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=5, flags=LITERAL))
        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=4, flags=LITERAL))
        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=3, flags=LITERAL))
        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=2, flags=LITERAL))
        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=1, flags=LITERAL))
        # self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=0, flags=LITERAL))

    def test_literal_end_position_is_linewise_2(self):
        self.write('xxx\naaa')
        self.assertEqual(self.Region(6, 7), reverse_search(self.view, 'a', start=0, end=7, flags=LITERAL))
        self.assertEqual(self.Region(5, 6), reverse_search(self.view, 'a', start=0, end=6, flags=LITERAL))
        self.assertEqual(self.Region(4, 5), reverse_search(self.view, 'a', start=0, end=5, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=4, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=3, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=2, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=1, flags=LITERAL))
        self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=0, flags=LITERAL))

        # XXX The current implementation of reverse_search() end position is not
        # technically not linewise. The start position *is* linewise. I don't
        # know if this is causing bugs or if internals depends on this
        # functionality, so "fixing it" and making it a true linewise search may
        # break things in unexpected ways. It needs reviewing. The way it should
        # probably work is to make the following tests pass:

        # self.assertEqual(self.Region(6, 7), reverse_search(self.view, 'a', start=0, end=7, flags=LITERAL))
        # self.assertEqual(self.Region(6, 7), reverse_search(self.view, 'a', start=0, end=6, flags=LITERAL))
        # self.assertEqual(self.Region(6, 7), reverse_search(self.view, 'a', start=0, end=5, flags=LITERAL))
        # self.assertEqual(self.Region(6, 7), reverse_search(self.view, 'a', start=0, end=4, flags=LITERAL))
        # self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=3, flags=LITERAL))
        # self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=2, flags=LITERAL))
        # self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=1, flags=LITERAL))
        # self.assertEqual(None, reverse_search(self.view, 'a', start=0, end=0, flags=LITERAL))

    def test_out_of_bounds(self):
        self.normal('ab|c def')
        self.assertEqual(reverse_search(self.view, 'a', -4, self.view.size()), None)
        self.assertEqual(reverse_search(self.view, 'a', 5, self.view.size() + 1), None)


class TestFindAllInRange(unittest.ViewTestCase):

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
