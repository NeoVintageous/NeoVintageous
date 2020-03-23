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

from NeoVintageous.nv.vi.text_objects import is_at_punctuation


class test_is_at_punctuation(unittest.ViewTestCase):

    def test_is_at_punctuation(self):
        self.write('a bc .,: d\nx\ty')
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
        self.assertTrue(is_at_punctuation(self.view, 5))
        self.assertTrue(is_at_punctuation(self.view, 6))
        self.assertTrue(is_at_punctuation(self.view, 7))
        self.assertFalse(is_at_punctuation(self.view, 8))
        self.assertFalse(is_at_punctuation(self.view, 9))
        self.assertFalse(is_at_punctuation(self.view, 10))
        self.assertFalse(is_at_punctuation(self.view, 11))
        self.assertFalse(is_at_punctuation(self.view, 12))
        self.assertFalse(is_at_punctuation(self.view, 13))
        self.assertFalse(is_at_punctuation(self.view, 14))
        self.assertFalse(is_at_punctuation(self.view, 15))
        self.assertFalse(is_at_punctuation(self.view, 16))

    def test_is_at_punctuation_newline_issue_a(self):
        self.write('a\nb\\nc')
        self.assertSize(6)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertTrue(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
        self.assertFalse(is_at_punctuation(self.view, 5))
        self.assertFalse(is_at_punctuation(self.view, 6))

    def test_is_at_punctuation_tab_char_issue_a(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.write('a\tb')
        self.assertContent('a   b')
        self.assertSize(5)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
        self.assertFalse(is_at_punctuation(self.view, 5))

    def test_is_at_punctuation_tab_char_issue_b(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', False)
        self.write('a\tb')
        self.assertContent('a\tb')
        self.assertSize(3)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertFalse(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))

    def test_is_at_punctuation_tab_char_issue_c(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', False)
        self.write('a\\tb')
        self.assertContent('a\\tb')
        self.assertSize(4)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertTrue(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))

    def test_is_at_punctuation_tab_char_issue_d(self):
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.write('a\\tb')
        self.assertContent('a\\tb')
        self.assertSize(4)
        self.assertFalse(is_at_punctuation(self.view, 0))
        self.assertTrue(is_at_punctuation(self.view, 1))
        self.assertFalse(is_at_punctuation(self.view, 2))
        self.assertFalse(is_at_punctuation(self.view, 3))
        self.assertFalse(is_at_punctuation(self.view, 4))
