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


class Test_gq(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('WrapPlus.include_line_endings', None)

    def test_gqip(self):
        self.eq('|aaa\nbbb\nccc\n', 'gqip', '|aaa bbb ccc\n')

    def test_gqip_should_only_mutate_current_paragraph(self):
        self.eq('x\n\na|a\nbb\ncc\n\nyyy', 'gqip', 'x\n\n|aa bb cc\n\nyyy')
        self.eq('x\n\na|a\nbb\ncc\n\ny\n', 'gqip', 'x\n\n|aa bb cc\n\ny\n')

    def test_gq_brace(self):
        self.eq('|aaa\nbbb\nccc\n', 'gq}', 'aaa bbb ccc\n|'),
        self.eq('|aaa\nbbb\nccc', 'gq}', 'aaa bbb cc|c'),

    def test_gq_brace_should_only_mutate_current_paragraph(self):
        self.eq('x\n\na|a\nbb\ncc\n\nyyy', 'gqip', 'x\n\n|aa bb cc\n\nyyy')
        self.eq('x\n\na|a\nbb\ncc\n\ny\n', 'gqip', 'x\n\n|aa bb cc\n\ny\n')

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

    def feed(self, seq):
        self.view.assign_syntax('Packages/Python/Python.sublime-syntax')
        super().feed(seq)

    def test_v_gq(self):
        self.eq('    if x:\n|        # fizz\n        # bu|zz\n\n', 'v_gq', 'n_    if x:\n        |# fizz buzz\n\n')
        self.eq('r_    if x:\n|        # fizz\n        # bu|zz\n\n', 'v_gq', 'n_    if x:\n        |# fizz buzz\n\n')
