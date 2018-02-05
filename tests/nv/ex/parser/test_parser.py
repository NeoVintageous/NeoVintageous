import unittest

from NeoVintageous.nv.ex.parser.parser import parse_command_line
from NeoVintageous.nv.ex.parser.parser import ParserState
from NeoVintageous.nv.ex.parser.tokens import TokenComma
from NeoVintageous.nv.ex.parser.tokens import TokenDigits
from NeoVintageous.nv.ex.parser.tokens import TokenDollar
from NeoVintageous.nv.ex.parser.tokens import TokenDot
from NeoVintageous.nv.ex.parser.tokens import TokenMark
from NeoVintageous.nv.ex.parser.tokens import TokenOffset
from NeoVintageous.nv.ex.parser.tokens import TokenPercent
from NeoVintageous.nv.ex.parser.tokens import TokenSearchBackward
from NeoVintageous.nv.ex.parser.tokens import TokenSearchForward
from NeoVintageous.nv.ex.parser.tokens import TokenSemicolon


class TestParserState(unittest.TestCase):

    def test_can_instantiate(self):
        parser_state = ParserState("foobar")
        self.assertEqual(parser_state.scanner.state.source, "foobar")


class TestParseLineRef(unittest.TestCase):

    def test_can_parse_empty(self):
        parsed = parse_command_line('')
        self.assertEqual(parsed.line_range, None)
        self.assertEqual(parsed.command, None)

    def test_can_parse_dot_as_start_line(self):
        parsed = parse_command_line('.')
        self.assertEqual(parsed.line_range.start, [TokenDot()])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_dot_with_offset(self):
        parsed = parse_command_line('.+10')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_lone_offset(self):
        parsed = parse_command_line('+10')
        self.assertEqual(parsed.line_range.start, [TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_fails_if_dot_after_offset(self):
        self.assertRaises(ValueError, parse_command_line, '+10.')

    def test_can_parse_multiple_offsets(self):
        parsed = parse_command_line('+10+10')
        self.assertEqual(parsed.line_range.start, [TokenOffset([10, 10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_forward(self):
        parsed = parse_command_line('/foo/')
        self.assertEqual(parsed.line_range.start, [TokenSearchForward('foo')])
        self.assertEqual(parsed.line_range.end, [])

    def test_search_forward_clears_previous_references(self):
        parsed = parse_command_line('./foo/')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenSearchForward('foo')])
        self.assertEqual(parsed.line_range.end, [])

    def test_search_forward_clears_previous_references_with_offsets(self):
        parsed = parse_command_line('.+10/foo/')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenOffset([10]), TokenSearchForward('foo')])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_backward(self):
        parsed = parse_command_line('?foo?')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo')])
        self.assertEqual(parsed.line_range.end, [])

    def test_search_backward_clears_previous_references(self):
        parsed = parse_command_line('.?foo?')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenSearchBackward('foo')])
        self.assertEqual(parsed.line_range.end, [])

    def test_search_backward_clears_previous_references_with_offsets(self):
        parsed = parse_command_line('.+10?foo?')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenOffset([10]), TokenSearchBackward('foo')])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_forward_with_offset(self):
        parsed = parse_command_line('/foo/+10')
        self.assertEqual(parsed.line_range.start, [TokenSearchForward('foo'), TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_forward_with_offsets(self):
        parsed = parse_command_line('/foo/+10+10+10')
        self.assertEqual(parsed.line_range.start, [TokenSearchForward('foo'), TokenOffset([10, 10, 10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_bacward_with_offset(self):
        parsed = parse_command_line('?foo?+10')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo'), TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_bacward_with_offsets(self):
        parsed = parse_command_line('?foo?+10+10+10')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo'), TokenOffset([10, 10, 10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_dollar_on_its_own(self):
        parsed = parse_command_line('$')
        self.assertEqual(parsed.line_range.start, [TokenDollar()])

    def test_can_parse_dollar_with_company(self):
        parsed = parse_command_line('0,$')
        self.assertEqual(parsed.line_range.start, [TokenDigits('0')])
        self.assertEqual(parsed.line_range.end, [TokenDollar()])

    def test_fails_if_dollar_offset(self):
        self.assertRaises(ValueError, parse_command_line, '$+10')

    def test_fails_if_preceded_by_anything(self):
        self.assertRaises(ValueError, parse_command_line, '.$')
        self.assertRaises(ValueError, parse_command_line, '/foo/$')
        self.assertRaises(ValueError, parse_command_line, '100$')

    def test_can_parse_lone_comma(self):
        parsed = parse_command_line(',')
        self.assertEqual(parsed.line_range.separator, TokenComma())

    def test_can_parse_dot_comma(self):
        parsed = parse_command_line('.,')
        self.assertEqual(parsed.line_range.start, [TokenDot()])
        self.assertEqual(parsed.line_range.end, [])
        self.assertEqual(parsed.line_range.separator, TokenComma())

    def test_can_parse_comma_dot(self):
        parsed = parse_command_line(',.')
        self.assertEqual(parsed.line_range.separator, TokenComma())
        self.assertEqual(parsed.line_range.start, [])
        self.assertEqual(parsed.line_range.end, [TokenDot()])

    def test_can_parse_lone_smicolon(self):
        parsed = parse_command_line(';')
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_parse_dot_smicolon(self):
        parsed = parse_command_line('.;')
        self.assertEqual(parsed.line_range.start, [TokenDot()])
        self.assertEqual(parsed.line_range.end, [])
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_parse_smicolon_dot(self):
        parsed = parse_command_line(';.')
        self.assertEqual(parsed.line_range.start, [])
        self.assertEqual(parsed.line_range.end, [TokenDot()])
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_parse_comma_offset(self):
        parsed = parse_command_line(',+10')
        self.assertEqual(parsed.line_range.separator, TokenComma())
        self.assertEqual(parsed.line_range.start, [])
        self.assertEqual(parsed.line_range.end, [TokenOffset([10])])

    def test_can_parse_offset_comma_offset(self):
        parsed = parse_command_line('+10,+10')
        self.assertEqual(parsed.line_range.separator, TokenComma())
        self.assertEqual(parsed.line_range.start, [TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [TokenOffset([10])])

    def test_can_parse_semicolon_offset(self):
        parsed = parse_command_line('+10;+10')
        self.assertEqual(parsed.line_range.start, [TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [TokenOffset([10])])
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_parse_number(self):
        parsed = parse_command_line('10')
        self.assertEqual(parsed.line_range.start, [TokenDigits('10')])

    def test_can_parse_number_right_hand_side(self):
        parsed = parse_command_line(',10')
        self.assertEqual(parsed.line_range.start, [])
        self.assertEqual(parsed.line_range.end, [TokenDigits('10')])

    def test_fails_if_dot_digits(self):
        self.assertRaises(ValueError, parse_command_line, '.10')


class TestParseLineRefTokenComma(unittest.TestCase):

    def test_can_parse_long_sequence(self):
        # Vim allows this.
        parsed = parse_command_line('1,2,3,4')
        self.assertEqual(parsed.line_range.start, [TokenDigits('3')])
        self.assertEqual(parsed.line_range.end, [TokenDigits('4')])


class TestParseLineRefParseSubstituteCommand(unittest.TestCase):

    def test_can_parse_it_on_its_own(self):
        parsed = parse_command_line('substitute')
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_alias(self):
        parsed = parse_command_line('s')
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_with_simple_range(self):
        parsed = parse_command_line('4s')
        self.assertEqual(parsed.line_range.start, [TokenDigits('4')])
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_with_start_and_end_lines(self):
        parsed = parse_command_line('4,5s')
        self.assertEqual(parsed.line_range.start, [TokenDigits('4')])
        self.assertEqual(parsed.line_range.end, [TokenDigits('5')])
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_with_search_forward(self):
        parsed = parse_command_line('/foo/s')
        self.assertEqual(parsed.line_range.start, [TokenSearchForward('foo')])
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_with_search_backward(self):
        parsed = parse_command_line('?foo?s')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo')])
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_with_search_backward_and_search_forward(self):
        parsed = parse_command_line('?foo?,/bar/s')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo')])
        self.assertEqual(parsed.line_range.end, [TokenSearchForward('bar')])
        self.assertEqual(parsed.command.content, 'substitute')

    def test_can_parse_with_zero_and_dollar(self):
        parsed = parse_command_line('0,$s')
        self.assertEqual(parsed.line_range.start, [TokenDigits('0')])
        self.assertEqual(parsed.line_range.end, [TokenDollar()])
        self.assertEqual(parsed.command.content, 'substitute')


class TestParseLineRefPercent(unittest.TestCase):

    def test_can_parse_percent(self):
        parsed = parse_command_line("%")
        self.assertEqual(parsed.line_range.start, [TokenPercent()])


class TestParseLineRefSetLineRangeSeparator(unittest.TestCase):

    def test_can_set_comma(self):
        parsed = parse_command_line(",")
        self.assertEqual(parsed.line_range.separator, TokenComma())

    def test_can_set_semicolon(self):
        parsed = parse_command_line(";")
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_set_comma_multiple_times(self):
        parsed = parse_command_line("1,2,3,4")
        self.assertEqual(parsed.line_range.separator, TokenComma())

    def test_can_set_semicolon_multiple_times(self):
        parsed = parse_command_line("1;2;3;4")
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_set_multiple_times_semicolon_last(self):
        parsed = parse_command_line("1;2,3;4")
        self.assertEqual(parsed.line_range.separator, TokenSemicolon())

    def test_can_set_multiple_times_comma_last(self):
        parsed = parse_command_line("1;2;3,4")
        self.assertEqual(parsed.line_range.separator, TokenComma())


class TestParseLineRefParseMarks(unittest.TestCase):

    def test_can_parse_it_on_its_own(self):
        parsed = parse_command_line("'a")
        self.assertEqual(parsed.line_range.start, [TokenMark('a')])

    def test_can_parse_on_two_sides(self):
        parsed = parse_command_line("'a,'b")
        self.assertEqual(parsed.line_range.start, [TokenMark('a')])
        self.assertEqual(parsed.line_range.end, [TokenMark('b')])


class TestParseLineRefParseOnlyCommand(unittest.TestCase):

    def test_can_parse_it_on_its_own(self):
        parsed = parse_command_line('only')
        self.assertEqual(parsed.command.content, 'only')

    def test_can_parse_alias(self):
        parsed = parse_command_line('on')
        self.assertEqual(parsed.command.content, 'only')


class TestParseLineRefParseRegistersCommand(unittest.TestCase):

    def test_can_parse_it_on_its_own(self):
        parsed = parse_command_line('registers')
        self.assertEqual(parsed.command.content, 'registers')

    def test_can_parse_alias(self):
        parsed = parse_command_line('reg')
        self.assertEqual(parsed.command.content, 'registers')


class TestParseLineRefParseWriteCommand(unittest.TestCase):

    def test_can_parse_it_on_its_own(self):
        parsed = parse_command_line('write')
        self.assertEqual(parsed.command.content, 'write')

    def test_can_parse_alias(self):
        parsed = parse_command_line('w')
        self.assertEqual(parsed.command.content, 'write')
