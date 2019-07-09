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

from NeoVintageous.nv.search import calculate_buffer_search_flags
from NeoVintageous.nv.search import calculate_word_search_flags


class Test_flags(unittest.ViewTestCase):

    def test_calculate_buffer_search_flags(self):
        self.set_option('ignorecase', False)
        self.set_option('magic', True)
        self.assertEqual(0, calculate_buffer_search_flags(self.view, '[0-9]'))
        self.set_option('ignorecase', False)
        self.set_option('magic', False)
        self.assertEqual(1, calculate_buffer_search_flags(self.view, '[0-9]'))
        self.set_option('ignorecase', True)
        self.set_option('magic', True)
        self.assertEqual(2, calculate_buffer_search_flags(self.view, '[0-9]'))
        self.set_option('ignorecase', True)
        self.set_option('magic', False)
        self.assertEqual(3, calculate_buffer_search_flags(self.view, '[0-9]'))

    def test_calculate_buffer_search_flags_in_magic_mode(self):
        self.set_option('ignorecase', False)
        self.set_option('magic', True)
        self.assertEqual(0, calculate_buffer_search_flags(self.view, '[0-9]'))
        literals = ('[', ']', '(', ')', '\'[', '"[')
        for literal in literals:
            self.assertEqual(1, calculate_buffer_search_flags(self.view, literal))

        regex = ('[0-9]+', '.+', '^', '.*', 'x?', '(x|y)')
        for literal in regex:
            self.assertEqual(0, calculate_buffer_search_flags(self.view, literal))

    def test_calculate_word_search_flags(self):
        self.set_option('magic', True)
        self.set_option('ignorecase', False)
        self.assertEqual(0, calculate_word_search_flags(self.view, 'fizz'))
        self.set_option('magic', False)
        self.set_option('ignorecase', False)
        self.assertEqual(0, calculate_word_search_flags(self.view, 'fizz'))
        self.set_option('magic', True)
        self.set_option('ignorecase', True)
        self.assertEqual(2, calculate_word_search_flags(self.view, 'fizz'))
        self.set_option('magic', False)
        self.set_option('ignorecase', True)
        self.assertEqual(2, calculate_word_search_flags(self.view, 'fizz'))
