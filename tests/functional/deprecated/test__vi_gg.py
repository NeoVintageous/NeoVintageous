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


class Test_gg_InNormalMode(unittest.ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.select(5)
        self.view.run_command('nv_vi_gg', {'mode': unittest.NORMAL})
        self.assertSelection(0)

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.select(5)
        self.view.run_command('nv_vi_gg', {'mode': unittest.NORMAL})
        self.assertSelection(0)


class Test_gg_InVisualMode(unittest.ViewTestCase):

    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.select((1, 2))
        self.view.run_command('nv_vi_gg', {'mode': unittest.VISUAL})
        self.assertSelection((2, 0))

    def test_can_move_in_visual_mode__reversed(self):
        self.write('abc\nabc\n')
        self.select((2, 1))
        self.view.run_command('nv_vi_gg', {'mode': unittest.VISUAL})
        self.assertSelection((2, 0))


class Test_gg_InInternalNormalMode(unittest.ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc\nabc\n')
        self.select(1)
        self.view.run_command('nv_vi_gg', {'mode': unittest.INTERNAL_NORMAL})
        self.assertSelection((4, 0))


class Test_gg_InVisualLineMode(unittest.ViewTestCase):

    def test_can_move_in_visual_line_mode(self):
        self.write('abc\nabc\n')
        self.select((0, 4))
        self.view.run_command('nv_vi_gg', {'mode': unittest.VISUAL_LINE})
        self.assertSelection((4, 0))

    def test_extends_selection(self):
        self.write('abc\nabc\n')
        self.select((4, 8))
        self.view.run_command('nv_vi_gg', {'mode': unittest.VISUAL_LINE})
        self.assertSelection((8, 0))
