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


class Test_ex_tabnext(unittest.FunctionalTestCase):

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.window_tab_control')
    def test_n_tnext(self, window_tab_control):
        self.eq('f|izz', ':tabnext', 'f|izz')
        window_tab_control.assert_called_once_with(self.view.window(), action='next')
