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


class Test__nv_vi_e_InNormalMode(unittest.ViewTestCase):

    def test_move_to_end_of_word__on_last_line(self):
        self.write('abc\nabc\nabc')
        self.select(8)

        self.view.run_command('nv_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(10)

    def test_move_to_end_of_word__on_middle_line__with_trailing_whitespace(self):
        self.write('abc\nabc   \nabc')
        self.select(6)

        self.view.run_command('nv_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(13)

    def test_move_to_end_of_word__on_last_line__with_trailing_whitespace(self):
        self.write('abc\nabc\nabc   ')
        self.select(8)

        self.view.run_command('nv_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(10)

        self.view.run_command('nv_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(13)


class Test__nv_vi_e_InVisualMode(unittest.ViewTestCase):

    def test_move_to_end_of_word__on_last_line2(self):
        self.write('abc abc abc')
        self.select((0, 2))

        self.view.run_command('nv_vi_e', {'mode': unittest.VISUAL, 'count': 3})

        self.assertSelection((0, 11))
