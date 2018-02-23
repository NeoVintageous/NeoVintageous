import unittest

from NeoVintageous.nv.ex.cmd_tab_next import scan_cmd_tab_next
from NeoVintageous.nv.ex.cmd_tab_next import TokenCommandTabNext
from NeoVintageous.nv.ex.cmd_tab_next import TokenEof
from NeoVintageous.nv.ex.scanner_state import ScannerState


def _scan_cmd_tab_next(source):
    return scan_cmd_tab_next(ScannerState(source))


class Test_scan_cmd_tab_next(unittest.TestCase):

    def assertScanEqual(self, actual, expected):
        actual = _scan_cmd_tab_next(actual)
        expected = (None, [TokenCommandTabNext(**expected), TokenEof()])

        self.assertEqual(actual, expected)
        # Workaround a potential bug, See TokenOfCommand.__eq__().
        self.assertEqual(actual[1][0].forced, expected[1][0].forced)

    def test_can_scan(self):
        self.assertScanEqual('', {})
        self.assertScanEqual('', {'forced': False})
        self.assertScanEqual('!', {'forced': True})
