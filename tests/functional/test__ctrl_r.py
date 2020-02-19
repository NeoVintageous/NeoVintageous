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


class Test_ctrl_r(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('redo')
    @unittest.mock_bell()
    def test_ctrl_r_invokes_bell_when_nothing_to_redo(self):
        self.eq('fi|zz', '<C-r>', 'fi|zz')
        self.assertRunCommand('redo')
        self.assertBell('Already at newest change')

    @unittest.mock_run_commands('redo')
    @unittest.mock_bell()
    def test_ctrl_r_count(self):
        self.eq('fi|zz', '3<C-r>', 'fi|zz')
        self.assertRunCommand('redo', count=3)
        self.assertBell('Already at newest change')
