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

from NeoVintageous.nv.ex.cmd_buffers import scan_cmd_buffers
from NeoVintageous.nv.ex.cmd_buffers import TokenCommand
from NeoVintageous.nv.ex.cmd_buffers import TokenEof
from NeoVintageous.nv.ex.scanner import _ScannerState


class Test_scan_cmd_buffers(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_buffers(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('buffers', target='ex_prompt_select_open_file'), TokenEof()]))

    def test_raises_exception(self):
        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            scan_cmd_buffers(_ScannerState(' '))

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            scan_cmd_buffers(_ScannerState('x'))

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            scan_cmd_buffers(_ScannerState('foo'))

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            scan_cmd_buffers(_ScannerState('!'))
