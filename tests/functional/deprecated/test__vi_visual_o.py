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


class Test__nv_vi_visual_o_InNormalMode(unittest.ViewTestCase):

    def test_doesnt_do_anything(self):
        self.write('abc')
        self.select((2, 0))

        self.view.run_command('nv_vi_visual_o', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection((2, 0))


class Test__nv_vi_visual_o_InInternalNormalMode(unittest.ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc')
        self.select((2, 0))

        self.view.run_command('nv_vi_visual_o', {'mode': unittest.INTERNAL_NORMAL, 'count': 1})

        self.assertSelection((2, 0))


class Test__nv_vi_visual_o_InVisualMode(unittest.ViewTestCase):

    def test_can_move(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('nv_vi_visual_o', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection((2, 0))


class Test__nv_vi_visual_o_InVisualLineMode(unittest.ViewTestCase):

    def test_can_move(self):
        self.write('abc\ndef')
        self.select((0, 4))

        self.view.run_command('nv_vi_visual_o', {'mode': unittest.VISUAL_LINE, 'count': 1})

        self.assertSelection((4, 0))
