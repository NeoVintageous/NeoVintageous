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


class Test_O(unittest.FunctionalTestCase):

    def test_O(self):
        self.eq('|', 'O', 'i_|\n')
        self.eq('|\n', 'O', 'i_|\n\n')
        self.eq('a\n|b\n', 'O', 'i_a\n|\nb\n')
        self.eq('1\na|bc\n3', 'O', 'i_1\n|\nabc\n3')
        self.eq('1\na|bc\n3\nx|yz\n5', 'O', 'i_1\n|\nabc\n3\n|\nxyz\n5')

    def test_O_count(self):
        self.eq('1\na|bc\n3', '3O', 'i_1\n|\n|\n|\nabc\n3')

    def test_O_count_with_multiple_cursor(self):
        self.eq('1\na|bc\n3\nx|yz\n5', '3O', 'i_1\n|\n|\n|\nabc\n3\n|\n|\n|\nxyz\n5')

    def test_v(self):
        self.eq('x|fizz|x', 'v_O', 'r_x|fizz|x')
        self.eq('r_x|fizz|x', 'v_O', 'x|fizz|x')
        self.assertStatusLineIsVisual()

    def test_V(self):
        self.eq('x\n|fizz\n|x', 'V_O', 'r_x\n|fizz\n|x')
        self.eq('r_x\n|fizz\n|x', 'V_O', 'x\n|fizz\n|x')
        self.assertStatusLineIsVisualLine()

    def test_ctrl_v(self):
        self.eq('x\nfi|zz bu|zz\nfi|zz bu|zz\nx', 'b_O', 'r_x\nfi|zz bu|zz\nfi|zz bu|zz\nx')
        self.feed('O')
        self.assertVblock('x\nfi|zz bu|zz\nfi|zz bu|zz\nx', direction=unittest.DIRECTION_DOWN)
        self.feed('O')
        self.assertRVblock('x\nfi|zz bu|zz\nfi|zz bu|zz\nx', direction=unittest.DIRECTION_DOWN)
        self.assertStatusLineIsVisualBlock()


class Test_O_auto_indent(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('translate_tabs_to_spaces', True)
        self.syntax('Packages/Python/Python.sublime-syntax')

    def test_O(self):
        self.eq('def x():\n    |x = 1', 'O', 'i_def x():\n    |\n    x = 1')
        self.eq('def x():\n    def y():\n        |x = 1', 'O', 'i_def x():\n    def y():\n        |\n        x = 1')
        self.eq('def x():\n|x = 1', 'O', 'i_def x():\n    |\nx = 1')

    def test_O_count(self):
        self.eq('def x():\n    |x = 1', '3O', 'i_def x():\n    |\n    |\n    |\n    x = 1')
