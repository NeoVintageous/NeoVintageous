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


class Test_bar(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('12|3', 'n_|', '|123')
        self.eq('123x', 'n_3|', '12|3x')
        self.eq('fi|zz', 'n_|', '|fizz')
        self.eq('fi|zz', 'n_1|', '|fizz')
        self.eq('|fizz', 'n_2|', 'f|izz')
        self.eq('|fizz', 'n_3|', 'fi|zz')
        self.eq('|fizz', 'n_4|', 'fiz|z')
        self.eq('|fizz', 'n_9|', 'fiz|z')
        self.eq('|fizz\nbuzz', 'n_4|', 'fiz|z\nbuzz')
        self.eq('|fizz\nbuzz', 'n_5|', 'fiz|z\nbuzz')
        self.eq('|fizz\nbuzz', 'n_6|', 'fiz|z\nbuzz')
        self.eq('|fizz\nbuzz', 'n_9|', 'fiz|z\nbuzz')
        self.eq('x\n|123\nx', 'n_7|', 'x\n12|3\nx')
        self.eq('fizz\n|buzz', 'n_|', 'fizz\n|buzz')
        self.eq('\n\n|\n\n', 'n_|', '\n\n|\n\n')

    def test_v(self):
        self.eq('fi|zz buzz', 'v_7|', 'fi|zz bu|zz')
        self.eq('r_f|izz| buzz', 'v_7|', 'fiz|z bu|zz')
        self.eq('fizz b|uz|z', 'v_2|', 'r_f|izz bu|zz')
        self.eq('r_fizz b|uz|z', 'v_2|', 'r_f|izz buz|z')
        self.eq('r_fizz\n|buzz|', 'v_|', 'r_fizz\n|buzz|')
        self.eq('x\n|fizz\n|buzz', 'v_|', 'x\n|f|izz\nbuzz')
        self.eq('r_x\n|fizz\n|buzz', 'v_|', 'r_x\n|fizz\n|buzz')

    def test_d(self):
        self.eq('fi|zz buzz', '7d|', 'fiz|uzz')
        self.eq('fi|zz| buzz', '8d|', 'fiz|zz')
        self.eq('r_fi|zz| buzz', '8d|', 'fiz|zz')
