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

from collections import namedtuple

from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.units import next_big_word_start
from NeoVintageous.nv.vi.units import big_word_starts


test_data = namedtuple('test_data', 'initial_text region expected msg')
region_data = namedtuple('region_data', 'regions')


TESTS_MOVE_FORWARD = (
    test_data(initial_text='  foo bar\n', region=(0, 0), expected=2, msg=''),
    test_data(initial_text='  (foo)\n', region=(0, 0), expected=2, msg=''),
    test_data(initial_text='  \n\n\n', region=(0, 0), expected=3, msg=''),
    test_data(initial_text='  \n  \n\n', region=(0, 0), expected=3, msg=''),
    test_data(initial_text='  \n', region=(0, 0), expected=3, msg=''),
    test_data(initial_text='   ', region=(0, 0), expected=3, msg=''),
    test_data(initial_text='   \nfoo\nbar', region=(0, 0), expected=4, msg=''),
    test_data(initial_text='   \n foo\nbar', region=(0, 0), expected=4, msg=''),
    test_data(initial_text='  a foo bar\n', region=(0, 0), expected=2, msg=''),
    test_data(initial_text='  \na\n\n', region=(0, 0), expected=3, msg=''),
    test_data(initial_text='  \n a\n\n', region=(0, 0), expected=3, msg=''),

    test_data(initial_text='(foo) bar\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo) (bar)\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)\n\n\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)\n  \n\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)', region=(0, 0), expected=5, msg=''),
    test_data(initial_text='(foo)\nbar\nbaz', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)\n bar\nbaz', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo) a bar\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)\na\n\n', region=(0, 0), expected=6, msg=''),
    test_data(initial_text='(foo)\n a\n\n', region=(0, 0), expected=6, msg=''),
)


class Test_big_word_all(unittest.ViewTestCase):

    def test_all(self):
        self.write('  foo bar\n')

        for (i, data) in enumerate(TESTS_MOVE_FORWARD):
            self.write(data.initial_text)
            r = self._R(*data.region)
            self.select(r)

            pt = next_big_word_start(self.view, r.b)
            self.assertEqual(pt, data.expected, 'failed at test index {0}'.format(i))


