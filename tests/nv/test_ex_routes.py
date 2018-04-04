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
from NeoVintageous.nv.ex_routes import _ex_route_exit
from NeoVintageous.nv.ex_routes import _ex_route_file
from NeoVintageous.nv.ex_routes import _ex_route_global
from NeoVintageous.nv.ex_routes import _ex_route_noremap
from NeoVintageous.nv.ex_routes import _ex_route_only
from NeoVintageous.nv.ex_routes import _ex_route_substitute
from NeoVintageous.nv.ex_routes import _ex_route_tabnext
from NeoVintageous.nv.ex_routes import ex_routes
from NeoVintageous.nv.ex_routes import TokenCommand
from NeoVintageous.nv.ex_routes import TokenEof


class Test_ex_route_buffers(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_buffers(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('buffers'), TokenEof()]))

    def test_raises_exception(self):
        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _ex_route_buffers(_ScannerState(' '))

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _ex_route_buffers(_ScannerState('x'))

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _ex_route_buffers(_ScannerState('foo'))

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _ex_route_buffers(_ScannerState('!'))


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
        # TODO [bug] Currently ":close" followed by character not "!" is accepted
        # and it shouldn't be e.g. ":closex" is currently a valid command.

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            _ex_route_close(_ScannerState('  '))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            _ex_route_close(_ScannerState('! '))

        # "x" shouldn't be valid, oppose "y", see TODO above.
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got y instead'):
            _ex_route_close(_ScannerState('xy'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got x instead'):
            _ex_route_close(_ScannerState('!x'))

        # "b" shouldn't be valid, oppose to "a", see TODO above.
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got a instead'):
            _ex_route_close(_ScannerState('baz'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got f instead'):
            _ex_route_close(_ScannerState('!foo'))

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got ! instead'):
            _ex_route_close(_ScannerState('!!'))


class Test_ex_route_exit(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_exit(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': ''}), TokenEof()]))  # noqa: E501

        actual = _ex_route_exit(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': ''}, forced=False), TokenEof()]))  # noqa: E501

        actual = _ex_route_exit(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': ''}, forced=True), TokenEof()]))  # noqa: E501

        actual = _ex_route_exit(_ScannerState('/tmp/path/to/file'))
        self.assertEqual(actual, (None, [TokenCommand('exit', addressable=True, params={'file_name': '/tmp/path/to/file'}), TokenEof()]))  # noqa: E501


class Test_ex_route_file(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_file(_ScannerState(''))
        self.assertEqual(actual, (None, [TokenCommand('file'), TokenEof()]))

        actual = _ex_route_file(_ScannerState('!'))
        self.assertEqual(actual, (None, [TokenCommand('file', forced=True), TokenEof()]))

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
            _ex_route_only(_ScannerState('x'))

        with self.assertRaises(Exception):
            _ex_route_only(_ScannerState('!x'))

        with self.assertRaises(Exception):
            _ex_route_only(_ScannerState('! '))

        with self.assertRaises(Exception):
            _ex_route_only(_ScannerState(' '))


class Test_ex_route_noremap(unittest.TestCase):

    def test_can_scan(self):
        actual = _ex_route_noremap(_ScannerState('w 2w'))
        self.assertEqual(actual, (None, [TokenCommand('noremap', params={'keys': 'w', 'command': '2w'}), TokenEof()]))


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

    def routeMatch(self, string):
        matches = []
        for route, command in ex_routes.items():
            match = re.compile(route).match(string)
            if match:
                matches.append((match, route, command))

        return matches

    def test_invalid_routes(self):
        def assert_no_route(string):
            self.assertEquals(self.routeMatch(string), [], 'failed asserting no route for {}'.format(string))

        assert_no_route('')
        assert_no_route('zfoobar')
        assert_no_route(' ')
        assert_no_route('$')

        # TODO assert_no_route('foobar') shouldn't match :file

    def test_routes(self):

        def assert_route(string, first=False, name=None):
            matches = self.routeMatch(string)

            if not first:
                self.assertEqual(
                    len(matches), 1,
                    'expected only one route to match "{}"; found {}'
                    .format(string, [s[0].group(0) for s in matches]))
            else:
                self.assertTrue(
                    len(matches) > 1,
                    'expected more than one route to match "{}"; found {}'
                    .format(string, [s[0].group(0) for s in matches]))

            self.assertEqual(matches[0][0].group(0), string, 'failed for "{}"'.format(string))

            if name:
                expected = '_ex_route_' + name
            else:
                expected = '_ex_route_' + string

            self.assertEqual(matches[0][2].__name__[0:len(expected)], expected)

        # TODO [review] assert_route('g') works for the command scanner but fails a regex match, why?
        # TODO [review] assert_route('global') works for the command scanner but fails a regex match, why?

        assert_route('ab')
        assert_route('abbreviate')
        assert_route('bro')
        assert_route('browse')
        assert_route('buffers')
        assert_route('cd')
        assert_route('cdd')
        assert_route('clo')
        assert_route('close')
        assert_route('co')
        assert_route('copy')
        assert_route('cq')
        assert_route('cquit')
        assert_route('d')
        assert_route('delete')
        assert_route('e')
        assert_route('edit')
        assert_route('exi', first=True)
        assert_route('exit', first=True)
        assert_route('f')
        assert_route('file')
        assert_route('files', first=True, name='buffers')
        assert_route('h')
        assert_route('help')
        assert_route('let ', name='let')
        assert_route('ls', name='buffers')
        assert_route('m')
        assert_route('move')
        assert_route('new')
        assert_route('nn')
        assert_route('nnoremap')
        assert_route('no')
        assert_route('noremap')
        assert_route('nun')
        assert_route('nunmap')
        assert_route('ono')
        assert_route('onoremap')
        assert_route('ou')
        assert_route('ounmap')
        assert_route('p')
        assert_route('print')
        assert_route('pw')
        assert_route('pwd')
        assert_route('q')
        assert_route('qa')
        assert_route('qall')
        assert_route('quit')
        assert_route('r')
        assert_route('read')
        assert_route('reg')
        assert_route('registers')
        assert_route('s')
        assert_route('se')
        assert_route('set')
        assert_route('setl')
        assert_route('setlocal')
        assert_route('sh')
        assert_route('shell')
        assert_route('snor')
        assert_route('snoremap')
        assert_route('sp')
        assert_route('split')
        assert_route('substitute')
        assert_route('sunm')
        assert_route('sunmap')
        assert_route('tabc')
        assert_route('tabclose')
        assert_route('tabfir')
        assert_route('tabfirst')
        assert_route('tabl')
        assert_route('tablast')
        assert_route('tabn')
        assert_route('tabnext')
        assert_route('tabo')
        assert_route('tabonly')
        assert_route('tabp')
        assert_route('tabprevious')
        assert_route('tabr', name='tabfirst')
        assert_route('tabrewind', name='tabfirst')
        assert_route('una')
        assert_route('unabbreviate')
        assert_route('unm')
        assert_route('unmap')
        assert_route('vn')
        assert_route('vnoremap')
        assert_route('vs')
        assert_route('vsplit')
        assert_route('vu')
        assert_route('vunmap')
        assert_route('w')
        assert_route('wa')
        assert_route('wall')
        assert_route('wq')
        assert_route('wqall', first=True)
        assert_route('write')
        assert_route('x', name='exit')
        assert_route('xa', name="wqall")
        assert_route('xall', name="wqall")
        assert_route('xit', name='exit')
        assert_route('y')
        assert_route('yank')
