import unittest

from NeoVintageous.lib.ex.parser.state import EOF
from NeoVintageous.lib.ex.parser.state import ScannerState


class TestScanner(unittest.TestCase):
    def test_instantiate(self):
        state = ScannerState("foo")

        self.assertEqual("foo", state.source)
        self.assertEqual(0, state.position)
        self.assertEqual(0, state.start)

    def test_can_consume(self):
        state = ScannerState("foo")
        c = state.consume()

        self.assertEqual('f', c)
        self.assertEqual(1, state.position)
        self.assertEqual(0, state.start)

    def test_consuming_reaches_eof(self):
        state = ScannerState("f")
        state.consume()
        eof = state.consume()

        self.assertEqual(EOF, eof)
        self.assertEqual(1, state.position)

    def test_consuming_stops_at_eof(self):
        state = ScannerState("f")
        state.consume()
        a = state.consume()
        b = state.consume()
        c = state.consume()

        self.assertEqual([EOF, EOF, EOF], [a, b, c])
        self.assertEqual(1, state.position)
        self.assertEqual(0, state.start)

    def test_backup_works(self):
        state = ScannerState("foo")
        state.consume()
        state.consume()
        state.backup()

    def test_skip_works(self):
        state = ScannerState("aafoo")
        state.skip("a")

        self.assertEqual(2, state.position)
        self.assertEqual('f', state.consume())

    def test_skip_stops_at_eof(self):
        state = ScannerState("aa")
        state.skip("a")

        self.assertEqual(2, state.position)
        self.assertEqual(EOF, state.consume())

    def test_skip_run_works(self):
        state = ScannerState("aafoo")
        state.skip_run("af")

        self.assertEqual(3, state.position)
        self.assertEqual('o', state.consume())

    def test_skip_run__stops_at_eof(self):
        state = ScannerState("aaf")
        state.skip_run("af")

        self.assertEqual(3, state.position)
        self.assertEqual(EOF, state.consume())

    def test_emit_works(self):
        state = ScannerState("aabb")
        state.skip("a")

        self.assertEqual('aa', state.emit())
        self.assertEqual(2, state.position)

    def test_ignore_works(self):
        state = ScannerState("aabb")
        state.skip("a")
        state.ignore()

        self.assertEqual(2, state.position)

    def test_expect_can_succeed(self):
        state = ScannerState('foo')
        c = state.expect('f')
        self.assertEqual('f', c)

    def test_expect_can_fail(self):
        state = ScannerState('foo')
        self.assertRaises(ValueError, state.expect, 'x')

    def test_expect_match_can_succeed(self):
        state = ScannerState('foo')
        c = state.expect_match('fo{2}')
        self.assertEqual('foo', c.group(0))

    def test_expect_match_can_fail(self):
        state = ScannerState('foo')
        self.assertRaises(ValueError, state.expect_match, 'x')

    def test_peek_can_succeed(self):
        state = ScannerState('foo')
        self.assertTrue(state.peek('foo'))

    def test_peek_can_fail(self):
        state = ScannerState('foo')
        self.assertFalse(state.peek('fxo'))

    def test_match_can_succeed(self):
        state = ScannerState('foo123')
        state.consume()
        state.consume()
        state.consume()
        self.assertTrue(state.match(r'\d{3}'))
        self.assertEqual(6, state.position)
        self.assertEqual(EOF, state.consume())
