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

import re

import unittest

from NeoVintageous.nv.ex.scanner import _ScannerState
from NeoVintageous.nv.ex_routes import _ex_route_buffers
from NeoVintageous.nv.ex_routes import _ex_route_cd
from NeoVintageous.nv.ex_routes import _ex_route_close
from NeoVintageous.nv.ex_routes import _ex_route_file
from NeoVintageous.nv.ex_routes import _ex_route_global
from NeoVintageous.nv.ex_routes import _ex_route_noremap
from NeoVintageous.nv.ex_routes import _ex_route_only
from NeoVintageous.nv.ex_routes import _ex_route_onoremap
from NeoVintageous.nv.ex_routes import _ex_route_substitute
from NeoVintageous.nv.ex_routes import _ex_route_tabnext
from NeoVintageous.nv.ex_routes import ex_routes
from NeoVintageous.nv.ex_routes import TokenCommand
from NeoVintageous.nv.ex_routes import TokenEof


class Test_ex_route_buffers(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_buffers(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('buffers'), TokenEof()]))


class Test_ex_route_cd(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_cd(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('cd', params={'-': None, 'path': None}), TokenEof()]))

        actual = _ex_route_cd(_ScannerState(' /tmp/foo/bar'))
        self.assertEqual(actual, (None, [TokenCommand('cd', params={'-': None, 'path': '/tmp/foo/bar'}, forced=False), TokenEof()]))  # noqa: E501

        actual = _ex_route_cd(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('cd', params={'-': None, 'path': None}, forced=True), TokenEof()]))  # noqa: E501

    def test_not_implemented(self):
        with self.assertRaises(Exception):
            _ex_route_cd(_ScannerState(' -'))


class Test_ex_route_close(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_close(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('close'), TokenEof()]))

        actual = _ex_route_close(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('close', forced=True), TokenEof()]))

        actual = _ex_route_close(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('close', forced=False), TokenEof()]))

    def test_raises_exception(self):
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            _ex_route_close(_ScannerState('  '))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            _ex_route_close(_ScannerState('! '))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got x instead'):
            _ex_route_close(_ScannerState('xy'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got x instead'):
            _ex_route_close(_ScannerState('!x'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got b instead'):
            _ex_route_close(_ScannerState('baz'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got f instead'):
            _ex_route_close(_ScannerState('!foo'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got ! instead'):
            _ex_route_close(_ScannerState('!!'))


class Test_ex_route_file(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_file(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('file'), TokenEof()]))

        actual = _ex_route_file(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('file', forced=False), TokenEof()]))

    def test_can_raise_exception(self):
        with self.assertRaises(Exception):
            _ex_route_file(_ScannerState('x'))

        with self.assertRaises(Exception):
            _ex_route_file(_ScannerState('!x'))

        with self.assertRaises(Exception):
            _ex_route_file(_ScannerState('! '))

        with self.assertRaises(Exception):
            _ex_route_file(_ScannerState(' '))


class Test_ex_route_global(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_global(_ScannerState('/111/print'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'print'}), TokenEof()]))  # noqa: E501

        actual = _ex_route_global(_ScannerState('/111/p'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'p'}), TokenEof()]))  # noqa: E501

        actual = _ex_route_global(_ScannerState('/111/delete'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'delete'}), TokenEof()]))  # noqa: E501

    def test_issue_181(self):
        actual = _ex_route_global(_ScannerState('!/111/print'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, forced=True, params={'pattern': '111', 'cmd': 'print'}), TokenEof()]))  # noqa: E501

        actual = _ex_route_global(_ScannerState('!/111/delete'))
        self.assertEqual(actual, (None, [TokenCommand('global', addressable=True, forced=True, params={'pattern': '111', 'cmd': 'delete'}), TokenEof()]))  # noqa: E501


class Test_ex_route_noremap(unittest.TestCase):

    def test_ex_route_noremap(self):
        actual = _ex_route_noremap(_ScannerState('w 2w'))
        self.assertEqual(actual, (None, [TokenCommand('noremap', params={'keys': 'w', 'command': '2w'}), TokenEof()]))


class Test_ex_route_only(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_only(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('only'), TokenEof()]))

        actual = _ex_route_only(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('only', forced=True), TokenEof()]))

        actual = _ex_route_only(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('only', forced=False), TokenEof()]))

    def test_can_raise_exception(self):
        with self.assertRaises(Exception):
            _ex_route_only(_ScannerState('!x'))

        with self.assertRaises(Exception):
            _ex_route_only(_ScannerState('! '))


class Test_ex_route_onoremap(unittest.TestCase):

    def test_ex_route_onoremap(self):
        actual = _ex_route_onoremap(_ScannerState('L $'))
        self.assertEqual(actual, (None, [TokenCommand('onoremap', params={'keys': 'L', 'command': '$'}), TokenEof()]))


class Test_ex_route_substitute(unittest.TestCase):

    def test_none(self):
        actual = _ex_route_substitute(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('substitute', addressable=True), TokenEof()]))

    def test_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'bad command'):
            _ex_route_substitute(_ScannerState('/'))

        with self.assertRaisesRegex(ValueError, 'bad command'):
            _ex_route_substitute(_ScannerState('/abc'))

    def _test_ex_route_substitute(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': [],
            }), TokenEof()])
        )

    def test_empty(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('///')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': '',
                'replacement': '',
                'count': 1,
                'flags': [],
            }), TokenEof()])
        )

    def test_flags(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/g')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g']
            }), TokenEof()])
        )

        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/i')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['i']
            }), TokenEof()])
        )

        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/gi')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g', 'i']
            }), TokenEof()])
        )

    def test_closing_delimiter_is_not_required(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def')),
            (None, [TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': []
            }), TokenEof()])
        )


