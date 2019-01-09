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


class Test_pipe(unittest.FunctionalTestCase):

    def test_pipe(self):
        self.eq('12|3', 'n_|', '|123')
        self.eq('123x', 'n_3|', '12|3x')
        self.eq('x\n|123\nx', 'n_7|', 'x\n12|3\nx')

    def test_v_pipe(self):
        self.eq('fi|zz buzz', 'v_7|', 'fi|zz bu|zz')
        self.eq('r_f|izz| buzz', 'v_7|', 'fiz|z bu|zz')
        self.eqr('fizz b|uz|z', 'v_2|', 'f|izz bu|zz')
        self.eqr('r_fizz b|uz|z', 'v_2|', 'f|izz buz|z')

    def test_N_pipe(self):
        self.eq('fi|zz buzz', '7|', 'N_fiz|z b|uzz')
        self.eq('fi|zz| buzz', '8|', 'N_fiz|z bu|zz')
        self.eq('r_fi|zz| buzz', '8|', 'N_fiz|z bu|zz')
