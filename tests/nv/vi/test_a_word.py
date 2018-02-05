# DEPRECATED This can be removed when the functional test suite is merged.
from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.text_objects import a_word


class Test_a_word_InInternalNormalMode_Inclusive(unittest.ViewTestCase):

    def test_returns_full_word__count_one(self):
        self.write('foo bar baz\n')
        self.select(5)

        self.assertEqual('bar ', self.view.substr(a_word(self.view, 5)))

    def test_returns_word_and_preceding_white_space__count_one(self):
        self.write('(foo bar) baz\n')
        self.select(5)

        self.assertEqual(' bar', self.view.substr(a_word(self.view, 5)))

    def test_returns_word_and_all_preceding_white_space__count_one(self):
        self.write('(foo   bar) baz\n')
        self.select(8)

        self.assertEqual('   bar', self.view.substr(a_word(self.view, 8)))
