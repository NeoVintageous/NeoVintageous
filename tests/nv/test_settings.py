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

import os

from NeoVintageous.tests import unittest

from NeoVintageous.nv.settings import get_cmdline_cwd
from NeoVintageous.nv.settings import set_cmdline_cwd


class TestCmdlineCwd(unittest.ViewTestCase):

    @unittest.mock.patch('NeoVintageous.nv.settings.active_window')
    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', clear=True)
    def test_returns_cwd(self, active_window, *args):
        active_window.return_value = None
        self.assertEqual(get_cmdline_cwd(), os.getcwd())

    @unittest.mock.patch('sublime.Window.extract_variables')
    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', clear=True)
    def test_returns_cwd_when_no_folder_variable_found(self, extract_variables):
        extract_variables.return_value = {}
        self.assertEqual(get_cmdline_cwd(), os.getcwd())

    @unittest.mock.patch('sublime.Window.extract_variables')
    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', clear=True)
    def test_returns_cwd_folder_variable(self, extract_variables):
        extract_variables.return_value = {'folder': '/tmp/folder'}
        self.assertEqual(get_cmdline_cwd(), '/tmp/folder')

    def test_returns_set_cwd(self):
        set_cmdline_cwd('/tmp/fizz')
        self.assertEqual(get_cmdline_cwd(), '/tmp/fizz')
