from NeoVintageous.lib.vi.text_objects import a_word

from NeoVintageous.tests import ViewTest
from NeoVintageous.tests import set_text
from NeoVintageous.tests import add_sel


class Test_a_word_InInternalNormalMode_Inclusive(ViewTest):
    def testReturnsFullWord_CountOne(self):
        set_text(self.view, 'foo bar baz\n')
        r = self.R(5, 5)
        add_sel(self.view, r)

        reg = a_word(self.view, r.b)
        self.assertEqual('bar ', self.view.substr(reg))

    def testReturnsWordAndPrecedingWhiteSpace_CountOne(self):
        set_text(self.view, '(foo bar) baz\n')
        r = self.R(5, 5)
        add_sel(self.view, r)

        reg = a_word(self.view, r.b)
        self.assertEqual(' bar', self.view.substr(reg))

    def testReturnsWordAndAllPrecedingWhiteSpace_CountOne(self):
        set_text(self.view, '(foo   bar) baz\n')
        r = self.R(8, 8)
        add_sel(self.view, r)

        reg = a_word(self.view, r.b)
        self.assertEqual('   bar', self.view.substr(reg))
