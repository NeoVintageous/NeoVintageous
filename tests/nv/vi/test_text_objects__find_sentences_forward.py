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

from NeoVintageous.nv.vi.text_objects import find_sentences_forward


class Test_find_sentences_forward(unittest.ViewTestCase):

    def test_find_sentences_forward_empty(self):
        self.normal('|')
        self.assertIsNone(find_sentences_forward(self.view, 0))

    def test_find_sentences_forward_empty_none(self):
        self.normal('|x y.')
        self.assertIsNone(find_sentences_forward(self.view, 0))
        self.assertIsNone(find_sentences_forward(self.view, 1))
        self.assertIsNone(find_sentences_forward(self.view, 2))
        self.assertIsNone(find_sentences_forward(self.view, 3))
        self.assertIsNone(find_sentences_forward(self.view, 4))

    def test_find_sentences_forward(self):
        for c in ('.', '?', '!'):
            self.normal('|x y{0} a b c{0}    x y'.format(c))
            self.assertEqual(find_sentences_forward(self.view, 0), self.Region(5))
            self.assertEqual(find_sentences_forward(self.view, 5), self.Region(15))
            self.assertIsNone(find_sentences_forward(self.view, 15))

    def test_find_sentences_forward_closing_characters(self):
        for c in ('.', '?', '!'):
            self.normal('|x y{0}) a b c{0}))]    x y{0}"\'])  x y'.format(c))
            self.assertEqual(find_sentences_forward(self.view, 0), self.Region(6))
            self.assertEqual(find_sentences_forward(self.view, 6), self.Region(19))
            self.assertEqual(find_sentences_forward(self.view, 19), self.Region(29))
            self.assertIsNone(find_sentences_forward(self.view, 29))

    def test_find_sentences_forward_count(self):
        for c in ('.', '?', '!'):
            self.normal('|x y{0} a b c{0}))]    x y{0}"\'])  x y.  a b c. xy.'.format(c))
            self.assertEqual(find_sentences_forward(self.view, 0, count=2), self.Region(18))
            self.assertEqual(find_sentences_forward(self.view, 0, count=3), self.Region(28))
            self.assertEqual(find_sentences_forward(self.view, 0, count=4), self.Region(34))
            self.assertEqual(find_sentences_forward(self.view, 0, count=5), self.Region(41))
            self.assertEqual(find_sentences_forward(self.view, 0, count=6), self.Region(41))
