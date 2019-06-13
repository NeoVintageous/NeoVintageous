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

    def test_v_gv(self):
        self.visual('a|b\nc|d\n')
        self.feed('<Esc>')
        self.assertNormal('ab\n|cd\n')
        self.feed('gv')
        self.assertVisual('a|b\nc|d\n')
        self.assertStatusLineIsVisual()

    def test_V_gv(self):
        self.vline('ab\n|cd|\ne\n')
        self.feed('<Esc>')
        self.assertNormal('ab\nc|d\ne\n')
        self.feed('gv')
        self.assertVline('ab\n|cd\n|e\n')
        self.assertStatusLineIsVisualLine()

    def test_V_gv_many_lines(self):
        self.vline('ab\n|cd\nef|\ng\n')
        self.feed('<Esc>')
        self.assertNormal('ab\ncd\ne|f\ng\n')
        self.feed('gv')
        self.assertVline('ab\n|cd\nef\n|g\n')
        self.assertStatusLineIsVisualLine()

    def test_V_gv_empty_line(self):
        self.vline('x\n|\n\n\n|\n\ny')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertVline('x\n|\n\n\n|\n\ny')
        self.assertStatusLineIsVisualLine()

    def test_V_gv_eof(self):
        self.vline('1\n|2\n3\ny|')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertVline('1\n|2\n3\ny|')
        self.assertStatusLineIsVisualLine()

    def test_V_gv_reverse(self):
        self.rvline('1\n|2\n3\n|xy')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertRVline('1\n|2\n3\n|xy')
        self.assertStatusLineIsVisualLine()

    def test_V_gv_reverse_eof(self):
        self.rvline('1\n|2\n3\ny|')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertRVline('1\n|2\n3\ny|')
        self.assertStatusLineIsVisualLine()

    def test_b_gv(self):
        self.vblock('a\nb|cd|e\nf|gh|i\nj\n')
        self.feed('<Esc>')
        self.assertNormal('a\nbcde\nfg|hi\nj\n')
        self.feed('gv')
        self.assertVblock('a\nb|cd|e\nf|gh|i\nj\n')
        self.assertStatusLineIsVisualBlock()

    def test_noop(self):
        self.normal('a|bc')
        self.view.erase_regions('visual_sel')
        self.settings().erase('_nv_visual_sel_mode')
        self.feed('gv')
        self.assertNormal('a|bc')
        self.assertStatusLineIsBlank()

    def test_issue_338(self):
        self.vline('1111\n2222\n    |3333\n    4444\n|')
        self.feed('<Esc>')
        self.assertNormal('1111\n2222\n    3333\n    444|4\n')
        self.feed('gv')
        self.assertVline('1111\n2222\n|    3333\n    4444\n|')
        self.assertStatusLineIsVisualLine()

    def test_issue_426_V_eol_newline(self):
        self.vline('111\n|222\n333\n|\n5')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertVline('111\n|222\n333\n|\n5')
        self.assertStatusLineIsVisualLine()

    def test_issue_426_v(self):
        self.visual('111\na|bc\nx|yz\n444\n5')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertVisual('111\na|bc\nx|yz\n444\n5')
        self.assertStatusLineIsVisual()

    def test_issue_426_l(self):
        self.vline('111\n|222\n333\n|444\n5')
        self.feed('<Esc>')
        self.feed('gv')
        self.assertVline('111\n|222\n333\n|444\n5')
        self.assertStatusLineIsVisualLine()
