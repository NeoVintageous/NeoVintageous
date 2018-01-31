from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.text_objects import word_reverse


class Test_word_reverse(unittest.ViewTestCase):

    def test_find_word_start_from_the_middle_of_a_word(self):
        self.write('abc')
        self.assertEqual(0, word_reverse(self.view, 2, 1))

    def test_find_word_start_from_next_word(self):
        self.write('abc abc abc')
        self.assertEqual(4, word_reverse(self.view, 8, 1))

    def test_find_word_start_from_next_word__count_2(self):
        self.write('abc abc abc')
        self.assertEqual(0, word_reverse(self.view, 8, 2))

    def test_find_word_start_from_different_line(self):
        self.write('abc\nabc\nabc')
        self.assertEqual(4, word_reverse(self.view, 8, 1))

    def test_stop_at_empty_line(self):
        self.write('abc\n\nabc')
        self.assertEqual(4, word_reverse(self.view, 5, 1))

    def test_stop_at_single_char_word(self):
        self.write('abc a abc')
        self.assertEqual(4, word_reverse(self.view, 6, 1))

    def test_skip_over_punctuation_simple(self):
        self.write('(abc) abc')
        self.assertEqual(4, word_reverse(self.view, 6, 1))

    def test_skip_over_punctuation_complex(self):
        self.write('abc.(abc)')
        self.assertEqual(3, word_reverse(self.view, 5, 1))

    def test_stop_at_isolated_punctuation_word(self):
        self.write('abc == abc')
        self.assertEqual(4, word_reverse(self.view, 7, 1))
