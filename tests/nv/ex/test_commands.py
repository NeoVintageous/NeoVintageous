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

from NeoVintageous.nv.ex.scanner import _ScannerState
from NeoVintageous.nv.ex_routes import scan_cmd_buffers
from NeoVintageous.nv.ex_routes import scan_cmd_cd
from NeoVintageous.nv.ex_routes import scan_cmd_close
from NeoVintageous.nv.ex_routes import scan_cmd_exit
from NeoVintageous.nv.ex_routes import scan_cmd_file
from NeoVintageous.nv.ex_routes import scan_cmd_global
from NeoVintageous.nv.ex_routes import scan_cmd_noremap
from NeoVintageous.nv.ex_routes import scan_cmd_only
from NeoVintageous.nv.ex_routes import scan_cmd_substitute
from NeoVintageous.nv.ex_routes import scan_cmd_tabnext
from NeoVintageous.nv.ex_routes import TokenCommand
from NeoVintageous.nv.ex_routes import TokenEof


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


class Test_scan_cmd_file(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_file(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('file'), TokenEof()]))

        actual = scan_cmd_file(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('file', forced=True), TokenEof()]))

        actual = scan_cmd_file(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('file', forced=False), TokenEof()]))

    def test_can_raise_exception(self):
        with self.assertRaises(Exception):
            scan_cmd_file(_ScannerState('x'))

        with self.assertRaises(Exception):
            scan_cmd_file(_ScannerState('!x'))

        with self.assertRaises(Exception):
            scan_cmd_file(_ScannerState('! '))

        with self.assertRaises(Exception):
            scan_cmd_file(_ScannerState(' '))


class Test_scan_cmd_global(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_global(_ScannerState('/111/print'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'print'}), TokenEof()]))  # noqa: E501

        actual = scan_cmd_global(_ScannerState('/111/p'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'p'}), TokenEof()]))  # noqa: E501

        actual = scan_cmd_global(_ScannerState('/111/delete'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'delete'}), TokenEof()]))  # noqa: E501

    def test_issue_181(self):
        actual = scan_cmd_global(_ScannerState('!/111/print'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, forced=True, params={'pattern': '111', 'cmd': 'print'}), TokenEof()]))  # noqa: E501

        actual = scan_cmd_global(_ScannerState('!/111/delete'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, forced=True, params={'pattern': '111', 'cmd': 'delete'}), TokenEof()]))  # noqa: E501


class Test_scan_cmd_only(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_only(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('only'), TokenEof()]))

        actual = scan_cmd_only(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('only', forced=True), TokenEof()]))

        actual = scan_cmd_only(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('only', forced=False), TokenEof()]))

    def test_can_raise_exception(self):
        with self.assertRaises(Exception):
            scan_cmd_only(_ScannerState('x'))

        with self.assertRaises(Exception):
            scan_cmd_only(_ScannerState('!x'))

        with self.assertRaises(Exception):
            scan_cmd_only(_ScannerState('! '))

        with self.assertRaises(Exception):
            scan_cmd_only(_ScannerState(' '))


class Test_scan_cmd_noremap(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_noremap(_ScannerState('w 2w'))
        self.assertEqual(actual, (None, [TokenCommand('noremap', params={'keys': 'w', 'command': '2w'}), TokenEof()]))


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


class Test_scan_cmd_tab_next(unittest.TestCase):

    def test_can_scan(self):
        actual = scan_cmd_tabnext(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('tabnext'), TokenEof()]))

        actual = scan_cmd_tabnext(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('tabnext', forced=True), TokenEof()]))

        actual = scan_cmd_tabnext(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('tabnext', forced=False), TokenEof()]))
