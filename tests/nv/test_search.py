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

from NeoVintageous.nv.search import process_search_pattern
from NeoVintageous.nv.search import process_word_search_pattern


class Test_flags(unittest.ViewTestCase):

    def test_process_search_pattern(self):
        self.set_option('ignorecase', False)
        self.set_option('magic', True)
        self.assertEqual(('[0-9]', 0), process_search_pattern(self.view, '[0-9]'))
        self.set_option('ignorecase', False)
        self.set_option('magic', False)
        self.assertEqual(('[0-9]', 1), process_search_pattern(self.view, '[0-9]'))
        self.set_option('ignorecase', True)
        self.set_option('magic', True)
        self.assertEqual(('[0-9]', 2), process_search_pattern(self.view, '[0-9]'))
        self.set_option('ignorecase', True)
        self.set_option('magic', False)
        self.assertEqual(('[0-9]', 3), process_search_pattern(self.view, '[0-9]'))

    def test_process_search_pattern_non_regex_in_magic_mode(self):
        self.set_option('ignorecase', False)
        self.set_option('magic', True)
        self.assertEqual(('[0-9]', 0), process_search_pattern(self.view, '[0-9]'))
        literals = ('[', ']', '(', ')', '\'[', '"[')
        for literal in literals:
            self.assertEqual((literal, 1), process_search_pattern(self.view, literal))

        regex = ('[0-9]+', '.+', '^', '.*', 'x?', '(x|y)')
        for literal in regex:
            self.assertEqual((literal, 0), process_search_pattern(self.view, literal))

    def test_process_search_pattern_with_modes(self):
        self.set_option('ignorecase', False)
        for boolean in (True, False):
            self.set_option('magic', boolean)  # Inline modes should override magic option.
            self.assertEqual(('[0-9]', 0), process_search_pattern(self.view, '\\v[0-9]'))
            self.assertEqual(('[0-9]', 1), process_search_pattern(self.view, '\\V[0-9]'))
            self.assertEqual(('[0-9]', 0), process_search_pattern(self.view, '\\m[0-9]'))
            self.assertEqual(('[0-9]', 1), process_search_pattern(self.view, '\\M[0-9]'))

    def test_calculate_word_search_flags(self):
        self.set_option('magic', True)
        self.set_option('ignorecase', False)
        self.assertEqual(('\\bfizz\\b', 0), process_word_search_pattern(self.view, 'fizz'))
        self.set_option('magic', False)
        self.set_option('ignorecase', False)
        self.assertEqual(('\\bfizz\\b', 0), process_word_search_pattern(self.view, 'fizz'))
        self.set_option('magic', True)
        self.set_option('ignorecase', True)
        self.assertEqual(('\\bfizz\\b', 2), process_word_search_pattern(self.view, 'fizz'))
        self.set_option('magic', False)
        self.set_option('ignorecase', True)
        self.assertEqual(('\\bfizz\\b', 2), process_word_search_pattern(self.view, 'fizz'))
