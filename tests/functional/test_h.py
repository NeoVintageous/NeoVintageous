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


class Test_h(unittest.FunctionalTestCase):

    def test_n_h(self):
        self.eq('ab|cd', 'n_h', 'a|bcd')
        self.eq('foo bar b|az', 'n_7h', 'fo|o bar baz')
        self.eq('pin|g', 'n_9h', '|ping')
        self.eq('pin|g\n', 'n_9h', '|ping\n')
        self.eq('x\npin|g', 'n_9h', 'x\n|ping')
        self.eq('x\npin|g\n', 'n_9h', 'x\n|ping\n')

    def test_n_h_empty_lines(self):
        self.eq('|', 'n_h', '|')
        self.eq('\n\n|\n\n', 'n_h', '\n\n|\n\n')

    def test_v_h(self):
        self.eq('ab|c', 'v_h', 'a|bc|')
        self.eq('ab|c', 'v_1h', 'a|bc|')
        self.eq('foo bar |baz', 'v_6h', 'fo|o bar b|az')
        self.eq('pin|g', 'v_9h', '|ping|')
        self.eq('ping|\n', 'v_9h', '|ping\n|')
        self.eq('abc|\nx', 'v_5h', '|abc\n|x')
        self.eq('x\npin|g', 'v_9h', 'x\n|ping|')
        self.eq('x\nping|\n', 'v_9h', 'x\n|ping\n|')
        self.eq('x\nabc|\nx', 'v_5h', 'x\n|abc\n|x')

    def test_v_h_empty_lines(self):
        self.eq('|', 'v_h', '|')
        self.eq('\n\n|\n|\n', 'v_h', '\n\n|\n|\n')

    def test_v_h_reverse(self):
        self.visual('hello |wo|rld')
        self.feed('v_5h')
        self.assertRVisual('he|llo w|orld')

    def test_v_h_to_sol(self):
        self.visual('x\nhe|ll|o')
        self.feed('v_7h')
        self.assertRVisual('x\n|hel|lo')

    def test_v_h_to_sol_2(self):
        self.visual('x\na|b\n|')
        self.feed('v_9h')
        self.assertRVisual('x\n|ab|\n')

    def test_v_h_to_sol_3(self):
        self.visual('x\n|ab\n|')
        self.feed('v_9h')
        self.assertVisual('x\n|a|b\n')

    def test_v_h_to_sol_4(self):
        self.visual('x\na|b\ncd\n|')
        self.feed('v_9h')
        self.assertVisual('x\na|b\nc|d\n')

    def test_v_h_reversed_selections(self):
        self.rvisual('hello |wor|ld')
        self.feed('v_4h')
        self.assertVisual('he|llo wor|ld')

    def test_h_internal_mode(self):
        self.eqr('hel|lo', 'h', 'N_he|l|lo')

    def test_b_h(self):
        self.eq('fi|z|z\nbu|z|z', 'b_h', 'f|iz|z\nb|uz|z')
        self.eq('|fi|zz\n|bu|zz', 'b_h', '|f|izz\n|b|uzz')
        self.eq('|f|izz\n|b|uzz', 'b_h', '|f|izz\n|b|uzz')
        self.eq('fizz|e|r\nbuzz|e|r', 'b_3h', 'f|izze|r\nb|uzze|r')
        self.eq('x\nfi|z|z\nbu|z|z', 'b_9h', 'x\n|fiz|z\n|buz|z')

    def test_b_h_jagged_selections(self):
        # For jagged selections (on the rhs), only those sticking out need to move leftwards.
        # Example ([] denotes the selection):
        #
        #   10 foo bar foo [bar]
        #   11 foo bar foo [bar foo bar]
        #   12 foo bar foo [bar foo]
        #
        #  Only lines 11 and 12 should move when we press h.
        self.eq('|a| b\n|a b c d|\n|a b c|', 'b_h', '|a| b\n|a b c |d\n|a b |c')
