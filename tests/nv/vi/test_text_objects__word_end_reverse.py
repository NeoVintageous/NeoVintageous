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

from NeoVintageous.nv.vi.text_objects import word_end_reverse


class Test_word_end_reverse(unittest.ViewTestCase):

    def test_go_to_bof_from_first_word(self):
        self.write('abc')
        self.assertEqual(0, word_end_reverse(self.view, 2, 1))

    def test_go_to_previous_word_end(self):
        self.write('abc abc abc')
        self.assertEqual(6, word_end_reverse(self.view, 8, 1))

    def test_go_to_previous_word_end_count_2(self):
        self.write('abc abc abc')
        self.assertEqual(2, word_end_reverse(self.view, 8, 2))

    def test_go_to_previous_word_end_over_white_space(self):
        self.write('abc\nabc\nabc')
        self.assertEqual(6, word_end_reverse(self.view, 8, 1))

    def test_stop_at_empty_line(self):
        self.write('abc\n\nabc')
        self.assertEqual(3, word_end_reverse(self.view, 5, 1))

    def test_stop_at_singl_char_word(self):
        self.write('abc a abc')
        self.assertEqual(4, word_end_reverse(self.view, 6, 1))

    def test_stop_at_isolated_punctuation_word(self):
        self.write('abc == abc')
        self.assertEqual(5, word_end_reverse(self.view, 7, 1))

    def test_stop_at_word_end_from_isolated_punctuation(self):
        self.write('abc =')
        self.assertEqual(2, word_end_reverse(self.view, 4, 1))

    def test_stop_at_previous_word_end_from_contiguous_punctuation(self):
        self.write('abc abc.abc')
        self.assertEqual(6, word_end_reverse(self.view, 7, 1))

    def test_skip_over_punctuatio_(self):
        self.write('abc abc.abc')
        self.assertEqual(2, word_end_reverse(self.view, 10, 1, True))

    def test_stop_at_previous_word_end_if_starting_from_contiguous_space(self):
        self.write('abc ')
        self.assertEqual(2, word_end_reverse(self.view, 3, 1))
