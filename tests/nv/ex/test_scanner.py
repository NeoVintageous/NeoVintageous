import unittest

from NeoVintageous.nv.ex.cmd_substitute import TokenCommandSubstitute
from NeoVintageous.nv.ex.cmd_write import TokenCommandWrite
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
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandSubstitute(None), TokenEof()], tokens)
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
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandSubstitute(params=None), TokenEof()], tokens)

    def test_can_scan_substitute_paramaters(self):
        scanner = Scanner("substitute:foo:bar:")
        tokens = list(scanner.scan())
        params = {"search_term": "foo", "replacement": "bar", "flags": [], "count": 1}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandSubstitute(params), TokenEof()], tokens)

    def test_can_scan_substitute_paramaters_with_flags(self):
        scanner = Scanner("substitute:foo:bar:r")
        tokens = list(scanner.scan())
        params = {"search_term": "foo", "replacement": "bar", "flags": ['r'], "count": 1}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandSubstitute(params), TokenEof()], tokens)

    def test_scan_can_fail_if_substitute_paramaters_flags_have_wrong_order(self):
        scanner = Scanner("substitute:foo:bar:r&")
        self.assertRaises(ValueError, lambda: list(scanner.scan()))

    def test_can_scan_substitute_paramaters_with_count(self):
        scanner = Scanner("substitute:foo:bar: 10")
        tokens = list(scanner.scan())
        params = {"search_term": "foo", "replacement": "bar", "flags": [], "count": 10}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandSubstitute(params), TokenEof()], tokens)

    def test_can_scan_substitute_paramater_with_range(self):
        scanner = Scanner(r'%substitute:foo:bar: 10')
        tokens = list(scanner.scan())
        params = {"search_term": "foo", "replacement": "bar", "flags": [], "count": 10}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenPercent(), TokenCommandSubstitute(params), TokenEof()], tokens)


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
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_instantiate_alias(self):
        scanner = Scanner("w")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_plus_plus_bin(self):
        scanner = Scanner("w ++bin")
        tokens = list(scanner.scan())
        params = {'++': 'binary', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

        scanner = Scanner("w ++binary")
        tokens = list(scanner.scan())
        params = {'++': 'binary', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_plus_plus_nobin(self):
        scanner = Scanner("w ++nobinary")
        tokens = list(scanner.scan())
        params = {'++': 'nobinary', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

        scanner = Scanner("w ++nobin")
        tokens = list(scanner.scan())
        params = {'++': 'nobinary', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_plus_plus_fileformat(self):
        scanner = Scanner("w ++fileformat")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

        scanner = Scanner("w ++ff")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_plus_plus_fileencoding(self):
        scanner = Scanner("w ++fileencoding")
        tokens = list(scanner.scan())
        params = {'++': 'fileencoding', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

        scanner = Scanner("w ++enc")
        tokens = list(scanner.scan())
        params = {'++': 'fileencoding', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_plus_plus_bad(self):
        scanner = Scanner("w ++bad")
        tokens = list(scanner.scan())
        params = {'++': 'bad', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

        scanner = Scanner("w ++fileformat")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_plus_plus_edit(self):
        scanner = Scanner("w ++edit")
        tokens = list(scanner.scan())
        params = {'++': 'edit', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

        scanner = Scanner("w ++fileformat")
        tokens = list(scanner.scan())
        params = {'++': 'fileformat', 'file_name': '', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_redirection(self):
        scanner = Scanner("w>>")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': True, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_redirection_followed_by_filename(self):
        scanner = Scanner("w>>foo.txt")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': 'foo.txt', '>>': True, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_redirection_followed_by_filename_separated(self):
        scanner = Scanner("w>> foo.txt")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': 'foo.txt', '>>': True, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_command(self):
        scanner = Scanner("w !dostuff")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': 'dostuff'}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_command_absorbs_every_thing(self):
        scanner = Scanner("w !dostuff here")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': '', '>>': False, 'cmd': 'dostuff here'}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)

    def test_can_parse_command_and_detect_file_name(self):
        scanner = Scanner("w foo.txt")
        tokens = list(scanner.scan())
        params = {'++': '', 'file_name': 'foo.txt', '>>': False, 'cmd': ''}
        # TODO Use a mock token command instead of introducing dependency.
        self.assertEqual([TokenCommandWrite(params), TokenEof()], tokens)
