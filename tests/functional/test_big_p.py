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


class Test_P(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_P_paste_characterwise_content(self):
        self.register('"abc')
        self.eq('x|y', 'P', 'xab|cy')
        self.assertRegister('"abc')

    def test_P_paste_characterwise_content_multiline(self):
        self.register('"fizz\nbuzz')
        self.eq('x|y', 'P', 'x|fizz\nbuzzy')
        self.assertRegister('"fizz\nbuzz')

    def test_P_paste_characterwise_content_with_newline(self):
        self.register('"abc\n')
        self.eq('x|y', 'P', 'x|abc\ny')
        self.assertRegister('"abc\n')

    def test_P_paste_characterwise_content_with_newline_multiline(self):
        self.register('"fizz\nbuzz\n')
        self.eq('x|y', 'P', 'x|fizz\nbuzz\ny')
        self.assertRegister('"fizz\nbuzz\n')

    def test_P_paste_linewise_content(self):
        self.register('"abc\n', linewise=True)
        self.eq('x\ny|z', 'P', 'x\n|abc\nyz')
        self.assertRegister('"abc\n', linewise=True)

    def test_P_paste_linewise_content_multiline(self):
        self.register('"fizz\nbuzz\n', linewise=True)
        self.eq('x\ny|z', 'P', 'x\n|fizz\nbuzz\nyz')
        self.assertRegister('"fizz\nbuzz\n', linewise=True)

    def test_P_paste_linewise_content_puts_cursor_on_first_non_whitespace_character(self):
        self.register('"    abc\n', linewise=True)
        self.eq('x\ny|z', 'P', 'x\n    |abc\nyz')
        self.assertRegister('"    abc\n', linewise=True)

    def test_P_paste_linewise_content_puts_cursor_on_first_non_whitespace_character_multiline(self):
        self.register('"    fizz\n    buzz\n', linewise=True)
        self.eq('x\ny|z', 'P', 'x\n    |fizz\n    buzz\nyz')
        self.assertRegister('"    fizz\n    buzz\n', linewise=True)


class Test_v_P(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_v_P_paste_characterwise_content(self):
        self.register('"abc')
        self.eq('x|456|y', 'v_P', 'n_xab|cy')
        self.assertRegister('"456')

    def test_v_P_paste_characterwise_content_with_newline(self):
        self.register('"abc\n')
        self.eq('x|456|y', 'v_P', 'n_xab|c\ny')
        self.assertRegister('"456')

    def test_v_P_paste_linewise_content(self):
        self.register('"abc\n', linewise=True)
        self.eq('x|456|y', 'v_P', 'n_x\n|abc\ny')
        self.assertRegister('"456')

    def test_v_P_paste_linewise_content_puts_cursor_on_first_non_whitespace_character(self):
        self.register('"    abc\n', linewise=True)
        self.eq('x|456|y', 'v_P', 'n_x\n    |abc\ny')
        self.assertRegister('"456')

    def test_224(self):
        self.register('"bc\n')
        self.eq('abc\nd|ef', 'P', 'abc\nd|bc\nef')
        self.assertRegister('"bc\n')
