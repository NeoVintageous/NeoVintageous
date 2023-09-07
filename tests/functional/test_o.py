# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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


class Test_o(unittest.FunctionalTestCase):

    def test_N(self):
        self.eq('|', 'o', 'i_\n|')
        self.eq('|\n', 'o', 'i_\n|\n')
        self.eq('|a\nb\n', 'o', 'i_a\n|\nb\n')
        self.eq('|', '2o', 'i_\n|\n|')
        self.eq('fo|o\nba|r', '2o', 'i_foo\n|\n|\nbar\n|\n|')
        self.assertStatusLineIsInsert()

    def test_v(self):
        self.eq('x|fizz|x', 'v_o', 'r_x|fizz|x')
        self.eq('r_x|fizz|x', 'v_o', 'x|fizz|x')
        self.assertStatusLineIsVisual()

    def test_V(self):
        self.eq('x\n|fizz\n|x', 'V_o', 'r_x\n|fizz\n|x')
        self.eq('r_x\n|fizz\n|x', 'V_o', 'x\n|fizz\n|x')
        self.assertStatusLineIsVisualLine()

    def test_ctrl_v(self):
        self.eq('x\nfi|zz bu|zz\nfi|zz bu|zz\nx', 'b_o', 'r_u_x\nfi|zz bu|zz\nfi|zz bu|zz\nx')
        self.feed('o')
        self.assertVblock('x\nfi|zz bu|zz\nfi|zz bu|zz\nx', direction=unittest.DIRECTION_DOWN)
        self.feed('o')
        self.assertRVblock('x\nfi|zz bu|zz\nfi|zz bu|zz\nx', direction=unittest.DIRECTION_UP)
        self.assertStatusLineIsVisualBlock()

    def test_issue_974_xpos_should_be_updated(self):
        self.eq('fizz\nfi|zz\nfizz buzz\nfizz bu|zz', 'v_o', 'r_fizz\nfi|zz\nfizz buzz\nfizz bu|zz')
        self.feed('j')
        self.assertRVisual('fizz\nfizz\nfi|zz buzz\nfizz bu|zz')


class Test_o_auto_indent(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('translate_tabs_to_spaces', True)
        self.syntax('Packages/Python/Python.sublime-syntax')

    def test_N(self):
        self.eq('def x():\n    |x = 1', 'o', 'i_def x():\n    x = 1\n    |')
        self.eq('def x():\n    def y():\n        |x = 1', 'o', 'i_def x():\n    def y():\n        x = 1\n        |')
        self.eq('def x():\n    |x = 1', '3o', 'i_def x():\n    x = 1\n    |\n    |\n    |')
        self.assertStatusLineIsInsert()