class Test_ex_route_tabnext(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_tabnext(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('tabnext'), TokenEof()]))

        actual = _ex_route_tabnext(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('tabnext', forced=True), TokenEof()]))

        actual = _ex_route_tabnext(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('tabnext', forced=False), TokenEof()]))


class TestRoutes(unittest.TestCase):

    def _matchRoute(self, string):
        for route, command in ex_routes.items():
            match = re.compile(route).match(string)
            if match:
                return (match, route, command)

        return None

    def assertNotRoute(self, string):
        self.assertEquals(self._matchRoute(string), None, 'failed asserting no route for {}'.format(string))

    def assertRoute(self, expected, values, multiple_matches=False):
        for value in values:
            match, route, command = self._matchRoute(value)
            self.assertEqual(command.__name__, expected)
            self.assertEqual(match.group(0), value, 'failed at "{}"'.format(value))

    def test_invalid_routes(self):

        self.assertNotRoute(' ')
        self.assertNotRoute('$')
        self.assertNotRoute('')
        self.assertNotRoute('zfoobar')

    def test_valid_routes(self):

        self.assertRoute('_ex_route_bfirst', ['bfirst', 'bf', 'brewind', 'br'])
        self.assertRoute('_ex_route_blast', ['blast', 'bl'])
        self.assertRoute('_ex_route_bnext', ['bnext', 'bn'])
        self.assertRoute('_ex_route_bprevious', ['bNext', 'bN', 'bprevious', 'bp'])
        self.assertRoute('_ex_route_browse', ['browse', 'bro'])
        self.assertRoute('_ex_route_buffers', ['files', 'buffers', 'ls'])
        self.assertRoute('_ex_route_cd', ['cd'])
        self.assertRoute('_ex_route_close', ['close', 'clo'])
        self.assertRoute('_ex_route_copy', ['copy', 'co'])
        self.assertRoute('_ex_route_cquit', ['cquit', 'cq'])
        self.assertRoute('_ex_route_delete', ['delete', 'd'])
        self.assertRoute('_ex_route_edit', ['edit', 'e'])
        self.assertRoute('_ex_route_exit', ['exit', 'exi', 'xit', 'x'])
        self.assertRoute('_ex_route_file', ['file', 'f'])
        self.assertRoute('_ex_route_help', ['help', 'h'])
        self.assertRoute('_ex_route_let', ['let '])
        self.assertRoute('_ex_route_move', ['move', 'm'])
        self.assertRoute('_ex_route_new', ['new'])
        self.assertRoute('_ex_route_nnoremap', ['nnoremap', 'nn'])
        self.assertRoute('_ex_route_noremap', ['noremap', 'no'])
        self.assertRoute('_ex_route_nunmap', ['nunmap', 'nun'])
        self.assertRoute('_ex_route_only', ['only', 'on'])
        self.assertRoute('_ex_route_onoremap', ['onoremap', 'ono'])
        self.assertRoute('_ex_route_ounmap', ['ounmap', 'ou'])
        self.assertRoute('_ex_route_print', ['print', 'p'])
        self.assertRoute('_ex_route_pwd', ['pwd', 'pw'])
        self.assertRoute('_ex_route_qall', ['qall', 'qa'])
        self.assertRoute('_ex_route_quit', ['quit', 'q'])
        self.assertRoute('_ex_route_read', ['read', 'r'])
        self.assertRoute('_ex_route_registers', ['registers', 'reg'])
        self.assertRoute('_ex_route_set', ['set', 'se'])
        self.assertRoute('_ex_route_setlocal', ['setlocal', 'setl'])
        self.assertRoute('_ex_route_shell', ['shell', 'sh'])
        self.assertRoute('_ex_route_snoremap', ['snoremap', 'snor'])
        self.assertRoute('_ex_route_sort', ['sort', 'sor'])
        self.assertRoute('_ex_route_split', ['split', 'sp'])
        self.assertRoute('_ex_route_substitute', ['substitute', 's'])
        self.assertRoute('_ex_route_sunmap', ['sunmap', 'sunm'])
        self.assertRoute('_ex_route_tabclose', ['tabclose', 'tabc'])
        self.assertRoute('_ex_route_tabfirst', ['tabfirst', 'tabfir', 'tabrewind', 'tabr'])
        self.assertRoute('_ex_route_tablast', ['tablast', 'tabl'])
        self.assertRoute('_ex_route_tabnext', ['tabnext', 'tabn'])
        self.assertRoute('_ex_route_tabonly', ['tabonly', 'tabo'])
        self.assertRoute('_ex_route_tabprevious', ['tabNext', 'tabN', 'tabprevious', 'tabp'])
        self.assertRoute('_ex_route_unmap', ['unmap', 'unm'])
        self.assertRoute('_ex_route_vnoremap', ['vnoremap', 'vn'])
        self.assertRoute('_ex_route_vsplit', ['vsplit', 'vs'])
        self.assertRoute('_ex_route_vunmap', ['vunmap', 'vu'])
        self.assertRoute('_ex_route_wall', ['wall', 'wa'])
        self.assertRoute('_ex_route_wq', ['wq'])
        self.assertRoute('_ex_route_wqall', ['wqall', 'wqa', 'xall', 'xa'])
        self.assertRoute('_ex_route_write', ['write', 'w'])
        self.assertRoute('_ex_route_yank', ['yank', 'y'])
