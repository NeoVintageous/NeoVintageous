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

from NeoVintageous.nv.ex.cmd_exit import scan_cmd_exit
from NeoVintageous.nv.ex.cmd_exit import TokenCommand
from NeoVintageous.nv.ex.cmd_exit import TokenEof
from NeoVintageous.nv.ex.scanner import _ScannerState


class Test_scan_cmd_exit(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_exit(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': ''}), TokenEof()]))  # noqa: E501

        actual = scan_cmd_exit(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': ''}, forced=False), TokenEof()]))  # noqa: E501

        actual = scan_cmd_exit(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': ''}, forced=True), TokenEof()]))  # noqa: E501

        actual = scan_cmd_exit(_ScannerState('/tmp/path/to/file'))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': '/tmp/path/to/file'}), TokenEof()]))  # noqa: E501
