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


class Test_l(unittest.FunctionalTestCase):

    def test_n_l(self):
        self.eq('|abc', 'n_l', 'a|bc')
        self.eq('|foo bar baz', 'n_9l', 'foo bar b|az')
        self.eq('|ping', 'n_9l', 'pin|g')
        self.eq('|ping\n', 'n_9l', 'pin|g\n')

    def test_n_l_empty_lines(self):
        self.eq('|', 'n_l', '|')
        self.eq('\n\n|\n\n', 'n_l', '\n\n|\n\n')

    def test_v_l(self):
        self.eq('|abc', 'v_l', '|ab|c')
        self.eq('|abc', 'v_1l', '|ab|c')
        self.eq('f|oo bar baz', 'v_5l', 'f|oo bar| baz')
        self.eq('|ping', 'v_9l', '|ping|')
        self.eq('p|ing\n', 'v_9l', 'p|ing\n|')
        self.eq('a|bc\nx', 'v_5l', 'a|bc\n|x')
        self.eq('a|bc\nd|ef\nx', 'v_9l', 'a|bc\ndef\n|x')

    def test_v_l_empty_lines(self):
        self.eq('|', 'v_l', '|')
        self.eq('\n\n|\n|\n', 'v_l', '\n\n|\n|\n')

    def test_v_l_reversed_selections(self):
        self.eq('r_h|el|lo world', 'v_5l', 'he|llo w|orld')

    def test_v_l_reversed_selections_to_eol(self):
        self.eq('r_h|el|lo\n', 'v_5l', 'he|llo\n|')

    def test_v_l_reversed_selections_to_eol_2(self):
        self.eqr('r_a|\n|', 'v_5l', 'a|\n|')

    def test_v_l_reversed_selections_to_eol_3(self):
        self.eq('r_|ab|\n', 'v_9l', 'a|b\n|')

    def test_v_l_reversed_selections_to_eol_4(self):
        self.eqr('r_|ab\n|', 'v_9l', 'ab|\n|')

    def test_l_internal_mode(self):
        self.eq('|abc', 'l', 'N_|a|bc')
