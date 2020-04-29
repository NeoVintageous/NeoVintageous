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

from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.vim import enter_normal_mode


class TestViEnterNormalModeSingleSelectionLeftRoRight(unittest.ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select((8, 11))
        set_mode(self.view, unittest.VISUAL)
        enter_normal_mode(self.view, unittest.VISUAL)

        self.assertSelection(10)


class TestViEnterNormalModeSingleSelectionRightToLeft(unittest.ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select((11, 8))
        set_mode(self.view, unittest.VISUAL)
        enter_normal_mode(self.view, unittest.VISUAL)

        self.assertSelection(8)


class TestViEnterNormalModeMulipleSelectionsFromSelectMode(unittest.ViewTestCase):

    def test_carets_end_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([(8, 11), (16, 19)])
        set_mode(self.view, unittest.SELECT)
        enter_normal_mode(self.view, unittest.SELECT)

        self.assertSelection([self.Region(8), self.Region(16)])


class TestViEnterNormalModeMulipleSelectionsFromNormalMode(unittest.ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([8, 16])
        set_mode(self.view, unittest.NORMAL)
        enter_normal_mode(self.view, unittest.NORMAL)

        self.assertSelection(8)


class TestVisualBlock(unittest.ViewTestCase):

    def test_enter_normal_from_visual_block(self):
        self.write('1111\n2222\n')
        self.select([(1, 3), (6, 8)])
        set_mode(self.view, unittest.VISUAL_BLOCK)
        enter_normal_mode(self.view, unittest.VISUAL_BLOCK)

        self.assertNormalMode()
        self.assertSelection(7)


class TestEnterNormalMode(unittest.ViewTestCase):

    def test_visual_mode_positions_cursor_on_last_character_not_eol_char(self):
        self.write('ab\n')
        self.select((1, 3))
        set_mode(self.view, unittest.VISUAL)
        enter_normal_mode(self.view, unittest.VISUAL)

        self.assertNormalMode()
        self.assertSelection(1)

        self.write('ab\n')
        self.select((3, 1))
        set_mode(self.view, unittest.VISUAL)
        enter_normal_mode(self.view, unittest.VISUAL)

        self.assertNormalMode()
        self.assertSelection(1)

        self.write('abc\ndef\n')
        self.select((1, 4))
        set_mode(self.view, unittest.VISUAL)
        enter_normal_mode(self.view, unittest.VISUAL)

        self.assertNormalMode()
        self.assertSelection(2)

        self.write('abc\ndef\n')
        self.select((6, 3))
        set_mode(self.view, unittest.VISUAL)
        enter_normal_mode(self.view, unittest.VISUAL)

        self.assertNormalMode()
        self.assertSelection(2)
