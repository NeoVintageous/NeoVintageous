import unittest

from NeoVintageous.nv.ex.cmd_buffers import scan_cmd_buffers
from NeoVintageous.nv.ex.cmd_buffers import TokenCommandBuffers
from NeoVintageous.nv.ex.cmd_buffers import TokenEof
from NeoVintageous.nv.ex.scanner_state import ScannerState


def _scan_cmd_buffers(source):
    return scan_cmd_buffers(ScannerState(source))


class Test_scan_cmd_buffers(unittest.TestCase):

    def assertScanEqual(self, actual, expected):
        actual = _scan_cmd_buffers(actual)
        expected = None, [TokenCommandBuffers(**expected), TokenEof()]

        self.assertEqual(actual, expected)
        # Workaround a potential bug, See TokenOfCommand.__eq__().
        self.assertEqual(actual[1][0].forced, expected[1][0].forced)

    def test_can_scan(self):
        self.assertScanEqual('', {})

    def test_raises_exception(self):
        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers(' ')

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers('x')

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers('foo')

        with self.assertRaisesRegex(Exception, 'E488: Trailing characters'):
            _scan_cmd_buffers('!')
