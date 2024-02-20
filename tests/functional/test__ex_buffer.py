# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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


class Test_ex_buffer(unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    @unittest.mock_bell()
    @unittest.mock.patch('NeoVintageous.nv.window.get_alternate_file_register')
    def test_no_alternate_buffer(self, get_alternate_file_register):
        get_alternate_file_register.return_value = None
        self.normal('fi|zz')
        self.feed(':buffer #')
        self.assertBell("E23: No alternate file")

    @unittest.mock_bell()
    @unittest.mock.patch('sublime.Window.open_file')
    @unittest.mock.patch('NeoVintageous.nv.window.get_alternate_file_register')
    def test_alternate_buffer(self, get_alternate_file_register, open_file):
        get_alternate_file_register.return_value = 'fname'
        self.normal('fi|zz')
        self.feed(':buffer #')
        open_file.assert_called_once_with('fname')
        self.assertNoBell()
