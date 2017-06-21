import unittest

from NeoVintageous.lib.ex.parser.parser import ParserState


class TestParserState(unittest.TestCase):

    def test_can_instantiate(self):
        parser_state = ParserState("foobar")
        self.assertEqual(parser_state.scanner.state.source, "foobar")
