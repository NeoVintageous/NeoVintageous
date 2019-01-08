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


class Test_ctrl_x(unittest.FunctionalTestCase):

    def test_basic_subtraction(self):
        self.eq('|1000', '<C-x>', '99|9')
        self.eq('1|00', '<C-x>', '9|9')
        self.eq('1|0', '<C-x>', '|9')
        self.eq('|1', '<C-x>', '|0')
        self.eq('|0', '<C-x>', '-|1')
        self.eq('-|1', '<C-x>', '-|2')
        self.eq('|-9', '<C-x>', '-1|0')
        self.eq('-9|9', '<C-x>', '-10|0')
        self.eq('|-999', '<C-x>', '-100|0')

    def test_dirty_tests(self):
        self.eq('|', '<C-x>', '|')
        self.eq(' | ', '<C-x>', ' | ')
        self.eq('a|b', '<C-x>', 'a|b')

    def test_should_work_between_strings(self):
        self.eq('x|11y', '<C-x>', 'x1|0y')
        self.eq('x1|1y', '<C-x>', 'x1|0y')
        self.eq('x|-11y', '<C-x>', 'x-1|2y')

    def test_should_work_between_lines(self):
        self.eq('9\n|11\n8', '<C-x>', '9\n1|0\n8')
        self.eq('9\n|11\n8\n', '<C-x>', '9\n1|0\n8\n')

    def test_should_work_at_eof(self):
        self.eq('9\n|11', '<C-x>', '9\n1|0')

    def test_should_work_at_eof_indente(self):
        self.eq('9\n    |11', '<C-x>', '9\n    1|0')

    def test_should_work_with_cursor_on_the_number(self):
        self.eq('|999', '<C-x>', '99|8')
        self.eq('9|99', '<C-x>', '99|8')
        self.eq('99|9', '<C-x>', '99|8')

    def test_should_work_when_cursor_is_before_the_number(self):
        self.eq('| 999', '<C-x>', ' 99|8')
        self.eq('|    999', '<C-x>', '    99|8')
        self.eq('| x y z 999', '<C-x>', ' x y z 99|8')
        self.eq('9\n |   123', '<C-x>', '9\n    12|2')

    def test_should_not_work_when_cursor_is_after_number(self):
        self.eq('1|', '<C-x>', '1|')
        self.eq('1    |', '<C-x>', '1    |')
        self.eq('1 x |', '<C-x>', '1 x |')

    def test_should_not_apply_to_numbers_on_next_line(self):
        self.eq('|\n1', '<C-x>', '|\n1')

    def test_should_not_apply_to_numbers_on_previous_line(self):
        self.eq('1\n|', '<C-x>', '1\n|')
