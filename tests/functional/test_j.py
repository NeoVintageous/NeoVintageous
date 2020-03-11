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


class Test_j(unittest.PatchFeedCommandXpos, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('a|bc\nabc\nabc', 'n_j', 'abc\na|bc\nabc')
        self.eq('f|oo\nfoo bar\nfoo bar', 'n_j', 'foo\nf|oo bar\nfoo bar')
        self.eq('foo b|ar\nfoo\nbar', 'n_j', 'foo bar\nfo|o\nbar')
        self.eq('|\nfoo\nbar', 'n_j', '\n|foo\nbar')
        self.eq('|\n\nbar', 'n_j', '\n|\nbar')
        self.eq('|foo\nbar\nbaz', 'n_j', 'foo\n|bar\nbaz')
        self.eq('a|aa\nbbb\n', 'n_j', 'aaa\nb|bb\n')
        self.eq('|\n\n', 'n_j', '\n|\n')
        self.eq('aa|a\n\n', 'n_j', 'aaa\n|\n')
        self.eq('|\naaa\n', 'n_j', '\n|aaa\n')
        self.eq('aa|a\naaa bbb\n', 'n_j', 'aaa\naa|a bbb\n')
        self.eq('aaa bb|b\naaa\n', 'n_j', 'aaa bbb\naa|a\n')
        self.eq('aaa bbb |ccc\naaa\n', 'n_j', 'aaa bbb ccc\naa|a\n')

    def test_v(self):
        self.eq('a|b|c\nabc', 'v_1j', 'a|bc\nab|c')
        self.eq('r_a|bc\nabc\nab|c', 'v_1j', 'r_abc\na|bc\nab|c')
        self.eq('r_a|bc\nab|c\nabc', 'v_2j', 'abc\na|bc\nab|c')
        self.eq('r_a|bc\nab|c\nabc', 'v_9j', 'abc\na|bc\nab|c')
        self.eq('r_a|bc\nab|c\nabc', 'v_1j', 'r_abc\na|b|c\nabc')
        self.eq('r_abc\na|b|c\nabc', 'v_1j', 'abc\na|bc\nab|c')
        self.eq('f|o|o\nfoo bar\nfoo bar', 'v_1j', 'f|oo\nfo|o bar\nfoo bar')
        self.eq('foo b|a|r\nfoo\nbar', 'v_1j', 'foo b|ar\nfoo\n|bar')
        self.eq('|\n|foo\nbar', 'v_1j', '|\nf|oo\nbar')
        self.eq('|\n|\nbar', 'v_1j', '|\n\n|bar')
        self.eq('f|o|o\nbar\nbaz', 'v_9j', 'f|oo\nbar\nba|z')
        self.eq('|\n|aaa\n', 'v_j', '|\na|aa\n')

    def test_V(self):
        self.eq('|abc\n|abc\nabc', 'V_j', '|abc\nabc\n|abc')
        self.eq('|\n|foo\nbar', 'V_j', '|\nfoo\n|bar')
        self.eq('r_|\n|\nbar', 'V_j', '|\n\n|bar')
        self.eq('|foo\n|bar\nbaz', 'V_9j', '|foo\nbar\nbaz|')
        self.eq('r_1\n|2\n3\n4\n5\n|6\n7', 'V_j', 'r_1\n2\n|3\n4\n5\n|6\n7')
        self.eq('r_x\n|two\nfizz\nthree\n|buzz\n', 'V_j', 'r_x\ntwo\n|fizz\nthree\n|buzz\n')

    def test_d(self):
        self.eq('a|bc\nabc\nabc', 'dj', '|abc')
        self.eq('f|oo\nfoo bar\nfoo bar', 'dj', '|foo bar')
        self.eq('foo b|ar\nfoo\nbar', 'dj', '|bar')
        self.eq('|\nfoo\nbar', 'dj', '|bar')
        self.eq('|\n\nbar', 'dj', '|bar')
        self.eq('f|oo\nbar\nbaz', '9dj', '|')

    def test_b(self):
        self.eq('fiz|zbuzz\n|fizzbuzz\n', 'b_j', 'fiz|zbuzz\n|fiz|zbuzz\n|')
        self.eq('f|izzbuz|z\nfizz\n', 'b_j', 'f|izzb|uzz\nf|izz\n|')
        self.eq('f|iz|z\nb|uz|z\nfizz\nbuzz', 'b_j', 'f|iz|z\nb|uz|z\nf|iz|z\nbuzz')
        self.eq('f|iz|z\nfizz\nfizz\nfizz\nfizz\n', 'b_3j', 'f|iz|z\nf|iz|z\nf|iz|z\nf|iz|z\nfizz\n')
        self.eq('f|iz|z\nfizzbuzz\n', 'b_j', 'f|iz|z\nf|iz|zbuzz\n')
        self.eq('f|i|zz\nb|u|zz\nfizz\nbuzz', 'b_j', 'f|i|zz\nb|u|zz\nf|i|zz\nbuzz')
        self.eq('f|i|zz\nfizz\n', 'b_j', 'f|i|zz\nf|i|zz\n')
        self.eq('x\nfiz|zbuzz\n|fizzbuzz\ny', 'b_j', 'x\nfiz|zbuzz\n|fiz|zbuzz\n|y')
        self.eq('x\nfiz|zbu|zz\nfizzbuzz\ny', 'b_j', 'x\nfiz|zbu|zz\nfiz|zbu|zz\ny')
        self.eq('x\n|fizz\n|fizz\ny', 'b_j', 'x\n|fizz\n||fizz\n|y')
        self.eq('|fizz\n|fizz\n', 'b_j', '|fizz\n||fizz\n|')
        self.eq('|fiz|z\n\n\n', 'b_j', '|f|izz\n|\n|\n')
        self.eq('|fiz|z\n\n\n\n', 'b_2j', '|f|izz\n|\n||\n|\n')
        self.eq('|fiz|z\n\n\n\n\n', 'b_3j', '|f|izz\n|\n||\n||\n|\n')
        self.eq('|f|izz\n\n\n', 'b_j', '|f|izz\n|\n|\n')
        self.eq('|f|izz\nfizz\n', 'b_j', '|f|izz\n|f|izz\n')
        self.eq('f|izz buz|z\nfizz\nx', 'b_j', 'f|izz |buzz\nf|izz\n|x')
        self.eq('f|izz buz|z\nfizz\n', 'b_j', 'f|izz |buzz\nf|izz\n|')
        self.eq('f|izz buz|z\nfizz', 'b_j', 'f|izz| buzz\nf|izz|')
        self.eq('f|izz buz|z\nf\nx', 'b_j', 'f|i|zz buzz\nf|\n|x')
        self.eq('|fiz|z\n\nx', 'b_j', '|f|izz\n|\n|x')
        self.eq('|fiz|z\n\n\n\nx', 'b_3j', '|f|izz\n|\n||\n||\n|x')
        self.eq('u_|fizz|\n|fizz|\n', 'b_j', 'u_fizz\n|fizz|\n')
        self.eq('r_u_|fizz|\n|fizz|\n', 'b_j', 'r_u_fizz\n|fizz|\n')
        self.eq('u_|fizz|\n|fizz|\nfizz\n', 'b_2j', 'd_fizz\n|fizz|\n|fizz|\n')
        self.eq('r_u_|fizz|\n|fizz|\nfizz\n', 'b_2j', 'r_d_fizz\n|fizz|\n|fizz|\n')
        self.eq('r_u_|fizz|\n|fizz|\nfizz\nfizz\nfizz\n', 'b_3j', 'r_d_fizz\n|fizz|\n|fizz|\n|fizz|\nfizz\n')
        self.eq('u_|fi|zz\n|fi|zz\nfizz\nx\nfizz', 'b_3j', 'd_fizz\n|fi|zz\n|fi|zz\n|x\n|fizz')
        self.eq('u_fi|zz|\nfi|zz|\nx\nx\nfizz\n', 'b_4j', 'd_fizz\nfi|zz|\nx\nx\nfi|zz|\n')
        self.eq('u_fi|zz|\nfi|zz|\nx\nx\nfizz\n', 'b_9j', 'd_fizz\nfi|zz|\nx\nx\nfi|zz|\n')
        self.eq('u_fi|zz|\nfi|zz|\nx\nbuzz', 'b_2j', 'r_d_fizz\nf|iz|z\nx|\n|buzz')
        self.eq('u_fizz |buzz|\nfizz |buzz|\nx\nfizz buzz\n', 'b_3j', 'd_fizz buzz\nfizz |buzz|\nx\nfizz |buzz|\n')
        self.eq('u_fizz b|uz|z\nfizz b|uz|z\nx\nfizz\nfizz', 'b_3j', 'r_d_fizz buzz\nfizz| bu|zz\nx\nfizz|\n|fizz')
        self.eq('r_fizz\n|fizz|\nfizz\nfizz\n', 'b_j', 'r_fizz\n|fizz|\n|fizz|\nfizz\n')
        self.eq('r_fizz\n|fizz|\n|fizz|\nfizz\nfizz\n', 'b_j', 'r_fizz\n|fizz|\n|fizz|\n|fizz|\nfizz\n')
        self.eq('r_fizz buzz\n|fizz b|uzz\n|fizz b|uzz\n|\n|fizz buzz\n', 'b_j', 'r_fizz buzz\n|fizz b|uzz\n|fizz b|uzz\n|\n||fizz b|uzz\n')  # noqa: E501
        self.eq('u_f|iz|z\nf|iz|z\nfizz\nfizz\n', 'b_2j', 'd_fizz\nf|iz|z\nf|iz|z\nfizz\n')
        self.eq('u_f|iz|z\nf|iz|z\nfizz\nfizz\nfizz', 'b_3j', 'd_fizz\nf|iz|z\nf|iz|z\nf|iz|z\nfizz')
        self.eq('r_u_f|iz|z\nf|iz|z\nfizz\nfizz\nfizz', 'b_3j', 'r_d_fizz\nf|iz|z\nf|iz|z\nf|iz|z\nfizz')
        self.eq('u_fi|zz|\nfi|zz|\n\nfizz\nfizz', 'b_3j', 'd_fizz\nfi|zz|\n\nfi|zz|\nfizz')
        self.eq('r_u_fi|zz|\nfi|zz|\n\nfizz\nfizz', 'b_3j', 'r_d_fizz\nfi|zz|\n\nfi|zz|\nfizz')

        self.setXpos(3)
        self.eq('fi|zz|\n\n\nfizz\nx', 'b_3j', 'fi|zz|\n\n\nfi|zz|\nx')
        self.eq('fi|zz|\nx\nx\nfizz\nx', 'b_3j', 'fi|zz|\nx\nx\nfi|zz|\nx')
        self.eq('fi|zz|\nxy\nxy\nfizz\nx', 'b_3j', 'fi|zz|\nxy|\n|xy|\n|fi|zz|\nx')

        self.setXpos(5)
        self.eq('|fizzbu|zz\nx\ny', 'b_j', '|fi|zzbuzz\n|x\n|y')
        self.eq('|fizzbu|zz\nx\nfizzbuzz\n', 'b_2j', '|fizzbu|zz\n|x\n||fizzbu|zz\n')
        self.eq('|fizzbu|zz\n\n\nfizzbuzz\n', 'b_3j', '|fizzbu|zz\n|\n||\n||fizzbu|zz\n')
        self.eq('r_fizz |buz|z\nfizz buzz\nx', 'b_j', 'r_fizz |buz|z\nfizz |buz|z\nx')
        self.eq('r_fizz |buz|z\nfizz buz\nx', 'b_j', 'r_fizz |buz|z\nfizz |buz|\nx')
        self.eq('r_fizz |buz|z\nfizz bu\nx', 'b_j', 'r_fizz |buz|z\nfizz |bu\n|x')
        self.eq('r_fizz |buz|z\nfizz b\nx', 'b_j', 'r_fizz |buz|z\nfizz |b\n|x')
        self.eq('r_fizz |buz|z\nfizz \nx', 'b_j', 'r_fizz |buz|z\nfizz |\n|x')
        self.eq('r_fizz |buz|z\nfizz\nx', 'b_j', 'r_fizz| buz|z\nfizz|\n|x')
        self.eq('r_fizz |buz|z\nfiz\nx', 'b_j', 'r_fiz|z buz|z\nfiz|\n|x')
        self.eq('r_fizz |buz|z\nfi\nx', 'b_j', 'r_fi|zz buz|z\nfi|\n|x')
        self.eq('r_fizz |buz|z\nf\nx', 'b_j', 'r_f|izz buz|z\nf|\n|x')
        self.eq('r_fizz |buz|z\n\nx', 'b_j', 'r_|fizz buz|z\n|\n|x')
        self.eq('r_fizz |buz|z\n\n\nfizz buzz\nx', 'b_3j', 'r_fizz |buz|z\n\n\nfizz |buz|z\nx')
        self.eq('r_fizz |buz|z\nfizz\nfizz\nfizz buzz\nx', 'b_3j', 'r_fizz |buz|z\nfizz\nfizz\nfizz |buz|z\nx')
        self.eq('r_fizz |buz|z\nfizz \nfizz \nfizz buzz\nx', 'b_3j', 'r_fizz |buz|z\nfizz |\n|fizz |\n|fizz |buz|z\nx')  # noqa: E501
        self.eq('r_fizz |buz|z\nfizz buzz\nfizz buzz\nfizz buzz\nfizz buzz\n', 'b_3j', 'r_fizz |buz|z\nfizz |buz|z\nfizz |buz|z\nfizz |buz|z\nfizz buzz\n')  # noqa: E501
        self.eq('r_fizz |buz|z\nx\nfizz buzz\nx\nfizz buzz\nx', 'b_4j', 'r_fizz |buz|z\nx\nfizz |buz|z\nx\nfizz |buz|z\nx')  # noqa: E501

        self.setXpos(7)
        self.eq('fizz |buz|z\nfizz buzz\nx', 'b_j', 'fizz |buz|z\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz buz\nx', 'b_j', 'fizz |buz|z\nfizz |buz|\nx')
        self.eq('fizz |buz|z\nfizz bu\nx', 'b_j', 'fizz |buz|z\nfizz |bu\n|x')
        self.eq('fizz |buz|z\nfizz b\nx', 'b_j', 'fizz |bu|zz\nfizz |b\n|x')
        self.eq('fizz |buz|z\nfizz \nx', 'b_j', 'fizz |b|uzz\nfizz |\n|x')
        self.eq('fizz |buz|z\nfizz\nx', 'b_j', 'r_d_fizz| b|uzz\nfizz|\n|x')
        self.eq('fizz |buz|z\nfiz\nx', 'b_j', 'r_d_fiz|z b|uzz\nfiz|\n|x')
        self.eq('fizz |buz|z\nfi\nx', 'b_j', 'r_d_fi|zz b|uzz\nfi|\n|x')
        self.eq('fizz |buz|z\nf\nx', 'b_j', 'r_d_f|izz b|uzz\nf|\n|x')
        self.eq('fizz |buz|z\n\nx', 'b_j', 'r_d_|fizz b|uzz\n|\n|x')
        self.eq('fizz |buz|z\nfizz buzz\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz |buz|z\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz buz\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz |buz|\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz bu\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz |bu\n|fizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz b\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz |b\n|fizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz \nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz |\n|fizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz \nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz |\n|fizz |buz|z\nx')
        self.eq('fizz |buz|z\nfizz\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfizz\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\nfiz\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfiz\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\nfi\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nfi\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\nf\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\nf\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\n\nfizz buzz\nx', 'b_2j', 'fizz |buz|z\n\nfizz |buz|z\nx')
        self.eq('fizz |buz|z\n\n\nfi\nx', 'b_3j', 'r_d_fi|zz b|uzz\n\n\nfi|\n|x')
        self.eq('fizz |buz|z\nf\nf\nfi\nx', 'b_3j', 'r_d_fi|zz b|uzz\nf\nf\nfi|\n|x')
        self.eq('fizz |buz|z\nfi\nfi\nfi\nx', 'b_3j', 'r_d_fi|zz b|uzz\nfi|\n|fi|\n|fi|\n|x')
        self.eq('fizz |buz|z\nf\nfizz buzz\nf\nfizz buzz', 'b_4j', 'fizz |buz|z\nf\nfizz |buz|z\nf\nfizz |buz|z')
