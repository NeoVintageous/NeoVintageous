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
# along with NeoVintageous.  If not, see <https://www.gnu.org/licensesubstitute/>.

from NeoVintageous.tests import unittest


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
@unittest.mock.patch('NeoVintageous.nv.session.save_session', unittest.mock.Mock())
class Test_ex_substitute(unittest.FunctionalTestCase):

    def test_substitute(self):
        self.eq('|', ':substitute/a/b/', '|')
        self.eq('|  ', ':substitute/a/b/', '|  ')
        self.eq('|a', ':substitute/a/b/', '|b')
        self.eq('|a', ':substitute/a/b/', '|b')
        self.eq('|a', ':substitute/a/b/', '|b')
        self.eq('|a\n', ':substitute/a/b/', '|b\n')
        self.eq('|a\n', ':substitute/a/b', '|b\n')
        self.eq('|xxx', ':substitute/x/y/', '|yxx')
        self.eq('x|xx', ':substitute/x/y/', '|yxx')
        self.eq('   x|xx', ':substitute/x/y/', '   |yxx')
        self.eq('xx|x\n', ':substitute/x/y/', '|yxx\n')
        self.eq('xx\n|xx\n', ':substitute/x/y/', 'xx\n|yx\n')
        self.eq('xx\n|yy\n', ':substitute/x/a/', 'xx\n|yy\n')
        self.eq('xx\n|xx\nxx\n', ':substitute/x/y/', 'xx\n|yx\nxx\n')
        self.eq('axxa\n|bxxb\ncxxc\n', ':substitute/x/y/', 'axxa\n|byxb\ncxxc\n')
        self.eq('axxa\n   bx|xb\ncxxc\n', ':substitute/x/y/', 'axxa\n   |byxb\ncxxc\n')
        self.eq('a\n|b\nc\n', ':%substitute/$/,/', 'a,\nb,\n|c,\n')
        self.eq('a\n|b\nc\n', ':substitute/$/,/', 'a\n|b,\nc\n')
        self.eq('a\n|b\nc\n', ':s/$/,/g', 'a\n|b,\nc\n')
        self.eq('aa\nb|b\ncc\n', ':s/$/,/g', 'aa\n|bb,\ncc\n')
        self.eq('|<app>jdk\n', ':substitute/$/<app>/', '|<app>jdk<app>\n')
        # TODO Fix self.eq('|<app>jdk\n', ':substitute/$/<\\/app>/', '<app>jdk</app>')

    def test_flags(self):
        self.eq('axxa\n|bxxb\ncxxc\n', ':substitute/x/y/g', 'axxa\n|byyb\ncxxc\n')
        self.eq('axxa\n|bxxb\ncxxc\n', ':substitute/x/y/i', 'axxa\n|byxb\ncxxc\n')
        self.eq('axxa\n|bXXb\ncxxc\n', ':substitute/x/y/i', 'axxa\n|byXb\ncxxc\n')
        self.eq('axxa\n|bxXb\ncxxc\n', ':substitute/x/y/gi', 'axxa\n|byyb\ncxxc\n')
        self.eq('axxa\n|bXxb\ncxxc\n', ':substitute/x/y/gi', 'axxa\n|byyb\ncxxc\n')

    def test_i_flag_ignore_case(self):
        self.set_option('ignorecase', True)
        self.eq('|aA', ':s/a/x/g', '|xx')
        self.eq('|aA', ':s/a/x/gi', '|xx')
        self.set_option('ignorecase', False)
        self.eq('|aA', ':s/a/x/g', '|xA')
        self.eq('|aA', ':s/a/x/gi', '|xx')

    def test_I_flag_dont_ignore_case(self):
        self.set_option('ignorecase', True)
        self.eq('|aA', ':s/a/x/gI', '|xA')
        self.set_option('ignorecase', False)
        self.eq('|aA', ':s/a/x/gI', '|xA')

    def test_smartcase(self):
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.eq('|fizz FIZZ fIzZ', ':s/FIZZ/x/g', '|fizz x fIzZ')
        self.eq('|fizz FIZZ fIzZ', ':s/fizz/x/g', '|x x x')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', False)
        self.eq('|fizz FIZZ fIzZ', ':s/FIZZ/x/g', '|x x x')
        self.set_option('ignorecase', False)
        self.set_option('smartcase', False)
        self.eq('|fizz FIZZ fIzZ', ':s/FIZZ/x/g', '|fizz x fIzZ')

    def test_ranges(self):
        self.eq('axxa\n|bxxb\ncxxc\n', ':1,$substitute/x/y/', 'ayxa\nbyxb\n|cyxc\n')
        self.eq('axxa\n|bxxb\ncxxc\n', ':1,$substitute/x/y/g', 'ayya\nbyyb\n|cyyc\n')
        self.eq('axxa\n|bxxb\ncxxc\n', ':%substitute/x/y/', 'ayxa\nbyxb\n|cyxc\n')
        self.eq('axxa\n|bxxb\ncxxc\n', ':%substitute/x/y/g', 'ayya\nbyyb\n|cyyc\n')
        self.eq('xx\n|xx\nxx\nxx\nxx', ':2,4substitute/x/y/', 'xx\nyx\nyx\n|yx\nxx')
        self.eq('xx\n|xx\nxx\nxx\nxx', ':1,3substitute/x/y/', 'yx\nyx\n|yx\nxx\nxx')
        self.eq('xx\n|xx\nxx\nxx\nxx', ':2,4substitute/x/y/g', 'xx\nyy\nyy\n|yy\nxx')

    def test_in_visual_mode(self):
        self.eq('xx\n|xx\nxx\nxx|\nxx', ':\'<,\'>substitute/x/y/g', 'n_xx\nyy\nyy\n|yy\nxx')
        self.eq('xx\n|xx\nx|x\nxx\nxx', ':\'<,\'>substitute/x/y/g', 'n_xx\nyy\n|yy\nxx\nxx')

    def test_issue_210_single_line_eol_match(self):
        self.eq('a\n|b\nc', ':substitute/$/,/', 'a\n|b,\nc')
        self.eq('a\n|b\nc', ':substitute/$/,/g', 'a\n|b,\nc')
        self.eq('a\n|b\nc\n', ':substitute/$/,/', 'a\n|b,\nc\n')
        self.eq('aa\nb|b\ncc\n', ':substitute/$/,/', 'aa\n|bb,\ncc\n')
        self.eq('a\n|b\n\nc\n\nd\n\n', ':substitute/$/,/', 'a\n|b,\n\nc\n\nd\n\n')
        self.eq('a\n|b\n\nc\n\nd\n\n', ':substitute/$/,/g', 'a\n|b,\n\nc\n\nd\n\n')

    def test_issue_210_match_every_eol(self):
        self.eq('a\n|b\nc', ':%substitute/$/,/', 'a,\nb,\n|c,')
        self.eq('a\n|b\nc', ':%substitute/$/,/g', 'a,\nb,\n|c,')
        self.eq('a\n|b\nc\n', ':%substitute/$/,/', 'a,\nb,\n|c,\n')
        self.eq('aa\nb|b\ncc\n', ':%substitute/$/,/', 'aa,\nbb,\n|cc,\n')
        self.eq('a\n|b\n\nc\n\nd\n\n', ':%substitute/$/,/', 'a,\nb,\n,\nc,\n,\nd,\n|,\n')
        self.eq('a\n|b\n\nc\n\nd\n\n', ':%substitute/$/,/g', 'a,\nb,\n,\nc,\n,\nd,\n|,\n')

    @unittest.mock.patch('NeoVintageous.nv.session._session', {})
    @unittest.mock_status_message()
    def test_repeat_no_previous(self):
        self.eq('a|bc', ':substitute', 'a|bc')
        self.assertStatusMessage('E33: No previous substitute regular expression')

    def test_repeat(self):
        self.eq('|abc abc', ':substitute/b/x/', '|axc abc')
        self.eq('|abc abc', ':substitute', '|axc abc')
