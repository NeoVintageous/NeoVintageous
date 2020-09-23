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


class Test__nv_vi_l_InNormalMode(unittest.ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('nv_vi_l', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(1)

    def test_can_move_in_normal_mode_with_count(self):
        self.write('foo bar baz')
        self.select(0)

        self.view.run_command('nv_vi_l', {'mode': unittest.NORMAL, 'count': 10})

        self.assertSelection(10)

    def test_stops_at_right_end_in_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('nv_vi_l', {'mode': unittest.NORMAL, 'count': 10000})

        self.assertSelection(2)


class Test__nv_vi_l_InInternalNormalMode(unittest.ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('nv_vi_l', {'mode': unittest.INTERNAL_NORMAL, 'count': 1})

        self.assertSelection((0, 1))

    def test_can_move_in_internal_normal_mode_with_count(self):
        self.write('foo bar baz')
        self.select(0)

        self.view.run_command('nv_vi_l', {'mode': unittest.INTERNAL_NORMAL, 'count': 10})

        self.assertSelection((0, 10))

    def test_stops_at_right_end_in_internal_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('nv_vi_l', {'mode': unittest.INTERNAL_NORMAL, 'count': 10000})

        self.assertSelection((0, 3))


class Test__nv_vi_l_InVisualMode(unittest.ViewTestCase):

    def test_can_move(self):
        self.write('abc')
        self.select((0, 1))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection((0, 2))

    def test_can_move_reversed_no_cross_over(self):
        self.write('abc')
        self.select((2, 0))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection((2, 1))

    def test_can_move_reversed_minimal(self):
        self.write('abc')
        self.select((1, 0))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection((0, 2))

    def test_can_move_reversed_cross_over(self):
        self.write('foo bar baz')
        self.select((5, 0))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 5})

        self.assertSelection((4, 6))

    def test_can_move_reversed_different_lines(self):
        self.write('foo\nbar\n')
        self.select((5, 1))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection((5, 2))

    def test_stops_at_eol_different_lines_reversed(self):
        self.write('foo\nbar\n')
        self.select((5, 3))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 1})

        self.assertSelection((5, 3))

    def test_stops_at_eol_different_lines_reversed_large_count(self):
        self.write('foo\nbar\n')
        self.select((5, 3))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 100})

        self.assertSelection((5, 3))

    def test_can_move_with_count(self):
        self.write('foo bar fuzz buzz')
        self.select((0, 1))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 10})

        self.assertSelection((0, 11))

    def test_stops_at_right_end(self):
        self.write('abc\n')
        self.select((0, 1))

        self.view.run_command('nv_vi_l', {'mode': unittest.VISUAL, 'count': 10000})

        self.assertSelection((0, 4))
