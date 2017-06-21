from collections import namedtuple

from sublime import Region

from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.text_objects import find_prev_lone_bracket
from NeoVintageous.lib.vi.text_objects import find_next_lone_bracket


test = namedtuple('simple_test', 'content start brackets expected msg')

TESTS = (
    test(content='aaa',      start=1, brackets=('\\{', '\\}'), expected=None, msg='should return none'),
    test(content='a{a}a',    start=1, brackets=('\\{', '\\}'), expected=Region(1, 2), msg='should find bracket at caret position'),
    test(content='{aa}a',    start=1, brackets=('\\{', '\\}'), expected=Region(0, 1), msg='should find bracket at BOF'),
    test(content='bbb{aa}a', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find brackets after caret'),
    test(content='a{bc',     start=3, brackets=('\\{', '\\}'), expected=Region(1, 2), msg='should find unbalanced bracket before caret'),

    test(content='foo {bar {foo} bar}', start=16, brackets=('\\{', '\\}'), expected=Region(4, 5), msg='should find outer bracket from RHS'),
    test(content='foo {bar {foo} bar}', start=7, brackets=('\\{', '\\}'), expected=Region(4, 5), msg='should find outer bracket from LHS'),
    test(content='foo {bar {foo} bar}', start=13, brackets=('\\{', '\\}'), expected=Region(9, 10), msg='should find inner bracket'),

    test(content='foo {bar {foo} bar', start=16, brackets=('\\{', '\\}'), expected=Region(4, 5), msg='should find outer if unbalanced outer'),
    test(content='foo {bar {foo} bar', start=12, brackets=('\\{', '\\}'), expected=Region(9, 10), msg='should find inner if unbalanced outer'),
    test(content='foo {bar {foo} bar', start=4, brackets=('\\{', '\\}'), expected=Region(4, 5), msg='should find bracket at caret position'),

    test(content='a\\{bc', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket at caret position'),
    test(content='a\\{bc', start=3, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket'),
)

TESTS_NEXT_BRACKET = (
    test(content='a\\}bc', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket at caret position'),
    test(content='a\\}bc', start=0, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket'),
    test(content='foo {bar foo bar}', start=16, brackets=('\\{', '\\}'), expected=Region(16, 17), msg='should find next bracket at caret position'),
)


class Test_previous_bracket(ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.content)
            self.view.sel().clear()

            actual = find_prev_lone_bracket(self.view, data.start, data.brackets)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))


class Test_next_bracket(ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS_NEXT_BRACKET):
            self.write(data.content)
            self.view.sel().clear()

            actual = find_next_lone_bracket(self.view, data.start, data.brackets)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))
