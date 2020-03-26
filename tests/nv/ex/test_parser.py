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

from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.parser import _ParsedCommandLine
from NeoVintageous.nv.ex.parser import TokenComma
from NeoVintageous.nv.ex.parser import TokenDigits
from NeoVintageous.nv.ex.parser import TokenDollar
from NeoVintageous.nv.ex.parser import TokenDot
from NeoVintageous.nv.ex.parser import TokenMark
from NeoVintageous.nv.ex.parser import TokenOffset
from NeoVintageous.nv.ex.parser import TokenPercent
from NeoVintageous.nv.ex.parser import TokenSearchBackward
from NeoVintageous.nv.ex.parser import TokenSearchForward
from NeoVintageous.nv.ex.parser import TokenSemicolon
from NeoVintageous.nv.ex.parser import _ParserState
from NeoVintageous.nv.ex.parser import parse_command_line
from NeoVintageous.nv.ex.tokens import TokenCommand


class TestParsedCommandLine(unittest.TestCase):

    def test_can_instantiate(self):
        range_node = RangeNode(["foo"], ["bar"], False)
        command = TokenCommand('substitute')
        command_line_node = _ParsedCommandLine(range_node, command)

        self.assertEqual(range_node, command_line_node.line_range)
        self.assertEqual(command, command_line_node.command)

    def test_to_str(self):
        self.assertEqual(str(_ParsedCommandLine(RangeNode(['1'], ['10'], ','), 'cmd')), '1,10cmd')
        self.assertEqual(str(_ParsedCommandLine(RangeNode(['1'], ['10'], ','), None)), '1,10')

    def test_validate(self):
        class NotAddressableCommand:
            addressable = False

        class AddressableCommand:
            addressable = True

        _ParsedCommandLine(RangeNode(), AddressableCommand()).validate()
        _ParsedCommandLine(RangeNode(), NotAddressableCommand()).validate()
        _ParsedCommandLine(RangeNode(['1'], ['2'], ';'), AddressableCommand()).validate()

        with self.assertRaisesRegex(Exception, 'E481: No range allowed'):
            _ParsedCommandLine(RangeNode(['1'], ['2'], ';'), NotAddressableCommand()).validate()


class TestParserState(unittest.TestCase):

    def test_can_instantiate(self):
        parser_state = _ParserState("foobar")
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

    def test_invalid_offset(self):
        self.assertRaises(ValueError, parse_command_line, '+2$')
        self.assertRaises(ValueError, parse_command_line, '$+2')
        self.assertRaises(ValueError, parse_command_line, '1,$+2')

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

    def test_search_forward_start_and_end(self):
        parsed = parse_command_line('.+5/foo/,.+10/bar/')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenOffset([5]), TokenSearchForward('foo')])
        self.assertEqual(parsed.line_range.end, [TokenDot(), TokenOffset([10]), TokenSearchForward('bar')])

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

    def test_can_parse_search_backward_with_offset(self):
        parsed = parse_command_line('?foo?+10')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo'), TokenOffset([10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_search_backward_end(self):
        parsed = parse_command_line('?foo?+5,?bar?+10+20')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo'), TokenOffset([5])])
        self.assertEqual(parsed.line_range.end, [TokenSearchBackward('bar'), TokenOffset([10, 20])])

    def test_search_backward_start_and_end(self):
        parsed = parse_command_line('.+5?foo?,.+10?bar?')
        self.assertEqual(parsed.line_range.start, [TokenDot(), TokenOffset([5]), TokenSearchBackward('foo')])
        self.assertEqual(parsed.line_range.end, [TokenDot(), TokenOffset([10]), TokenSearchBackward('bar')])

    def test_can_parse_search_backward_with_offsets(self):
        parsed = parse_command_line('?foo?+10+10+10')
        self.assertEqual(parsed.line_range.start, [TokenSearchBackward('foo'), TokenOffset([10, 10, 10])])
        self.assertEqual(parsed.line_range.end, [])

    def test_can_parse_dollar_on_its_own(self):
        parsed = parse_command_line('$')
        self.assertEqual(parsed.line_range.start, [TokenDollar()])

    def test_invalid_dollar(self):
        self.assertRaises(ValueError, parse_command_line, '1,1$')
        self.assertRaises(ValueError, parse_command_line, '1,$$')
        self.assertRaises(ValueError, parse_command_line, '1,.$')

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

    def test_invalid_dot(self):
        self.assertRaises(ValueError, parse_command_line, '+1.')
        self.assertRaises(ValueError, parse_command_line, '1,+2.')

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

    def test_fails_dot_digits(self):
        self.assertRaises(ValueError, parse_command_line, '.10')
        self.assertRaises(ValueError, parse_command_line, '10,.10')

    def test_unknown_command_raises_exception(self):
        with self.assertRaisesRegex(Exception, 'E492: Not an editor command'):
            parse_command_line('foobar')

        with self.assertRaisesRegex(Exception, 'E492: Not an editor command'):
            parse_command_line('1,2foobar')

        with self.assertRaisesRegex(Exception, 'E492: Not an editor command'):
            parse_command_line('1,$foobar')


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
        self.assertEqual(parsed.line_range.end, [])
        parsed = parse_command_line("%,%")
        self.assertEqual(parsed.line_range.start, [TokenPercent()])
        self.assertEqual(parsed.line_range.end, [TokenPercent()])

    def test_invalid_percent(self):
        self.assertRaises(ValueError, parse_command_line, '1%')
        self.assertRaises(ValueError, parse_command_line, '%,1%')
        self.assertRaises(ValueError, parse_command_line, '%%')


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
