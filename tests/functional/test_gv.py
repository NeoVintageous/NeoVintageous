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


class Test_gv(unittest.FunctionalTestCase):

    def test_gv_works_for_visual_mode(self):
        self.visual('a|b\nc|d\n')
        self.feed('<Esc>')
        self.assertNormal('ab\n|cd\n')
        self.feed('gv')
        self.assertVisual('a|b\nc|d\n')
        self.assertStatusLineRegex('-- VISUAL --')

    def test_gv_works_for_visual_line_mode(self):
        self.vline('ab\n|cd|\ne\n')
        self.feed('<Esc>')
        self.assertNormal('ab\nc|d\ne\n')
        self.feed('gv')
        self.assertVline('ab\n|cd|\ne\n')
        self.assertStatusLineRegex('-- VISUAL LINE --')

    def test_gv_works_for_visual_lines_mode(self):
        self.vline('ab\n|cd\nef|\ng\n')
        self.feed('<Esc>')
        self.assertNormal('ab\ncd\ne|f\ng\n')
        self.feed('gv')
        self.assertVline('ab\n|cd\nef|\ng\n')
        self.assertStatusLineRegex('-- VISUAL LINE --')

    def test_gv_works_for_visual_block_mode(self):
        self.vblock('a\nb|cd|e\nf|gh|i\nj\n')
        self.feed('<Esc>')
        self.assertNormal('a\nbcde\nfg|hi\nj\n')
        self.feed('gv')
        self.assertVblock('a\nb|cd|e\nf|gh|i\nj\n')
        self.assertStatusLineRegex('-- VISUAL BLOCK --')

    def test_issue_338(self):
        self.vline('1111\n2222\n    |3333\n    4444\n|')
        self.feed('<Esc>')
        self.assertNormal('1111\n2222\n    3333\n    444|4\n')
        self.feed('gv')
        self.assertVline('1111\n2222\n|    3333\n    4444\n|')
        self.assertStatusLineRegex('-- VISUAL LINE --')
