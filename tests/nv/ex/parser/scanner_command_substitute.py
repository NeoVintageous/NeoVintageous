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

from NeoVintageous.nv.ex.parser.state import ScannerState
from NeoVintageous.nv.ex.parser.scanner_command_substitute import scan_command_substitute
from NeoVintageous.nv.ex.parser.scanner_command_substitute import TokenCommandSubstitute
from NeoVintageous.nv.ex.parser.scanner_command_substitute import TokenEof


def _scan(source, start=1, position=1):
    state = ScannerState(source)
    state.start = start
    state.position = position

    return scan_command_substitute(state)


def _create_expected(params):
    return (None, [TokenCommandSubstitute(params), TokenEof()])


class TestScanCommanSubstitute(unittest.TestCase):

    def test_none(self):
        self.assertEqual(
            _create_expected(None),
            _scan('', 0, 0))

        self.assertEqual(
            _create_expected(None),
            _scan('s'))

    def test_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'bad command'):
            _scan('s/')

        with self.assertRaisesRegex(ValueError, 'bad command'):
            _scan('s/abc')

    def test_basic(self):
        self.assertEqual(
            _create_expected({
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': [],
            }),
            _scan('s/abc/def/'))

    def test_basic_with_offset_start_and_position(self):
        self.assertEqual(
            _create_expected({
                'search_term': 'cmd',
                'replacement': 'shell_cmd',
                'count': 1,
                'flags': ['g'],
            }),
            _scan('1,$s/cmd/shell_cmd/g', 4, 4))

    def test_empty(self):
        self.assertEqual(
            _create_expected({
                'search_term': '',
                'replacement': '',
                'count': 1,
                'flags': [],
            }),
            _scan('s///'))

    def test_flags(self):
        self.assertEqual(
            _create_expected({
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g']
            }),
            _scan('s/abc/def/g'))

        self.assertEqual(
            _create_expected({
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['i']
            }),
            _scan('s/abc/def/i'))

        self.assertEqual(
            _create_expected({
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g', 'i']
            }),
            _scan('s/abc/def/gi'))

    def test_closing_delimiter_is_not_required(self):
        self.assertEqual(
            _create_expected({
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': []
            }),
            _scan('s/abc/def'))
