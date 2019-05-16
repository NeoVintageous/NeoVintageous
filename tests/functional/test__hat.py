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


class Test_hat(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('', 'n_^', '|')
        self.eq('012|a4', 'n_^', '|012a4')
        self.eq('  2|a4', 'n_^', '  |2a4')
        self.eq(' | 234', 'n_^', '  |234')
        self.eq('    fi|zz', 'n_^', '    |fizz')

    def test_v(self):
        self.eq('r_0|b2a|45', 'v_^', 'r_v_|0b2a|45')
        self.eq('0|a2b4|5', 'v_^', 'r_v_|0a|2b45')
        self.eq('r_  2|ba5|', 'v_^', 'r_v_  |2ba5|')
        self.eq('  2|ab5|', 'v_^', 'r_v_  |2a|b5')
        self.eq('|  |2345', 'v_^', 'v_|  2|345')
        self.eq('r_ | 23a5|', 'v_^', 'r_v_  |23a5|')
        self.eq(' | 23b5|', 'v_^', 'v_ | 2|3b5')
        self.eq('|f|', 'v_^', '|f|')
        self.eq('r_|x|', 'v_^', 'r_|x|')
        self.eq('| 123\n| 678', 'v_^', '| 1|23\n 678')
        self.eq('r_ 123|\n 67|8', 'v_^', 'r_ |123\n 67|8')
        self.eq(' 1|23\n 67|8', 'v_^', ' 1|23\n 6|78')
        self.eq('r_ 1|23\n 67|8', 'v_^', 'r_ |123\n 67|8')
        self.eq('r_|    |fizz', 'v_^', 'v_   | f|izz')
        self.eq('r_|    f|izz', 'v_^', 'r_v_    |f|izz')

    def test_b(self):
        self.eq('  fi|zz|buzz\n  fi|zz|buzz\n', 'b_^', 'r_  |fiz|zbuzz\n  |fiz|zbuzz\n')
        self.eq('|  |  fizzbuzz\n|  |  fizzbuzz\n', 'b_^', '|    f|izzbuzz\n|    f|izzbuzz\n')

    @unittest.mock_bell()
    def test_c(self):
        self.eq('    fi|zz', 'c^', 'i_    |zz')
        self.eq('  |  fizz', 'c^', 'i_  |fizz')
        self.eq('|  fizz', 'c^', 'i_|fizz')
        self.eq('  |fizz', 'c^', 'i_  |fizz')
        self.eq('\n\n|\n\n', 'c^', 'i_\n\n|\n\n')
        self.eq('|', 'c^', 'i_|')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('012|a4', 'd^', '|a4')
        self.eq('  2|a4', 'd^', '  |a4')
        self.eq('    fi|zz', 'd^', '    |zz')
        self.eq('|  234', 'd^', '|234')
        self.assertNoBell()
        self.eq('|', 'd^', '|')
        self.eq('    |fizz', 'd^', '    |fizz')
