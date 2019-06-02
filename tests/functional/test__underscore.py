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


class Test_underscore(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('| 123\n 678', 'n_2_', ' 123\n |678')
        self.eq(' 1|23\n 678', 'n_2_', ' 123\n |678')
        self.eq('| 123\n 678', 'n_2_', ' 123\n |678')
        self.eq('  2|a4', 'n__', '  |2a4')
        self.eq(' | 234', 'n_2_', '  |234')

    def test_v(self):
        self.eq('| 12|3\n 678', 'v_2_', '| 123\n 6|78')
        self.eq('r_| 12|3\n 678', 'v_2_', ' 1|23\n 6|78')
        self.eq('| 12|3\n 678', 'v_2_', '| 123\n 6|78')
        self.eq('r_  2|ba|5', 'v__', 'r_  |2ba|5')
        self.eq('  2|ab|5', 'v__', 'r_  |2a|b5')
        self.eq('r_|  |2345', 'v__', ' | 2|345')
        self.eq('|  |2345', 'v__', '|  2|345')
        self.eq(' | 23b|5', 'v__', ' | 2|3b5')
        self.eq('r_ | 23a|5', 'v__', 'r_  |23a|5')
        self.eq('| 123\n| 678', 'v__', '| 1|23\n 678')
        self.eq('r_ 123|\n 67|8', 'v__', 'r_ |123\n 67|8')
        self.eq(' 1|23\n 67|8', 'v__', ' 1|23\n 6|78')
        self.eq('r_ 1|23\n 67|8', 'v__', 'r_ |123\n 67|8')
        self.eq('|f|', 'v__', '|f|')
        self.eq('r_|r|', 'v__', 'r_|r|')
        self.eq('r_|fiz|z\n  buzz\n', 'v_2_', 'fi|zz\n  b|uzz\n')

    def test_V(self):
        self.eq('fizz1\n|fizz2\n|fizz3\nfizz4\n', 'V_2_', 'fizz1\n|fizz2\nfizz3\n|fizz4\n')
        self.eq('fizz1\n|fizz2\n|fizz3\nfizz4\n5', 'V_3_', 'fizz1\n|fizz2\nfizz3\nfizz4\n|5')
        self.eq('r_|fizz1\nfizz2\n|fizz3\nfizz4\n5', 'V_2_', 'r_fizz1\n|fizz2\n|fizz3\nfizz4\n5')
        self.eq('r_|fizz1\nfizz2\n|fizz3\nfizz4\n5', 'V_3_', 'fizz1\n|fizz2\nfizz3\n|fizz4\n5')
        self.eq('r_|fizz1\nfizz2\n|fizz3\nfizz4\n5', 'V_4_', 'fizz1\n|fizz2\nfizz3\nfizz4\n|5')
        self.eq('r_|fizz1\nfizz2\n|fizz3\nfizz4\n5x', 'V_6_', 'fizz1\n|fizz2\nfizz3\nfizz4\n5x|')
        self.eq('r_|fizz1\nfizz2\n|fizz3\nfizz4\n5x', 'V_9_', 'fizz1\n|fizz2\nfizz3\nfizz4\n5x|')

    def test_b(self):
        self.eq('  fiz|zbu|zz\n  fiz|zbu|zz\n', 'b__', 'r_  |fizz|buzz\n  |fizz|buzz\n')
        self.eq(' | |  fizzbuzz\n | |  fizzbuzz\n', 'b__', ' |   f|izzbuzz\n |   f|izzbuzz\n')
        self.eq('fizzb|uzz|\n  fiz|zbu|zz\n', 'b__', 'r_fi|zzbu|zz\n  |fizz|buzz\n')

    def test_c(self):
        self.eq('  fi|zz', 'c_', 'i_|')
        self.eq('1\n  fi|zz\n3', 'c_', 'i_1\n|\n3')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', 'c_', 'i_  1\n|\n  fizz3\n  fizz4\n  fizz5\n')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', '1c_', 'i_  1\n|\n  fizz3\n  fizz4\n  fizz5\n')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', '2c_', 'i_  1\n|\n  fizz4\n  fizz5\n')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', '3c_', 'i_  1\n|\n  fizz5\n')

    def test_d(self):
        self.eq('| 12\n 56', 'd_', ' |56')
        self.eq(' 1|2\n 56', 'd_', ' |56')
        self.eq(' 12\n 5|6', 'd_', ' 12\n|')
        self.eq(' 1|23\n 678\n bcd', '2d_', ' |bcd')
        self.eq(' 123\n 6|78\n bcd', '3d_', ' 123\n|')
        self.eq('123\n4|56\n789', 'd_', '123\n|789')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', 'd_', '  1\n  |fizz3\n  fizz4\n  fizz5\n')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', '1d_', '  1\n  |fizz3\n  fizz4\n  fizz5\n')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', '2d_', '  1\n  |fizz4\n  fizz5\n')
        self.eq('  1\n  fi|zz2\n  fizz3\n  fizz4\n  fizz5\n', '3d_', '  1\n  |fizz5\n')
