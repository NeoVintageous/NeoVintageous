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


class Test_ctrl_r(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('redo')
    @unittest.mock_bell()
    def test_ctrl_r_invokes_bell_when_nothing_to_redo(self):
        self.eq('fi|zz', '<C-r>', 'fi|zz')
        self.assertRunCommand('redo')
        self.assertBell('Already at newest change')

    @unittest.mock_run_commands('redo')
    @unittest.mock_bell()
    def test_ctrl_r_count(self):
        self.eq('fi|zz', '3<C-r>', 'fi|zz')
        self.assertRunCommand('redo', count=3)
        self.assertBell('Already at newest change')

    @unittest.mock_bell()
    def test_n_ctrl_r(self):
        self.normal('fizz ab|cd buzz')
        self.feed('ciw')
        self.feed('<Esc>')
        self.assertNormal('fizz|  buzz')
        self.feed('u')
        self.assertNormal('fizz ab|cd buzz')
        self.feed('<C-r>')
        self.assertNormal('fizz | buzz')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_n_ctrl_r_fix_eol_with_single_word(self):
        self.normal('fiz|z')
        self.feed('ciw')
        self.feed('<Esc>')
        self.assertNormal('|')
        self.feed('u')
        self.assertNormal('fiz|z')
        self.feed('<C-r>')
        self.assertNormal('|')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_n_ctrl_r_fix_eol_with_multi_word(self):
        self.normal('fizz buz|z')
        self.feed('ciw')
        self.feed('<Esc>')
        self.assertNormal('fizz| ')
        self.feed('u')
        self.assertNormal('fizz buz|z')
        self.feed('<C-r>')
        self.assertNormal('fizz| ')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_n_ctrl_r_fix_eol_with_single_word_and_newline(self):
        self.normal('fiz|z\n')
        self.feed('ciw')
        self.feed('<Esc>')
        self.assertNormal('|\n')
        self.feed('u')
        self.assertNormal('fiz|z\n')
        self.feed('<C-r>')
        self.assertNormal('|\n')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_n_ctrl_r_fix_eol_with_multi_word_and_newline(self):
        self.normal('fizz buz|z\n')
        self.feed('ciw')
        self.feed('<Esc>')
        self.assertNormal('fizz| \n')
        self.feed('u')
        self.assertNormal('fizz buz|z\n')
        self.feed('<C-r>')
        self.assertNormal('fizz| \n')
        self.assertNoBell()
