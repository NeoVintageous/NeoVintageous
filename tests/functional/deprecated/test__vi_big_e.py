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


class Test__nv_vi_big_e(unittest.ViewTestCase):

    def test_normal(self):
        self.write('01. 4')
        self.select(1)
        self.view.run_command('nv_vi_big_e', {'mode': unittest.NORMAL, 'count': 1})
        self.assertSelection(2)

    def test_internal_normal(self):
        self.write('012 4')
        self.select(1)
        self.view.run_command('nv_vi_big_e', {'mode': unittest.INTERNAL_NORMAL, 'count': 1})
        self.assertSelection((1, 3))

    def test_visual_forward(self):
        self.write('0ab3 5')
        self.select((1, 3))
        self.view.run_command('nv_vi_big_e', {'mode': unittest.VISUAL, 'count': 1})
        self.assertSelection((1, 4))

    def test_visual_reverse_no_crossover(self):
        self.write('0b2 a5')
        self.select((5, 1))
        self.view.run_command('nv_vi_big_e', {'mode': unittest.VISUAL, 'count': 1})
        self.assertSelection((5, 2))

    def test_visual_reverse_crossover(self):
        self.write('0ba3 5')
        self.select((3, 1))
        self.view.run_command('nv_vi_big_e', {'mode': unittest.VISUAL, 'count': 1})
        self.assertSelection((2, 4))
