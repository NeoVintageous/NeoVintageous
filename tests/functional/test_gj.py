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


class Test_gj(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('word_wrap', True)
        self.settings().set('wrap_width', 4)

    def test_gj(self):
        self.eq('1|23\n456\n', 'gj', '123\n4|56\n')
        self.eq('1|23456\nx\n', 'gj', '1234|56\nx\n')

    def test_v_gj(self):
        self.eq('1|2|3\n456\n', 'v_gj', '1|23\n456|\n')

    def test_l_gj(self):
        self.eq('|123\n|456\nx\n', 'l_gj', '|123\n456\n|x\n')
        self.eq('x\n|123456\n|123456\ny', 'l_gj', 'x\n|123456\n123456\n|y')
