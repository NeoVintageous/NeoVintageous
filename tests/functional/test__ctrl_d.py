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


class Test_ctrl_d(unittest.FunctionalTestCase):

    @unittest.mock_ui()
    def test_ctrl_d(self):
        self.eq('|1\n2\n3\n4\n5\n6', 'n_<C-d>', '1\n2\n3\n|4\n5\n6')
        self.eq('1\n|2\n3\n4\n5\n6', 'n_<C-d>', '1\n2\n3\n4\n|5\n6')
        self.eq('1\n2\n|3\n4\n5\n6', 'n_<C-d>', '1\n2\n3\n4\n5\n|6')
        self.eq('1\n2\n3\n|4\n5\n6', 'n_<C-d>', '1\n2\n3\n4\n5\n|6')
        self.eq('1\n2\n3\n4\n|5\n6', 'n_<C-d>', '1\n2\n3\n4\n5\n|6')
        self.eq('1\n2\n3\n4\n5\n|6', 'n_<C-d>', '1\n2\n3\n4\n5\n|6')
        self.eq('|1\n2\n3\n        4\n5\n6', 'n_<C-d>', '1\n2\n3\n        |4\n5\n6')
        self.eq('1\n2\n3\n4\n5\n|6\n', 'n_<C-d>', '1\n2\n3\n4\n5\n|6\n')
        self.eq('1\n2\n3\n4\n5\n|6\n\n', 'n_<C-d>', '1\n2\n3\n4\n5\n6\n|\n')
        self.eq('1\n2\n3\n4\n5\n|6\n\n\n', 'n_<C-d>', '1\n2\n3\n4\n5\n6\n\n|\n')

    @unittest.mock_ui()
    def test_ctrl_d_already_at_eof_invokes_bell_and_does_not_scroll(self):
        self.eq('1\n2\n3\n4\nfi|zz', 'n_<C-d>', '1\n2\n3\n4\nfi|zz')
        self.assertBell()

    @unittest.mock_ui()
    def test_ctrl_d_on_empty_view_invokes_bell(self):
        self.eq('|', 'n_<C-d>', '|')
        self.assertBell()

    @unittest.mock_ui(screen_rows=12)
    def test_ctrl_d_uses_screen_size_to_calculate_number_of_lines_to_scroll(self):
        self.eq('|1\n2\n3\n4\n5\n6\n7\n8\n9', 'n_<C-d>', '1\n2\n3\n4\n5\n6\n|7\n8\n9')

    @unittest.mock_ui(screen_rows=10)
    def test_ctrl_d_ignores_the_last_line_if_it_is_an_empty_line(self):
        self.eq('1\n2\n3\n|4\n5\n6\n', 'n_<C-d>', '1\n2\n3\n4\n5\n|6\n')

    @unittest.mock_ui(screen_rows=20)
    def test_ctrl_d_should_use_count_as_number_of_lines_to_scroll(self):
        self.normal('|' + ('\n' * 10))
        self.feed('n_5<C-d>')
        self.assertSelection(5)
        self.feed('n_2<C-d>')
        self.assertSelection(7)
        self.feed('n_1<C-d>')
        self.assertSelection(8)
        self.feed('n_4<C-d>')
        self.assertSelection(9)
        self.assertNoBell()

    @unittest.mock_ui()
    def test_v_ctrl_d(self):
        self.eq('1\n2\n3\n4\n5\n|6', 'v_<C-d>', '1\n2\n3\n4\n5\n|6|')
        self.eq('1\n2\n3\n4\n5\n|6\n', 'v_<C-d>', '1\n2\n3\n4\n5\n|6|\n')
        self.eq('1\n2\n3\n4\n5\n|6xy', 'v_<C-d>', '1\n2\n3\n4\n5\n|6|xy')
        self.eq('1\n2\n3\n4\n5\n|6xy\n', 'v_<C-d>', '1\n2\n3\n4\n5\n|6|xy\n')
        self.eq('a|bc\n2\n3\n    4xy\n5\n6', 'v_<C-d>', 'a|bc\n2\n3\n    4|xy\n5\n6')
        self.eq('a|bc\n2\n3\n4xy\n5\n6', 'v_<C-d>', 'a|bc\n2\n3\n4|xy\n5\n6')
        self.eq('a|bc\n2xy\n3xy\n4xy\n5x|y\n6xy', 'v_<C-d>', 'a|bc\n2xy\n3xy\n4xy\n5xy\n6|xy')
        self.eq('a|bc\n2xy\n3x|y\n4xy\n5xy\n6xy', 'v_<C-d>', 'a|bc\n2xy\n3xy\n4xy\n5xy\n6|xy')
        self.eq('a|bc\n2x|y\n3\n4xy\n5xy\n6', 'v_<C-d>', 'a|bc\n2xy\n3\n4xy\n5|xy\n6')
        self.eq('r_1\nabc\n3\n|4|xy\n5xy\n6', 'v_<C-d>', '1\nabc\n3\n|4xy\n5xy\n6|')
        self.eq('r_1\na|bc\n3\n4xy\n5|xy\n6', 'v_<C-d>', 'r_1\nabc\n3\n4xy\n|5|xy\n6')
        self.eq('r_1\na|bc\n3\n4xy|\n5xy\n6', 'v_<C-d>', '1\nabc\n3\n4x|y\n5|xy\n6')
        self.eq('r_1\na|bc\n3\n4x|y\n5xy\n6', 'v_<C-d>', '1\nabc\n3\n4|xy\n5|xy\n6')
        self.eq('r_1\na|bc\n3\n4|xy\n5xy\n6', 'v_<C-d>', '1\nabc\n3\n|4xy\n5|xy\n6')
        self.eq('r_a|b|c\n2\n3\n4xy\n5\n6', 'v_<C-d>', 'a|bc\n2\n3\n4|xy\n5\n6')
        self.eq('r_|abc\n2xy\n3xy\n4xy\n5x|y\n6', 'v_<C-d>', 'r_abc\n2xy\n3xy\n|4xy\n5x|y\n6')
        self.eq('r_|abc\n2xy\n3xy\n4xy|\n5\n6', 'v_<C-d>', 'r_abc\n2xy\n3xy\n|4xy|\n5\n6')
        self.eq('r_|abc\n2xy\n3xy\n4x|y\n5\n6', 'v_<C-d>', 'r_abc\n2xy\n3xy\n|4x|y\n5\n6')
        self.eq('r_|abc\n2xy\n3xy\n4|xy\n5\n6', 'v_<C-d>', 'r_abc\n2xy\n3xy\n|4|xy\n5\n6')
        self.eq('r_|abc\n2xy\n3xy|\n4xy\n5\n6', 'v_<C-d>', 'abc\n2xy\n3x|y\n4|xy\n5\n6')
        self.eq('r_|abc\n2xy\n3|xy\n4xy\n5\n6', 'v_<C-d>', 'abc\n2xy\n|3xy\n4|xy\n5\n6')
        self.eq('r_|abc\n2x|y\n3\n4xy\n5\n6', 'v_<C-d>', 'abc\n2|xy\n3\n4|xy\n5\n6')
        self.eq('r_|abc|\n2\n3\n    4xy\n5\n6', 'v_<C-d>', 'ab|c\n2\n3\n    4|xy\n5\n6')
        self.eq('r_|abc|\n2\n3\n4xy\n5\n6', 'v_<C-d>', 'ab|c\n2\n3\n4|xy\n5\n6')

    @unittest.mock_ui()
    def test_v_ctrl_d_invokes_bell_when_at_eof(self):
        self.eq('a|bc\n2\n3\nfi|zz', 'v_<C-d>', 'a|bc\n2\n3\nfi|zz')
        self.assertBell()

    @unittest.mock_ui()
    def test_V(self):
        self.eq('|1x\n|2x\n3x\n4x\n5x\n6x', 'V_<C-d>', '|1x\n2x\n3x\n4x\n|5x\n6x')
        self.eq('|1x\n2x\n|3x\n4x\n5x\n6x', 'V_<C-d>', '|1x\n2x\n3x\n4x\n5x\n|6x')
        self.eq('1x\n|2x\n|3x\n4x\n5x\n6x', 'V_<C-d>', '1x\n|2x\n3x\n4x\n5x\n|6x')
        self.eq('1x\n|2x\n3x\n|4x\n5x\n6x', 'V_<C-d>', '1x\n|2x\n3x\n4x\n5x\n6x|')
        self.eq('1x\n|2x\n3x\n4x\n|5x\n6x', 'V_<C-d>', '1x\n|2x\n3x\n4x\n5x\n6x|')
        self.eq('1x\n|2x\n3x\n4x\n|5x\n6x\n', 'V_<C-d>', '1x\n|2x\n3x\n4x\n5x\n6x\n|')
        self.eq('1x\n|2x\n3x\n4x\n|5x\n6x\n\n', 'V_<C-d>', '1x\n|2x\n3x\n4x\n5x\n6x\n\n|')
        self.eq('r_|1x\n2x\n|3x\n4x\n5x\n6x', 'V_<C-d>', '1x\n|2x\n3x\n4x\n|5x\n6x')
        self.eq('r_1x\n|2x\n|3x\n4x\n5x\n6x', 'V_<C-d>', '1x\n|2x\n3x\n4x\n5x\n|6x')
        self.eq('r_|1x\n2x\n3x\n|4x\n5x\n6x', 'V_<C-d>', '1x\n2x\n|3x\n4x\n|5x\n6x')
        self.eq('r_1x\n|2x\n3x\n|4x\n5x\n6x', 'V_<C-d>', '1x\n2x\n|3x\n4x\n5x\n|6x')
        self.eq('r_1x\n|2x\n3x\n4x\n|5x\n6x', 'V_<C-d>', '1x\n2x\n3x\n|4x\n5x\n|6x')
        self.eq('r_|1x\n2x\n3x\n4x\n|5x\n6x', 'V_<C-d>', 'r_1x\n2x\n3x\n|4x\n|5x\n6x')
        self.eq('r_1x\n2x\n|3x\n4x\n|5x\n6x', 'V_<C-d>', '1x\n2x\n3x\n|4x\n5x\n6x|')
        self.eq('r_|1x\n2x\n3x\n4x\n5x\n|6x', 'V_<C-d>', 'r_1x\n2x\n3x\n|4x\n5x\n|6x')

    @unittest.mock_ui()
    def test_V_ctrl_d_invokes_bell_when_at_eof(self):
        self.eq('|1\n2\n3|', 'V_<C-d>', '|1\n2\n3|')
        self.assertBell()

    @unittest.mock_ui()
    def test_d(self):
        self.eq('|1\n2\n3\n4\n5\n6', 'd<C-d>', '|4\n5\n6')
        self.eq('1\n|2\n3\n4\n5\n6', 'd<C-d>', '1\n|5\n6')
