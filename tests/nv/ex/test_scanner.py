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

from NeoVintageous.nv.ex.scanner import _scan_command
from NeoVintageous.nv.ex.scanner import _ScannerState
from NeoVintageous.nv.ex.scanner import Scanner
from NeoVintageous.nv.ex.scanner import TokenComma
from NeoVintageous.nv.ex.scanner import TokenDigits
from NeoVintageous.nv.ex.scanner import TokenDollar
from NeoVintageous.nv.ex.scanner import TokenDot
from NeoVintageous.nv.ex.scanner import TokenEof
from NeoVintageous.nv.ex.scanner import TokenMark
from NeoVintageous.nv.ex.scanner import TokenOffset
from NeoVintageous.nv.ex.scanner import TokenPercent
from NeoVintageous.nv.ex.scanner import TokenSearchBackward
from NeoVintageous.nv.ex.scanner import TokenSearchForward
from NeoVintageous.nv.ex.scanner import TokenSemicolon
from NeoVintageous.nv.ex.tokens import TokenCommand


class TestScannerState(unittest.TestCase):

    def test_defaults(self):
        state = _ScannerState('abc')

        self.assertEqual('abc', state.source)
        self.assertEqual(0, state.position)
        self.assertEqual(0, state.start)

    def test_can_consume(self):
        state = _ScannerState('abc')

        self.assertEqual('a', state.consume())
        self.assertEqual(1, state.position)
        self.assertEqual(0, state.start)

    def test_consuming_reaches_eof(self):
        state = _ScannerState('a')
        state.consume()

        self.assertEqual(state.EOF, state.consume())
        self.assertEqual(1, state.position)

    def test_consuming_stops_at_eof(self):
        state = _ScannerState('a')
        state.consume()
        a = state.consume()
        b = state.consume()
        c = state.consume()

        self.assertEqual([state.EOF, state.EOF, state.EOF], [a, b, c])
        self.assertEqual(1, state.position)
        self.assertEqual(0, state.start)

    def test_backup_works(self):
        state = _ScannerState('abc')
        state.consume()
        state.consume()
        state.backup()

        self.assertEqual('b', state.consume())
        self.assertEqual(2, state.position)
        self.assertEqual(0, state.start)

        state.backup()

        self.assertEqual('b', state.consume())
        self.assertEqual(2, state.position)
        self.assertEqual(0, state.start)

    def test_skip_works(self):
        state = _ScannerState("aafoo")
        state.skip("a")

        self.assertEqual(2, state.position)
        self.assertEqual('f', state.consume())

    def test_skip_stops_at_eof(self):
        state = _ScannerState("aa")
        state.skip("a")

        self.assertEqual(2, state.position)
        self.assertEqual(state.EOF, state.consume())

    def test_skip_run_works(self):
        state = _ScannerState("aafoo")
        state.skip_run("af")

        self.assertEqual(3, state.position)
        self.assertEqual('o', state.consume())

    def test_skip_run__stops_at_eof(self):
        state = _ScannerState("aaf")
        state.skip_run("af")

        self.assertEqual(3, state.position)
        self.assertEqual(state.EOF, state.consume())

    def test_emit(self):
        state = _ScannerState('abcdef')
        state.consume()
        state.consume()
        state.consume()

        self.assertEqual('abc', state.emit())
        self.assertEqual(3, state.start)
        self.assertEqual(3, state.position)

    def test_skip_then_emit(self):
        state = _ScannerState("aabb")
        state.skip("a")

        self.assertEqual('aa', state.emit())
        self.assertEqual(2, state.start)
        self.assertEqual(2, state.position)

    def test_ignore_works(self):
        state = _ScannerState("aabb")
        state.skip("a")
        state.ignore()

        self.assertEqual(2, state.start)
        self.assertEqual(2, state.position)

    def test_expect_can_succeed(self):
        state = _ScannerState('abc')
        self.assertEqual('a', state.expect('a'))

    def test_expect_can_fail(self):
        state = _ScannerState('foo')
        self.assertRaises(ValueError, state.expect, 'x')

    def test_expect_match_can_succeed(self):
        state = _ScannerState('foo')
        c = state.expect_match('fo{2}')
        self.assertEqual('foo', c.group(0))

    def test_expect_match_can_fail(self):
        state = _ScannerState('foo')
        self.assertRaises(ValueError, state.expect_match, 'x')

    def test_expect_eof(self):
        state = _ScannerState('')
        self.assertEqual(state.EOF, state.expect_eof())

    def test_expect_eof_exception(self):
        state = _ScannerState('x')
        self.assertRaisesRegex(ValueError, 'expected __EOF__, got x instead', state.expect_eof)

        state = _ScannerState('foo')
        self.assertRaisesRegex(ValueError, 'expected __EOF__, got f instead', state.expect_eof)

        state = _ScannerState(' ')
        self.assertRaisesRegex(ValueError, 'expected __EOF__, got   instead', state.expect_eof)

    def test_peek_can_succeed(self):
        state = _ScannerState('abc')
        self.assertTrue(state.peek('abc'))

    def test_peek_can_fail(self):
        state = _ScannerState('foo')
        self.assertFalse(state.peek('fxo'))

    def test_match_can_succeed(self):
        state = _ScannerState('foo123')
        state.consume()
        state.consume()
        state.consume()

        self.assertTrue(state.match(r'\d{3}'))
        self.assertEqual(6, state.position)
        self.assertEqual(state.EOF, state.consume())


