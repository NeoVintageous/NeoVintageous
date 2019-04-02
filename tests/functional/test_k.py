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


class Test_k(unittest.FunctionalTestCase):

    def _run_feed_command(self, command, args):
        sel = self.view.sel()[-1]
        xpos_pt = sel.b - 1 if sel.b > sel.a else sel.b
        xpos = self.view.rowcol(xpos_pt)[1]

        # Commands like k receive a motion xpos argument on operations like
        # "dk". This updates the command with whatever the test fixture xpos
        # should to be. It's a bit hacky, but just a temporary solution.
        if 'motion' in args and 'motion_args' in args['motion']:
            args['motion']['motion_args']['xpos'] = xpos
        else:
            args['xpos'] = xpos

        self.state.settings.vi['visual_block_direction'] = None
        super()._run_feed_command(command, args)

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

    def test_n_tabs(self):
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
        self.eq('1x\nfizz\n|buzz\n|4x', 'l_k', 'r_1x\n|fizz\nbuzz\n|4x')
        self.eq('|fizz\n|buzz\n', 'l_k', 'r_|fizz\n|buzz\n')
        self.eq('r_1x\nfizz\n|buzz\n|4x', 'l_k', 'r_1x\n|fizz\nbuzz\n|4x')
        self.eq('1x\n|fizz\nbuzz\n|4x', 'l_k', '1x\n|fizz\n|buzz\n4x')

    def test_b(self):
        self.eq('fizz buzz\nfiz|z bu|zz\n', 'b_k', 'fiz|z bu|zz\nfiz|z bu|zz\n')
        self.eq('fizz buzz\nfiz|z bu|zz\nfiz|z bu|zz\n', 'b_k', 'fizz buzz\nfiz|z bu|zz\nfizz buzz\n')
        self.eq('fiz|z bu|zz\nfiz|z bu|zz\n', 'b_k', 'fiz|z bu|zz\nfizz buzz\n')
        self.eq('fiz|z bu|zz\nfiz|z bu|zz\nfiz|z bu|zz\n', 'b_k', 'fiz|z bu|zz\nfiz|z bu|zz\nfizz buzz\n')
        self.eq('r_fi|zz bu|zz\n', 'b_k', 'r_fi|zz bu|zz\n')
        self.eq('fizzbuzz\nfizzbuzz\nfizzbuzz\nfi|zzbu|zz\n', 'b_2k', 'fizzbuzz\nfi|zzbu|zz\nfi|zzbu|zz\nfi|zzbu|zz\n')

    def test_d(self):
        self.eq('1\n2\n|3\n4\n5', 'dk', '1\n|4\n5')
