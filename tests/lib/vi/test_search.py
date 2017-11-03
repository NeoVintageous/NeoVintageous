from sublime import LITERAL

from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.search import find_wrapping
from NeoVintageous.lib.vi.search import reverse_search
from NeoVintageous.lib.vi.search import reverse_search_by_pt


class TestFindWrapping(ViewTestCase):

    def test_can_wrap_around_buffer(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(15)
        self.assertEqual(self.Region(0, 3), find_wrapping(self.view, 'xxx', 15, self.view.size()))

    def test_fails_if_search_string_not_present(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(15)
        self.assertEqual(None, find_wrapping(self.view, 'yyy', 15, self.view.size()))

    def test_can_find_next_occurrence(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(4)
        self.assertEqual(self.Region(12, 15), find_wrapping(self.view, 'xxx', 4, self.view.size()))


class TestReverseSearchByPt(ViewTestCase):

    def test_found_literal_returns_region(self):
        self.write('abc')
        self.assertEqual(self.Region(0, 1), reverse_search_by_pt(self.view, 'a', start=0, end=3, flags=LITERAL))
        self.assertEqual(self.Region(1, 2), reverse_search_by_pt(self.view, 'b', start=0, end=3, flags=LITERAL))
        self.assertEqual(self.Region(2, 3), reverse_search_by_pt(self.view, 'c', start=0, end=3, flags=LITERAL))

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


class TestReverseSearch(ViewTestCase):

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
