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


class Test_ctrl_u(unittest.FunctionalTestCase):

    @unittest.mock_ui()
    def test_ctrl_u(self):
        self.eq('1\n2\n3\n4\n5\n|6', 'n_<C-u>', '1\n2\n|3\n4\n5\n6')
        self.eq('1\n2\n3\n4\n|5\n6', 'n_<C-u>', '1\n|2\n3\n4\n5\n6')
        self.eq('1\n2\n3\n|4\n5\n6', 'n_<C-u>', '|1\n2\n3\n4\n5\n6')
        self.eq('1\n2\n|3\n4\n5\n6', 'n_<C-u>', '|1\n2\n3\n4\n5\n6')
        self.eq('1\n|2\n3\n4\n5\n6', 'n_<C-u>', '|1\n2\n3\n4\n5\n6')
        self.eq('|1\n2\n3\n4\n5\n6', 'n_<C-u>', '|1\n2\n3\n4\n5\n6')
        self.eq('|1\n2\n3\n4\n5\n6', 'n_<C-u>', '|1\n2\n3\n4\n5\n6')
        self.eq('1\n2\n    3\n4\n5\n6|', 'n_<C-u>', '1\n2\n    |3\n4\n5\n6')
        self.eq('\n1\n|2\n3\n4\n5\n6', 'n_<C-u>', '|\n1\n2\n3\n4\n5\n6')
        self.eq('\n\n1\n|2\n3\n4\n5\n6', 'n_<C-u>', '|\n\n1\n2\n3\n4\n5\n6')
        self.eq('\n\n\n1\n|2\n3\n4\n5\n6', 'n_<C-u>', '|\n\n\n1\n2\n3\n4\n5\n6')

    def test_i_ctrl_u(self):
        self.eq('fiz |buz', 'i_<C-u>', '|buz')
        self.eq('fiz bu|zz', 'i_<C-u>', '|zz')
        self.eq('fiz bu|zz\nx\nx', 'i_<C-u>', '|zz\nx\nx')

    @unittest.mock_ui()
    def test_ctrl_u_already_at_eof_invokes_bell_and_does_not_scroll(self):
        self.eq('fi|zz\n2\n3\n4', 'n_<C-u>', 'fi|zz\n2\n3\n4')
        self.assertBell()

    @unittest.mock_ui()
    def test_ctrl_u_on_empty_view_invokes_bell(self):
        self.eq('|', 'n_<C-u>', '|')
        self.assertBell()

    @unittest.mock_ui(screen_rows=12)
    def test_ctrl_u_uses_screen_size_to_calculate_number_of_lines_to_scroll(self):
        self.eq('1\n2\n3\n4\n5\n6\n7\n8\n|9', 'n_<C-u>', '1\n2\n|3\n4\n5\n6\n7\n8\n9')

    @unittest.mock_ui(screen_rows=20)
    def test_ctrl_u_should_use_count_as_number_of_lines_to_scroll(self):
        self.normal(('\n' * 10) + '|')
        self.feed('n_3<C-u>')
        self.assertSelection(7)
        self.feed('n_4<C-u>')
        self.assertSelection(3)
        self.feed('n_1<C-u>')
        self.assertSelection(2)
        self.feed('n_5<C-u>')
        self.assertSelection(0)
        self.assertNoBell()

    @unittest.mock_ui()
    def test_v_ctrl_u(self):
        self.eq('r_1\n2\n3xy\n4\n5\na|b|c', 'v_<C-u>', 'r_1\n2\n|3xy\n4\n5\nab|c')
        self.eq('r_1\n2\n3xy\n4\n5\n|a|bc', 'v_<C-u>', 'r_1\n2\n|3xy\n4\n5\na|bc')
        self.eq('r_1\n2\n3xy\n4\n5\nab|c|', 'v_<C-u>', 'r_1\n2\n|3xy\n4\n5\nabc|')
        self.eq('r_1\n2\n3xy\n4\n5\n|ab|c', 'v_<C-u>', 'r_1\n2\n|3xy\n4\n5\nab|c')
        self.eq('r_1\n2xy\n3xy\n4\n|5\nab|c', 'v_<C-u>', 'r_1\n|2xy\n3xy\n4\n5\nab|c')
        self.eq('r_1\n2xy\n3xy\n4\n5x|y\nab|c', 'v_<C-u>', 'r_1\n|2xy\n3xy\n4\n5xy\nab|c')
        self.eq('r_1xy\n2\n3\n4|x\n5\nab|c', 'v_<C-u>', 'r_|1xy\n2\n3\n4x\n5\nab|c')
        self.eq('r_1xy\n2\n3\n4|x\n5x|y\n6', 'v_<C-u>', 'r_|1xy\n2\n3\n4x\n5x|y\n6')
        self.eq('r_1\n2\n    3xy\n4\n5\na|b|c', 'v_<C-u>', 'r_1\n2\n    |3xy\n4\n5\nab|c')
        self.eq('1\n2\n3x\n4\n5xy\nf|iz|z', 'v_<C-u>', 'r_1\n2\n|3x\n4\n5xy\nfi|zz')
        self.eq('1\n2\n3x\n4\n5|xy\n6|xy', 'v_<C-u>', 'r_1\n2\n|3x\n4\n5x|y\n6xy')
        self.eq('1\n2\n3x\n|4xy\n5\n6x|y', 'v_<C-u>', 'r_1\n2\n|3x\n4|xy\n5\n6xy')
        self.eq('1\n2x\n3\n|4xy\n5x|y\n6', 'v_<C-u>', 'r_1\n|2x\n3\n4|xy\n5xy\n6')
        self.eq('|1x\n2x\n3x\n4x\n5x\n6|x', 'v_<C-u>', '|1x\n2x\n3|x\n4x\n5x\n6x')
        self.eq('1\n2\n|3x\n4\n5\n6x|y', 'v_<C-u>', '1\n2\n|3|x\n4\n5\n6xy')
        self.eq('1\n|2\n3\n4\n5|\n6', 'v_<C-u>', '1\n|2|\n3\n4\n5\n6')
        self.eq('1\n2x\n3\n4\nf|iz|z\n6', 'v_<C-u>', 'r_1\n|2x\n3\n4\nfi|zz\n6')

    @unittest.mock_ui()
    def test_v_ctrl_u_invokes_bell_when_at_bof(self):
        self.eq('r_fi|zz\n2\n3\na|bc', 'v_<C-u>', 'r_fi|zz\n2\n3\na|bc')
        self.assertBell()

    @unittest.mock_ui()
    def test_V_ctrl_u_invokes_bell_when_at_sof(self):
        self.eq('r_|1\n2\n3|', 'V_<C-u>', 'r_|1\n2\n3|')
        self.assertBell()

    @unittest.mock_ui()
    def test_V_ctrl_u(self):
        self.eq('r_1x\n2x\n3x\n4x\n5x\n|6x|', 'V_<C-u>', 'r_1x\n2x\n|3x\n4x\n5x\n6x|')
        self.eq('r_1x\n2x\n3x\n4x\n5x\n|6x\n|', 'V_<C-u>', 'r_1x\n2x\n|3x\n4x\n5x\n6x\n|')
        self.eq('r_1x\n2x\n3x\n4x\n|5x\n6x|', 'V_<C-u>', 'r_1x\n|2x\n3x\n4x\n5x\n6x|')
        self.eq('r_1x\n2x\n3x\n4x\n|5x\n|6x', 'V_<C-u>', 'r_1x\n|2x\n3x\n4x\n5x\n|6x')
        self.eq('r_1x\n2x\n3x\n|4x\n5x\n6x|', 'V_<C-u>', 'r_|1x\n2x\n3x\n4x\n5x\n6x|')
        self.eq('r_1x\n2x\n3x\n|4x\n5x\n|6x', 'V_<C-u>', 'r_|1x\n2x\n3x\n4x\n5x\n|6x')
        self.eq('r_1x\n2x\n|3x\n4x\n5x\n6x|', 'V_<C-u>', 'r_|1x\n2x\n3x\n4x\n5x\n6x|')
        self.eq('r_\n\n2x\n|3x\n4x\n5x\n6x|', 'V_<C-u>', 'r_|\n\n2x\n3x\n4x\n5x\n6x|')
        self.eq('r_\n\n\n2x\n|3x\n4x\n5x\n6x|', 'V_<C-u>', 'r_|\n\n\n2x\n3x\n4x\n5x\n6x|')
        self.eq('1x\n2x\n3x\n4x\n5x\n|6x|', 'V_<C-u>', 'r_1x\n2x\n|3x\n4x\n5x\n6x|')
        self.eq('1x\n2x\n3x\n4x\n|5x\n6x|', 'V_<C-u>', 'r_1x\n2x\n|3x\n4x\n5x\n|6x')
        self.eq('1x\n2x\n3x\n|4x\n5x\n6x|', 'V_<C-u>', 'r_1x\n2x\n|3x\n4x\n|5x\n6x')
        self.eq('1x\n2x\n3x\n|4x\n5x\n|6x', 'V_<C-u>', 'r_1x\n|2x\n3x\n4x\n|5x\n6x')
        self.eq('1x\n2x\n|3x\n4x\n|5x\n6x', 'V_<C-u>', 'r_|1x\n2x\n3x\n|4x\n5x\n6x')
        self.eq('1x\n2x\n|3x\n4x\n5x\n6x|', 'V_<C-u>', 'r_1x\n2x\n|3x\n|4x\n5x\n6x')
        self.eq('1x\n|2x\n3x\n|4x\n5x\n6x', 'V_<C-u>', 'r_|1x\n2x\n|3x\n4x\n5x\n6x')
        self.eq('|1x\n2x\n3x\n4x\n5x\n6x|', 'V_<C-u>', '|1x\n2x\n3x\n|4x\n5x\n6x')

    @unittest.mock_ui()
    def test_d(self):
        self.eq('1\n2\n3\n4\n5\n|6', 'd<C-u>', '1\n2\n|6')
        self.eq('1\n2\n3\n4\n|5\n6', 'd<C-u>', '1\n|5\n6')