class Test_next_big_word_start_InNormalMode_FromWord(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('(foo) bar\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_punctuation_start(self):
        self.write('(foo) (bar)\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_empty_line(self):
        self.write('(foo)\n\n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_whitespace_line(self):
        self.write('(foo)\n  \n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_eof_with_newline(self):
        self.write('(foo)\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_eof(self):
        self.write('(foo)')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 5)

    def test_to_one_word_line(self):
        self.write('(foo)\nbar\nbaz')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('(foo)\n bar\nbaz')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_one_char_word(self):
        self.write('(foo) a bar\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_one_char_line(self):
        self.write('(foo)\na\n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('(foo)\n a\n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)


class Test_next_big_word_start_InNormalMode_FromPunctuationStart(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write(':foo\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 5)

    def test_to_punctuation_start(self):
        self.write(': (foo)\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_empty_line(self):
        self.write(':\n\n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_whitespace_line(self):
        self.write(':\n  \n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_eof_with_newline(self):
        self.write(':\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_eof(self):
        self.write(':')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_one_word_line(self):
        self.write(':\nbar\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write(':\n bar\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_one_char_word(self):
        self.write(':a bar\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 3)

    def test_to_one_char_line(self):
        self.write(':\na\n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write(':\n a\n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 2)


class Test_next_big_word_start_InNormalMode_FromEmptyLine(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('\nfoo\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_punctuation_start(self):
        self.write('\n (foo)\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_empty_line(self):
        self.write('\n\n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_whitespace_line(self):
        self.write('\n  \n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_eof_with_newline(self):
        self.write('\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_eof(self):
        self.write('')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 0)

    def test_to_one_word_line(self):
        self.write('\nbar\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_one_char_word(self):
        self.write('\na bar\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_one_char_line(self):
        self.write('\na\n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('\n a\n\n')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0), 1)


class Test_next_big_word_start_InNormalMode_FromPunctuation(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('::foo\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 6)

    def test_to_punctuation_start(self):
        self.write(':: (foo)\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_empty_line(self):
        self.write('::\n\n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_whitespace_line(self):
        self.write('::\n  \n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_eof_with_newline(self):
        self.write('::\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_eof(self):
        self.write('::')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 2)

    def test_to_one_word_line(self):
        self.write('::\nbar\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_one_char_word(self):
        self.write('::a bar\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 4)

    def test_to_one_char_line(self):
        self.write('::\na\n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('::\n a\n\n')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1), 3)


class Test_next_big_word_start_InInternalNormalMode_FromWhitespace(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('  \n  ')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('  \n foo')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 2)


class Test_next_big_word_start_InInternalNormalMode_FromWordStart(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 3)


class Test_next_big_word_start_InInternalNormalMode_FromWord(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('(foo)\n  ')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1, internal=True), 5)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('(foo)\n bar')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1, internal=True), 5)


class Test_next_big_word_start_InInternalNormalMode_FromPunctuationStart(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('.\n  ')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('.\n bar')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 1)


class Test_next_big_word_start_InInternalNormalMode_FromPunctuation(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('::\n  ')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1, internal=True), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar')
        self.select(1)

        self.assertEqual(next_big_word_start(self.view, 1, internal=True), 2)


class Test_next_big_word_start_InInternalNormalMode_FromEmptyLine(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('\n  ')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 0)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar')
        self.select(0)

        self.assertEqual(next_big_word_start(self.view, 0, internal=True), 0)


class Test_big_word_starts_InNormalMode(unittest.ViewTestCase):

    def test_move1(self):
        self.write('(foo) bar\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0), 6)

    def test_move2(self):
        self.write('(foo) bar fizz\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, count=2), 10)

    def test_move10(self):
        self.write(''.join(('(foo) bar\n',) * 5))
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, count=9), 46)


# We can assume the stuff tested for normal mode applies to internal normal mode, so we
# don't bother with that. Instead, we only test the differing behavior when advancing by
# word starts in internal normal.
class Test_big_word_starts_InInternalNormalMode_FromEmptyLine(unittest.ViewTestCase):

    def test_move1_to_line_with_leading_white_space(self):
        self.write('\n (bar)\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True), 1)

    def test_move1_to_whitespace_line(self):
        self.write('\n  \n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, count=1, internal=True), 1)

    def test_move2_to_one_word_line(self):
        self.write('\n(foo)\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)

    def test_move3_and_swallow_last_newline_char(self):
        self.write('\nfoo\n (bar)\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=3), 12)

    def test_move2_to_line_with_leading_white_space(self):
        self.write('\n(foo)\n  \n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)


# We can assume the stuff tested for normal mode applies to internal normal mode, so we
# don't bother with that. Instead, we only test the differing behavior when advancing by
# word starts in internal normal.
class Test_big_word_starts_InInternalNormalMode_FromOneWordLine(unittest.ViewTestCase):

    def test_move2_to_eol(self):
        self.write('foo\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=1), 3)

    def test_move2_to_line_with_leading_white_space_from_word_start(self):
        self.write('(foo)\n\nbar\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)

    def test_move2_to_empty_line_from_word(self):
        self.write('(foo)\n\nbar\n')
        self.select(1)

        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 6)

    def test_move2_to_one_word_line_from_word_start(self):
        self.write('(foo)\nbar\nccc\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 10)

    def test_move2_to_one_word_line_from_word(self):
        self.write('(foo)\nbar\nccc\n')
        self.select(1)

        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 9)

    def test_move2_to_whitespaceline(self):
        self.write('(foo)\n  \nccc\n')
        self.select(1)

        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 12)

    def test_move2_to_whitespaceline_followed_by_leading_whitespace_from_word(self):
        self.write('(foo)\n  \n ccc\n')
        self.select(1)

        self.assertEqual(big_word_starts(self.view, 1, internal=True, count=2), 13)

    def test_move2_to_whitespaceline_followed_by_leading_whitespace_from_word_start(self):
        self.write('(foo)\n  \n ccc\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 14)


class Test_big_word_starts_InInternalNormalMode_FromLine(unittest.ViewTestCase):

    def test_move2_to_eol(self):
        self.write('foo bar\n')
        self.select(0)

        self.assertEqual(big_word_starts(self.view, 0, internal=True, count=2), 7)
