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


class Test_ga(unittest.FunctionalTestCase):

    @unittest.mock_status_message()
    def test_ga(self):
        self.eq('a|bc', 'ga', 'a|bc')
        self.eq('a|bc', ':ascii', 'a|bc')
        self.eq('a|bc', ':as', 'a|bc')
        self.assertStatusMessage('    <b>  98,  Hex 0x62,  Octal 0o142', count=3)

    @unittest.mock_status_message()
    def test_ga_space(self):
        self.eq('a| b', 'ga', 'a| b')
        self.eq('a| b', ':ascii', 'a| b')
        self.assertStatusMessage('<Space>  32,  Hex 0x20,  Octal  0o40', count=2)

    @unittest.mock_status_message()
    def test_ga_newline(self):
        self.eq('a|\nb', 'ga', 'a|\nb')
        self.eq('a|\nb', ':ascii', 'a|\nb')
        self.assertStatusMessage('   <NL>  10,  Hex  0xa,  Octal  0o12', count=2)

    @unittest.mock_status_message()
    def test_ga_null(self):
        self.eq('|', 'ga', '|')
        self.eq('|', ':ascii', '|')
        self.assertStatusMessage('  <Nul>   0,  Hex  0x0,  Octal   0o0', count=2)

    @unittest.mock_status_message()
    def test_ga_tab(self):
        self.settings().set('translate_tabs_to_spaces', False)
        self.eq('a|\tb', 'ga', 'a|\tb')
        self.eq('a|\tb', ':ascii', 'a|\tb')
        self.assertStatusMessage('  <Tab>   9,  Hex  0x9,  Octal  0o11', count=2)
