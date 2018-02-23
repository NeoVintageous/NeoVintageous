import unittest

from NeoVintageous.nv.ex.cmd_substitute import scan_cmd_substitute
from NeoVintageous.nv.ex.cmd_substitute import TokenCommandSubstitute
from NeoVintageous.nv.ex.cmd_substitute import TokenEof
from NeoVintageous.nv.ex.scanner_state import ScannerState


def _scan_cmd_substitute(source):
    return scan_cmd_substitute(ScannerState(source))


class Test_scan_cmd_substitute(unittest.TestCase):

    def assertScanEqual(self, actual, expected):
        actual = _scan_cmd_substitute(actual)
        expected = None, [TokenCommandSubstitute(**expected), TokenEof()]

        self.assertEqual(actual, expected)
        # Workaround a potential bug, See TokenOfCommand.__eq__().
        self.assertEqual(actual[1][0].forced, expected[1][0].forced)

    def test_none(self):
        self.assertScanEqual('', {'params': {}})

    def test_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'bad command'):
            _scan_cmd_substitute('/')

        with self.assertRaisesRegex(ValueError, 'bad command'):
            _scan_cmd_substitute('/abc')

    def test_scan_cmd_substitute(self):
        self.assertScanEqual(
            '/abc/def/',
            {'params': {
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': [],
            }}
        )

    def test_empty(self):
        self.assertScanEqual(
            '///',
            {'params': {
                'search_term': '',
                'replacement': '',
                'count': 1,
                'flags': [],
            }}
        )

    def test_flags(self):
        self.assertScanEqual(
            '/abc/def/g',
            {'params': {
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g']
            }}
        )

        self.assertScanEqual(
            '/abc/def/i',
            {'params': {
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['i']
            }}
        )

        self.assertScanEqual(
            '/abc/def/gi',
            {'params': {
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': ['g', 'i']
            }}
        )

    def test_closing_delimiter_is_not_required(self):
        self.assertScanEqual(
            '/abc/def',
            {'params': {
                'search_term': 'abc',
                'replacement': 'def',
                'count': 1,
                'flags': []
            }}
        )
