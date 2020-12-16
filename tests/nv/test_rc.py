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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.rc import _parse_line
from NeoVintageous.nv.rc import _PARSE_LINE_PATTERN


class TestRcfile(unittest.TestCase):

    def test_regex_does_not_match_empty_line(self):
        self.assertIsNone(_PARSE_LINE_PATTERN.match(''))

    def test_regex_does_not_match_comments(self):
        self.assertIsNone(_PARSE_LINE_PATTERN.match('" comment'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('"map x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('" map x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('"noremap x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('" noremap x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('" let mapleader=,'))

    def test_regex_does_not_match_plain_text(self):
        self.assertIsNone(_PARSE_LINE_PATTERN.match('foo'))

    def test_regex_matches_valid_commands(self):
        self.assertIsNotNone(_PARSE_LINE_PATTERN.match('let mapleader=,'))
        self.assertIsNotNone(_PARSE_LINE_PATTERN.match('noremap x y'))
        self.assertIsNotNone(_PARSE_LINE_PATTERN.match('nnoremap x y'))
        self.assertIsNotNone(_PARSE_LINE_PATTERN.match('onoremap x y'))
        self.assertIsNotNone(_PARSE_LINE_PATTERN.match('snoremap x y'))
        self.assertIsNotNone(_PARSE_LINE_PATTERN.match('vnoremap x y'))

    def test_parse_line_return_none_for_non_commands(self):
        self.assertEquals(None, _parse_line(''))
        self.assertEquals(None, _parse_line('"'))
        self.assertEquals(None, _parse_line('foobar'))
        self.assertEquals(None, _parse_line('" foobar'))
        self.assertEquals(None, _parse_line('":let mapleader=,'))
        self.assertEquals(None, _parse_line('":map x zy'))
        self.assertEquals(None, _parse_line('":noremap x zy'))
        self.assertEquals(None, _parse_line('zap x zy'))

    def test_parse_line_returns_valid_commands(self):
        self.assertEquals(':let mapleader=,', _parse_line(':let mapleader=,'))
        self.assertEquals(':noremap x yz', _parse_line(':noremap x yz'))
        self.assertEquals(':inoremap x yz', _parse_line(':inoremap x yz'))
        self.assertEquals(':nnoremap x yz', _parse_line(':nnoremap x yz'))
        self.assertEquals(':onoremap x yz', _parse_line(':onoremap x yz'))
        self.assertEquals(':snoremap x yz', _parse_line(':snoremap x yz'))
        self.assertEquals(':vnoremap x yz', _parse_line(':vnoremap x yz'))

    def test_parse_line_colon_prefix_should_be_optional(self):
        self.assertEquals(':let mapleader=,', _parse_line('let mapleader=,'))
        self.assertEquals(':noremap x yz', _parse_line('noremap x yz'))
        self.assertEquals(':inoremap x yz', _parse_line('inoremap x yz'))
        self.assertEquals(':nnoremap x yz', _parse_line('nnoremap x yz'))
        self.assertEquals(':onoremap x yz', _parse_line('onoremap x yz'))
        self.assertEquals(':snoremap x yz', _parse_line('snoremap x yz'))
        self.assertEquals(':vnoremap x yz', _parse_line('vnoremap x yz'))

    def test_parse_line_strips_trailing_whitespace(self):
        self.assertEquals(':let mapleader=,', _parse_line('let mapleader=,    '))
        self.assertEquals(':noremap x yz', _parse_line('noremap x yz  '))

    def test_regex_does_not_match_recursive_mappings(self):
        self.assertIsNone(_PARSE_LINE_PATTERN.match('map x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('imap x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('nmap x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('omap x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('smap x y'))
        self.assertIsNone(_PARSE_LINE_PATTERN.match('vmap x y'))

    def test_parse_line_returns_none_for_recursive_mapping_commands(self):

        # The recursive mapping commands are disabled, and will emit an error
        # message to the user because:
        # * They were not implement correctly in the first place.
        # * Avoid potential problems in the future such as recursive mappings
        #   being implemented in the future causing user mappings which worked
        #   fine, but now cause a hange due the mapping now being recursive.

        self.assertEquals(None, _parse_line(':map x yz'))
        self.assertEquals(None, _parse_line(':imap x yz'))
        self.assertEquals(None, _parse_line(':nmap x yz'))
        self.assertEquals(None, _parse_line(':omap x yz'))
        self.assertEquals(None, _parse_line(':smap x yz'))
        self.assertEquals(None, _parse_line(':vmap x yz'))
        self.assertEquals(None, _parse_line('map x yz'))
        self.assertEquals(None, _parse_line('imap x yz'))
        self.assertEquals(None, _parse_line('nmap x yz'))
        self.assertEquals(None, _parse_line('omap x yz'))
        self.assertEquals(None, _parse_line('smap x yz'))
        self.assertEquals(None, _parse_line('vmap x yz'))

    @unittest.mock.patch('NeoVintageous.nv.rc.message')
    def test_unescaped_pipe_character_is_invalid(self, message):
        tests = (
            'noremap |',
            'noremap | |',
            'noremap || ||',
            'noremap x |',
            'noremap | y',
            'noremap abc x|y',
            'noremap x|y abc'
        )

        for i, test in enumerate(tests):
            self.assertEquals(None, _parse_line(test))
            self.assertEqual(message.call_count, i + 1)

    def test_escaped_pipe_character_is_valid(self):
        tests = (
            (':noremap <bar> <bar>', ':noremap <bar> <bar>'),
            (':noremap <bar> \\|', ':noremap <bar> <bar>'),
            (':noremap \\| \\|', ':noremap <bar> <bar>'),
            (':noremap \\| <bar>', ':noremap <bar> <bar>'),
            (':noremap x \\|', ':noremap x <bar>'),
            (':noremap x a\\|c', ':noremap x a<bar>c'),
            (':noremap x a\\|\\|c', ':noremap x a<bar><bar>c')
        )

        for value, expected in tests:
            self.assertEqual(expected, _parse_line(value))
