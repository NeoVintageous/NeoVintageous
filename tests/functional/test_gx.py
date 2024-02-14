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


class Test_gx(unittest.FunctionalTestCase):

    @unittest.mock.patch('webbrowser.open_new_tab')
    def test_gx(self, open_new_tab):
        self.eq('x https://exa|mple.com x', 'n_gx', 'x https://exa|mple.com x')
        open_new_tab.assert_called_once_with('https://example.com')

    @unittest.mock.patch('webbrowser.open_new_tab')
    def test_gx_localhost(self, open_new_tab):
        self.eq('x http://local|host:5173 x', 'n_gx', 'x http://local|host:5173 x')
        open_new_tab.assert_called_once_with('http://localhost:5173')

    @unittest.mock.patch('webbrowser.open_new_tab')
    def test_gx_noop(self, open_new_tab):
        self.eq('fi|zz', 'n_gx', 'fi|zz')
        self.assertMockNotCalled(open_new_tab)
