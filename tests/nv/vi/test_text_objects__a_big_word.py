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

from NeoVintageous.nv.vi.text_objects import a_big_word


class Test_a_big_word(unittest.ViewTestCase):

    def test_returns_full_words(self):
        self.write('a baz bA.__ eol')
        self.assertRegion(a_big_word(self.view, 0), 'a')
        self.assertRegion(a_big_word(self.view, 1), ' baz')
        self.assertRegion(a_big_word(self.view, 2), 'baz')
        self.assertRegion(a_big_word(self.view, 3), 'baz')
        self.assertRegion(a_big_word(self.view, 4), 'baz')
        self.assertRegion(a_big_word(self.view, 5), ' bA.__')
        self.assertRegion(a_big_word(self.view, 6), 'bA.__')
        self.assertRegion(a_big_word(self.view, 7), 'bA.__')
        self.assertRegion(a_big_word(self.view, 8), 'bA.__')
        self.assertRegion(a_big_word(self.view, 9), 'bA.__')
        self.assertRegion(a_big_word(self.view, 10), 'bA.__')
        self.assertRegion(a_big_word(self.view, 11), ' eol')
        self.assertRegion(a_big_word(self.view, 12), 'eol')
        self.assertRegion(a_big_word(self.view, 13), 'eol')
        self.assertRegion(a_big_word(self.view, 14), 'eol')

    def test_should_not_error_when_cursor_starts_on_whitespace(self):
        self.write('a   b')
        self.assertRegion(a_big_word(self.view, 0), 'a')
        self.assertRegion(a_big_word(self.view, 1), '   b')
        self.assertRegion(a_big_word(self.view, 2), '   b')
        self.assertRegion(a_big_word(self.view, 3), '   b')
        self.assertRegion(a_big_word(self.view, 4), 'b')
