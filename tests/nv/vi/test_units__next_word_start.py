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

from NeoVintageous.nv.vi.units import next_word_start


class Test_next_word_start_InNormalMode_FromWhitespace(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('  foo bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_punctuation_start(self):
        self.write('  (foo)\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_empty_line(self):
        self.write('  \n\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)

    def test_to_whitespace_line(self):
        self.write('  \n  \n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)

    def test_to_eof_with_newline(self):
        self.write('  \n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)

    def test_to_eof(self):
        self.write('   ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)

    def test_to_one_word_line(self):
        self.write('   \nfoo\nbar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('   \n foo\nbar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_one_char_word(self):
        self.write('  a foo bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_one_char_line(self):
        self.write('  \na\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('  \n a\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)


class Test_next_word_start_InNormalMode_FromWordStart(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('foo bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_punctuation_start(self):
        self.write('foo (bar)\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_empty_line(self):
        self.write('foo\n\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_whitespace_line(self):
        self.write('foo\n  \n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_eof_with_newline(self):
        self.write('foo\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_eof(self):
        self.write('foo')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 3)

    def test_to_one_word_line(self):
        self.write('foo\nbar\nbaz')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar\nbaz')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_one_char_word(self):
        self.write('foo a bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_one_char_line(self):
        self.write('foo\na\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('foo\n a\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 4)


class Test_next_word_start_InNormalMode_FromWord(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('foo bar\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_punctuation_start(self):
        self.write('foo (bar)\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_empty_line(self):
        self.write('foo\n\n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_whitespace_line(self):
        self.write('foo\n  \n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_eof_with_newline(self):
        self.write('foo\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_eof(self):
        self.write('foo')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_one_word_line(self):
        self.write('foo\nbar\nbaz')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar\nbaz')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_one_char_word(self):
        self.write('foo a bar\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_one_char_line(self):
        self.write('foo\na\n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('foo\n a\n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 4)


class Test_next_word_start_InNormalMode_FromPunctuationStart(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write(':foo\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_punctuation_start(self):
        self.write(': (foo)\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_empty_line(self):
        self.write(':\n\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_whitespace_line(self):
        self.write(':\n  \n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_eof_with_newline(self):
        self.write(':\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_eof(self):
        self.write(':')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_one_word_line(self):
        self.write(':\nbar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write(':\n bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_one_char_word(self):
        self.write(':a bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_one_char_line(self):
        self.write(':\na\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write(':\n a\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 2)


class Test_next_word_start_InNormalMode_FromEmptyLine(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('\nfoo\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_punctuation_start(self):
        self.write('\n (foo)\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_empty_line(self):
        self.write('\n\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_whitespace_line(self):
        self.write('\n  \n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_eof_with_newline(self):
        self.write('\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_eof(self):
        self.write('')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 0)

    def test_to_one_word_line(self):
        self.write('\nbar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_one_char_word(self):
        self.write('\na bar\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_one_char_line(self):
        self.write('\na\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('\n a\n\n')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0), 1)


class Test_next_word_start_InNormalMode_FromPunctuation(unittest.ViewTestCase):

    def test_to_word_start(self):
        self.write('::foo\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 2)

    def test_to_punctuation_start(self):
        self.write(':: (foo)\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_empty_line(self):
        self.write('::\n\n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_whitespace_line(self):
        self.write('::\n  \n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_eof_with_newline(self):
        self.write('::\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_eof(self):
        self.write('::')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 2)

    def test_to_one_word_line(self):
        self.write('::\nbar\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_one_char_word(self):
        self.write('::a bar\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 2)

    def test_to_one_char_line(self):
        self.write('::\na\n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('::\n a\n\n')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1), 3)


class Test_next_word_start_InInternalNormalMode_FromWhitespace(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('  \n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('  \n foo')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 2)


class Test_next_word_start_InInternalNormalMode_FromWordStart(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 3)


class Test_next_word_start_InInternalNormalMode_FromWord(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 3)


class Test_next_word_start_InInternalNormalMode_FromPunctuationStart(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('.\n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('.\n bar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 1)


class Test_next_word_start_InInternalNormalMode_FromPunctuation(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('::\n  ')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 2)


class Test_next_word_start_InInternalNormalMode_FromEmptyLine(unittest.ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('\n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 2)
