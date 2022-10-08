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

    def test_expect_match_raises_on_error(self):
        state = _ScannerState('foo')
        with self.assertRaisesRegex(ValueError, 'fizz buzz'):
            state.expect_match('x', lambda: ValueError('fizz buzz'))

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

    def test_can_scan_forward_raises_exception_on_unclosed_pattern(self):
        scanner = Scanner("/fizz")
        with self.assertRaisesRegex(ValueError, 'unclosed search pattern'):
            list(scanner.scan())

    def test_can_scan_backward_raises_exception_on_unclosed_pattern(self):
        scanner = Scanner("?fizz")
        with self.assertRaisesRegex(ValueError, 'unclosed search pattern'):
            list(scanner.scan())

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

    def test_whitespace_is_ingored(self):
        scanner = Scanner("10delete")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDigits('10'), TokenCommand('delete', params={'register': '"', 'count': None}, cooperates_with_global=True, addressable=True), TokenEof()], tokens)  # noqa: E501
        self.assertEqual(8, scanner.state.position)
        scanner = Scanner("10 delete")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDigits('10'), TokenCommand('delete', params={'register': '"', 'count': None}, cooperates_with_global=True, addressable=True), TokenEof()], tokens)  # noqa: E501
        self.assertEqual(9, scanner.state.position)
        scanner = Scanner("10    delete")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDigits('10'), TokenCommand('delete', params={'register': '"', 'count': None}, cooperates_with_global=True, addressable=True), TokenEof()], tokens)  # noqa: E501
        self.assertEqual(12, scanner.state.position)


