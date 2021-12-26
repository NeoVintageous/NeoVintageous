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


class Test_ex_route_buffers(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_buffers(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('buffers'))


class Test_ex_route_cd(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_cd(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('cd'))

        actual = _ex_route_cd(_ScannerState(' /tmp/foo/bar'))
        self.assertEqual(actual, TokenCommand('cd', params={'path': '/tmp/foo/bar'}, forced=False))  # noqa: E501

        actual = _ex_route_cd(_ScannerState('!'))
        self.assertEqual(actual, TokenCommand('cd', forced=True))  # noqa: E501

    def test_not_implemented(self):
        with self.assertRaises(Exception):
            _ex_route_cd(_ScannerState(' -'))


class Test_ex_route_close(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_close(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('close'))

        actual = _ex_route_close(_ScannerState('!'))
        self.assertEqual(actual, TokenCommand('close', forced=True))

        actual = _ex_route_close(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('close', forced=False))


class Test_ex_route_file(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_file(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('file'))

        actual = _ex_route_file(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('file', forced=False))


class Test_ex_route_global(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_global(_ScannerState('/111/print'))
        self.assertEqual(actual, TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'print'}))  # noqa: E501

        actual = _ex_route_global(_ScannerState('/111/p'))
        self.assertEqual(actual, TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'p'}))  # noqa: E501

        actual = _ex_route_global(_ScannerState('/111/delete'))
        self.assertEqual(actual, TokenCommand('global', addressable=True, params={'pattern': '111', 'cmd': 'delete'}))  # noqa: E501

    def test_issue_181(self):
        actual = _ex_route_global(_ScannerState('!/111/print'))
        self.assertEqual(actual, TokenCommand('global', addressable=True, forced=True, params={'pattern': '111', 'cmd': 'print'}))  # noqa: E501

        actual = _ex_route_global(_ScannerState('!/111/delete'))
        self.assertEqual(actual, TokenCommand('global', addressable=True, forced=True, params={'pattern': '111', 'cmd': 'delete'}))  # noqa: E501


class Test_ex_route_noremap(unittest.TestCase):

    def test_ex_route_noremap(self):
        actual = _ex_route_noremap(_ScannerState('w 2w'))
        self.assertEqual(actual, TokenCommand('noremap', params={'lhs': 'w', 'rhs': '2w'}))


class Test_ex_route_only(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_only(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('only'))

        actual = _ex_route_only(_ScannerState('!'))
        self.assertEqual(actual, TokenCommand('only', forced=True))

        actual = _ex_route_only(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('only', forced=False))


class Test_ex_route_onoremap(unittest.TestCase):

    def test_ex_route_onoremap(self):
        actual = _ex_route_onoremap(_ScannerState('L $'))
        self.assertEqual(actual, TokenCommand('onoremap', params={'lhs': 'L', 'rhs': '$'}))


class Test_ex_route_substitute(unittest.TestCase):

    def test_none(self):
        actual = _ex_route_substitute(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('substitute', addressable=True))

    def test_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'bad command'):
            _ex_route_substitute(_ScannerState('/'))

        with self.assertRaisesRegex(ValueError, 'bad command'):
            _ex_route_substitute(_ScannerState('/abc'))

    def _test_ex_route_substitute(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/')),
            TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': [],
            })
        )

    def test_empty(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('///')),
            TokenCommand('substitute', addressable=True, params={
                'pattern': '',
                'replacement': '',
                'count': 1,
                'flags': [],
            })
        )

    def test_flags(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/g')),
            TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g']
            })
        )

        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/i')),
            TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['i']
            })
        )

        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def/gi')),
            TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g', 'i']
            })
        )

    def test_closing_delimiter_is_not_required(self):
        self.assertEqual(
            _ex_route_substitute(_ScannerState('/abc/def')),
            TokenCommand('substitute', addressable=True, params={
                'pattern': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': []
            })
        )


class Test_ex_route_tabnext(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_tabnext(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('tabnext'))

        actual = _ex_route_tabnext(_ScannerState('!'))
        self.assertEqual(actual, TokenCommand('tabnext', forced=True))

        actual = _ex_route_tabnext(_ScannerState(''))
        self.assertEqual(actual, TokenCommand('tabnext', forced=False))


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
        self.assertRoute('_ex_route_buffer', ['buffer', 'b'])
        self.assertRoute('_ex_route_buffers', ['files', 'buffers', 'ls'])
        self.assertRoute('_ex_route_cd', ['cd'])
        self.assertRoute('_ex_route_close', ['close', 'clo'])
        self.assertRoute('_ex_route_copy', ['copy', 'co'])
        self.assertRoute('_ex_route_cquit', ['cquit', 'cq'])
        self.assertRoute('_ex_route_delete', ['delete', 'd'])
        self.assertRoute('_ex_route_edit', ['edit', 'e'])
        self.assertRoute('_ex_route_exit', ['exit', 'exi', 'xit', 'x'])
        self.assertRoute('_ex_route_file', ['file', 'f'])
        self.assertRoute('_ex_route_global', ['global', 'g'])
        self.assertRoute('_ex_route_help', ['help', 'h'])
        self.assertRoute('_ex_route_history', ['history', 'his'])
        self.assertRoute('_ex_route_inoremap', ['inoremap', 'ino'])
        self.assertRoute('_ex_route_let', ['let '])
        self.assertRoute('_ex_route_move', ['move', 'm'])
        self.assertRoute('_ex_route_new', ['new'])
        self.assertRoute('_ex_route_nnoremap', ['nnoremap', 'nn'])
        self.assertRoute('_ex_route_nohlsearch', ['nohlsearch', 'noh'])
        self.assertRoute('_ex_route_noremap', ['noremap', 'no'])
        self.assertRoute('_ex_route_nunmap', ['nunmap', 'nun'])
        self.assertRoute('_ex_route_only', ['only', 'on'])
        self.assertRoute('_ex_route_onoremap', ['onoremap', 'ono'])
        self.assertRoute('_ex_route_ounmap', ['ounmap', 'ou'])
        self.assertRoute('_ex_route_print', ['print', 'p'])
        self.assertRoute('_ex_route_pwd', ['pwd', 'pw'])
        self.assertRoute('_ex_route_qall', ['qall', 'qa'])
        self.assertRoute('_ex_route_quit', ['quit', 'q'])
        self.assertRoute('_ex_route_qall', ['quitall', 'quita'])
        self.assertRoute('_ex_route_read', ['read', 'r'])
        self.assertRoute('_ex_route_registers', ['registers', 'reg'])
        self.assertRoute('_ex_route_set', ['set', 'se'])
        self.assertRoute('_ex_route_setlocal', ['setlocal', 'setl'])
        self.assertRoute('_ex_route_shell', ['shell', 'sh'])
        self.assertRoute('_ex_route_silent', ['silent', 'sil'])
        self.assertRoute('_ex_route_snoremap', ['snoremap', 'snor'])
        self.assertRoute('_ex_route_sort', ['sort', 'sor'])
        self.assertRoute('_ex_route_spellgood', ['spellgood', 'spe'])
        self.assertRoute('_ex_route_spellundo', ['spellundo', 'spellu'])
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