class TestScanner(unittest.TestCase):

    def test_can_instantiate(self):
        scanner = Scanner("foo")
        self.assertEqual(scanner.state.source, 'foo')

    def test_can_scan_dot(self):
        scanner = Scanner(".")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDot(), TokenEof()], tokens)

    def test_can_scan_dollar(self):
        scanner = Scanner("$")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDollar(), TokenEof()], tokens)

    def test_can_scan_dollar2(self):
        scanner = Scanner(",")
        tokens = list(scanner.scan())
        self.assertEqual([TokenComma(), TokenEof()], tokens)

    def test_can_scan_dollar3(self):
        scanner = Scanner(";")
        tokens = list(scanner.scan())
        self.assertEqual([TokenSemicolon(), TokenEof()], tokens)

    def test_can_scan_forward_search(self):
        scanner = Scanner("/foo/")
        tokens = list(scanner.scan())
        self.assertEqual([TokenSearchForward('foo'), TokenEof()], tokens)

    def test_can_scan_backward_search(self):
        scanner = Scanner("?foo?")
        tokens = list(scanner.scan())
        self.assertEqual([TokenSearchBackward('foo'), TokenEof()], tokens)

    def test_can_scan_offset(self):
        scanner = Scanner("+100")
        tokens = list(scanner.scan())
        self.assertEqual([TokenOffset([100]), TokenEof()], tokens)

    def test_can_scan_offset_with_trailing_chars(self):
        scanner = Scanner("+100,")
        tokens = list(scanner.scan())
        self.assertEqual([TokenOffset([100]), TokenComma(), TokenEof()], tokens)

    def test_can_scan_percent(self):
        scanner = Scanner("%")
        tokens = list(scanner.scan())
        self.assertEqual([TokenPercent(), TokenEof()], tokens)

    def test_can_scan_empty_range(self):
        scanner = Scanner("s")
        tokens = list(scanner.scan())
        self.assertEqual([TokenCommand('substitute', addressable=True), TokenEof()], tokens)
        self.assertEqual(1, scanner.state.position)

    def test_can_scan_dot_offset_search_forward(self):
        scanner = Scanner(".+10/foobar/")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDot(), TokenOffset([10]), TokenSearchForward('foobar'), TokenEof()], tokens)
        self.assertEqual(12, scanner.state.position)


class TestScannerOffsets(unittest.TestCase):

    def test_can_scan_negative_offset(self):
        scanner = Scanner(".-100")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDot(), TokenOffset([-100]), TokenEof()], tokens)


class TestScannerDigits(unittest.TestCase):

    def test_can_scan_digits(self):
        scanner = Scanner("100")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDigits('100'), TokenEof()], tokens)

    def test_can_scan_digits_dot(self):
        scanner = Scanner("100.")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDigits('100'), TokenDot(), TokenEof()], tokens)


