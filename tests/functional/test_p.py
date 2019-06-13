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
        self.settings().set('vintageous_use_sys_clipboard', False)
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
        self.registerLinewise('"', 'fizz\nbuzz\n')
        self.eq('|', 'p', '|fizz\nbuzz\n')
        self.eq('x\na|bc\ny', 'p', 'x\nabc\n|fizz\nbuzz\ny')
        self.eq('x\na|bc\ny', '2p', 'x\nabc\n|fizz\nbuzz\nfizz\nbuzz\ny')
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

    def test_n_multi_cursor_content_and_one_selection(self):
        self.register('"', ['fizz', 'buzz'])
        self.eq('|', 'p', 'fizzbuz|z')
        self.eq('a|bc', 'p', 'abfizzbuz|zc')
        self.registerLinewise('"', ['fizz\n', 'buzz\n'])
        self.eq('|', 'p', '|fizz\nbuzz\n')
        self.eq('x\na|bc\ny', 'p', 'x\nabc\n|fizz\nbuzz\ny')

    @unittest.mock_status_message()
    def test_n_nothing_in_register(self):
        self.eq('fi|zz', 'p', 'fi|zz')
        self.assertStatusMessage('E353: Nothing in register "')

    @unittest.mock_bell()
    def test_n_multi_cursor_content_count_not_equal_to_selection_count(self):
        self.register('"', ['one', 'two'])
        self.eq('x|xx x|xx x|xx', 'p', 'x|xx x|xx x|xx')
        self.assertBell()

    def test_issue_93(self):
        self.register('"', ['THIS ', 'THIS ', 'THIS '])
        self.eq('|THIS IS\n|THIS IS\n|THIS IS', 'p', 'TTHIS| HIS IS\nTTHIS| HIS IS\nTTHIS| HIS IS')

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
