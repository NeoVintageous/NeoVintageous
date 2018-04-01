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

from NeoVintageous.nv.ex.cmd_substitute import scan_cmd_substitute
from NeoVintageous.nv.ex.cmd_substitute import TokenCommand
from NeoVintageous.nv.ex.cmd_substitute import TokenEof
from NeoVintageous.nv.ex.scanner import _ScannerState


class Test_scan_cmd_substitute(unittest.TestCase):

    def test_none(self):
        actual = scan_cmd_substitute(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('substitute', addressable=True), TokenEof()]))

    def test_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'bad command'):
            scan_cmd_substitute(_ScannerState('/'))

        with self.assertRaisesRegex(ValueError, 'bad command'):
            scan_cmd_substitute(_ScannerState('/abc'))

    def test_scan_cmd_substitute(self):
        self.assertEqual(
            scan_cmd_substitute(_ScannerState('/abc/def/')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': [],
            }), TokenEof()])
        )

    def test_empty(self):
        self.assertEqual(
            scan_cmd_substitute(_ScannerState('///')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': '',
                'replacement': '',
                'count': 1,
                'flags': [],
            }), TokenEof()])
        )

    def test_flags(self):
        self.assertEqual(
            scan_cmd_substitute(_ScannerState('/abc/def/g')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g']
            }), TokenEof()])
        )

        self.assertEqual(
            scan_cmd_substitute(_ScannerState('/abc/def/i')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['i']
            }), TokenEof()])
        )

        self.assertEqual(
            scan_cmd_substitute(_ScannerState('/abc/def/gi')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g', 'i']
            }), TokenEof()])
        )

    def test_closing_delimiter_is_not_required(self):
        self.assertEqual(
            scan_cmd_substitute(_ScannerState('/abc/def')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': []
            }), TokenEof()])
        )
