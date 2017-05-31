from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.text_objects import a_word


class Test_a_word_InInternalNormalMode_Inclusive(ViewTestCase):

    def test_returns_full_word__count_one(self):
        self.write('foo bar baz\n')
        r = self.R(5, 5)
        self.select(r)

        reg = a_word(self.view, r.b)
        self.assertEqual('bar ', self.view.substr(reg))

    def test_returns_word_and_preceding_white_space__count_one(self):
        self.write('(foo bar) baz\n')
        r = self.R(5, 5)
        self.select(r)

        reg = a_word(self.view, r.b)
        self.assertEqual(' bar', self.view.substr(reg))

    def test_returns_word_and_all_preceding_white_space__count_one(self):
        self.write('(foo   bar) baz\n')
        r = self.R(8, 8)
        self.select(r)

        reg = a_word(self.view, r.b)
        self.assertEqual('   bar', self.view.substr(reg))
