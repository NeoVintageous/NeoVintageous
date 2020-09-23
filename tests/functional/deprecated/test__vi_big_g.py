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


class Test__nv_vi_big_g_InNormalMode(unittest.ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.select(0)

        self.view.run_command('nv_vi_big_g', {'mode': unittest.NORMAL})

        self.assertSelection((4, 4))

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.select(0)

        self.view.run_command('nv_vi_big_g', {'mode': unittest.NORMAL})

        self.assertSelection((8, 8))


class Test__nv_vi_big_g_InVisualMode(unittest.ViewTestCase):

    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.select((0, 1))

        self.view.run_command('nv_vi_big_g', {'mode': unittest.VISUAL})

        self.assertSelection((0, 8))


class Test__nv_vi_big_g_InInternalNormalMode(unittest.ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc\nabc\n')
        self.select(1)

        self.view.run_command('nv_vi_big_g', {'mode': unittest.INTERNAL_NORMAL})

        self.assertSelection((0, 8))

    def test_operates_linewise(self):
        self.write('abc\nabc\nabc\n')
        self.select((4, 5))

        self.view.run_command('nv_vi_big_g', {'mode': unittest.INTERNAL_NORMAL})

        self.assertSelection((4, 12))


class Test__nv_vi_big_g_InVisualLineMode(unittest.ViewTestCase):

    def test_can_move_in_visual_line_mode(self):
        self.write('abc\nabc\n')
        self.select((0, 4))

        self.view.run_command('nv_vi_big_g', {'mode': unittest.VISUAL_LINE})

        self.assertSelection((0, 8))
