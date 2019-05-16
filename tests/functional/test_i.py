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


class Test_i(unittest.FunctionalTestCase):

    def test_i(self):
        self.eq('fi|zz', 'n_i', 'i_fi|zz')
        self.assertStatusLineIsInsert()

    def test_s(self):
        self.eq('fi|zz bu|zz', 's_i', 'i_fizz b|uzz')
        self.eq('r_fi|zz bu|zz', 's_i', 'i_fi|zz buzz')
        self.assertStatusLineIsInsert()
