import sublime

import unittest

from NeoVintageous.lib.ex.ex_location import get_line_nr
from NeoVintageous.lib.ex.ex_location import find_eol
from NeoVintageous.lib.ex.ex_location import find_bol
from NeoVintageous.lib.ex.ex_location import find_line
from NeoVintageous.lib.ex.ex_location import search_in_range
from NeoVintageous.lib.ex.ex_location import find_last_match
from NeoVintageous.lib.ex.ex_location import reverse_search


class TestHelpers(unittest.TestCase):
    @unittest.skip('todo: revise tests')
    def test_get_correct_line_number(self):
        self.assertEquals(get_line_nr(g_test_view, 1000), 19)

    @unittest.skip('todo: revise tests')
    def test_find_bol_and_eol(self):
        values = (
            (find_eol(g_test_view, 1000), 1062),
            (find_eol(g_test_view, 2000), 2052),
            (find_bol(g_test_view, 1000), 986),
            (find_bol(g_test_view, 2000), 1981),
        )

        for actual, expected in values:
            self.assertEquals(actual, expected)


class TestSearchHelpers(unittest.TestCase):
    @unittest.skip('todo: revise tests')
    def test_forward_search(self):
        values = (
            (find_line(g_test_view, target=30), sublime.Region(1668, 1679)),
            (find_line(g_test_view, target=1000), -1),
        )

        for actual, expected in values:
            self.assertEquals(actual, expected)

    @unittest.skip('todo: revise tests')
    def test_search_in_range(self):
        values = (
            (search_in_range(g_test_view, 'THIRTY', 1300, 1800), True),
            (search_in_range(g_test_view, 'THIRTY', 100, 100), None),
            (search_in_range(g_test_view, 'THIRTY', 100, 1000), None),
        )

        for actual, expected in values:
            self.assertEquals(actual, expected)

    @unittest.skip('todo: revise tests')
    def test_find_last_match(self):
        values = (
            (find_last_match(g_test_view, 'Lorem', 0, 1200), sublime.Region(913, 918)),
        )

        for actual, expected in values:
            self.assertEquals(actual, expected)

    @unittest.skip('todo: revise tests')
    def test_reverse_search(self):
        values = (
            (reverse_search(g_test_view, 'THIRTY'), 30),
        )

        for actual, expected in values:
            self.assertEquals(actual, expected)

    @unittest.skip('todo: revise tests')
    def test_reverse_search_non_matches_return_current_line(self):
        self.assertEquals(g_test_view.rowcol(g_test_view.sel()[0].a)[0], 0)
        values = (
            (reverse_search(g_test_view, 'FOOBAR'), 1),
        )

        select_line(g_test_view, 10)
        values += (
            (reverse_search(g_test_view, 'FOOBAR'), 10),
        )

        select_line(g_test_view, 100)
        values += (
            (reverse_search(g_test_view, 'FOOBAR'), 100),
        )

        for actual, expected in values:
            self.assertEquals(actual, expected)

    def setUp(self):
        super().setUp()
        select_line(g_test_view, 1)

    def tearDown(self):
        super().tearDown()
        select_line(g_test_view, 1)
