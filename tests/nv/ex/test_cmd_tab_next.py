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

import unittest

from NeoVintageous.nv.ex.cmd_tab_next import scan_cmd_tab_next
from NeoVintageous.nv.ex.cmd_tab_next import TokenCommandTabNext
from NeoVintageous.nv.ex.cmd_tab_next import TokenEof
from NeoVintageous.nv.ex.scanner_state import ScannerState


def _scan_cmd_tab_next(source):
    return scan_cmd_tab_next(ScannerState(source))


class Test_scan_cmd_tab_next(unittest.TestCase):

    def assertScanEqual(self, actual, expected):
        actual = _scan_cmd_tab_next(actual)
        expected = (None, [TokenCommandTabNext(**expected), TokenEof()])

        self.assertEqual(actual, expected)
        # Workaround a potential bug, See TokenOfCommand.__eq__().
        self.assertEqual(actual[1][0].forced, expected[1][0].forced)

    def test_can_scan(self):
        self.assertScanEqual('', {})
        self.assertScanEqual('', {'forced': False})
        self.assertScanEqual('!', {'forced': True})
