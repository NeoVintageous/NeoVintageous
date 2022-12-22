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


class Test_ctrl_hat(unittest.FunctionalTestCase):

    @unittest.mock_bell()
    @unittest.mock.patch('NeoVintageous.nv.commands.get_alternate_file_register')
    def test_n_no_alternate_file(self, get_alternate_file_register):
        get_alternate_file_register.return_value = None
        self.eq('fi|zz', 'n_<C-^>', 'fi|zz')
        self.assertBell("E23: No alternate file")

    @unittest.mock.patch('sublime.Window.open_file')
    @unittest.mock.patch('NeoVintageous.nv.commands.get_alternate_file_register')
    def test_n(self, get_alternate_file_register, open_file):
        get_alternate_file_register.return_value = 'fname'
        self.eq('fi|zz', 'n_<C-^>', 'fi|zz')
        open_file.assert_called_once_with('fname')
