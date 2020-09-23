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


class Test__nv_vi_ctrl_r(unittest.ViewTestCase):

    def test_does_not_linger_past_soft_eol(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('nv_vi_dd', {'mode': unittest.INTERNAL_NORMAL})
        self.view.window().run_command('nv_vi_u')
        self.view.window().run_command('nv_vi_ctrl_r')  # passing mode is irrelevant

        self.assertContent('abc\nabc\nabc')
        self.assertSelection(4)

    def test_does_not_linger_past_soft_eol2(self):
        self.write('abc\nxxx foo bar\nabc\nabc')
        self.select(12)

        self.view.run_command('nv_vi_big_d', {'mode': unittest.INTERNAL_NORMAL})
        self.view.window().run_command('nv_vi_u')
        self.view.window().run_command('nv_vi_ctrl_r')  # passing mode is irrelevant

        self.assertContent('abc\nxxx foo \nabc\nabc')
        self.assertSelection(11)
