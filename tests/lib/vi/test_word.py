from NeoVintageous.lib.vi.units import next_word_start
from NeoVintageous.lib.vi.units import word_starts

from NeoVintageous.tests.utils import ViewTestCase


class Test_next_word_start_InNormalMode_FromWhitespace(ViewTestCase):
    def test_to_word_start(self):
        self.write('  foo bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_punctuation_start(self):
        self.write('  (foo)\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_empty_line(self):
        self.write('  \n\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_whitespace_line(self):
        self.write('  \n  \n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_eof_with_newline(self):
        self.write('  \n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_eof(self):
        self.write('   ')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_word_line(self):
        self.write('   \nfoo\nbar')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('   \n foo\nbar')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_word(self):
        self.write('  a foo bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_one_char_line(self):
        self.write('  \na\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('  \n a\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)


class Test_next_word_start_InNormalMode_FromWordStart(ViewTestCase):
    def test_to_word_start(self):
        self.write('foo bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_punctuation_start(self):
        self.write('foo (bar)\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_empty_line(self):
        self.write('foo\n\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_whitespace_line(self):
        self.write('foo\n  \n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_eof_with_newline(self):
        self.write('foo\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_eof(self):
        self.write('foo')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_word_line(self):
        self.write('foo\nbar\nbaz')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar\nbaz')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_word(self):
        self.write('foo a bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_line(self):
        self.write('foo\na\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('foo\n a\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)


class Test_next_word_start_InNormalMode_FromWord(ViewTestCase):
    def test_to_word_start(self):
        self.write('foo bar\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_punctuation_start(self):
        self.write('foo (bar)\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_empty_line(self):
        self.write('foo\n\n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_whitespace_line(self):
        self.write('foo\n  \n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_eof_with_newline(self):
        self.write('foo\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_eof(self):
        self.write('foo')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_word_line(self):
        self.write('foo\nbar\nbaz')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar\nbaz')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_word(self):
        self.write('foo a bar\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_line(self):
        self.write('foo\na\n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('foo\n a\n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 4)


class Test_next_word_start_InNormalMode_FromPunctuationStart(ViewTestCase):
    def test_to_word_start(self):
        self.write(':foo\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_punctuation_start(self):
        self.write(': (foo)\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_empty_line(self):
        self.write(':\n\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_whitespace_line(self):
        self.write(':\n  \n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_eof_with_newline(self):
        self.write(':\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_eof(self):
        self.write(':')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_one_word_line(self):
        self.write(':\nbar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write(':\n bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_one_char_word(self):
        self.write(':a bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_one_char_line(self):
        self.write(':\na\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write(':\n a\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)


class Test_next_word_start_InNormalMode_FromEmptyLine(ViewTestCase):
    def test_to_word_start(self):
        self.write('\nfoo\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_punctuation_start(self):
        self.write('\n (foo)\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_empty_line(self):
        self.write('\n\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_whitespace_line(self):
        self.write('\n  \n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_eof_with_newline(self):
        self.write('\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_eof(self):
        self.write('')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 0)

    def test_to_one_word_line(self):
        self.write('\nbar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_one_char_word(self):
        self.write('\na bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_one_char_line(self):
        self.write('\na\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('\n a\n\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 1)


class Test_next_word_start_InNormalMode_FromPunctuation(ViewTestCase):
    def test_to_word_start(self):
        self.write('::foo\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_punctuation_start(self):
        self.write(':: (foo)\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_empty_line(self):
        self.write('::\n\n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_whitespace_line(self):
        self.write('::\n  \n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_eof_with_newline(self):
        self.write('::\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_eof(self):
        self.write('::')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_one_word_line(self):
        self.write('::\nbar\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_char_word(self):
        self.write('::a bar\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 2)

    def test_to_one_char_line(self):
        self.write('::\na\n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)

    def test_to_one_char_line_with_leading_whitespace(self):
        self.write('::\n a\n\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b)
        self.assertEqual(pt, 3)


class Test_next_word_start_InInternalNormalMode_FromWhitespace(ViewTestCase):
    def test_to_whitespace_line(self):
        self.write('  \n  ')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('  \n foo')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 2)


class Test_next_word_start_InInternalNormalMode_FromWordStart(ViewTestCase):
    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 3)


class Test_next_word_start_InInternalNormalMode_FromWord(ViewTestCase):
    def test_to_whitespace_line(self):
        self.write('foo\n  ')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('foo\n bar')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 3)


class Test_next_word_start_InInternalNormalMode_FromPunctuationStart(ViewTestCase):
    def test_to_whitespace_line(self):
        self.write('.\n  ')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 1)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('.\n bar')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 1)


class Test_next_word_start_InInternalNormalMode_FromPunctuation(ViewTestCase):
    def test_to_whitespace_line(self):
        self.write('::\n  ')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 2)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('::\n bar')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 2)


class Test_next_word_start_InInternalNormalMode_FromEmptyLine(ViewTestCase):
    def test_to_whitespace_line(self):
        self.write('\n  ')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 3)

    def test_to_one_word_line_with_leading_whitespace(self):
        self.write('\n bar')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = next_word_start(self.view, r.b, internal=True)
        self.assertEqual(pt, 2)


class Test_words_InNormalMode(ViewTestCase):
    def test_move1(self):
        self.write('foo bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b)
        self.assertEqual(pt, 4)

    def test_move2(self):
        self.write('foo bar fizz\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, count=2)
        self.assertEqual(pt, 8)

    def test_move10(self):
        self.write(''.join(('foo bar\n',) * 5))
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, count=9)
        self.assertEqual(pt, 36)


class Test_words_InInternalNormalMode_FromEmptyLine(ViewTestCase):
    # We can assume the stuff tested for normal mode applies to internal normal mode, so we
    # don't bother with that. Instead, we only test the differing behavior when advancing by
    # word starts in internal normal.
    def test_move1_to_line_with_leading_white_space(self):
        self.write('\n bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True)
        self.assertEqual(pt, 1)

    def test_move1_to_whitespace_line(self):
        self.write('\n  \n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, count=1, internal=True)
        self.assertEqual(pt, 1)

    def test_move2_to_one_word_line(self):
        self.write('\nfoo\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 5)

    def test_move3_and_swallow_last_newline_char(self):
        self.write('\nfoo\n bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=3)
        self.assertEqual(pt, 10)

    def test_move2_to_line_with_leading_white_space(self):
        self.write('\nfoo\n  \n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 5)


class Test_words_InInternalNormalMode_FromOneWordLine(ViewTestCase):
    # We can assume the stuff tested for normal mode applies to internal normal mode, so we
    # don't bother with that. Instead, we only test the differing behavior when advancing by
    # word starts in internal normal.
    def test_move1_to_eol(self):
        self.write('foo\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=1)
        self.assertEqual(pt, 3)

    def test_move2_to_line_with_leading_white_space_from_word_start(self):
        self.write('foo\n\nbar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 5)

    def test_move2_to_empty_line_from_word(self):
        self.write('foo\n\nbar\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 4)

    def test_move2_to_one_word_line_from_word_start(self):
        self.write('foo\nbar\nccc\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 8)

    def test_move2_to_one_word_line_from_word(self):
        self.write('foo\nbar\nccc\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 7)

    def test_move2_to_whitespaceline(self):
        self.write('foo\n  \nccc\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 10)

    def test_move2_to_whitespaceline_followed_by_leading_whitespace_from_word(self):
        self.write('foo\n  \n ccc\n')
        r = self.R((0, 1), (0, 1))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 11)

    def test_move2_to_whitespaceline_followed_by_leading_whitespace_from_word_start(self):
        self.write('foo\n  \n ccc\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 12)


class Test_words_InInternalNormalMode_FromOneCharLongWord(ViewTestCase):
    def test_move1_to_eol(self):
        self.write('x\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=1)
        self.assertEqual(pt, 1)


class Test_words_InInternalNormalMode_FromLine(ViewTestCase):
    def test_move2_to_eol(self):
        self.write('foo bar\n')
        r = self.R((0, 0), (0, 0))
        self.add_sel(r)

        pt = word_starts(self.view, r.b, internal=True, count=2)
        self.assertEqual(pt, 7)
