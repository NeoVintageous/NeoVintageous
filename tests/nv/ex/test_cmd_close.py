import unittest

from NeoVintageous.nv.ex.cmd_close import scan_cmd_close
from NeoVintageous.nv.ex.cmd_close import TokenCommandClose
from NeoVintageous.nv.ex.cmd_close import TokenEof
from NeoVintageous.nv.ex.scanner_state import ScannerState


def _scan_cmd_close(source):
    return scan_cmd_close(ScannerState(source))


class Test_scan_cmd_close(unittest.TestCase):

    def assertScanEqual(self, actual, expected):
        actual = _scan_cmd_close(actual)
        expected = (None, [TokenCommandClose(**expected), TokenEof()])

        self.assertEqual(actual, expected)
        # Workaround a potential bug, See TokenOfCommand.__eq__().
        self.assertEqual(actual[1][0].forced, expected[1][0].forced)

    def test_can_scan(self):
        self.assertScanEqual('', {})
        self.assertScanEqual('', {'forced': False})
        self.assertScanEqual('!', {'forced': True})

    def test_raises_exception(self):
        # TODO [bug] Currently ":close" followed by character not "!" is accepted
        # and it shouldn't be e.g. ":closex" is currently a valid command.

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            _scan_cmd_close('  ')

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got   instead'):
            _scan_cmd_close('! ')

        # "x" shouldn't be valid, oppose "y", see TODO above.
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got y instead'):
            _scan_cmd_close('xy')

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got x instead'):
            _scan_cmd_close('!x')

        # "b" shouldn't be valid, oppose to "a", see TODO above.
        with self.assertRaisesRegex(Exception, 'expected __EOF__, got a instead'):
            _scan_cmd_close('baz')

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got f instead'):
            _scan_cmd_close('!foo')

        with self.assertRaisesRegex(Exception, 'expected __EOF__, got ! instead'):
            _scan_cmd_close('!!')
