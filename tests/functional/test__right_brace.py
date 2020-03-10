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


class Test_right_brace(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'n_}', '|')
        self.eq('fi|zz', 'n_}', 'fiz|z')
        self.eq('|1\n2\n\n3\n\n\n4\n5', 'n_}', '1\n2\n|\n3\n\n\n4\n5')
        self.eq('1\n2\n|\n3\n\n\n4\n5', 'n_}', '1\n2\n\n3\n|\n\n4\n5')
        self.eq('1\n2\n\n3\n|\n\n4\n5', 'n_}', '1\n2\n\n3\n\n\n4\n|5')
        self.eq('fi|zz\n\n\n\n', 'n_}', 'fizz\n|\n\n\n')
        self.eq('fi|zz\n    \n\n\n', 'n_}', 'fizz\n    \n|\n\n')
        self.eq('fi|zz\n    \n  \n\n\n', 'n_}', 'fizz\n    \n  \n|\n\n')
        self.eq('1\n2\n|\n\n\n\n', 'n_}', '1\n2\n\n\n\n\n|')

    def test_v(self):
        self.eq('fi|zz', 'v_}', 'fi|zz|')
        self.eq('|1\n2\n\n3\n\n\n4\n5', 'v_}', '|1\n2\n\n|3\n\n\n4\n5')
        self.eq('|1\n2\n\n3\n\n|\n4\n5', 'v_}', '|1\n2\n\n3\n\n\n4\n5|')
        self.eq('|1\n2\n\n|3\n\n\n4\n5', 'v_}', '|1\n2\n\n3\n\n|\n4\n5')
        self.eq('r_|1\n2\n\n3\n\n\n4\n5|', 'v_}', 'r_1\n2\n|\n3\n\n\n4\n5|')
        self.eq('r_|1\nfi|zz\n\n3\n\n\n4\n5', 'v_}', '1\nf|izz\n\n|3\n\n\n4\n5')
        self.eq('fi|zz\n\n\n\n', 'v_}', 'fi|zz\n\n|\n\n')
        self.eq('fi|zz\n    \n\n\n\n\n', 'v_}', 'fi|zz\n    \n\n|\n\n\n')
        self.eq('r_fi|zz\n\n|\n\n', 'v_}', 'r_fizz\n|\n|\n\n')
        self.eq('r_fi|zz\n|\n\n\n', 'v_}', 'fizz|\n\n|\n\n')

    def test_V(self):
        self.eq('|1\n|2\n\n3\n\n\n\n4\n5', 'V_}', '|1\n2\n\n|3\n\n\n\n4\n5')
        self.eq('|1\n2\n\n|3\n\n\n\n4\n5', 'V_}', '|1\n2\n\n3\n\n|\n\n4\n5')
        self.eq('|1\n2\n\n3\n\n|\n\n4\n5', 'V_}', '|1\n2\n\n3\n\n\n\n4\n5|')
        self.eq('r_|1\n2\n\n3\n\n\n\n4\n5|', 'V_}', 'r_1\n2\n|\n3\n\n\n\n4\n5|')
        self.eq('r_1\n2\n|\n3\n\n\n\n4\n5|', 'V_}', 'r_1\n2\n\n3\n|\n\n\n4\n5|')
        self.eq('r_|1\nfizz\n|2\n\n\n\n4', 'V_}', '1\n|fizz\n2\n\n|\n\n4')
        self.eq('r_|1\nfizz\n2\n|\n\n\n4', 'V_}', '1\nfizz\n|2\n\n|\n\n4')
        self.eq('r_|1\nfizz\nbuzz\n|\n\n\n4', 'V_}', '1\nfizz\n|buzz\n\n|\n\n4')
        self.eq('|1\n|', 'V_}', '|1\n|')
        self.eq('|1\n2\n|', 'V_}', '|1\n2\n|')
        self.eq('|1\n2|', 'V_}', '|1\n2|')
        self.eq('|1|', 'V_}', 'r_|1|')

    def test_d(self):
        self.eq('1\n\na|bc\n\n3', 'd}', '1\n\n|a\n\n3')
        self.eq('1\n\na|bc\ndef\n\n3', 'd}', '1\n\n|a\n\n3')
        self.eq('1\n\nabc |def\n\n3', 'd}', '1\n\nabc| \n\n3')
        self.eq('1\n\nabc| \n\n3', 'd}', '1\n\nab|c\n\n3')
        self.eq('1\n\nab|c\n\n3', 'd}', '1\n\na|b\n\n3')
        self.eq('1\n\na|b\n\n3', 'd}', '1\n\n|a\n\n3')
        self.eq('1\n\n|a\n\n3', 'd}', '1\n\n|\n3')
        self.eq('1\n\n|\n3\n\n4', 'd}', '1\n\n|\n4')
        self.eq('1\n2\n\nfizz\n|one\ntwo', 'd}', '1\n2\n\nfizz\n|')
