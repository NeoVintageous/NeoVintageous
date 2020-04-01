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


class Test_gf(unittest.FunctionalTestCase):

    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_gf(self, open_file):
        self.eq('x path/to/READ|ME.md y', 'n_gf', 'x path/to/READ|ME.md y')
        self.assertEqual(open_file.call_args[0][1], 'path/to/README.md')

    @unittest.mock_status_message()
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_gf_no_file_name_under_cursor(self, open_file):
        self.eq('|', 'n_gf', '|')
        self.assertMockNotCalled(open_file)
        self.assertStatusMessage('E446: No file name under cursor')