class TestScannerCommandName(unittest.TestCase):

    def test_can_instantiate(self):
        scanner = Scanner("substitute")
        tokens = list(scanner.scan())
        self.assertEqual([TokenCommand('substitute', addressable=True, params=None), TokenEof()], tokens)

    def test_can_scan_substitute_paramaters(self):
        scanner = Scanner("substitute:foo:bar:")
        tokens = list(scanner.scan())
        params = {"pattern": "foo", "replacement": "bar", "flags": [], "count": 1}
        self.assertEqual([TokenCommand('substitute', addressable=True, params=params), TokenEof()], tokens)

    def test_can_scan_substitute_paramaters_with_flags(self):
        scanner = Scanner("substitute:foo:bar:r")
        tokens = list(scanner.scan())
        params = {"pattern": "foo", "replacement": "bar", "flags": ['r'], "count": 1}
        self.assertEqual([TokenCommand('substitute', addressable=True, params=params), TokenEof()], tokens)

    def test_scan_can_fail_if_substitute_paramaters_flags_have_wrong_order(self):
        scanner = Scanner("substitute:foo:bar:r&")
        self.assertRaises(ValueError, lambda: list(scanner.scan()))

    def test_can_scan_substitute_paramaters_with_count(self):
        scanner = Scanner("substitute:foo:bar: 10")
        tokens = list(scanner.scan())
        params = {"pattern": "foo", "replacement": "bar", "flags": [], "count": 10}
        self.assertEqual([TokenCommand('substitute', addressable=True, params=params), TokenEof()], tokens)

    def test_can_scan_substitute_paramater_with_range(self):
        scanner = Scanner(r'%substitute:foo:bar: 10')
        tokens = list(scanner.scan())
        params = {"pattern": "foo", "replacement": "bar", "flags": [], "count": 10}
        self.assertEqual([TokenPercent(), TokenCommand('substitute', addressable=True, params=params), TokenEof()], tokens)  # noqa: E501


class TestScannerMarksScanner(unittest.TestCase):

    def test_can_instantiate(self):
        scanner = Scanner("'a")
        tokens = list(scanner.scan())
        self.assertEqual([TokenMark('a'), TokenEof()], tokens)


