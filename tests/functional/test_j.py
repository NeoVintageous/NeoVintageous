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
        self.eq('|abc\n|abc\nabc', 'l_j', '|abc\nabc\n|abc')
        self.eq('|\n|foo\nbar', 'l_j', '|\nfoo\n|bar')
        self.eq('r_|\n|\nbar', 'l_j', '|\n\n|bar')
        self.eq('|foo\n|bar\nbaz', 'l_9j', '|foo\nbar\nbaz|')
        self.eq('r_1\n|2\n3\n4\n5\n|6\n7', 'l_j', 'r_1\n2\n|3\n4\n5\n|6\n7')

    def test_b(self):
        self.eq('fiz|zbu|zz\nfizzbuzz\nfizzbuzz\n', 'b_j', 'fiz|zbu|zz\nfiz|zbu|zz\nfizzbuzz\n')
        self.eq('f|iz|z\nfizz\nfizz\nfizz\nfizz\n', 'b_3j', 'f|iz|z\nf|iz|z\nf|iz|z\nf|iz|z\nfizz\n')

    def test_d(self):
        self.eq('a|bc\nabc\nabc', 'dj', '|abc')
        self.eq('f|oo\nfoo bar\nfoo bar', 'dj', '|foo bar')
        self.eq('foo b|ar\nfoo\nbar', 'dj', '|bar')
        self.eq('|\nfoo\nbar', 'dj', '|bar')
        self.eq('|\n\nbar', 'dj', '|bar')
        self.eq('f|oo\nbar\nbaz', '9dj', '|')
