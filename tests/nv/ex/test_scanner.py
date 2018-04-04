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

    def test_can_scan_commands(self):
        def assert_command(string, expected):
            actual = _scan_command(_ScannerState(string))
            # Do this check so that if assertion fails
            # we get a diff of the command in the
            # failure in result.
            self.assertEqual(actual[1], expected[1])
            self.assertEqual(actual, expected)

        assert_command('&&', (None, [TokenCommand('&&', target='ex_double_ampersand', params={'flags': [], 'count': ''}, addressable=True), TokenEof()]))  # noqa: E501
        assert_command('buffers', (None, [TokenCommand('buffers'), TokenEof()]))  # noqa: E501
        assert_command('cd!', (None, [TokenCommand('cd', params={'path': None, '-': None}, forced=True), TokenEof()]))  # noqa: E501
        assert_command('cd', (None, [TokenCommand('cd', params={'path': None, '-': None}), TokenEof()]))  # noqa: E501
        assert_command('clo', (None, [TokenCommand('close'), TokenEof()]))  # noqa: E501
        assert_command('clos', (None, [TokenCommand('close'), TokenEof()]))  # noqa: E501
        assert_command('close!', (None, [TokenCommand('close', forced=True), TokenEof()]))  # noqa: E501
        assert_command('close', (None, [TokenCommand('close'), TokenEof()]))  # noqa: E501
        assert_command('copy 3', (None, [TokenCommand('copy', params={'address': '3'}, addressable=True), TokenEof()]))  # noqa: E501
        assert_command('cquit', (None, [TokenCommand('cquit'), TokenEof()]))  # noqa: E501
        assert_command('delete', (None, [TokenCommand('delete', params={'register': '"', 'count': None}, addressable=True), TokenEof()]))  # noqa: E501
        assert_command('f', (None, [TokenCommand('file'), TokenEof()]))  # noqa: E501
        assert_command('file', (None, [TokenCommand('file'), TokenEof()]))  # noqa: E501
        assert_command('files', (None, [TokenCommand('buffers'), TokenEof()]))  # noqa: E501
        assert_command('g/foo/print', (None, [TokenCommand('global', params={'pattern': 'foo', 'cmd': 'print'}, addressable=True), TokenEof()]))  # noqa: E501
        assert_command('global/foo/print', (None, [TokenCommand('global', params={'pattern': 'foo', 'cmd': 'print'}, addressable=True), TokenEof()]))  # noqa: E501
        assert_command('h intro', (None, [TokenCommand('help', params={'subject': 'intro'}), TokenEof()]))  # noqa: E501
        assert_command('help intro', (None, [TokenCommand('help', params={'subject': 'intro'}), TokenEof()]))  # noqa: E501
        assert_command('ls', (None, [TokenCommand('buffers'), TokenEof()]))  # noqa: E501
        assert_command('nn', (None, [TokenCommand('nnoremap', params={'command': None, 'keys': None}), TokenEof()]))  # noqa: E501
        assert_command('nnoremap', (None, [TokenCommand('nnoremap', params={'command': None, 'keys': None}), TokenEof()]))  # noqa: E501
        assert_command('no', (None, [TokenCommand('noremap', params={'command': None, 'keys': None}), TokenEof()]))  # noqa: E501
        assert_command('noremap', (None, [TokenCommand('noremap', params={'command': None, 'keys': None}), TokenEof()]))  # noqa: E501
        assert_command('only', (None, [TokenCommand('only'), TokenEof()]))  # noqa: E501
        assert_command('ou', (None, [TokenCommand('ounmap', params={'keys': None}), TokenEof()]))  # noqa: E501
        assert_command('ounmap', (None, [TokenCommand('ounmap', params={'keys': None}), TokenEof()]))  # noqa: E501
