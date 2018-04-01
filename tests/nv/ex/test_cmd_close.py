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

from NeoVintageous.nv.ex.cmd_close import scan_cmd_close
from NeoVintageous.nv.ex.cmd_close import TokenCommand
from NeoVintageous.nv.ex.cmd_close import TokenEof
from NeoVintageous.nv.ex.scanner import _ScannerState


class Test_scan_cmd_close(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_close(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('close'), TokenEof()]))

        actual = scan_cmd_close(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('close', forced=True), TokenEof()]))

        actual = scan_cmd_close(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('close', forced=False), TokenEof()]))

    def test_raises_exception(self):
        # TODO [bug] Currently ":close" followed by character not "!" is accepted
        # and it shouldn't be e.g. ":closex" is currently a valid command.

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            scan_cmd_close(_ScannerState('  '))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            scan_cmd_close(_ScannerState('! '))

        # "x" shouldn't be valid, oppose "y", see TODO above.
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got y instead'):
            scan_cmd_close(_ScannerState('xy'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got x instead'):
            scan_cmd_close(_ScannerState('!x'))

        # "b" shouldn't be valid, oppose to "a", see TODO above.
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got a instead'):
            scan_cmd_close(_ScannerState('baz'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got f instead'):
            scan_cmd_close(_ScannerState('!foo'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got ! instead'):
            scan_cmd_close(_ScannerState('!!'))
