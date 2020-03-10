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


class Test_left_brace(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'n_{', '|')
        self.eq('fi|zz', 'n_{', '|fizz')
        self.eq('1\n2\n\n3\n\n\n4\n|5', 'n_{', '1\n2\n\n3\n\n|\n4\n5')
        self.eq('1\n2\n\n3\n\n|\n4\n5', 'n_{', '1\n2\n|\n3\n\n\n4\n5')
        self.eq('1\n2\n|\n3\n\n\n4\n5', 'n_{', '|1\n2\n\n3\n\n\n4\n5')
        self.eq('\n\n\n|\nx\n', 'n_{', '|\n\n\n\nx\n')

    def test_v(self):
        self.eq('fiz|z b|uzz', 'v_{', 'r_|fizz| buzz')
        self.eq('r_fiz|z b|uzz', 'v_{', 'r_|fizz b|uzz')
        self.eq('r_1\n2\n\n3\n\n\n|4\n5|', 'v_{', 'r_1\n2\n\n3\n\n|\n4\n5|')
        self.eq('r_1\n2\n\n3\n\n|\n4\n5|', 'v_{', 'r_1\n2\n|\n3\n\n\n4\n5|')
        self.eq('1\n2\n\n3\n\nfi|zz\n4\n5|', 'v_{', 'r_1\n2\n\n3\n|\nfiz|z\n4\n5')
        self.eq('|fizz\n\n\nbuzz|', 'v_{', '|fizz\n\n\n|buzz')
        self.eq('|fizz|', 'v_{', '|f|izz')
        self.eq('|f|izz', 'v_{', '|f|izz')
        self.eq('|a|', 'v_{', '|a|')
        self.eq('r_|a|', 'v_{', 'r_|a|')
        self.eq('|1\n2\n\n3\n4\n\n|5\n', 'v_{', '|1\n2\n\n|3\n4\n\n5\n')

    def test_V(self):
        self.eq('|1\n2\n\n3\n\n\n\n4\n5|', 'V_{', '|1\n2\n\n3\n\n\n\n|4\n5')
        self.eq('3\n\n\n\n4\n|fizz\n5|', 'V_{', 'r_3\n\n\n|\n4\nfizz\n|5')
        self.eq('r_1\n2\n\n3\n\n\n\n4\n|5|', 'V_{', 'r_1\n2\n\n3\n\n\n|\n4\n5|')
        self.eq('r_1\n2\n\n3\n\n|\n\n4\n5|', 'V_{', 'r_1\n2\n|\n3\n\n\n\n4\n5|')
        self.eq('|fizz\n|', 'V_{', 'r_|fizz\n|')
        self.eq('|fizz|', 'V_{', 'r_|fizz|')
        self.eq('|x\n|', 'V_{', 'r_|x\n|')
        self.eq('|x|', 'V_{', 'r_|x|')

    def test_d(self):
        self.eq('fizz\n\n\n\nb|uzz', 'd{', 'fizz\n\n\n|uzz')
        self.eq('fizz\n\n\n|uzz', 'd{', 'fizz\n\n|uzz')
        self.eq('fizz\n\n|uzz', 'd{', 'fizz\n|uzz')
        self.eq('x\n\n\nfizz\nbuzz\nf|izz\nbuzz', 'd{', 'x\n\n|izz\nbuzz')