class TestScannerWriteCommand(unittest.TestCase):

    def test_can_instantiate(self):
        scanner = Scanner("write")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_instantiate_alias(self):
        scanner = Scanner("w")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_plus_plus_bin(self):
        scanner = Scanner("w ++bin")
        tokens = list(scanner.scan())
        params = {'++': 'binary', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

        scanner = Scanner("w ++binary")
        tokens = list(scanner.scan())
        params = {'++': 'binary', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_plus_plus_nobin(self):
        scanner = Scanner("w ++nobinary")
        tokens = list(scanner.scan())
        params = {'++': 'nobinary', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

        scanner = Scanner("w ++nobin")
        tokens = list(scanner.scan())
        params = {'++': 'nobinary', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_plus_plus_fileformat(self):
        scanner = Scanner("w ++fileformat")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

        scanner = Scanner("w ++ff")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_plus_plus_fileencoding(self):
        scanner = Scanner("w ++fileencoding")
        tokens = list(scanner.scan())
        params = {'++': 'fileencoding', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

        scanner = Scanner("w ++enc")
        tokens = list(scanner.scan())
        params = {'++': 'fileencoding', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_plus_plus_bad(self):
        scanner = Scanner("w ++bad")
        tokens = list(scanner.scan())
        params = {'++': 'bad', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

        scanner = Scanner("w ++fileformat")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_plus_plus_edit(self):
        scanner = Scanner("w ++edit")
        tokens = list(scanner.scan())
        params = {'++': 'edit', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

        scanner = Scanner("w ++fileformat")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_redirection(self):
        scanner = Scanner("w>>")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': True, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_redirection_followed_by_filename(self):
        scanner = Scanner("w>>foo.txt")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': 'foo.txt', '>>': True, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_redirection_followed_by_filename_separated(self):
        scanner = Scanner("w>> foo.txt")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': 'foo.txt', '>>': True, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_command(self):
        scanner = Scanner("w !dostuff")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': 'dostuff'}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_command_absorbs_every_thing(self):
        scanner = Scanner("w !dostuff here")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': 'dostuff here'}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)

    def test_can_parse_command_and_detect_file_name(self):
        scanner = Scanner("w foo.txt")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': 'foo.txt', '>>': False, 'cmd': ''}
        self.assertEqual([TokenCommand('write', addressable=True, params=params), TokenEof()], tokens)


class Test_scan_command(unittest.TestCase):

    def assertRoute(self, sources, expected):
        if isinstance(sources, str):
            sources = [sources]

        for source in sources:
            actual = _scan_command(_ScannerState(source))
            # Check the command part first, so that if there's a failure we get
            # a good diff on the test results.
            self.assertEqual(actual[1], expected[1])
            self.assertEqual(actual, expected)

    def test_valid_command_routes(self):
        def cmd(*args, **kwargs):
            return None, [TokenCommand(*args, **kwargs), TokenEof()]

        self.assertRoute(['!ls'], cmd('!', target='shell_out', params={'cmd': 'ls'}, addressable=True))
        self.assertRoute(['&&'], cmd('&&', target='double_ampersand', params={'count': '', 'flags': []}, addressable=True))  # noqa: E501
        self.assertRoute(['bfirst', 'bf', 'brewind', 'br'], cmd('bfirst'))
        self.assertRoute(['blast', 'bl'], cmd('blast'))
        self.assertRoute(['bNext', 'bN', 'bprevious', 'bp'], cmd('bprevious'))
        self.assertRoute(['bnext', 'bn'], cmd('bnext'))
        self.assertRoute(['browse', 'bro'], cmd('browse'))
        self.assertRoute(['buffers', 'files', 'ls'], cmd('buffers'))
        self.assertRoute(['cd /tmp/path'], cmd('cd', params={'path': '/tmp/path', '-': None}))
        self.assertRoute(['cd ~'], cmd('cd', params={'path': '~', '-': None}))
        self.assertRoute(['cd!'], cmd('cd', params={'path': None, '-': None}, forced=True))
        self.assertRoute(['cd'], cmd('cd', params={'path': None, '-': None}))
        self.assertRoute(['close!', 'clo!'], cmd('close', forced=True))
        self.assertRoute(['close', 'clo'], cmd('close'))
        self.assertRoute(['copy .', 'co .'], cmd('copy', params={'address': '.'}, addressable=True))
        self.assertRoute(['copy .+3', 'co .+3'], cmd('copy', params={'address': '.+3'}, addressable=True))
        self.assertRoute(['cquit', 'cq'], cmd('cquit'))
        self.assertRoute(['delete x', 'd x'], cmd('delete', params={'count': None, 'register': 'x'}, addressable=True))
        self.assertRoute(['delete', 'd'], cmd('delete', params={'count': None, 'register': '"'}, addressable=True))
        self.assertRoute(['edit file.txt', 'e file.txt'], cmd('edit', params={'file_name': 'file.txt'}))  # noqa: E501
        self.assertRoute(['edit x/y.txt', 'e x/y.txt'], cmd('edit', params={'file_name': 'x/y.txt'}))  # noqa: E501
        self.assertRoute(['edit!', 'e!'], cmd('edit', params={'file_name': None}, forced=True))  # noqa: E501
        self.assertRoute(['edit', 'e'], cmd('edit', params={'file_name': None}))  # noqa: E501
        self.assertRoute(['exit', 'exi', 'xit', 'x'], cmd('exit'))
        self.assertRoute(['file', 'f'], cmd('file'))
        self.assertRoute(['global/x/y', 'g/x/y'], cmd('global', params={'pattern': 'x', 'cmd': 'y'}, addressable=True))
        self.assertRoute(['help fizz', 'h fizz'], cmd('help', params={'subject': 'fizz'}))
        self.assertRoute(['help!', 'h!'], cmd('help', params={'subject': None}, forced=True))
        self.assertRoute(['help', 'h'], cmd('help', params={'subject': None}))
        self.assertRoute(['let n=v'], cmd('let', params={'name': 'n', 'value': 'v'}))
        self.assertRoute(['move 3', 'm 3'], cmd('move', params={'address': '3'}, addressable=True))
        self.assertRoute(['move', 'm'], cmd('move', params={'address': '.'}, addressable=True))
        self.assertRoute(['new'], cmd('new'))
        self.assertRoute(['nnoremap lhs rhs', 'nn lhs rhs'], cmd('nnoremap', params={'keys': 'lhs', 'command': 'rhs'}))
        self.assertRoute(['nnoremap', 'nn'], cmd('nnoremap', params={'keys': None, 'command': None}))
        self.assertRoute(['noremap lhs rhs', 'no lhs rhs'], cmd('noremap', params={'keys': 'lhs', 'command': 'rhs'}))
        self.assertRoute(['noremap', 'no'], cmd('noremap', params={'keys': None, 'command': None}))
        self.assertRoute(['nunmap lhs', 'nun lhs'], cmd('nunmap', params={'keys': 'lhs'}))
        self.assertRoute(['nunmap', 'nun'], cmd('nunmap', params={'keys': None}))
        self.assertRoute(['only!', 'on!'], cmd('only', forced=True))
        self.assertRoute(['only', 'on'], cmd('only'))
        self.assertRoute(['onoremap lhs rhs', 'ono lhs rhs'], cmd('onoremap', params={'keys': 'lhs', 'command': 'rhs'}))
        self.assertRoute(['onoremap', 'ono'], cmd('onoremap', params={'keys': None, 'command': None}))
        self.assertRoute(['ounmap lhs', 'ou lhs'], cmd('ounmap', params={'keys': 'lhs'}))
        self.assertRoute(['ounmap', 'ou'], cmd('ounmap', params={'keys': None}))
        self.assertRoute(['print', 'p'], cmd('print', params={'count': '', 'flags': []}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['pwd', 'pw'], cmd('pwd'))
        self.assertRoute(['qall!', 'qa!'], cmd('qall', forced=True))
        self.assertRoute(['qall', 'qa'], cmd('qall'))
        self.assertRoute(['quit!', 'q!'], cmd('quit', forced=True))
        self.assertRoute(['quit', 'q'], cmd('quit'))
        self.assertRoute(['read file.txt', 'r file.txt'], cmd('read', params={'cmd': None, 'file_name': 'file.txt'}))
        self.assertRoute(['registers', 'reg'], cmd('registers'))
        self.assertRoute(['set opt=val', 'se opt=val'], cmd('set', params={'option': 'opt', 'value': 'val'}))
        self.assertRoute(['setlocal opt=val', 'setl opt=val'], cmd('setlocal', params={'option': 'opt', 'value': 'val'}))  # noqa: E501
        self.assertRoute(['shell', 'sh'], cmd('shell'))
        self.assertRoute(['snoremap lhs rhs', 'snor lhs rhs'], cmd('snoremap', params={'keys': 'lhs', 'command': 'rhs'}))  # noqa: E501
        self.assertRoute(['snoremap', 'snor'], cmd('snoremap', params={'keys': None, 'command': None}))
        self.assertRoute(['split file.txt', 'sp file.txt'], cmd('split', params={'file': 'file.txt'}))
        self.assertRoute(['split', 'sp'], cmd('split', params={'file': None}))
        self.assertRoute(['substitute', 's'], cmd('substitute', addressable=True))
        self.assertRoute(['substitute/x/y/', 's/x/y/'], cmd('substitute', params={'pattern': 'x', 'replacement': 'y', 'flags': [], 'count': 1}, addressable=True))  # noqa: E501
        self.assertRoute(['substitute/x/y/ic', 's/x/y/ic'], cmd('substitute', params={'pattern': 'x', 'replacement': 'y', 'flags': ['i', 'c'], 'count': 1}, addressable=True))  # noqa: E501
        self.assertRoute(['sunmap lhs', 'sunm lhs'], cmd('sunmap', params={'keys': 'lhs'}))
        self.assertRoute(['sunmap', 'sunm'], cmd('sunmap', params={'keys': None}))
        self.assertRoute(['tabclose!', 'tabc!'], cmd('tabclose', forced=True))
        self.assertRoute(['tabclose', 'tabc'], cmd('tabclose'))
        self.assertRoute(['tabfirst!', 'tabfir!', 'tabrewind!', 'tabr!'], cmd('tabfirst', forced=True))
        self.assertRoute(['tabfirst', 'tabfir', 'tabrewind', 'tabr'], cmd('tabfirst'))
        self.assertRoute(['tablast!', 'tabl!'], cmd('tablast', forced=True))
        self.assertRoute(['tablast', 'tabl'], cmd('tablast'))
        self.assertRoute(['tabNext!', 'tabN!', 'tabprevious!', 'tabp!'], cmd('tabprevious', forced=True))
        self.assertRoute(['tabnext!', 'tabn!'], cmd('tabnext', forced=True))
        self.assertRoute(['tabNext', 'tabN', 'tabprevious', 'tabp'], cmd('tabprevious'))
        self.assertRoute(['tabnext', 'tabn'], cmd('tabnext'))
        self.assertRoute(['tabonly!', 'tabo!'], cmd('tabonly', forced=True))
        self.assertRoute(['tabonly', 'tabo'], cmd('tabonly'))
        self.assertRoute(['unmap lhs', 'unm lhs'], cmd('unmap', params={'keys': 'lhs'}))
        self.assertRoute(['unmap', 'unm'], cmd('unmap', params={'keys': None}))
        self.assertRoute(['unvsplit'], cmd('unvsplit'))
        self.assertRoute(['vnoremap lhs rhs', 'vn lhs rhs'], cmd('vnoremap', params={'keys': 'lhs', 'command': 'rhs'}))
        self.assertRoute(['vnoremap', 'vn'], cmd('vnoremap', params={'keys': None, 'command': None}))
        self.assertRoute(['vsplit file.txt', 'vs file.txt'], cmd('vsplit', params={'file': 'file.txt'}))
        self.assertRoute(['vsplit', 'vs'], cmd('vsplit', params={'file': None}))
        self.assertRoute(['vunmap lhs', 'vu lhs'], cmd('vunmap', params={'keys': 'lhs'}))
        self.assertRoute(['vunmap', 'vu'], cmd('vunmap', params={'keys': None}))
        self.assertRoute(['wall!', 'wa!'], cmd('wall', forced=True))
        self.assertRoute(['wall', 'wa'], cmd('wall'))
        self.assertRoute(['wq file.txt'], cmd('wq', params={'++': None, 'file': 'file.txt'}))
        self.assertRoute(['wq!'], cmd('wq', params={'++': None, 'file': None}, forced=True))
        self.assertRoute(['wq'], cmd('wq', params={'++': None, 'file': None}))
        self.assertRoute(['wqall', 'wqa', 'xall', 'xa'], cmd('wqall', params={'++': ''}, addressable=True))
        self.assertRoute(['write file.txt', 'w file.txt'], cmd('write', params={'++': '', 'file_name': 'file.txt', '>>': False, 'cmd': ''}, addressable=True))  # noqa: E501
        self.assertRoute(['write', 'w'], cmd('write', params={'++': '', 'file_name': '', '>>': False, 'cmd': ''}, addressable=True))  # noqa: E501
        self.assertRoute(['yank x', 'y x'], cmd('yank', params={'register': 'x', 'count': None}, addressable=True))
        self.assertRoute(['yank', 'y'], cmd('yank', params={'register': '"', 'count': None}, addressable=True))

    def assertRaisesE492NotAnEditorCommand(self, sources):
        self.assertRaisesExeption(sources, Exception, 'E492: Not an editor command')

    def assertRaisesNotImplemented(self, sources):
        self.assertRaisesExeption(sources, NotImplementedError, '')

    def assertRaisesExpectMatch(self, sources):
        self.assertRaisesExeption(sources, ValueError, 'expected match with \'.+\', at \'.*\'')

    def assertRaisesExpectEof(self, sources):
        self.assertRaisesExeption(sources, ValueError, 'expected __EOF__, got . instead')

    def assertRaisesE488TrailingCharacters(self, sources):
        self.assertRaisesExeption(sources, Exception, 'E488: Trailing characters')

    def assertRaisesExeption(self, sources, exception, message):
        if isinstance(sources, str):
            sources = [sources]

        for source in sources:
            with self.assertRaisesRegex(exception, message):
                _scan_command(_ScannerState(source))

    def test_invalid_command_routes(self):
        self.assertRaisesExpectEof([
            'bf x',
            'bfirst x',
            'blast x',
            'blast x',
            'blastx',
            'bnext x',
            'bnext x',
            'browse x',
            'buffers ',
            'buffers x',
            'close ',
            'close x',
            'close! ',
            'close! x',
            'close!x',
            'closex',
            'cq x',
            'cquit x',
            'cquitx',
            'exitx',
            'ls x ',
            'new x',
            'newx',
            'qall!x',
            'qallx',
            'quit!x',
            'quitx',
            'qx',
            'q!x',
            'shellx',
            'tabclose x',
            'tabclosex',
            'wall ',
            'wallx',
        ])

        self.assertRaisesExpectMatch([
            'copy',
        ])

        self.assertRaisesE492NotAnEditorCommand([
            'let'
            'only!x',
            'onlyx',
            'registers ',
            'registersx',
        ])

        self.assertRaisesNotImplemented([
            'cd -',
            'delete x 3',
            'e#',
            'edit #',
            'edit +',
            'edit ++',
            'edit#',
            'edit+',
            'read +',
            'read ++',
            'read+',
            'read++',
            'yank x 3',
            'yank x 3',
        ])
