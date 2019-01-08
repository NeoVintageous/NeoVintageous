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


class Test_ctrl_a(unittest.FunctionalTestCase):

    def test_basic_addition(self):
        self.eq('-10|00', '<C-a>', '-99|9')
        self.eq('-1|00', '<C-a>', '-9|9')
        self.eq('-|10', '<C-a>', '-|9')
        self.eq('|-2', '<C-a>', '-|1')
        self.eq('-|1', '<C-a>', '|0')
        self.eq('|0', '<C-a>', '|1')
        self.eq('|1', '<C-a>', '|2')
        self.eq('|9', '<C-a>', '1|0')
        self.eq('9|9', '<C-a>', '10|0')
        self.eq('99|9', '<C-a>', '100|0')

    def test_dirty_tests(self):
        self.eq('|', '<C-a>', '|')
        self.eq(' | ', '<C-a>', ' | ')
        self.eq('a|b', '<C-a>', 'a|b')

    def test_should_work_between_strings(self):
        self.eq('x|41y', '<C-a>', 'x4|2y')
        self.eq('x4|1y', '<C-a>', 'x4|2y')
        self.eq('x|-1000y', '<C-a>', 'x-99|9y')

    def test_should_work_between_lines(self):
        self.eq('9\n|123\n8', '<C-a>', '9\n12|4\n8')
        self.eq('9\n|123\n8\n', '<C-a>', '9\n12|4\n8\n')

    def test_should_work_at_eof(self):
        self.eq('9\n|123', '<C-a>', '9\n12|4')

    def test_should_work_at_eof_indented(self):
        self.eq('9\n    |123', '<C-a>', '9\n    12|4')

    def test_should_work_at_bof(self):
        self.eq('|123\n9', '<C-a>', '12|4\n9')

    def test_should_work_at_bof_indented(self):
        self.eq('    |123\n9', '<C-a>', '    12|4\n9')

    def test_should_work_with_cursor_on_the_number(self):
        self.eq('|999', '<C-a>', '100|0')
        self.eq('9|99', '<C-a>', '100|0')
        self.eq('99|9', '<C-a>', '100|0')

    def test_should_work_when_cursor_is_before_the_number(self):
        self.eq('| 999', '<C-a>', ' 100|0')
        self.eq('|    999', '<C-a>', '    100|0')
        self.eq('| x y z 999', '<C-a>', ' x y z 100|0')
        self.eq('9\n |   123', '<C-a>', '9\n    12|4')

    def test_should_not_work_when_cursor_is_after_number(self):
        self.eq('1|', '<C-a>', '1|')
        self.eq('1    |', '<C-a>', '1    |')
        self.eq('1 x |', '<C-a>', '1 x |')

    def test_should_not_apply_to_numbers_on_next_line(self):
        self.eq('|\n1', '<C-a>', '|\n1')

    def test_should_not_apply_to_numbers_on_previous_line(self):
        self.eq('1\n|', '<C-a>', '1\n|')
