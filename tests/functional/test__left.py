# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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


class Test_left(unittest.FunctionalTestCase):

    def test_i(self):
        self.eq('ab|c', 'i_<left>', 'i_a|bc')
        self.eq('x\na|bc', 'i_<left>', 'i_x\n|abc')
        self.eq('x\n|abc', 'i_<left>', 'i_x\n|abc')
        self.eq('\n\n|\n\n', 'i_<left>', 'i_\n\n|\n\n')
