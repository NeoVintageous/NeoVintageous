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


class Test_P(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)

    def test_n(self):
        self.register('"abc')
        self.eq('x|y', 'P', 'xab|cy')
        self.assertRegister('"abc')
        self.eq('x|y', '2P', 'xabcab|cy')
        self.eq('x|y', '3P', 'xabcabcab|cy')
        self.eq('|', 'P', 'ab|c')
        self.register('"', 'buzz')
        self.eq('fizz\n|\na\nb', 'P', 'fizz\nbuz|z\na\nb')

    def test_n_characterwise_content_multiline(self):
        self.register('"fizz\nbuzz')
        self.eq('x|y', 'P', 'x|fizz\nbuzzy')
        self.assertRegister('"fizz\nbuzz')
        self.eq('x|y', '3P', 'x|fizz\nbuzzfizz\nbuzzfizz\nbuzzy')

    def test_n_characterwise_content_with_newline(self):
        self.register('"abc\n')
        self.eq('x|y', 'P', 'x|abc\ny')
        self.assertRegister('"abc\n')

    def test_n_characterwise_content_with_newline_multiline(self):
        self.register('"fizz\nbuzz\n')
        self.eq('x|y', 'P', 'x|fizz\nbuzz\ny')
        self.assertRegister('"fizz\nbuzz\n')

    def test_n_linewise_content(self):
        self.registerLinewise('"abc\n')
        self.eq('x\ny|z', 'P', 'x\n|abc\nyz')
        self.assertLinewiseRegister('"abc\n')
        self.eq('a\n|b\nc', '3P', 'a\n|abc\nabc\nabc\nb\nc')

    def test_n_linewise_content_multiline(self):
        self.registerLinewise('"fizz\nbuzz\n')
        self.eq('x\ny|z', 'P', 'x\n|fizz\nbuzz\nyz')
        self.assertLinewiseRegister('"fizz\nbuzz\n')

    def test_n_linewise_content_puts_cursor_on_first_non_whitespace_character(self):
        self.registerLinewise('"    abc\n')
        self.eq('x\ny|z', 'P', 'x\n    |abc\nyz')
        self.assertLinewiseRegister('"    abc\n')

    def test_n_linewise_content_puts_cursor_on_first_non_whitespace_character_multiline(self):
        self.registerLinewise('"    fizz\n    buzz\n')
        self.eq('x\ny|z', 'P', 'x\n    |fizz\n    buzz\nyz')
        self.assertLinewiseRegister('"    fizz\n    buzz\n')

    def test_n_multi_cursor(self):
        self.register('"', ['zz bu'])
        self.eq('fi|zz', 'P', 'fizz b|uzz')
        self.register('"', ['zz', 'bu'])
        self.eq('fi| x |zz', 'P', 'fiz|z x b|uzz')
        self.register('"', ['on', 'tw', 'thre'])
        self.eq('x 1|e 2|o 3|e x', 'P', 'x 1o|ne 2t|wo 3thr|ee x')

    @unittest.mock_status_message()
    def test_n_nothing_in_register(self):
        self.eq('fi|zz', 'P', 'fi|zz')
        self.assertStatusMessage('E353: Nothing in register "')

    @unittest.mock_bell()
    def test_n_multiple_cursor_content_count_not_equal_to_selection_count(self):
        self.register('"', ['one', 'two'])
        self.eq('x|xx x|xx x|xx', 'P', 'x|xx x|xx x|xx')
        self.assertBell()

    def test_n_multi_cursor_content_and_one_selection(self):
        self.register('"', ['fizz', 'buzz'])
        self.eq('|___\n___\nx', 'P', '|fizz___\nbuzz___\nx')
        self.eq('_|__\n___\nx', 'P', '_|fizz__\n_buzz__\nx')
        self.eq('__|_\n___\nx', 'P', '__|fizz_\n__buzz_\nx')
        self.eq('|___\n\nx', 'P', '|fizz___\nbuzz\nx')
        self.eq('_|__\n\nx', 'P', '_|fizz__\n buzz\nx')
        self.eq('__|_\n\nx', 'P', '__|fizz_\n  buzz\nx')
        self.eq('|\n\nx', 'P', '|fizz\nbuzz\nx')
        self.eq('|\n_\nx', 'P', '|fizz\nbuzz_\nx')
        self.eq('__|______\nfizz\nx', 'P', '__|fizz______\nfibuzzzz\nx')
        self.eq('___|_____\nfizz\nx', 'P', '___|fizz_____\nfizbuzzz\nx')
        self.eq('____|____\nfizz\nx', 'P', '____|fizz____\nfizzbuzz\nx')
        self.eq('_____|___\nfizz\nx', 'P', '_____|fizz___\nfizz buzz\nx')
        self.eq('______|__\nfizz\nx', 'P', '______|fizz__\nfizz  buzz\nx')
        self.eq('_______|_\nfizz\nx', 'P', '_______|fizz_\nfizz   buzz\nx')

        self.register('"', ['fiz', 'buz', 'foo', 'bar'])
        self.eq('|\n\n\n\nx', 'P', '|fiz\nbuz\nfoo\nbar\nx')
        self.eq('\n|\n\n\n\nx', 'P', '\n|fiz\nbuz\nfoo\nbar\nx')
        self.eq('|\n\n\n\nx', 'P', '|fiz\nbuz\nfoo\nbar\nx')
        self.eq('|\n_\n_\n_\nx', 'P', '|fiz\nbuz_\nfoo_\nbar_\nx')
        self.eq('|', 'P', '|fiz\nbuz\nfoo\nbar')
        self.eq('xx|xxx', 'P', 'xx|fizxxx\n  buz\n  foo\n  bar')
        self.eq('xx|xxx\n', 'P', 'xx|fizxxx\n  buz\n  foo\n  bar')
        self.eq('xx|xxx\n\n', 'P', 'xx|fizxxx\n  buz\n  foo\n  bar')
        self.eq('xx|x', 'P', 'xx|fizx\n  buz\n  foo\n  bar')
        self.eq('xx|x\n', 'P', 'xx|fizx\n  buz\n  foo\n  bar')
        self.eq('xx|x\n\n', 'P', 'xx|fizx\n  buz\n  foo\n  bar')
        self.eq('11|11\n2222\n3333', 'P', '11|fiz11\n22buz22\n33foo33\n  bar')
        self.eq('11|11\n2222\n3333\n', 'P', '11|fiz11\n22buz22\n33foo33\n  bar')
        self.eq('1111\n22|22\n3333', 'P', '1111\n22|fiz22\n33buz33\n  foo\n  bar')
        self.eq('xx|xx\nx\n\nxxxx', 'P', 'xx|fizxx\nx buz\n  foo\nxxbarxx')
        self.eq('xx|xx\n\nxxx\nxxxx', 'P', 'xx|fizxx\n  buz\nxxfoox\nxxbarxx')

    def test_n_multi_cursor_1_paste_with_many_selections(self):
        self.register('"', ['fi'])
        self.eq('fizz |zz |zz |zz', 'P', 'fizz f|izz f|izz f|izz')

    def test_n_multi_cursor_many_paste_with_less_selections_when_paste_content_is_all_the_same(self):
        self.register('"', ['fi', 'fi', 'fi', 'fi', 'fi'])
        self.eq('fizz |zz |zz', 'P', 'fizz f|izz f|izz')

    def test_n_multi_cursor_many_paste_with_more_selections_when_paste_content_is_all_the_same(self):
        self.register('"', ['fi', 'fi'])
        self.eq('fizz |zz |zz |zz |zz |zz', 'P', 'fizz f|izz f|izz f|izz f|izz f|izz')

    def test_n_multi_cursor_many_paste_with_less_selections_when_paste_content_is_not_the_same(self):
        self.register('"', ['fi', 'bu', 'fi', 'bu', 'fi', 'bu', 'fi'])
        self.eq('fizz |zz |zz |zz', 'P', 'fizz f|izz b|uzz f|izz')

    def test_n_multi_cursor_many_paste_with_more_selections_when_paste_content_is_not_the_same_is_noop(self):
        self.register('"', ['fi', 'bu', 'fi'])
        self.eq('fizz |zz |zz |zz |zz |zz |zz', 'P', 'fizz |zz |zz |zz |zz |zz |zz')

    def test_v(self):
        self.register('"abc')
        self.eq('x|456|y', 'v_P', 'n_xab|cy')
        self.assertRegister('"456')
        self.register('"abc\n')
        self.eq('x|456|y', 'v_P', 'n_x|abc\ny')
        self.assertRegister('"456')
        self.registerLinewise('"abc\n')
        self.eq('x|456|y', 'v_P', 'n_x\n|abc\ny')
        self.assertRegister('"456')
        self.register('"    abc\n')
        self.eq('x|456|y', 'v_P', 'n_x|    abc\ny')
        self.registerLinewise('"    abc\n')
        self.eq('x|456|y', 'v_P', 'n_x\n    |abc\ny')
        self.assertRegister('"456')

    def test_v_paste_multiple_cursor_content(self):
        self.register('"', ['zz bu'])
        self.eq('x|iz|y', 'v_P', 'n_xzz b|uy')
        self.register('"', ['one', 'two'])
        self.eq('a|xx|b a|xx|b', 'v_P', 'n_aon|eb atw|ob')
        self.register('"', ['on', 'tw', 'thre'])
        self.eq('x 1|xyz|e 2|xyz|o 3|xyz|e x', 'v_P', 'n_x 1o|ne 2t|wo 3thr|ee x')

    def test_V(self):
        self.register('"', 'fizz')
        self.eq('one\n|two\n|three', 'V_P', 'n_one\n|fizz\nthree')
        self.assertLinewiseRegister('"two\n')
        self.register('"', 'fizz')
        self.eq('one\n|    1234567890\n|three', 'V_P', 'n_one\n|fizz\nthree')
        self.register('"', '    fizz')
        self.eq('one\n|  foo  \n|three', 'V_P', 'n_one\n    |fizz\nthree')
        self.eq('one\n|xxx\n|three', 'V_P', 'n_one\n  |foo  \nthree')
        self.registerLinewise('"', 'fizz\n')
        self.eq('one\n|xxx\n|three', 'V_P', 'n_one\n|fizz\nthree')
        self.registerLinewise('"', '  fizz\n')
        self.eq('one\n|xxx\n|three', 'V_P', 'n_one\n  |fizz\nthree')
        self.assertLinewiseRegister('"xxx\n')
        self.register('"', '  fizz\n')
        self.eq('one\n|xxx\n|three', 'V_P', 'n_one\n  |fizz\n\nthree')

    def test_issue_93(self):
        self.register('"', ['THIS ', 'THIS ', 'THIS '])
        self.eq('|THIS IS\n|THIS IS\n|THIS IS', 'P', 'THIS| THIS IS\nTHIS| THIS IS\nTHIS| THIS IS')

    def test_n_issue_224(self):
        self.register('"bc\n')
        self.eq('abc\nd|ef', 'P', 'abc\nd|bc\nef')
        self.assertRegister('"bc\n')

    def test_issue_627(self):
        self.normal('one\nt|wo\nthree')
        self.feed('"xyy')
        self.feed('"xP')
        self.assertNormal('one\n|two\ntwo\nthree')
        self.normal('one\nt|wo\nthree')
        self.feed('"2yy')
        self.feed('"2P')
        self.assertNormal('one\n|two\ntwo\nthree')
        self.normal('one\nt|wo\nthree')
        self.feed('"2Y')
        self.feed('"2P')
        self.assertNormal('one\n|two\ntwo\nthree')
