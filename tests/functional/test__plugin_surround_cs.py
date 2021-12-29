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
        self.eq('f|izz', 'cs"\'', 'f|izz')
        self.eq('"f|izz', 'cs"\'', '"f|izz')

    def test_paren_punctuation_marks(self):
        self.eq('x(a|bc)y', 'cs("', 'x|"abc"y')
        self.eq('x(a|bc)y', 'cs)"', 'x|"abc"y')
        self.eq('x(a|bc)y', 'csb"', 'x|"abc"y')
        self.eq('x(a|bc)y', 'cs({', 'x|{ abc }y')
        self.eq('x(a|bc)y', 'cs){', 'x|{ abc }y')
        self.eq('x(a|bc)y', 'cs(}', 'x|{abc}y')
        self.eq('x(a|bc)y', 'cs)}', 'x|{abc}y')
        self.eq('x|"abc"y', 'cs"(', 'x|( abc )y')
        self.eq('x|"abc"y', 'cs")', 'x|(abc)y')
        self.eq('x"|abc"y', 'cs"(', 'x|( abc )y')
        self.eq('x"|abc"y', 'cs")', 'x|(abc)y')
        self.eq('x(a|bcy', 'cs("', 'x(a|bcy')
        self.eq('xa|bc)y', 'cs("', 'xa|bc)y')

    def test_brace_punctuation_marks(self):
        self.eq('x{a|bc}y', 'cs{(', 'x|( abc )y')
        self.eq('x{a|bc}y', 'cs}(', 'x|( abc )y')
        self.eq('x{a|bc}y', 'cs{)', 'x|(abc)y')
        self.eq('x{a|bc}y', 'cs})', 'x|(abc)y')
        self.eq('x{a|bc}y', 'csB"', 'x|"abc"y')

    def test_square_bracket_punctuation_marks(self):
        self.eq('x[a|bc]y', 'cs["', 'x|"abc"y')
        self.eq('x[a|bc]y', 'cs]"', 'x|"abc"y')
        self.eq('x[a|bc]y', 'csr"', 'x|"abc"y')
        self.eq('x"a|bc"y', 'cs"[', 'x|[ abc ]y')
        self.eq('x"a|bc"y', 'cs"]', 'x|[abc]y')

    def test_angle_bracket_punctuation_marks(self):
        self.eq('x"a|bc"y', 'cs">', 'x|<abc>y')
        self.eq('x[a|bc]y', 'cs]>', 'x|<abc>y')
        self.eq('x<a|bc>y', 'cs>"', 'x|"abc"y')
        self.eq('x<a|bc>y', 'csa"', 'x|"abc"y')
        self.eq('x<a|bc>y', 'cs>}', 'x|{abc}y')
        self.eq('x<a|bc>y', 'cs>{', 'x|{ abc }y')
        self.eq('x\'|abc\'y', 'cs\'<q>', 'x|<q>abc</q>y')
        self.eq('x"|abc"y', 'cs"<x>', 'x|<x>abc</x>y')

    def test_marks_like_stop_comma_dash_underscore_etc(self):
        self.eq('x.a|bc.y', 'cs."', 'x|"abc"y')
        self.eq('x,a|bc,y', 'cs,`', 'x|`abc`y')
        self.eq('x-a|bc-y', 'cs-_', 'x|_abc_y')
        self.eq('x_a|bc_y', 'cs_-', 'x|-abc-y')

    def test_should_work_in_all_cursor_positions(self):
        self.eq('|"abc"', 'cs"\'', "|'abc'")
        self.eq('"|abc"', 'cs"\'', "|'abc'")
        self.eq('"a|bc"', 'cs"\'', "|'abc'")
        self.eq('"ab|c"', 'cs"\'', "|'abc'")
        self.eq('"abc|"', 'cs"\'', "|'abc'")
        self.eq('x(|abc)y', 'cs("', 'x|"abc"y')
        self.eq('x(a|bc)y', 'cs("', 'x|"abc"y')
        self.eq('x(ab|c)y', 'cs("', 'x|"abc"y')
        self.eq('x(abc|)y', 'cs("', 'x|"abc"y')
        self.eq('x(a|bc)y', 'cs)"', 'x|"abc"y')
        self.eq('x(ab|c)y', 'cs)"', 'x|"abc"y')
        self.eq('x(abc|)y', 'cs)"', 'x|"abc"y')
        self.eq('x(|abc)y', 'csb"', 'x|"abc"y')
        self.eq('x(a|bc)y', 'csb"', 'x|"abc"y')
        self.eq('x(ab|c)y', 'csb"', 'x|"abc"y')
        self.eq('x(abc|)y', 'csb"', 'x|"abc"y')
        self.eq('x|"ab"x"cd"x"ef"', 'cs"\'', 'x|\'ab\'x"cd"x"ef"')
        self.eq('x"ab|"x"cd"x"ef"', 'cs"\'', 'x|\'ab\'x"cd"x"ef"')
        self.eq('x"ab"x|"cd"x"ef"', 'cs"\'', 'x"ab|\'x\'cd"x"ef"')
        self.eq('x"ab"x"cd|"x"ef"', 'cs"\'', 'x"ab"x|\'cd\'x"ef"')
        self.eq('x"ab"x"cd"x|"ef"', 'cs"\'', 'x"ab"x"cd|\'x\'ef"')

    def test_should_work_in_all_cursor_positions_bug_01(self):
        self.eq('x|(abc)y', 'cs("', 'x|"abc"y')
        self.eq('x|(abc)y', 'cs)"', 'x|"abc"y')
        self.eq('x|(abc)y', 'csb"', 'x|"abc"y')

    def test_should_work_within_line_for_quote_marks(self):
        self.eq('x"abc|"\n"def"', 'cs"\'', 'x|\'abc\'\n"def"')
        self.eq('_|\n_"ab"_\n_"cd"_\n_"ef"_', 'cs"\'', '_|\n_"ab"_\n_"cd"_\n_"ef"_')
        self.eq('_\n_"ab"_\n_|"cd"_\n_"ef"_', 'cs"\'', '_\n_"ab"_\n_|\'cd\'_\n_"ef"_')
        self.eq('_\n_"ab"_\n_"cd|"_\n_"ef"_', 'cs"\'', '_\n_"ab"_\n_|\'cd\'_\n_"ef"_')

    def test_multiple_cursors(self):
        self.eq('x"a|c"\n"d|c"y', 'cs"]', 'x|[ac]\n|[dc]y')

    def test_tags(self):
        self.eq('|<li>ab</li>', 'cst"', '|"ab"')
        self.eq('<l|i>ab</li>', 'cstta>', '|<a>ab</a>')
        self.eq('<li>a|b</li>', 'cst<a>', '|<a>ab</a>')
        self.eq("'a|b'", "cs'<q>", '|<q>ab</q>')
        self.eq("'a|b'", "cs'tq>", '|<q>ab</q>')
        self.eq("'a|b'", "cs'<div>", '|<div>ab</div>')
        self.eq("'a|b'", "cs'tdiv>", '|<div>ab</div>')
        self.eq('"fi|zz"', 'cs"ti x="y">', '|<i x="y">fizz</i>')
        self.eq('"fi|zz"', 'cs"<i x="y">', '|<i x="y">fizz</i>')
        self.eq('f|izz', 'cst"', 'f|izz')
        self.eq('|<li>ab', 'cst"', '|<li>ab')
        self.eq('<li>f|izz', 'cst"', '<li>f|izz')
        self.eq('|ab</li>', 'cst"', '|ab</li>')
        self.eq('f|izz</li>', 'cst"', 'f|izz</li>')

    def test_can_disable_plugin(self):
        self.normal('"x|xx"')
        self.feed('cs"\'')
        self.assertNormal("|'xxx'")
        self.set_setting('enable_surround', False)
        self.normal('"x|xx"')
        self.feed('cs"\'')
        self.assertNormal('"x|xx"')
        self.set_setting('enable_surround', True)
        self.normal('"x|xx"')
        self.feed('cs"\'')
        self.assertNormal("|'xxx'")

    def test_issue_305_multiple_selection_leaves_cursors_in_the_wrong_place(self):
        self.eq("eats 'fi|sh'\neats 'fi|sh'\neats 'fi|sh'", "cs'(", "eats |( fish )\neats |( fish )\neats |( fish )")
