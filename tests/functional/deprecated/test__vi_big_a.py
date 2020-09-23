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


class Test__nv_vi_big_a_InNormalMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(2)

        self.view.run_command('nv_vi_big_a', {'mode': unittest.INTERNAL_NORMAL, 'count': 1})

        self.assertSelection(3)


class Test__nv_vi_big_a_InNormalMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(1, 1), (5, 5)])

        self.view.run_command('nv_vi_big_a', {'mode': unittest.INTERNAL_NORMAL, 'count': 1})

        self.assertSelection([self.Region(3), self.Region(7)])


class Test__nv_vi_big_a_InVisualMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('nv_vi_big_a', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection(2)


class Test__nv_vi_big_a_InVisualMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 2), (4, 6)])

        self.view.run_command('nv_vi_big_a', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection([self.Region(2), self.Region(6)])


class Test__nv_vi_big_a_InVisualLineMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 3))

        self.view.run_command('nv_vi_big_a', {'mode': unittest.VISUAL_LINE, 'count': 1})

        self.assertSelection(3)


class Test__nv_vi_big_a_InVisualLineMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 4), (4, 7)])

        self.view.run_command('nv_vi_big_a', {'mode': unittest.VISUAL_LINE, 'count': 1})

        self.assertSelection([self.Region(3), self.Region(7)])


class Test__nv_vi_big_a_InVisualBlockMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('nv_vi_big_a', {'mode': unittest.VISUAL_BLOCK, 'count': 1})

        self.assertSelection(2)


class Test__nv_vi_big_a_InVisualBlockMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 2), (4, 6)])

        self.view.run_command('nv_vi_big_a', {'mode': unittest.VISUAL_BLOCK, 'count': 1})

        self.assertSelection([self.Region(2), self.Region(6)])
