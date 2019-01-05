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


class TestSurround_cs(unittest.FunctionalTestCase):

    def test_quote_marks(self):
        self.eq('x"a|bc"y', 'cs"\'', "x|'abc'y")
        self.eq('x"a|bc"y', 'cs"`', 'x|`abc`y')
        self.eq('x`a|bc`y', 'cs`"', 'x|"abc"y')
        self.eq('x`a|bc`y', 'cs`\'', 'x|\'abc\'y')
        self.eq("x'a|bc'y", 'cs\'"', 'x|"abc"y')
        self.eq("x'a|bc'y", 'cs\'"', 'x|"abc"y')
        self.eq("x'a|bc'y", 'cs\'`', 'x|`abc`y')

    def test_paren_punctuation_marks(self):
        self.eq('x(a|bc)y', 'cs("', 'x|"abc"y')
        self.eq('x(a|bc)y', 'cs)"', 'x|"abc"y')
        self.eq('x(a|bc)y', 'cs({', 'x|{ abc }y')
        self.eq('x(a|bc)y', 'cs){', 'x|{ abc }y')
        self.eq('x(a|bc)y', 'cs(}', 'x|{abc}y')
        self.eq('x(a|bc)y', 'cs)}', 'x|{abc}y')
        self.eq('x"|abc"y', 'cs"(', 'x|( abc )y')
        self.eq('x"|abc"y', 'cs")', 'x|(abc)y')

    def test_brace_punctuation_marks(self):
        self.eq('x{a|bc}y', 'cs{(', 'x|( abc )y')
        self.eq('x{a|bc}y', 'cs}(', 'x|( abc )y')
        self.eq('x{a|bc}y', 'cs{)', 'x|(abc)y')
        self.eq('x{a|bc}y', 'cs})', 'x|(abc)y')

    def test_square_bracket_punctuation_marks(self):
        self.eq('x[a|bc]y', 'cs["', 'x|"abc"y')
        self.eq('x[a|bc]y', 'cs]"', 'x|"abc"y')
        self.eq('x"a|bc"y', 'cs"[', 'x|[ abc ]y')
        self.eq('x"a|bc"y', 'cs"]', 'x|[abc]y')

    def test_angle_bracket_punctuation_marks(self):
        self.eq('x"a|bc"y', 'cs">', 'x|<abc>y')
        self.eq('x[a|bc]y', 'cs]>', 'x|<abc>y')
        self.eq('x<a|bc>y', 'cs>"', 'x|"abc"y')
        self.eq('x<a|bc>y', 'cs>}', 'x|{abc}y')
        self.eq('x<a|bc>y', 'cs>{', 'x|{ abc }y')
        # TODO Fix cs{target}<*> e.g. ('x"|abc"y', 'cs"<q>', 'x|<q>abc</q>y')

    def test_marks_like_stop_comma_dash_underscore_etc(self):
        self.eq('x.a|bc.y', 'cs."', 'x|"abc"y')
        self.eq('x,a|bc,y', 'cs,`', 'x|`abc`y')
        self.eq('x-a|bc-y', 'cs-_', 'x|_abc_y')
        self.eq('x_a|bc_y', 'cs_-', 'x|-abc-y')

    def test_should_work_in_all_cursor_positions(self):
        self.eq('"|abc"', 'cs"\'', "|'abc'")
        self.eq('"a|bc"', 'cs"\'', "|'abc'")
        self.eq('"ab|c"', 'cs"\'', "|'abc'")
        self.eq('"abc|"', 'cs"\'', "|'abc'")
        # TODO Fix cs{target}{replacement} should work at cursor position zero e.g. ('|"abc"', 'cs"\'', "|'abc'")

    def test_multiple_cursors(self):
        self.eq('x"a|c"\n"d|c"y', 'cs"]', 'x|[ac]\n|[dc]y')

    def test_issue_305_multiple_selection_leaves_cursors_in_the_wrong_place(self):
        self.eq("eats 'fi|sh'\neats 'fi|sh'\neats 'fi|sh'", "cs'(", "eats |( fish )\neats |( fish )\neats |( fish )")

    def test_tags(self):
        self.eq('|<li>ab</li>', 'cst"', '|"ab"')
        self.eq('<l|i>ab</li>', 'cstta>', '|<a>ab</a>')
        self.eq('<li>a|b</li>', 'cst<a>', '|<a>ab</a>')
        self.eq("'a|b'", "cs'<q>", '|<q>ab</q>')
        self.eq("'a|b'", "cs'tq>", '|<q>ab</q>')
        self.eq("'a|b'", "cs'<div>", '|<div>ab</div>')
        self.eq("'a|b'", "cs'tdiv>", '|<div>ab</div>')
