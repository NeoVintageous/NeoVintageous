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


class Test_A(unittest.FunctionalTestCase):

    def test_A(self):
        self.eq('|', 'A', 'i_|')
        self.eq('|ab', 'A', 'i_ab|')
        self.eq('a|b', 'A', 'i_ab|')
        self.eq('a|b\n', 'A', 'i_ab|\n')
        self.eq('a|b\nx', 'A', 'i_ab|\nx')

    def test_v_A(self):
        self.eq('x|ab|x', 'v_A', 'i_xab|x')
        self.eq('x|abx|\n', 'v_A', 'i_xabx|\n')
        self.eq('x|abx\n|', 'v_A', 'i_xabx|\n')

    def test_v_A_reverse(self):
        self.eq('r_fi|zz bu|zz', 'v_A', 'i_fi|zz buzz')

    def test_l_A(self):
        self.eq('|a|', 'l_A', 'i_a|')
        self.eq('|a\n|', 'l_A', 'i_a|\n')
        self.eq('|a\n|x', 'l_A', 'i_a|\nx')
        self.eq('|a\n|\nx', 'l_A', 'i_a|\n\nx')
        self.eq('|ab|', 'l_A', 'i_ab|')
        self.eq('|ab\n|', 'l_A', 'i_ab|\n')
        self.eq('|ab\n|x', 'l_A', 'i_ab|\nx')
        self.eq('|ab\n|\nx', 'l_A', 'i_ab|\n\nx')
        self.eq('|ab\ncd|', 'l_A', 'i_ab\ncd|')
        self.eq('|ab\ncd\n|', 'l_A', 'i_ab\ncd|\n')

    def test_l_A_multiple_selections(self):
        self.eq('|ab\n||cd|', 'l_A', 'i_ab|\ncd|')
        self.eq('|ab\n||cd\n|', 'l_A', 'i_ab|\ncd|\n')

    def test_issue_291_append_multi_line_is_off_by_one_char(self):
        self.eq('|aaaaa\n||bbbbb\n||ccccc|', 'l_A', 'i_aaaaa|\nbbbbb|\nccccc|')
        self.eq('|aaaaa\n||bbbbb\n||ccccc\n|', 'l_A', 'i_aaaaa|\nbbbbb|\nccccc|\n')
        self.eq('|aaaaa\n||bbbbb\n||ccccc\n|x', 'l_A', 'i_aaaaa|\nbbbbb|\nccccc|\nx')

    def test_b_A(self):
        self.eq('x\n1|11|1\nx\n2|22|2\nx', 'b_A', 'i_x\n111|1\nx\n222|2\nx')

    def test_b_A_eol(self):
        self.eq('x\na|bc\n|x\nd|ef\n|x', 'b_A', 'i_x\nabc|\nx\ndef|\nx')

    def test_s(self):
        self.eq('|fizz| buzz fizz buzz fizz', 's_A', '|fizz| buzz |fizz| buzz |fizz|')
