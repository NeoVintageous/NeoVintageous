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


class Test_G(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|1\n2\n3\n4\n', 'n_G', '1\n2\n3\n4\n|')
        self.eq('1\n2\n|3\n4\n', 'n_G', '1\n2\n3\n4\n|')
        self.eq('1\n2\n3\n4\n|', 'n_G', '1\n2\n3\n4\n|')
        self.eq('1\n2\n3\n|4\n', 'n_1G', '|1\n2\n3\n4\n')
        self.eq('1\n2\n3\n4|\n', 'n_2G', '1\n|2\n3\n4\n')
        self.eq('|1\n2\n3\n4\n', 'n_3G', '1\n2\n|3\n4\n')
        self.eq('|1\n2\n3\n4\n', 'n_4G', '1\n2\n3\n|4\n')
        self.eq('|1\n2\n3\n', 'n_8G', '1\n2\n3|\n')
        self.eq('|1\n2\n3', 'n_8G', '1\n2\n|3')
        self.eq('|1\n2\n    3\n4\n', 'n_3G', '1\n2\n    |3\n4\n')
        self.eq('|1\n2\n3', 'n_G', '1\n2\n|3')
        self.eq('|1\n2\n    foo', 'n_G', '1\n2\n    |foo')
        self.eq('|1\n2\n3', 'n_9G', '1\n2\n|3')
        self.eq('|1\n2\n3\n', 'n_9G', '1\n2\n3|\n')
        self.eq('|1\n2\n3\n\n', 'n_9G', '1\n2\n3\n|\n')
        self.eq('|', 'n_G', '|')
        self.eq('|1\n2\n    fizz', 'n_G', '1\n2\n    |fizz')

    def test_v(self):
        self.eq('1\nab|cd\n3\n456\n', 'v_G', '1\nab|cd\n3\n456\n|')
        self.eq('1\nab|cd\n3x\n4x\n5x\n6x\n', 'v_5G', '1\nab|cd\n3x\n4x\n5|x\n6x\n')
        self.eq('1\n    22\n3\n4a|bc\n5x|x\nx', 'v_2G', 'r_1\n    |22\n3\n4ab|c\n5xx\nx')
        self.eq('r_1\n    22\n3\n4a|bc\n5x|x\nx', 'v_2G', 'r_1\n    |22\n3\n4abc\n5x|x\nx')
        self.eq('r_1\n2|2\nab|cd\n4\n    5xx\nx', 'v_5G', '1\n22\na|bcd\n4\n    5|xx\nx')
        self.eq('1\nab|cd\n3x\n4x\n    5x\n6x\n', 'v_5G', '1\nab|cd\n3x\n4x\n    5|x\n6x\n')
        self.eq('fi|zz\n2\n    buzz', 'v_G', 'fi|zz\n2\n    b|uzz')
        self.eq('|1\nfizz\n    buzz', 'v_G', '|1\nfizz\n    b|uzz')

    def test_V(self):
        self.eq('1\n|two\n|three\n4\nfive\n', 'V_G', '1\n|two\nthree\n4\nfive\n|')
        self.eq('|1\n2\n|3\n4\n55\nx', 'V_5G', '|1\n2\n3\n4\n55\n|x')
        self.eq('1\n2\n3\n|4\n55\n|x', 'V_1G', 'r_|1\n2\n3\n4\n|55\nx')
        self.eq('1\n2\n3\n|4\n55\n|x', 'V_2G', 'r_1\n|2\n3\n4\n|55\nx')
        self.eq('1\n2\n3\n|4\n55\n|x', 'V_3G', 'r_1\n2\n|3\n4\n|55\nx')
        self.eq('1\n2\n3\n|4\n55\n|x', 'V_4G', '1\n2\n3\n|4\n|55\nx')
        self.eq('1\n2\n3\n|4\n55\n|x', 'V_5G', '1\n2\n3\n|4\n55\n|x')
        self.eq('r_1\n2\n3\n|4\n55\n|x', 'V_1G', 'r_|1\n2\n3\n4\n55\n|x')
        self.eq('r_1\n2\n3\n|4\n55\n|x', 'V_2G', 'r_1\n|2\n3\n4\n55\n|x')
        self.eq('r_1\n2\n3\n|4\n55\n|x', 'V_3G', 'r_1\n2\n|3\n4\n55\n|x')
        self.eq('r_1\n2\n3\n|4\n55\n|x', 'V_4G', 'r_1\n2\n3\n|4\n55\n|x')
        self.eq('r_1\n2\n3\n|4\n55\n|x', 'V_5G', 'r_1\n2\n3\n4\n|55\n|x')
        self.eq('r_1\n|2\n3\n|4\n55\nx', 'V_1G', 'r_|1\n2\n3\n|4\n55\nx')
        self.eq('r_1\n|2\n3\n|4\n55\nx', 'V_2G', 'r_1\n|2\n3\n|4\n55\nx')
        self.eq('r_1\n|2\n3\n|4\n55\nx', 'V_3G', 'r_1\n2\n|3\n|4\n55\nx')
        self.eq('r_1\n|2\n3\n|4\n55\nx', 'V_4G', '1\n2\n|3\n4\n|55\nx')
        self.eq('r_1\n|2\n3\n|4\n55\nx', 'V_5G', '1\n2\n|3\n4\n55\n|x')

    def test_d(self):
        self.eq('1\n2\n|3\n4\n', 'dG', '1\n2\n|')
        self.eq('1\n|2\n3\n4\n5\n6\n7', '5dG', '1\n|6\n7')
