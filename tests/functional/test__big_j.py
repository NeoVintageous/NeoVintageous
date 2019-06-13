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


class Test_J(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|aaa\nbbb', 'J', 'aaa| bbb')
        self.eq('|aaa\nbbb', '1J', 'aaa| bbb')
        self.eq('|aaa\nbbb', '2J', 'aaa| bbb')
        self.eq('|aaa\nbbb', '9J', 'aaa| bbb')
        self.eq('|aaa\nbbb\nccc', 'J', 'aaa| bbb\nccc')
        self.eq('|aaa\nbbb\nccc', '1J', 'aaa| bbb\nccc')
        self.eq('|aaa\nbbb\nccc', '2J', 'aaa| bbb\nccc')
        self.eq('|aaa\nbbb\nccc', '3J', 'aaa| bbb ccc'),  # TODO Fix: cursor position is incorrect
        self.eq('|aaa\nbbb\nccc', '9J', 'aaa| bbb ccc'),  # TODO Fix: cursor position is incorrect
        self.eq('|aaa\n    bbb', 'J', 'aaa| bbb')
        self.eq('|aaa\n    bbb', '1J', 'aaa| bbb')
        self.eq('|aaa\n    bbb', '2J', 'aaa| bbb')
        self.eq('|aaa\n    bbb', '9J', 'aaa| bbb')
        self.eq('|abc\nabc\nabc', 'J', 'N_abc| abc\nabc'),
        self.eq('|abc\n    abc\nabc', 'J', 'N_abc| abc\nabc'),
        self.eq('|abc\nabc\nabc', '2J', 'N_abc| abc\nabc'),
        self.eq('|abc\n    abc\nabc', '2J', 'N_abc| abc\nabc'),
        self.eq('|abc\nabc\nabc', '3J', 'N_abc| abc abc'),
        self.eq('|abc\n    abc\n    abc', '3J', 'N_abc| abc abc'),
        self.eq('|abc\nabc\nabc\nabc\nabc', '5J', 'N_abc| abc abc abc abc'),
        self.eq('|abc\n    abc\n    abc\n    abc\n    abc', '5J', 'N_abc| abc abc abc abc'),
        self.eq('|abc\n\n', '3J', 'N_abc| '),
        self.eq('|\n\nabc', '3J', 'N_|abc'),
        self.eq('|abc \n    abc  \n  abc', '3J', 'N_abc |abc  abc'),
        self.eq('|   abc\nabc   ', 'J', 'N_   abc| abc   '),

    def test_v(self):
        self.eq('|abc\na|bc\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('a|bc\n    a|bc\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('a|bc\na|bc\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('ab|c\n    abc|\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('r_|abc\nabc|\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('r_|abc\n    abc|\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('r_|abc\nabc|\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('r_|abc\n    abc|\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('|abc\n|abc\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('a|bc\n  |  abc\nabc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('|abc\nabc\n|abc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('|abc\n    abc\n|abc', 'v_J', 'n_abc| abc\nabc'),
        self.eq('|abc\nabc\na|bc', 'v_J', 'n_abc| abc abc'),
        self.eq('ab|c\n    abc\na|bc', 'v_J', 'n_abc| abc abc'),
        self.eq('a|bc\nabc\nabc|', 'v_J', 'n_abc| abc abc'),
        self.eq('ab|c\n    abc\na|bc', 'v_J', 'n_abc| abc abc'),
        self.eq('|a|bc\nabc\nabc', 'v_3J', 'n_abc| abc\nabc'),
        self.eq('|a|bc\n    abc\nabc', 'v_3J', 'n_abc| abc\nabc'),
        self.eq('|   abc\nabc   |', 'v_J', 'n_   abc| abc   '),
        self.eq('|    abc\n\n\n|', 'v_J', 'n_    abc| \n'),

    def test_b(self):
        self.eq('| |   abc  \n| |  abc\nabc', 'b_J', 'n_    abc  |abc\nabc'),


class Test_J_c_syntax(unittest.FunctionalTestCase):

    def feed(self, seq):
        # Test against a specific syntax, because views that
        # have no syntax applied have no comment behaviours.
        self.syntax('Packages/C++/C.sublime-syntax')
        super().feed(seq)

    def test_J_strips_leading_comment_tokens(self):
        self.eq('|// fizz\n// buzz', 'J', '// fizz| buzz')
        self.eq('|// fizz\n// buzz\n// fizz\n// buzz\nx', '4J', '// fizz| buzz fizz buzz\nx')

    def test_J_does_not_strip_leading_comment_tokens_that_have_end_tokens(self):
        self.eq('|/* fizz\n/* buzz\nx */', 'J', '/* fizz| /* buzz\nx */')

    def test_J_leading_comment_tokens_and_any_leading_whitespace(self):
        self.settings().set('translate_tabs_to_spaces', True)
        self.eq('|// fizz\n    // buzz', 'J', '// fizz| buzz')
        self.settings().set('translate_tabs_to_spaces', False)
        self.eq('|// fizz\n\t\t// buzz', 'J', '// fizz| buzz')

    def test_J_strips_comment_tokens_without_trailing_content(self):
        self.eq('|// fizz\n//', 'J', '// fizz| ')
        self.eq('|// fizz\n//\n// buzz\nx', '3J', '// fizz| buzz\nx')  # TODO Fix: cursor position is incorrect

    def test_J_does_not_strip_leading_comment_tokens_if_first_line_does_not_lead_with_a_comment(self):
        self.eq('|fizz\n// buzz', 'J', 'fizz| // buzz')
        self.eq('// fi|zz\n// buzz', 'J', '// fizz| buzz')
        self.eq('    // fi|zz\n// buzz', 'J', '    // fizz| buzz')


class Test_J_python_syntax(unittest.FunctionalTestCase):

    def feed(self, seq):
        # Test against a specific syntax, because views that
        # have no syntax applied have no comment behaviours.
        self.syntax('Packages/Python/Python.sublime-syntax')
        super().feed(seq)

    def test_J_strips_leading_comment_tokens(self):
        self.eq('|# fizz\n# buzz', 'J', '# fizz| buzz')
