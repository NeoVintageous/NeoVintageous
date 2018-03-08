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
from NeoVintageous.nv.ex.cmd_buffers import TokenCommandBuffers
from NeoVintageous.nv.ex.cmd_buffers import TokenEof
from NeoVintageous.nv.ex.scanner_state import ScannerState


def _scan_cmd_buffers(source):
    return scan_cmd_buffers(ScannerState(source))


class Test_scan_cmd_buffers(unittest.TestCase):

    def assertScanEqual(self, actual, expected):
        actual = _scan_cmd_buffers(actual)
        expected = None, [TokenCommandBuffers(**expected), TokenEof()]

        self.assertEqual(actual, expected)
        # Workaround a potential bug, See TokenOfCommand.__eq__().
        self.assertEqual(actual[1][0].forced, expected[1][0].forced)

    def test_can_scan(self):
        self.assertScanEqual('', {})

    def test_raises_exception(self):
        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers(' ')

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers('x')

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers('foo')

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers('!')