class TestScannerOffsets(unittest.TestCase):

    def test_can_scan_negative_offset(self):
        scanner = Scanner(".-100")
        tokens = list(scanner.scan())
        self.assertEqual([TokenDot(), TokenOffset([-100]), TokenEof()], tokens)

    def test_can_scan_offset_with_trailing_chars2(self):
        scanner = Scanner("+3+2")
        tokens = list(scanner.scan())
        self.assertEqual([TokenOffset([3, 2]), TokenEof()], tokens)

    def test_offset_number(self):
        scanner = Scanner("+3,12")
        tokens = list(scanner.scan())
        self.assertEqual([TokenOffset([3]), TokenComma(), TokenDigits('12'), TokenEof()], tokens)

    def test_offset_offset(self):
        scanner = Scanner("+12,+15")
        tokens = list(scanner.scan())
        self.assertEqual([TokenOffset([12]), TokenComma(), TokenOffset([15]), TokenEof()], tokens)

    def test_offset_number_command(self):
        scanner = Scanner("+3,6delete")
        tokens = list(scanner.scan())
        self.assertEqual([TokenOffset([3]), TokenComma(), TokenDigits('6'), TokenCommand('delete', params={'register': '"', 'count': None}, cooperates_with_global=True, addressable=True), TokenEof()], tokens)  # noqa: E501


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
        self.assertRoute(['bNext', 'bN', 'bprevious', 'bp'], cmd('bprevious'))
        self.assertRoute(['bfirst', 'bf', 'brewind', 'br'], cmd('bfirst'))
        self.assertRoute(['blast', 'bl'], cmd('blast'))
        self.assertRoute(['bnext', 'bn'], cmd('bnext'))
        self.assertRoute(['browse', 'bro'], cmd('browse'))
        self.assertRoute(['buffer 1', 'b 1'], cmd('buffer', params={'index': '1'}))
        self.assertRoute(['buffer 3', 'b 3'], cmd('buffer', params={'index': '3'}))
        self.assertRoute(['buffer!', 'b!'], cmd('buffer', forced=True))
        self.assertRoute(['buffer', 'b'], cmd('buffer'))
        self.assertRoute(['buffers', 'files', 'ls'], cmd('buffers'))
        self.assertRoute(['cd /tmp/path'], cmd('cd', params={'path': '/tmp/path'}))
        self.assertRoute(['cd ~'], cmd('cd', params={'path': '~'}))
        self.assertRoute(['cd!'], cmd('cd', forced=True))
        self.assertRoute(['cd'], cmd('cd'))
        self.assertRoute(['close!', 'clo!'], cmd('close', forced=True))
        self.assertRoute(['close', 'clo'], cmd('close'))
        self.assertRoute(['copy .', 'co .'], cmd('copy', params={'address': '.'}, addressable=True))
        self.assertRoute(['copy .+3', 'co .+3'], cmd('copy', params={'address': '.+3'}, addressable=True))
        self.assertRoute(['copy', 'co'], cmd('copy', addressable=True))
        self.assertRoute(['cquit', 'cq'], cmd('cquit'))
        self.assertRoute(['delete x', 'd x'], cmd('delete', params={'count': None, 'register': 'x'}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['delete', 'd'], cmd('delete', params={'count': None, 'register': '"'}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['edit file.txt', 'e file.txt'], cmd('edit', params={'file_name': 'file.txt'}))  # noqa: E501
        self.assertRoute(['edit x/y.txt', 'e x/y.txt'], cmd('edit', params={'file_name': 'x/y.txt'}))  # noqa: E501
        self.assertRoute(['edit!', 'e!'], cmd('edit', params={'file_name': None}, forced=True))  # noqa: E501
        self.assertRoute(['edit', 'e'], cmd('edit', params={'file_name': None}))  # noqa: E501
        self.assertRoute(['exit', 'exi', 'xit', 'x'], cmd('exit'))
        self.assertRoute(['file', 'f'], cmd('file'))
        self.assertRoute(['global!!x!y', 'g!!x!y'], cmd('global', params={'pattern': 'x', 'cmd': 'y'}, forced=True, addressable=True))  # noqa: E501
        self.assertRoute(['global!/x/y', 'g!/x/y'], cmd('global', params={'pattern': 'x', 'cmd': 'y'}, forced=True, addressable=True))  # noqa: E501
        self.assertRoute(['global#x#y', 'g#x#y'], cmd('global', params={'pattern': 'x', 'cmd': 'y'}, addressable=True))
        self.assertRoute(['global/^/', 'g/^/'], cmd('global', params={'pattern': '^'}, addressable=True))
        self.assertRoute(['global/^/y', 'g/^/y'], cmd('global', params={'pattern': '^', 'cmd': 'y'}, addressable=True))
        self.assertRoute(['global/x/y', 'g/x/y'], cmd('global', params={'pattern': 'x', 'cmd': 'y'}, addressable=True))
        self.assertRoute(['help fizz', 'h fizz'], cmd('help', params={'subject': 'fizz'}))
        self.assertRoute(['help!', 'h!'], cmd('help', params={'subject': None}, forced=True))
        self.assertRoute(['help', 'h'], cmd('help', params={'subject': None}))
        self.assertRoute(['history /', 'his /'], cmd('history', params={'name': '/'}))
        self.assertRoute(['history :', 'his :'], cmd('history', params={'name': ':'}))
        self.assertRoute(['history ?', 'his ?'], cmd('history', params={'name': '?'}))
        self.assertRoute(['history all', 'his all'], cmd('history', params={'name': 'all'}))
        self.assertRoute(['history search', 'his search'], cmd('history', params={'name': 'search'}))
        self.assertRoute(['history', 'his'], cmd('history'))
        self.assertRoute(['let n=v'], cmd('let', params={'name': 'n', 'value': 'v'}))
        self.assertRoute(['move .', 'm .'], cmd('move', params={'address': '.'}, addressable=True))
        self.assertRoute(['move 3', 'm 3'], cmd('move', params={'address': '3'}, addressable=True))
        self.assertRoute(['move', 'm'], cmd('move', addressable=True))
        self.assertRoute(['new'], cmd('new'))
        self.assertRoute(['nnoremap abc xyz', 'nn abc xyz'], cmd('nnoremap', params={'lhs': 'abc', 'rhs': 'xyz'}))
        self.assertRoute(['nnoremap', 'nn'], cmd('nnoremap'))
        self.assertRoute(['nohlsearch', 'noh'], cmd('nohlsearch'))
        self.assertRoute(['noremap abc xyz', 'no abc xyz'], cmd('noremap', params={'lhs': 'abc', 'rhs': 'xyz'}))
        self.assertRoute(['noremap', 'no'], cmd('noremap'))
        self.assertRoute(['nunmap xyz', 'nun xyz'], cmd('nunmap', params={'lhs': 'xyz'}))
        self.assertRoute(['only!', 'on!'], cmd('only', forced=True))
        self.assertRoute(['only', 'on'], cmd('only'))
        self.assertRoute(['onoremap abc xyz', 'ono abc xyz'], cmd('onoremap', params={'lhs': 'abc', 'rhs': 'xyz'}))
        self.assertRoute(['onoremap', 'ono'], cmd('onoremap'))
        self.assertRoute(['ounmap xyz', 'ou xyz'], cmd('ounmap', params={'lhs': 'xyz'}))
        self.assertRoute(['print 4 l#', 'p 4 l#'], cmd('print', params={'count': '4', 'flags': ['l', '#']}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['print 4 l', 'p 4 l'], cmd('print', params={'count': '4', 'flags': ['l']}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['print 4', 'p 4'], cmd('print', params={'count': '4'}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['print l#', 'p l#'], cmd('print', params={'flags': ['l', '#']}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['print l', 'p l'], cmd('print', params={'flags': ['l']}, addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['print', 'p'], cmd('print', addressable=True, cooperates_with_global=True))  # noqa: E501
        self.assertRoute(['pwd', 'pw'], cmd('pwd'))
        self.assertRoute(['qall!', 'qa!'], cmd('qall', forced=True))
        self.assertRoute(['qall', 'qa'], cmd('qall'))
        self.assertRoute(['quit!', 'q!'], cmd('quit', forced=True))
        self.assertRoute(['quit', 'q'], cmd('quit'))
        self.assertRoute(['read file.txt', 'r file.txt'], cmd('read', addressable=True, params={'file_name': 'file.txt'}))  # noqa: E501
        self.assertRoute(['read!p', 'r!p'], cmd('read', addressable=True, params={'cmd': 'p'}))
        self.assertRoute(['read!print', 'r!print'], cmd('read', addressable=True, params={'cmd': 'print'}))
        self.assertRoute(['read!yank', 'r!yank'], cmd('read', addressable=True, params={'cmd': 'yank'}))
        self.assertRoute(['registers', 'reg'], cmd('registers'))
        self.assertRoute(['set noopt', 'se noopt'], cmd('set', params={'option': 'noopt', 'value': None}))
        self.assertRoute(['set opt   =   val', 'se opt    =   val'], cmd('set', params={'option': 'opt', 'value': 'val'}))  # noqa: E501
        self.assertRoute(['set opt   =val', 'se opt     =val'], cmd('set', params={'option': 'opt', 'value': 'val'}))
        self.assertRoute(['set opt =val', 'se opt =val'], cmd('set', params={'option': 'opt', 'value': 'val'}))
        self.assertRoute(['set opt!', 'se opt!'], cmd('set', params={'option': 'opt!', 'value': None}))
        self.assertRoute(['set opt', 'se opt'], cmd('set', params={'option': 'opt', 'value': None}))
        self.assertRoute(['set opt=', 'se opt='], cmd('set', params={'option': 'opt', 'value': ''}))
        self.assertRoute(['set opt=3', 'se opt=3'], cmd('set', params={'option': 'opt', 'value': '3'}))
        self.assertRoute(['set opt=val', 'se opt=val'], cmd('set', params={'option': 'opt', 'value': 'val'}))
        self.assertRoute(['set opt?', 'se opt?'], cmd('set', params={'option': 'opt?', 'value': None}))
        self.assertRoute(['setlocal noopt', 'setl noopt'], cmd('setlocal', params={'option': 'noopt', 'value': None}))
        self.assertRoute(['setlocal opt   =   val', 'setl opt    =   val'], cmd('setlocal', params={'option': 'opt', 'value': 'val'}))  # noqa: E501
        self.assertRoute(['setlocal opt   =val', 'setl opt     =val'], cmd('setlocal', params={'option': 'opt', 'value': 'val'}))  # noqa: E501
        self.assertRoute(['setlocal opt =val', 'setl opt =val'], cmd('setlocal', params={'option': 'opt', 'value': 'val'}))  # noqa: E501
        self.assertRoute(['setlocal opt', 'setl opt'], cmd('setlocal', params={'option': 'opt', 'value': None}))
        self.assertRoute(['setlocal opt=', 'setl opt='], cmd('setlocal', params={'option': 'opt', 'value': ''}))
        self.assertRoute(['setlocal opt=3', 'setl opt=3'], cmd('setlocal', params={'option': 'opt', 'value': '3'}))
        self.assertRoute(['setlocal opt=val', 'setl opt=val'], cmd('setlocal', params={'option': 'opt', 'value': 'val'}))  # noqa: E501
        self.assertRoute(['shell', 'sh'], cmd('shell'))
        self.assertRoute(['silent ls', 'sil ls'], cmd('silent', params={'command': 'ls'}))  # noqa: E501
        self.assertRoute(['silent! ls', 'sil! ls'], cmd('silent', params={'command': 'ls'}, forced=True))  # noqa: E501
        self.assertRoute(['snoremap abc xyz', 'snor abc xyz'], cmd('snoremap', params={'lhs': 'abc', 'rhs': 'xyz'}))  # noqa: E501
        self.assertRoute(['snoremap', 'snor'], cmd('snoremap'))
        self.assertRoute(['sort i', 'sor i'], cmd('sort', params={'options': 'i'}, addressable=True))
        self.assertRoute(['sort iu', 'sor iu'], cmd('sort', params={'options': 'iu'}, addressable=True))
        self.assertRoute(['sort u', 'sor u'], cmd('sort', params={'options': 'u'}, addressable=True))
        self.assertRoute(['sort ui', 'sor ui'], cmd('sort', params={'options': 'ui'}, addressable=True))
        self.assertRoute(['sort', 'sor'], cmd('sort', addressable=True))
        self.assertRoute(['spellgood fizz', 'spe fizz'], cmd('spellgood', params={'word': 'fizz'}))
        self.assertRoute(['spellundo fizz', 'spellu fizz'], cmd('spellundo', params={'word': 'fizz'}))
        self.assertRoute(['split file.txt', 'sp file.txt'], cmd('split', params={'file': 'file.txt'}))
        self.assertRoute(['split', 'sp'], cmd('split'))
        self.assertRoute(['substitute', 's'], cmd('substitute', addressable=True))
        self.assertRoute(['substitute/x/', 's/x/'], cmd('substitute', params={'pattern': 'x', 'replacement': '', 'flags': [], 'count': 1}, addressable=True))  # noqa: E501
        self.assertRoute(['substitute/x//', 's/x//'], cmd('substitute', params={'pattern': 'x', 'replacement': '', 'flags': [], 'count': 1}, addressable=True))  # noqa: E501
        self.assertRoute(['substitute/x/y/', 's/x/y/'], cmd('substitute', params={'pattern': 'x', 'replacement': 'y', 'flags': [], 'count': 1}, addressable=True))  # noqa: E501
        self.assertRoute(['substitute/x/y/ic', 's/x/y/ic'], cmd('substitute', params={'pattern': 'x', 'replacement': 'y', 'flags': ['i', 'c'], 'count': 1}, addressable=True))  # noqa: E501
        self.assertRoute(['sunmap xyz', 'sunm xyz'], cmd('sunmap', params={'lhs': 'xyz'}))
        self.assertRoute(['tabNext!', 'tabN!', 'tabprevious!', 'tabp!'], cmd('tabprevious', forced=True))
        self.assertRoute(['tabNext', 'tabN', 'tabprevious', 'tabp'], cmd('tabprevious'))
        self.assertRoute(['tabclose!', 'tabc!'], cmd('tabclose', forced=True))
        self.assertRoute(['tabclose', 'tabc'], cmd('tabclose'))
        self.assertRoute(['tabfirst!', 'tabfir!', 'tabrewind!', 'tabr!'], cmd('tabfirst', forced=True))
        self.assertRoute(['tabfirst', 'tabfir', 'tabrewind', 'tabr'], cmd('tabfirst'))
        self.assertRoute(['tablast!', 'tabl!'], cmd('tablast', forced=True))
        self.assertRoute(['tablast', 'tabl'], cmd('tablast'))
        self.assertRoute(['tabnext!', 'tabn!'], cmd('tabnext', forced=True))
        self.assertRoute(['tabnext', 'tabn'], cmd('tabnext'))
        self.assertRoute(['tabonly!', 'tabo!'], cmd('tabonly', forced=True))
        self.assertRoute(['tabonly', 'tabo'], cmd('tabonly'))
        self.assertRoute(['unmap xyz', 'unm xyz'], cmd('unmap', params={'lhs': 'xyz'}))
        self.assertRoute(['unvsplit'], cmd('unvsplit'))
        self.assertRoute(['vnoremap abc xyz', 'vn abc xyz'], cmd('vnoremap', params={'lhs': 'abc', 'rhs': 'xyz'}))
        self.assertRoute(['vnoremap', 'vn'], cmd('vnoremap'))
        self.assertRoute(['vsplit file.txt', 'vs file.txt'], cmd('vsplit', params={'file': 'file.txt'}))
        self.assertRoute(['vsplit', 'vs'], cmd('vsplit'))
        self.assertRoute(['vunmap xyz', 'vu xyz'], cmd('vunmap', params={'lhs': 'xyz'}))
        self.assertRoute(['wall!', 'wa!'], cmd('wall', forced=True))
        self.assertRoute(['wall', 'wa'], cmd('wall'))
        self.assertRoute(['wq!'], cmd('wq', forced=True))
        self.assertRoute(['wq'], cmd('wq'))
        self.assertRoute(['wqall', 'wqa', 'xall', 'xa'], cmd('wqall', forced=False, addressable=True))
        self.assertRoute(['wqall!', 'wqa!', 'xall!', 'xa!'], cmd('wqall', forced=True, addressable=True))
        self.assertRoute(['wqall'], cmd('wqall', forced=False, addressable=True))
        self.assertRoute(['write file.txt', 'w file.txt'], cmd('write', params={'++': '', 'file_name': 'file.txt', '>>': False, 'cmd': ''}, addressable=True))  # noqa: E501
        self.assertRoute(['write! file.txt', 'w! file.txt'], cmd('write', params={'++': '', 'file_name': 'file.txt', '>>': False, 'cmd': ''}, addressable=True, forced=True))  # noqa: E501
        self.assertRoute(['write!', 'w!'], cmd('write', params={'++': '', 'file_name': '', '>>': False, 'cmd': ''}, addressable=True, forced=True))  # noqa: E501
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

    def assertRaisesE474InvalidArgument(self, sources):
        self.assertRaisesExeption(sources, Exception, 'E474: Invalid argument')

    def assertRaisesExeption(self, sources, exception, message):
        if isinstance(sources, str):
            sources = [sources]

        for source in sources:
            with self.assertRaisesRegex(exception, message):
                _scan_command(_ScannerState(source))

    def test_invalid_command_routes(self):
        self.assertRaisesExpectMatch([
            'nunmap',
            'ounmap',
            'print 4 x',
            'print x',
            'printx',
            'px',
            'sunmap',
            'unmap',
            'vunmap',
        ])

        self.assertRaisesExeption(['globala', 'ga'], ValueError, 'bad separator')
        self.assertRaisesExeption(['globalx', 'gx'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global"', 'g"'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global\\', 'g\\'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global|', 'g|'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global!a', 'g!a'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global!x', 'g!x'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global!"', 'g!"'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global!\\', 'g!\\'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global!|', 'g!|'], ValueError, 'bad separator')
        self.assertRaisesExeption(['global!/', 'g!/'], ValueError, 'unexpected EOF')
        self.assertRaisesExeption(['global/', 'g/'], ValueError, 'unexpected EOF')
        self.assertRaisesExeption(['substitute/x', 's/x'], ValueError, 'bad command')

        self.assertRaisesE492NotAnEditorCommand([
            'bf x',
            'bfirst x',
            'blast x',
            'blastx',
            'bnext x',
            'browse x',
            'buffers ',
            'buffers x',
            'close  ',
            'close ',
            'close x',
            'close! ',
            'close! x',
            'close!!',
            'close!foo',
            'close!x',
            'closex',
            'closexy',
            'cq x',
            'cquit x',
            'cquitx',
            'exitx',
            'file ',
            'file! ',
            'file!x',
            'filex',
            'foo bar',
            'foobar',
            'let',
            'ls x ',
            'new x',
            'newx',
            'only! ',
            'only!x',
            'onlyx',
            'pwdx',
            'q!x',
            'qall!x',
            'qallx',
            'quit!x',
            'quitx',
            'qx',
            'registers ',
            'registersx',
            'shellx',
            'tabclose x',
            'tabclosex',
            'wall ',
            'wallx',
            'wq +',
            'wq ++',
            'wq x',
            'wq+',
            'wqa ++',
            'wqall ++',
            'wqallx',
            'wqax',
            'wqx',
            'xitx',
            'xx',
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
        ])
