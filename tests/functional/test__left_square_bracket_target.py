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


class TestLeftSquareBracketTarget(unittest.FunctionalTestCase):

    def test_n_paren(self):
        self.eq('x(\n_|)_', 'n_[(', 'x|(\n_)_')

    def test_n_brace(self):
        self.eq('x{\n_|}_', 'n_[{', 'x|{\n_}_')

    def test_n_brace_balanced(self):
        self.eq('{ a { b { x |} c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a { b { x } c |} d }', 'n_]}', '{ a { b { x } c } d |}')
        self.eq('{ a { b { x } c } d |}', 'n_]}', '{ a { b { x } c } d |}')
        self.eq('{ a { b { x } c }| d }', 'n_]}', '{ a { b { x } c } d |}')
        self.eq('{ a { b { x } c| } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a { b { x } |c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a { b { x }| c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a { b { x| } c } d }', 'n_]}', '{ a { b { x |} c } d }')
        self.eq('{ a { b { |x } c } d }', 'n_]}', '{ a { b { x |} c } d }')
        self.eq('{ a { b {| x } c } d }', 'n_]}', '{ a { b { x |} c } d }')
        self.eq('{ a { b |{ x } c } d }', 'n_]}', '{ a { b { x |} c } d }')
        self.eq('{ a { b| { x } c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a { |b { x } c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a {| b { x } c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a |{ b { x } c } d }', 'n_]}', '{ a { b { x } c |} d }')
        self.eq('{ a| { b { x } c } d }', 'n_]}', '{ a { b { x } c } d |}')
        self.eq('{ |a { b { x } c } d }', 'n_]}', '{ a { b { x } c } d |}')
        self.eq('{| a { b { x } c } d }', 'n_]}', '{ a { b { x } c } d |}')
        self.eq('|{ a { b { x } c } d }', 'n_]}', '{ a { b { x } c } d |}')

    def test_n_brace_unbalanced(self):
        self.eq('{ x } x |{ y }', 'n_[{', '{ x } x |{ y }')
        self.eq('{ x } x| { y }', 'n_[{', '{ x } x| { y }')
        self.eq('{ x } |x { y }', 'n_[{', '{ x } |x { y }')
        self.eq('{ x }| x { y }', 'n_[{', '{ x }| x { y }')

    def test_n_brace_multiline(self):
        self.eq('{\n    {\nfi|zz\n    }\n}', 'n_[{', '{\n    |{\nfizz\n    }\n}')
        self.eq('{\n    |{\nfizz\n    }\n}', 'n_[{', '|{\n    {\nfizz\n    }\n}')

    def test_v(self):
        self.eq('{ a { b { |x } c } d }|', 'v_[{', 'r_|{ a { b { x| } c } d }')
        self.eq('{ a { b { |x } c }| d }', 'v_[{', 'r_{ a |{ b { x| } c } d }')
        self.eq('{ a { b { |x }| c } d }', 'v_[{', 'r_{ a { b |{ x| } c } d }')
        self.eq('{ a { b { |x| } c } d }', 'v_[{', 'r_{ a { b |{ x| } c } d }')
        self.eq('{ a { b {| x }| c } d }', 'v_[{', 'r_{ a { b |{ |x } c } d }')
        self.eq('{ a { b {| x| } c } d }', 'v_[{', 'r_{ a { b |{ |x } c } d }')
        self.eq('{ a { b |{ x }| c } d }', 'v_[{', '{ a { b |{| x } c } d }')
        self.eq('{ a { b |{ x| } c } d }', 'v_[{', '{ a { b |{| x } c } d }')
        self.eq('{ a { b| { x| } c } d }', 'v_[{', '{ a { b| {| x } c } d }')
        self.eq('{ a |{ b { x } c }| d }', 'v_[{', '{ a |{| b { x } c } d }')
        self.eq('{ a |{ b { x| } c } d }', 'v_[{', '{ a |{ b {| x } c } d }')
        self.eq('{ |a { b { x }| c } d }', 'v_[{', '{ |a { b {| x } c } d }')
        self.eq('r_{ a { b { |x| } c } d }', 'v_[{', 'r_{ a { b |{ x| } c } d }')
        self.eq('r_{ a { b {| x| } c } d }', 'v_[{', 'r_{ a { b |{ x| } c } d }')
        self.eq('r_{ a { b |{ x| } c } d }', 'v_[{', 'r_{ a |{ b { x| } c } d }')
