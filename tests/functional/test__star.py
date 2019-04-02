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


class Test_star(unittest.FunctionalTestCase):

    def test_star(self):
        self.eq('a|bc\nx\nabc\nx\nabc\nx', 'n_*', 'abc\nx\n|abc\nx\nabc\nx')
        self.assertSearch('|abc|\nx\n|abc|\nx\n|abc|\nx')
        self.assertSearchCurrent('abc\nx\n|abc|\nx\nabc\nx')
        self.eq('fi|zz', 'n_*', '|fizz')
        self.assertSearch('|fizz|')
        self.assertSearchCurrent('|fizz|')
        self.eq('x fi|zz x', 'n_*', 'x |fizz x')
        self.assertSearch('x |fizz| x')
        self.assertSearchCurrent('x |fizz| x')
        self.eq('|', 'n_*', '|')

    def test_N_star(self):
        self.eq('a|bc\nx\nabc\nx\nabc\nx', '*', 'N_a|bc\nx\n|abc\nx\nabc\nx')
        self.eq('fi|zz\nx\nabc\n', '*', 'r_N_|fi|zz\nx\nabc\n')
        self.eq('fi|zz\nx\nabc\n', '*', 'r_N_|fi|zz\nx\nabc\n')

    def test_star_no_match(self):
        self.eq('x\nfi|zz\nx\nabc\n', 'n_*', 'x\n|fizz\nx\nabc\n')
        self.eq('    fi|zz\nx\nabc\n', 'n_*', '    |fizz\nx\nabc\n')
        self.assertSearch('    |fizz|\nx\nabc\n')
        self.assertSearchCurrent('    |fizz|\nx\nabc\n')

    def test_star_repeat_match(self):
        self.eq('a|bc\nx\nabc\nx\nabc\nx\nabc\nx', 'n_*', 'abc\nx\n|abc\nx\nabc\nx\nabc\nx')
        self.assertSearchCurrent('abc\nx\n|abc|\nx\nabc\nx\nabc\nx')
        self.feed('n_*')
        self.assertSearchCurrent('abc\nx\nabc\nx\n|abc|\nx\nabc\nx')
        self.feed('n_*')
        self.assertSearchCurrent('abc\nx\nabc\nx\nabc\nx\n|abc|\nx')

    def test_star_wraps(self):
        self.eq('x\nabc\nx\nabc\nx\nabc\nx\na|bc\nx', 'n_*', 'x\n|abc\nx\nabc\nx\nabc\nx\nabc\nx')
        self.assertSearch('x\n|abc|\nx\n|abc|\nx\n|abc|\nx\n|abc|\nx')
        self.assertSearchCurrent('x\n|abc|\nx\nabc\nx\nabc\nx\nabc\nx')

    def test_star_no_partial_match(self):
        self.eq('fo|o\nfizz\nfom\nfoo\nfou\n', 'n_*', 'foo\nfizz\nfom\n|foo\nfou\n')
        self.assertSearch('|foo|\nfizz\nfom\n|foo|\nfou\n')
        self.assertSearchCurrent('foo\nfizz\nfom\n|foo|\nfou\n')

    def test_star_should_not_match_non_word_boundaries(self):
        self.eq('fo|o\nfoox\nfoo\nxfoo\n', 'n_*', 'foo\nfoox\n|foo\nxfoo\n')

    def test_v_star(self):
        self.eq('ab|c\nx\nabc\nx', 'v_*', 'ab|c\nx\na|bc\nx')
        self.eq('ab|c\nx\nx abc x\nx', 'v_*', 'ab|c\nx\nx a|bc x\nx')
        self.eq('x\nabc\nx\nx ab|c x\nx', 'v_*', 'r_x\n|abc\nx\nx abc| x\nx')
        self.eq('fi|zz\nx\n    fizz\nx', 'v_*', 'fi|zz\nx\n    f|izz\nx')
