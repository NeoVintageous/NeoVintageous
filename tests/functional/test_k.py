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


class Test_k(unittest.PatchFeedCommandXpos, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('abc\na|bc', 'n_k', 'a|bc\nabc')
        self.eq('abc\nabc\na|bc', 'n_2k', 'a|bc\nabc\nabc')
        self.eq('foo bar\nf|oo', 'n_k', 'f|oo bar\nfoo')
        self.eq('foo\nfoo b|ar', 'n_k', 'fo|o\nfoo bar')
        self.eq('f|oo\n\n', 'n_k', 'f|oo\n\n')
        self.eq('\n|\n\n', 'n_k', '|\n\n\n')
        self.eq('foo\nb|ar\nbaz\n', 'n_9k', 'f|oo\nbar\nbaz\n')
        self.eq('aaa\nb|bb', 'n_k', 'a|aa\nbbb')
        self.eq('\n|\n', 'n_k', '|\n\n')
        self.eq('\naa|a\n', 'n_k', '|\naaa\n')
        self.eq('aaa\n|\n', 'n_k', '|aaa\n\n')
        self.eq('aaa bbb\naa|a\n', 'n_k', 'aa|a bbb\naaa\n')
        self.eq('aaa\naaa bb|b\n', 'n_k', 'aa|a\naaa bbb\n')
        self.eq('aaa\naaa bbb |ccc\n', 'n_k', 'aa|a\naaa bbb ccc\n')

    def test_n_no_tabs_to_spaces(self):
        self.settings().set('translate_tabs_to_spaces', False)
        self.eq('\t\taaa\naaa bbb |ccc\n', 'n_k', '\t\t|aaa\naaa bbb ccc\n')

    def test_v(self):
        self.eq('foo\nb|a|r\nbaz\n', 'v_k', 'r_f|oo\nba|r\nbaz\n')
        self.eq('foo\nbar\nb|a|z\n', 'v_k', 'r_foo\nb|ar\nba|z\n')
        self.eq('foo\nf|oo|\nbaz', 'v_k', 'r_fo|o\nfo|o\nbaz')
        self.eq('foobar\nb|arf|oo\nbuzzfizz\n', 'v_k', 'r_foo|bar\nba|rfoo\nbuzzfizz\n')
        self.eq('f|oo\nbar\nb|az\n', 'v_k', 'f|oo\nb|ar\nbaz\n')
        self.eq('foo\n|bar\nb|az\n', 'v_k', 'foo\n|b|ar\nbaz\n')
        self.eq('foo bar\nfoo |bar\nfoo |bar\n', 'v_2k', 'r_foo| bar\nfoo b|ar\nfoo bar\n')
        self.eq('f|oo\nb|ar\nbaz\n', 'v_k', 'r_|fo|o\nbar\nbaz\n')
        self.eq('fo|o\n|bar\nbaz\n', 'v_k', 'fo|o\n|bar\nbaz\n')
        self.eq('1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n|11', 'v_9k', 'r_1\n|2\n3\n4\n5\n6\n7\n8\n9\n10\n1|1')
        self.eq('aaa\n|\n|ccc\n', 'v_k', 'r_|aaa\n\n|ccc\n')
        self.eq('aaa bb|b ccc ddd\naa|a bbb ccc ddd\n', 'v_k', 'r_a|aa bbb| ccc ddd\naaa bbb ccc ddd\n')
        self.eq('r_fizz\nb|uz|z\n', 'v_k', 'r_f|izz\nbuz|z\n')

    def test_V(self):
        self.eq('1x\nfizz\n|buzz\n|4x', 'V_k', 'r_1x\n|fizz\nbuzz\n|4x')
        self.eq('|fizz\n|buzz\n', 'V_k', 'r_|fizz\n|buzz\n')
        self.eq('r_1x\nfizz\n|buzz\n|4x', 'V_k', 'r_1x\n|fizz\nbuzz\n|4x')
        self.eq('1x\n|fizz\nbuzz\n|4x', 'V_k', '1x\n|fizz\n|buzz\n4x')

    def test_d(self):
        self.eq('1\n2\n|3\n4\n5', 'dk', '1\n|4\n5')

    def test_b(self):
        self.eq('fizz\n|fizz|\n|fizz|\n|fizz|\nfizz', 'b_k', 'fizz\n|fizz|\n|fizz|\nfizz\nfizz')
        self.eq('fizz\n|fizz|\n|fizz|\n|fizz|\n|fizz|\nfizz', 'b_3k', 'fizz\n|fizz|\nfizz\nfizz\nfizz\nfizz')
        self.eq('fizz\n|fizz|\n|fizz|\nfizz\nfizz', 'b_k', 'fizz\n|fizz|\nfizz\nfizz\nfizz')
        self.eq('u_fizz\n|fi|zz', 'b_k', 'u_|fi|zz\n|fi|zz')
        self.eq('r_fizz\n|fizz|\n|fizz|\n|fizz|\nfizz', 'b_k', 'r_fizz\n|fizz|\n|fizz|\nfizz\nfizz')
        self.eq('fizz\n|fizz|\n|\n||fizz|\nfizz', 'b_k', 'fizz\n|f|izz\n|\n|fizz\nfizz')
        self.eq('fizz\n\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\n|\n||fiz|z\nfizz\n')
        self.eq('fizz\nf\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nf|\n|f|iz|z\nfizz\n')
        self.eq('fizz\nfi\nfi|zz|\nfizz\n', 'b_k', 'u_fizz\nfi|\n|fi|z|z\nfizz\n')
        self.eq('fizz\nfiz\nfi|zz|\nfizz\n', 'b_k', 'u_fizz\nfi|z\n|fi|zz|\nfizz\n')
        self.eq('fizz\nfizz\nfi|zz|\nfizz\n', 'b_k', 'u_fizz\nfi|zz|\nfi|zz|\nfizz\n')
        self.eq('r_fizz\n\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\n|\n||fizz|\nfizz\n')
        self.eq('r_fizz\nf\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nf|\n|f|izz|\nfizz\n')
        self.eq('r_fizz\nfi\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nfi|\n|fi|zz|\nfizz\n')
        self.eq('r_fizz\nfiz\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nfi|z\n|fi|zz|\nfizz\n')
        self.eq('r_fizz\nfizz\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nfi|zz|\nfi|zz|\nfizz\n')
        self.eq('u_fizz\nfizz\nfi|zz|\nfizz\n', 'b_k', 'u_fizz\nfi|zz|\nfi|zz|\nfizz\n')
        self.eq('d_fizz\nfizz\nfi|zz|\nfizz\n', 'b_k', 'u_fizz\nfi|zz|\nfi|zz|\nfizz\n')
        self.eq('d_fizz\nfi|zz|\nfi|zz|\nfizz\n', 'b_k', 'd_fizz\nfi|zz|\nfizz\nfizz\n')
        self.eq('d_fi|zz|\nfi|zz|\nfi|zz|\nfizz\n', 'b_k', 'd_fi|zz|\nfi|zz|\nfizz\nfizz\n')
        self.eq('r_u_fizz\nfizz\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nfi|zz|\nfi|zz|\nfizz\n')
        self.eq('r_d_fizz\nfizz\nfi|zz|\nfizz\n', 'b_k', 'r_u_fizz\nfi|zz|\nfi|zz|\nfizz\n')
        self.eq('d_fizz |buzz|\nf\nfizz |buzz|\n', 'b_k', 'r_d_f|izz b|uzz\nf|\n|fizz buzz\n')
        self.eq('d_fizz\nfizz\nf|iz|z\nf|iz|z\n', 'b_2k', 'u_fizz\nf|iz|z\nf|iz|z\nfizz\n')
        self.eq('r_d_fizz\nfizz\nf|iz|z\nf|iz|z\n', 'b_2k', 'r_u_fizz\nf|iz|z\nf|iz|z\nfizz\n')
        self.eq('d_fizz\nfizz\nfizz\nf|iz|z\nf|iz|z\n', 'b_3k', 'u_fizz\nf|iz|z\nf|iz|z\nf|iz|z\nfizz\n')
        self.eq('d_fizz\nfizz\n\nf|iz|z\nf|iz|z\n', 'b_3k', 'u_fizz\nf|iz|z\n\nf|iz|z\nfizz\n')
        self.eq('d_fizz\nfizz\nf\nf|iz|z\nf|iz|z\n', 'b_3k', 'u_fizz\nf|iz|z\nf|\n|f|iz|z\nfizz\n')
        self.eq('d_fizz\nfizz\nfi\nf|iz|z\nf|iz|z\n', 'b_3k', 'u_fizz\nf|iz|z\nf|i\n|f|iz|z\nfizz\n')
        self.eq('d_fizz\n\nfi\nf|iz|z\nf|iz|z\n', 'b_3k', 'r_u_fizz\n|\n||fi|\n|fi|zz\nfizz\n')
        self.eq('d_fizz\nx\nfizz |buz|z\nfizz |buz|z\n', 'b_3k', 'r_u_fizz|\n|x\nfizz| b|uzz\nfizz buzz\n')

        self.eq('u_fizz buzz\nf\nfizz |buzz|\n', 'b_2k', 'u_fizz |buzz|\nf\nfizz |buzz|\n')
        self.eq('u_fizz\nf\nfizz |buzz|\n', 'b_2k', 'r_u_fizz|\n|f\nfizz| b|uzz\n')
        self.eq('u_fizz \nf\nfizz |buzz|\n', 'b_2k', 'u_fizz |\n|f\nfizz |b|uzz\n')
        self.eq('fizz buzz\nf\nfizz |buz|z\n', 'b_2k', 'u_fizz |buz|z\nf\nfizz |buz|z\n')
        self.eq('r_u_fizz \nf\nfizz |buzz|\n', 'b_2k', 'r_u_fizz |\n|f\nfizz |buzz|\n')
        self.eq('r_d_fizz |buzz|\nf\nfizz |buzz|\nfizz |buzz|\n', 'b_k', 'r_d_fizz |buzz|\nf\nfizz |buzz|\nfizz buzz\n')  # noqa: E501
