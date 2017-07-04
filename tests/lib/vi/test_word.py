from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.units import next_word_start
from NeoVintageous.lib.vi.units import word_starts


class Test_next_word_start_InNormalMode_FromWhitespace(ViewTestCase):

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


class Test_next_word_start_InNormalMode_FromWordStart(ViewTestCase):

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


class Test_next_word_start_InNormalMode_FromWord(ViewTestCase):

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


class Test_next_word_start_InNormalMode_FromPunctuationStart(ViewTestCase):

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


class Test_next_word_start_InNormalMode_FromEmptyLine(ViewTestCase):

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


class Test_next_word_start_InNormalMode_FromPunctuation(ViewTestCase):

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


class Test_next_word_start_InInternalNormalMode_FromWhitespace(ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('  \n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('  \n foo')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 2)


class Test_next_word_start_InInternalNormalMode_FromWordStart(ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 3)


class Test_next_word_start_InInternalNormalMode_FromWord(ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 3)


class Test_next_word_start_InInternalNormalMode_FromPunctuationStart(ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('.\n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('.\n bar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 1)


class Test_next_word_start_InInternalNormalMode_FromPunctuation(ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('::\n  ')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar')
        self.select(1)

        self.assertEqual(next_word_start(self.view, 1, internal=True), 2)


class Test_next_word_start_InInternalNormalMode_FromEmptyLine(ViewTestCase):

    def test_to_whitespace_line(self):
        self.write('\n  ')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar')
        self.select(0)

        self.assertEqual(next_word_start(self.view, 0, internal=True), 2)


class Test_words_InNormalMode(ViewTestCase):

    def test_move1(self):
        self.write('foo bar\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0), 4)

    def test_move2(self):
        self.write('foo bar fizz\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, count=2), 8)

    def test_move10(self):
        self.write(''.join(('foo bar\n',) * 5))
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, count=9), 36)


# We can assume the stuff tested for normal mode applies to internal normal mode, so we
# don't bother with that. Instead, we only test the differing behavior when advancing by
# word starts in internal normal.
class Test_words_InInternalNormalMode_FromEmptyLine(ViewTestCase):

    def test_move1_to_line_with_leading_white_space(self):
        self.write('\n bar\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True), 1)

    def test_move1_to_whitespace_line(self):
        self.write('\n  \n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, count=1, internal=True), 1)

    def test_move2_to_one_word_line(self):
        self.write('\nfoo\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=2), 5)

    def test_move3_and_swallow_last_newline_char(self):
        self.write('\nfoo\n bar\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=3), 10)

    def test_move2_to_line_with_leading_white_space(self):
        self.write('\nfoo\n  \n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=2), 5)


# We can assume the stuff tested for normal mode applies to internal normal mode, so we
# don't bother with that. Instead, we only test the differing behavior when advancing by
# word starts in internal normal.
class Test_words_InInternalNormalMode_FromOneWordLine(ViewTestCase):

    def test_move1_to_eol(self):
        self.write('foo\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=1), 3)

    def test_move2_to_line_with_leading_white_space_from_word_start(self):
        self.write('foo\n\nbar\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=2), 5)

    def test_move2_to_empty_line_from_word(self):
        self.write('foo\n\nbar\n')
        self.select(1)

        self.assertEqual(word_starts(self.view, 1, internal=True, count=2), 4)

    def test_move2_to_one_word_line_from_word_start(self):
        self.write('foo\nbar\nccc\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=2), 8)

    def test_move2_to_one_word_line_from_word(self):
        self.write('foo\nbar\nccc\n')
        self.select(1)

        self.assertEqual(word_starts(self.view, 1, internal=True, count=2), 7)

    def test_move2_to_whitespaceline(self):
        self.write('foo\n  \nccc\n')
        self.select(1)

        self.assertEqual(word_starts(self.view, 1, internal=True, count=2), 10)

    def test_move2_to_whitespaceline_followed_by_leading_whitespace_from_word(self):
        self.write('foo\n  \n ccc\n')
        self.select(1)

        self.assertEqual(word_starts(self.view, 1, internal=True, count=2), 11)

    def test_move2_to_whitespaceline_followed_by_leading_whitespace_from_word_start(self):
        self.write('foo\n  \n ccc\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=2), 12)


class Test_words_InInternalNormalMode_FromOneCharLongWord(ViewTestCase):

    def test_move1_to_eol(self):
        self.write('x\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=1), 1)


class Test_words_InInternalNormalMode_FromLine(ViewTestCase):

    def test_move2_to_eol(self):
        self.write('foo bar\n')
        self.select(0)

        self.assertEqual(word_starts(self.view, 0, internal=True, count=2), 7)
