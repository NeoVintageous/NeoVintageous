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


class Test_p(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)
        self.settings().set('tab_size', 2)

    def test_n(self):
        self.register('"', 'fizz')
        self.eq('a|bc', 'p', 'abfiz|zc')
        self.eq('ab|c', 'p', 'abcfiz|z')
        self.eq('ab|c\nbuzz', 'p', 'abcfiz|z\nbuzz')
        self.eq('|', 'p', 'fiz|z')
        self.eq('a|bc', '2p', 'abfizzfiz|zc')
        self.eq('a|bc', '3p', 'abfizzfizzfiz|zc')
        self.assertRegister('"fizz')
        self.register('"', 'fizz\n')
        self.eq('a|bc', 'p', 'ab|fizz\nc')
        self.eq('ab|c', 'p', 'abc|fizz\n')
        self.eq('ab|c\n', 'p', 'abc|fizz\n\n')
        self.eq('|', 'p', '|fizz\n')
        self.eq('a|bc', '2p', 'ab|fizz\nfizz\nc')
        self.eq('a|bc', '3p', 'ab|fizz\nfizz\nfizz\nc')
        self.assertRegister('"fizz\n')
        self.register('"', 'fizz\nbuzz')
        self.eq('a|bc', 'p', 'ab|fizz\nbuzzc')
        self.eq('|', 'p', '|fizz\nbuzz')
        self.eq('a|bc', '2p', 'ab|fizz\nbuzzfizz\nbuzzc')
        self.assertRegister('"fizz\nbuzz')
        self.registerLinewise('"', 'fizz\n')
        self.eq('x\na|bc\ny', 'p', 'x\nabc\n|fizz\ny')
        self.eq('x\nab|c\ny', 'p', 'x\nabc\n|fizz\ny')
        self.eq('x\na|bc\ny', '2p', 'x\nabc\n|fizz\nfizz\ny')
        self.eq('x\na|bc\ny', '3p', 'x\nabc\n|fizz\nfizz\nfizz\ny')
        self.eq('|', 'p', '|fizz\n')
        self.eq('1\n2\n|buzz', 'p', '1\n2\nbuzz\n|fizz\n')
        self.eq('1\n2\n|buzz', '2p', '1\n2\nbuzz\n|fizz\nfizz\n')
        self.registerLinewise('"', 'fizz\nbuzz\n')
        self.eq('|', 'p', '|fizz\nbuzz\n')
        self.eq('x\na|bc\ny', 'p', 'x\nabc\n|fizz\nbuzz\ny')
        self.eq('x\na|bc\ny', '2p', 'x\nabc\n|fizz\nbuzz\nfizz\nbuzz\ny')
        self.eq('1\n2\n|zing', 'p', '1\n2\nzing\n|fizz\nbuzz\n')
        self.eq('1\n2\n|zing', '2p', '1\n2\nzing\n|fizz\nbuzz\nfizz\nbuzz\n')
        self.register('"', 'buzz')
        self.eq('fizz\n|\na\nb', 'p', 'fizz\nbuz|z\na\nb')

    def test_n_multi_cursor(self):
        self.register('"', ['fizz', 'buzz'])
        self.eq('a|bc\nd|ef', 'p', 'abfiz|zc\ndebuz|zf')
        self.eq('|abc\nx\nde|f', 'p', 'afiz|zbc\nx\ndefbuz|z')
        self.eq('|1\n|2\n3', '2p', '1fizzfiz|z\n2buzzbuz|z\n3')
        self.eq('|1\n|2\n3', '3p', '1fizzfizzfiz|z\n2buzzbuzzbuz|z\n3')
        self.register('"', ['fizz\n', 'buzz\n'])
        self.eq('a|bc\nd|ef\nx', 'p', 'ab|fizz\nc\nde|buzz\nf\nx')
        self.eq('a|bc\nd|ef\nx', '2p', 'ab|fizz\nfizz\nc\nde|buzz\nbuzz\nf\nx')
        self.register('"', ['fizz\nbuzz', 'buzz\nfizz'])
        self.eq('a|bc\nd|ef\nx', 'p', 'ab|fizz\nbuzzc\nde|buzz\nfizzf\nx')
        self.registerLinewise('"', ['fizz\n', 'buzz\n'])
        self.eq('a|bc\n2\nd|ef\n4', 'p', 'abc\n|fizz\n2\ndef\n|buzz\n4')
        self.eq('11|1\n222\n33|3', 'p', '111\n|fizz\n222\n333\n|buzz\n')

    @unittest.mock_status_message()
    def test_n_nothing_in_register(self):
        self.eq('fi|zz', 'p', 'fi|zz')
        self.assertStatusMessage('E353: Nothing in register "')

    @unittest.mock_bell()
    def test_n_multi_cursor_content_count_not_equal_to_selection_count(self):
        self.register('"', ['one', 'two'])
        self.eq('x|xx x|xx x|xx', 'p', 'x|xx x|xx x|xx')
        self.assertBell()

    def test_n_multi_cursor_content_and_one_selection(self):
        self.register('"', ['fizz', 'buzz'])
        self.eq('a|bc', 'p', 'ab|fizzc\n  buzz')
        self.eq('|', 'p', '|fizz\nbuzz')
        self.eq('x\na|bc\ny', 'p', 'x\nab|fizzc\ny buzz')
        self.eq('|___\n___\nx', 'p', '_|fizz__\n_buzz__\nx')
        self.eq('_|__\n___\nx', 'p', '__|fizz_\n__buzz_\nx')
        self.eq('__|_\n___\nx', 'p', '___|fizz\n___buzz\nx')
        self.eq('|___\n\nx', 'p', '_|fizz__\n buzz\nx')
        self.eq('_|__\n\nx', 'p', '__|fizz_\n  buzz\nx')
        self.eq('__|_\n\nx', 'p', '___|fizz\n   buzz\nx')
        self.eq('|\n\nx', 'p', '|fizz\nbuzz\nx')
        self.eq('|\n_\nx', 'p', '|fizz\nbuzz_\nx')
        self.eq('__|______\nfizz\nx', 'p', '___|fizz_____\nfizbuzzz\nx')
        self.eq('___|_____\nfizz\nx', 'p', '____|fizz____\nfizzbuzz\nx')
        self.eq('____|____\nfizz\nx', 'p', '_____|fizz___\nfizz buzz\nx')
        self.eq('_____|___\nfizz\nx', 'p', '______|fizz__\nfizz  buzz\nx')
        self.eq('______|__\nfizz\nx', 'p', '_______|fizz_\nfizz   buzz\nx')
        self.eq('_______|_\nfizz\nx', 'p', '________|fizz\nfizz    buzz\nx')
        self.eq('|\n\nx', 'p', '|fizz\nbuzz\nx')
        self.eq('\n|\n\nx', 'p', '\n|fizz\nbuzz\nx')

        self.register('"', ['fiz', 'buz', 'foo', 'bar'])
        self.eq('__|__\n\n\n\nx', 'p', '___|fiz_\n   buz\n   foo\n   bar\nx')
        self.eq('xxxx|x\n\nxx\n\nx', 'p', 'xxxxx|fiz\n     buz\nxx   foo\n     bar\nx')
        self.eq('|', 'p', '|fiz\nbuz\nfoo\nbar')
        self.eq('xx|xxx', 'p', 'xxx|fizxx\n   buz\n   foo\n   bar')
        self.eq('xx|xxx\n', 'p', 'xxx|fizxx\n   buz\n   foo\n   bar')
        self.eq('xx|xxx\n\n', 'p', 'xxx|fizxx\n   buz\n   foo\n   bar')
        self.eq('xx|x', 'p', 'xxx|fiz\n   buz\n   foo\n   bar')
        self.eq('xx|x\n', 'p', 'xxx|fiz\n   buz\n   foo\n   bar')
        self.eq('xx|x\n\n', 'p', 'xxx|fiz\n   buz\n   foo\n   bar')
        self.eq('11|11\n2222\n3333', 'p', '111|fiz1\n222buz2\n333foo3\n   bar')
        self.eq('11|11\n2222\n3333\n', 'p', '111|fiz1\n222buz2\n333foo3\n   bar')
        self.eq('1111\n22|22\n3333', 'p', '1111\n222|fiz2\n333buz3\n   foo\n   bar')
        self.eq('xx|xx\nx\n\nxxxx', 'p', 'xxx|fizx\nx  buz\n   foo\nxxxbarx')
        self.eq('xx|xx\n\nxxx\nxxxx', 'p', 'xxx|fizx\n   buz\nxxxfoo\nxxxbarx')

    def test_n_multi_cursor_1_paste_with_many_selections(self):
        self.register('"', ['fi'])
        self.eq('fizz| zz| zz| zz', 'p', 'fizz f|izz f|izz f|izz')

    def test_n_multi_cursor_many_paste_with_less_selections_when_paste_content_is_all_the_same(self):
        self.register('"', ['fi', 'fi', 'fi', 'fi', 'fi'])
        self.eq('fizz| zz| zz', 'p', 'fizz f|izz f|izz')

    def test_n_multi_cursor_many_paste_with_more_selections_when_paste_content_is_all_the_same(self):
        self.register('"', ['fi', 'fi'])
        self.eq('fizz| zz| zz| zz| zz| zz', 'p', 'fizz f|izz f|izz f|izz f|izz f|izz')

    def test_n_multi_cursor_many_paste_with_less_selections_when_paste_content_is_not_the_same(self):
        self.register('"', ['fi', 'bu', 'fi', 'bu', 'fi', 'bu', 'fi'])
        self.eq('fizz| zz| zz| zz', 'p', 'fizz f|izz b|uzz f|izz')

    def test_n_multi_cursor_many_paste_with_more_selections_when_paste_content_is_not_the_same_is_noop(self):
        self.register('"', ['fi', 'bu', 'fi'])
        self.eq('fizz| zz| zz| zz| zz| zz| zz', 'p', 'fizz| zz| zz| zz| zz| zz| zz')

    def test_v(self):
        self.register('"', 'fizz')
        self.eq('a|xyz|b', 'v_p', 'n_afiz|zb')
        self.assertRegister('"', 'xyz')
        self.eq('r_a|fizz|b', 'v_p', 'n_axy|zb')
        self.register('"', 'fizz\n')
        self.eq('a|xyz|b', 'v_p', 'n_a|fizz\nb')
        self.register('"', 'fizz\nbuzz\na\nbc')
        self.eq('a|xyz|b', 'v_p', 'n_a|fizz\nbuzz\na\nbcb')
        self.registerLinewise('"', 'fizz\n')
        self.eq('a|xyz|b', 'v_p', 'n_a\n|fizz\nb')

    def test_V(self):
        self.register('"', 'fizz')
        self.eq('a\n|xyz\n|b\n', 'V_p', 'n_a\n|fizz\nb\n')
        self.register('"', 'fizz\n')
        self.eq('a\n|xyz\n|b\n', 'V_p', 'n_a\n|fizz\n\nb\n')
        self.registerLinewise('"', 'fizz\n')
        self.eq('a\n|xyz\n|b\n', 'V_p', 'n_a\n|fizz\nb\n')
        self.registerLinewise('"', 'fizz\nbuzz\nab\n')
        self.eq('a\n|xyz\n|b\n', 'V_p', 'n_a\n|fizz\nbuzz\nab\nb\n')

    def test_issue_93(self):
        self.register('"', ['THIS ', 'THIS ', 'THIS '])
        self.eq('|THIS IS\n|THIS IS\n|THIS IS', 'p', 'TTHIS| HIS IS\nTTHIS| HIS IS\nTTHIS| HIS IS')
