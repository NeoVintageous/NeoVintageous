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


class TestMultipleCursors(unittest.FunctionalTestCase):

    def test_n_enter_multi_cursor(self):
        for seq in ('<C-n>', 'gh'):
            self.eq('x fi|zz x', seq, 's_x |fizz| x')
            self.eq('x fizz fi|zz fizz x', seq, 's_x fizz |fizz| fizz x')
            self.eq('x fizz |fizz| fizz x', seq, 's_x fizz |fizz| fizz x')
            self.eq('x fizz f|iz|z fizz x', seq, 's_x fizz |fizz| fizz x')
            self.assertStatusLineIsSelect()

    def test_v_enter_multi_cursor(self):
        for seq in ('<C-n>', 'gh'):
            self.eq('|fizz| buzz\nx fizz buzz\nfizz\n', 'v_' + seq, 's_|fizz| buzz\nx |fizz| buzz\nfizz\n')
            self.assertStatusLineIsSelect()

    def test_v_from_visual_multi_cursor_enters_normal_mode(self):
        self.normal('x fi|zz fizz fizz x')
        self.feed('<C-n>')
        self.feed('s_<C-n>')
        self.feed('s_<C-n>')
        self.assertVselect('x |fizz| |fizz| |fizz| x')
        self.assertStatusLineIsSelect()
        self.feed('s_v')
        self.assertNormal('x |fizz |fizz |fizz x')
        self.assertStatusLineIsNormal()

    def test_V_enter_multi_cursor(self):
        for seq in ('<C-n>', 'gh'):
            self.eq('|fizz\n|x\nfizz\n\nfizz\nfizz\n', 'V_' + seq, 's_|fizz\n|x\n|fizz\n|\nfizz\nfizz\n')
            self.assertStatusLineIsSelect()

    def test_b_enter_multi_cursor(self):
        for seq in ('<C-n>',):
            self.eq('|fizz|\n|fizz|\n', 'b_' + seq, 'n_|fizz\n|fizz\n')
            self.assertStatusLineIsNormal()

    def test_add_match(self):
        for seq in ('<C-n>', 'j'):
            self.normal('x fizz |fizz| fizz x')
            self.feed('<C-n>')
            self.assertVselect('x fizz |fizz| fizz x')
            self.feed('s_' + seq)
            self.assertVselect('x fizz |fizz| |fizz| x')
            self.feed('s_' + seq)
            self.assertVselect('x |fizz| |fizz| |fizz| x')
            self.feed('s_' + seq)
            self.assertVselect('x |fizz| |fizz| |fizz| x')
            self.vselect('|fizz| buzz\nx |fizz| buzz\nbuzz fizz\nfizz\n')
            self.feed('s_' + seq)
            self.assertVselect('|fizz| buzz\nx |fizz| buzz\nbuzz |fizz|\nfizz\n')
            self.feed('s_' + seq)
            self.assertVselect('|fizz| buzz\nx |fizz| buzz\nbuzz |fizz|\n|fizz|\n')
            self.vselect('|fizz\n|x\n|fizz\n|\nfizz\nfizz\nfizz\n')
            self.feed('<C-n>')
            self.assertVselect('|fizz\n|x\n|fizz\n|\n|fizz\n|fizz\nfizz\n')
            self.feed('<C-n>')
            self.assertVselect('|fizz\n|x\n|fizz\n|\n|fizz\n||fizz\n|fizz\n')
            self.vselect('|fizz| fizz fizz fizz')
            self.feed('s_2' + seq)
            self.assertVselect('|fizz| |fizz| |fizz| fizz')
            self.feed('s_2' + seq)
            self.assertVselect('|fizz| |fizz| |fizz| |fizz|')
            self.assertStatusLineIsSelect()

    def test_remove_match(self):
        for seq in ('<C-p>', 'k'):
            self.normal('fizz fi|zz fizz fizz fizz')
            self.feed('<C-n>')
            self.feed('s_<C-n>')
            self.feed('s_<C-n>')
            self.assertVselect('fizz |fizz| |fizz| |fizz| fizz')
            self.feed('s_' + seq)
            self.assertVselect('fizz |fizz| |fizz| fizz fizz')
            self.feed('s_' + seq)
            self.assertVselect('fizz |fizz| fizz fizz fizz')
            self.feed('s_' + seq)
            self.assertNormal('fizz |fizz fizz fizz fizz')
            self.assertStatusLineIsBlank()
            self.normal('fizz |fizz| fizz fizz fizz')
            self.feed('<C-n>')
            self.feed('s_<C-n>')
            self.feed('s_<C-n>')
            self.assertVselect('fizz |fizz| |fizz| |fizz| fizz')
            self.feed('s_2' + seq)
            self.assertVselect('fizz |fizz| fizz fizz fizz')
            self.assertStatusLineIsSelect()
            self.feed('s_<C-n>')
            self.feed('s_<C-n>')
            self.assertVselect('fizz |fizz| |fizz| |fizz| fizz')
            self.assertStatusLineIsSelect()
            self.feed('s_6' + seq)
            self.assertNormal('fizz |fizz fizz fizz fizz')
            self.assertStatusLineIsBlank()

    def test_skip_match(self):
        for seq in ('<C-x>', 'l'):
            self.normal('fizz |fizz| fizz fizz fizz fizz fizz')
            self.feed('<C-n>')
            self.feed('s_<C-n>')
            self.feed('s_' + seq)
            self.assertVselect('fizz |fizz| fizz |fizz| fizz fizz fizz')
            self.feed('s_<C-n>')
            self.feed('s_<C-n>')
            self.assertVselect('fizz |fizz| fizz |fizz| |fizz| |fizz| fizz')
            self.feed('s_<C-n>')
            self.assertVselect('fizz |fizz| fizz |fizz| |fizz| |fizz| |fizz|')
            self.feed('s_<C-n>')
            self.assertVselect('|fizz| |fizz| fizz |fizz| |fizz| |fizz| |fizz|')
            self.assertStatusLineIsSelect()

    def test_multi_cursor_exit_from_visual_mode(self):
        for seq in ((True, '<C-n>', '<C-n>', '<Esc>'), (False, 'gh', 'j', 'J')):
            self.set_setting('multi_cursor_exit_from_visual_mode', seq[0])
            self.eq('fizz fi|zz fizz fizz fizz', seq[1], 's_fizz |fizz| fizz fizz fizz')
            self.feed('s_' + seq[2])
            self.feed('s_' + seq[2])
            self.assertVselect('fizz |fizz| |fizz| |fizz| fizz')
            self.feed('s_' + seq[3])
            if seq[0]:
                self.assertNormal('fizz |fizz fizz fizz fizz')
            else:
                self.assertNormal('fizz |fizz |fizz |fizz fizz')
            self.assertStatusLineIsBlank()

    def test_select_all(self):
        for seq in ('A', '<M-n>'):
            self.normal('fizz |fizz| buzz fizz fi zz fizz buzz')
            self.feed('<C-n>')
            self.feed('s_' + seq)
            self.assertVselect('|fizz| |fizz| buzz |fizz| fi zz |fizz| buzz')
            self.assertStatusLineIsSelect()

    def test_select_all_search_occurrences(self):
        self.normal('fizz fi|zz buzz fizz fi zz fizz buzz')
        self.feed('n_*')
        self.feed('gH')
        self.assertVselect('|fizz| |fizz| buzz |fizz| fi zz |fizz| buzz')
        self.assertStatusLineIsSelect()
        self.normal('foo f|oo buzz foo fi zz foo buzz')
        self.feed('n_#')
        self.feed('gH')
        self.assertVselect('|foo| |foo| buzz |foo| fi zz |foo| buzz')
        self.assertStatusLineIsSelect()

    @unittest.mock_bell()
    @unittest.mock_status_message()
    def test_no_search_occurrences(self):
        self.eq('fi|zz', 'n_gH', 'fi|zz')
        self.assertBell('no available search matches')
