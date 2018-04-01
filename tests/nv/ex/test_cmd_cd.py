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

from NeoVintageous.nv.ex.cmd_cd import scan_cmd_cd
from NeoVintageous.nv.ex.cmd_cd import TokenCommand
from NeoVintageous.nv.ex.cmd_cd import TokenEof
from NeoVintageous.nv.ex.scanner import _ScannerState


class Test_scan_cmd_cd(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_cd(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('cd', params={'-': None, 'path': None}), TokenEof()]))

        actual = scan_cmd_cd(_ScannerState(' /tmp/foo/bar'))
        self.assertEqual(actual, (None, [TokenCommand('cd', params={'-': None, 'path': '/tmp/foo/bar'}, forced=False), TokenEof()]))  # noqa: E501

        actual = scan_cmd_cd(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('cd', params={'-': None, 'path': None}, forced=True), TokenEof()]))  # noqa: E501

    def test_not_implemented(self):
        with self.assertRaises(Exception):
            scan_cmd_cd(_ScannerState(' -'))
