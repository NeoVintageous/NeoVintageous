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

from NeoVintageous.nv.vi.units import big_word_starts


class Test_big_word_starts_InNormalMode(unittest.ViewTestCase):

    def test_move(self):
        self.write('(foo) bar\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0), 6)

    def test_move2(self):
        self.write('(foo) bar fizz\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, count=2), 10)

    def test_move3(self):
        self.write(''.join(('(foo) bar\n',) * 5))
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, count=9), 46)


# We can assume the stuff tested for normal mode applies to internal normal mode, so we
# don't bother with that. Instead, we only test the differing behavior when advancing by
# word starts in internal normal.
class Test_big_word_starts_InInternalNormalMode_FromEmptyLine(unittest.ViewTestCase):

    def test_move_to_line_with_leading_white_space(self):
        self.write('\n (bar)\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True), 1)

    def test_move_to_line_with_leading_white_space2(self):
        self.write('\n(foo)\n  \n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)

    def test_move_to_whitespace_line(self):
        self.write('\n  \n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, count=1, internal=True), 1)

    def test_move_to_one_word_line(self):
        self.write('\n(foo)\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)

    def test_move_and_swallow_last_newline_char(self):
        self.write('\nfoo\n (bar)\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=3), 12)


# We can assume the stuff tested for normal mode applies to internal normal mode, so we
# don't bother with that. Instead, we only test the differing behavior when advancing by
# word starts in internal normal.
class Test_big_word_starts_InInternalNormalMode_FromOneWordLine(unittest.ViewTestCase):

    def test_move_to_eol(self):
        self.write('foo\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=1), 3)

    def test_move_to_line_with_leading_white_space_from_word_start(self):
        self.write('(foo)\n\nbar\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)

    def test_move_to_empty_line_from_word(self):
        self.write('(foo)\n\nbar\n')
        self.select(1)
        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 6)

    def test_move_to_one_word_line_from_word_start(self):
        self.write('(foo)\nbar\nccc\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 10)

    def test_move_to_one_word_line_from_word(self):
        self.write('(foo)\nbar\nccc\n')
        self.select(1)
        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 9)

    def test_move_to_whitespaceline(self):
        self.write('(foo)\n  \nccc\n')
        self.select(1)
        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 12)

    def test_move_to_whitespaceline_followed_by_leading_whitespace_from_word(self):
        self.write('(foo)\n  \n ccc\n')
        self.select(1)
        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 13)

    def test_move_to_whitespaceline_followed_by_leading_whitespace_from_word_start(self):
        self.write('(foo)\n  \n ccc\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 14)


class Test_big_word_starts_InInternalNormalMode_FromLine(unittest.ViewTestCase):

    def test_move_to_eol(self):
        self.write('foo bar\n')
        self.select(0)
        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)
