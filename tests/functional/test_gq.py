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


@unittest.skipIf(unittest.ST_VERSION >= 4000, 'broken in ST4 see https://github.com/sublimehq/sublime_text/issues/3177')
class Test_gq_wrapped_at_5(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('WrapPlus.include_line_endings', None)
        self.settings().set('wrap_width', 5)

    def test_n(self):
        self.eq('  a1 a2 a3\n  x1 |x2 x3\n  b1 b2 b3\n', 'gq$', '  a1 a2 a3\n  x1\n  x2\n  |x3\n  b1 b2 b3\n')
        self.eq('  a1 a2 a3\n  x1 |x2 x3\n  b1 b2 b3\n', 'gq$', '  a1 a2 a3\n  x1\n  x2\n  |x3\n  b1 b2 b3\n')


@unittest.skipIf(unittest.ST_VERSION >= 4000, 'broken in ST4 see https://github.com/sublimehq/sublime_text/issues/3177')
class Test_gq_wrapped_at_80(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('WrapPlus.include_line_endings', None)
        self.settings().set('wrap_width', 80)

    def test_gqip(self):
        self.eq('|aaa\nbbb\nccc\n', 'gqip', 'aaa bbb ccc\n|')
        self.eq('x\n\n    |aaa\nbbb\nccc\n', 'gqip', 'x\n\n    aaa bbb ccc\n|')

    def test_gqip_should_only_mutate_current_paragraph(self):
        self.eq('x\n\na|a\nbb\ncc\n\nyyy', 'gqip', 'x\n\naa bb cc\n|\nyyy')
        self.eq('x\n\na|a\nbb\ncc\n\ny\n', 'gqip', 'x\n\naa bb cc\n|\ny\n')

    def test_gq_brace(self):
        self.eq('|aaa\nbbb\nccc\n', 'gq}', 'aaa bbb ccc\n|'),
        self.eq('|aaa\nbbb\nccc', 'gq}', '|aaa bbb ccc'),

    def test_gq_brace_should_only_mutate_current_paragraph(self):
        self.eq('x\n\na|a\nbb\ncc\n\nyyy', 'gqip', 'x\n\naa bb cc\n|\nyyy')
        self.eq('x\n\na|a\nbb\ncc\n\ny\n', 'gqip', 'x\n\naa bb cc\n|\ny\n')

    def test_v_gq(self):
        self.eq('x\n\n|aa\nbb\ncc|\n\nyyy\n', 'v_gq', 'n_x\n\n|aa bb cc\n\nyyy\n')
        self.eq('x\n\na|a\nbb\ncc|\n\nyyy\n', 'v_gq', 'n_x\n\n|aa bb cc\n\nyyy\n')
        self.eq('x\n\n|one\ntwo\nthree|\n\nx', 'v_gq', 'n_x\n\n|one two three\n\nx')
        self.eq('x\n\n|one\ntwo\nthree\n|\nx', 'v_gq', 'n_x\n\n|one two three\n\nx')
        self.eq('x\n|one\ntwo\nthree|\nx', 'v_gq', 'n_x\n|one two three\nx')
        self.eq('x\n|one\ntwo\nthree\n|x', 'v_gq', 'n_x\n|one two three\nx')
        self.eq('    abc\n|        fizz\n        bu|zz\n\n', 'v_gq', 'n_    abc\n        |fizz buzz\n\n')
        self.eq('r_    abc\n|        fizz\n        bu|zz\n\n', 'v_gq', 'n_    abc\n        |fizz buzz\n\n')

    def test_v_gq_cursors_should_move_to_the_first_non_blank_character_of_the_line(self):
        self.eq('x\n\nx a|a\nbb\ncc|\n\nyyy\n', 'v_gq', 'n_x\n\n|x aa bb cc\n\nyyy\n')
        self.eq('x\n\n    x a|a\nbb\ncc|\n\nyyy\n', 'v_gq', 'n_x\n\n    |x aa bb cc\n\nyyy\n')


class Test_gq_python_syntax(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('WrapPlus.include_line_endings', None)
        self.settings().set('wrap_width', 80)

    def feed(self, seq):
        self.syntax('Packages/Python/Python.sublime-syntax')
        super().feed(seq)

    def test_gqip(self):
        self.eq('x = 1\n\n    |# aaa\n    # bbb\n    # ccc\n', 'gqip', 'x = 1\n\n    # aaa bbb ccc\n|')

    def test_v_gq(self):
        self.eq('    if x:\n|        # fizz\n        # bu|zz\n\n', 'v_gq', 'n_    if x:\n        |# fizz buzz\n\n')
        self.eq('r_    if x:\n|        # fizz\n        # bu|zz\n\n', 'v_gq', 'n_    if x:\n        |# fizz buzz\n\n')
        self.eq('#\n#\n|# one\n# two\n|#\n#\n', 'V_gq', 'n_#\n#\n|# one two\n#\n#\n')
        self.eq('r_#\n#\n|# one\n# two\n|#\n#\n', 'V_gq', 'n_#\n#\n|# one two\n#\n#\n')
