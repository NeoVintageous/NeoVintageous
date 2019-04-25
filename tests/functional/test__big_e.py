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


class Test_E(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('0|1. 4', 'n_E', '01|. 4')
        self.eq('fi|zz(buzz) xy', 'n_E', 'fizz(buzz|) xy')

    def test_v(self):
        self.eq('0|ab|3 5', 'v_E', '0|ab3| 5')
        self.eq('r_0|b2 a|5', 'v_E', 'r_0b|2 a|5')
        self.eq('r_0|ba|3 5', 'v_E', '0b|a3| 5')
        self.eq('r_fiz|z buzz fizz|', 'v_E', 'r_fizz buz|z fizz|')
        self.eq('r_fi|zz buzz fizz|', 'v_E', 'r_fiz|z buzz fizz|')

    def test_b(self):
        self.eq('|fi|zz buzz\n|fi|zz buzz', 'b_E', '|fizz| buzz\n|fizz| buzz')
        self.eq('r_f|izz bu|zz\nf|izz bu|zz', 'b_E', 'r_fiz|z bu|zz\nfiz|z bu|zz')
        self.eq('r_|fi|zz buzz\n|fi|zz buzz', 'b_E', 'f|izz| buzz\nf|izz| buzz')
        self.eq('f|i|zz buzz\nf|i|zz buzz\n', 'b_E', 'f|izz| buzz\nf|izz| buzz\n')
        self.eq('f|i|zzbuzz\nf|i|zz buzz\n', 'b_E', 'f|izz|buzz\nf|izz| buzz\n')

    def test_d(self):
        self.eq('fi|zz buzz', 'dE', 'fi| buzz')
        self.eq('f|izz buzz', 'dE', 'f| buzz')
        self.eq('f|izz        buzz', 'dE', 'f|        buzz')
