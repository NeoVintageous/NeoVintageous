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

    def test_G(self):
        self.eq('|1\n2\n3\n4\n', 'G', 'N_|1\n2\n3\n4\n|')

    def test_n_G(self):
        self.eq('|1\n2\n3\n4\n', 'n_G', '1\n2\n3\n4\n|')
        self.eq('1\n2\n|3\n4\n', 'n_G', '1\n2\n3\n4\n|')
        self.eq('1\n2\n3\n4\n|', 'n_G', '1\n2\n3\n4\n|')

    def test_n_G_moves_to_last_character(self):
        self.eq('|1\n2\n3', 'n_G', '1\n2\n|3')

    def test_v_G(self):
        self.eq('1\nab|cd\n3\n456\n', 'v_G', '1\nab|cd\n3\n456\n|')

    def test_V_G(self):
        self.eq('1\n|two\n|three\n4\nfive\n', 'l_G', '1\n|two\nthree\n4\nfive\n|')
