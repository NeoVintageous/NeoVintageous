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
        # Note: A wrap width of 6 means a buffer like:
        #
        #   1234567...
        #
        # will visually look like two lines, where every
        # 6th character is on a new visual line:
        #
        #   12345
        #   67...
        #
        self.set_wrap(6)

    def test_gj(self):
        self.eq('1|23\n4x6\n', 'n_gj', '123\n4|x6\n')
        self.eq('1|23456x89\n', 'n_gj', '123456|x89\n')

    def test_N_gj(self):
        self.eq('1|23\n4x6\n', 'gj', '123\n4|x6\n')
        self.eq('1|23456x89\n', 'gj', '123456|x89\n')

    def test_v_gj(self):
        self.eq('1|23\n456\n', 'v_gj', '1|23\n45|6\n')
        self.eq('1|23|4\n5678\n', 'v_gj', '1|234\n567|8\n')
        self.eq('|12|34\n5678\n', 'v_gj', '|1234\n56|78\n')
        self.eq('1|234567890', 'v_gj', '1|234567|890')
        self.eq('1|23|4567890', 'v_gj', '1|2345678|90')

    def test_V(self):
        self.eq('|123\n|456\nx\n', 'V_gj', '|123\n456\n|x\n')
        self.eq('x\n|123456\n|123456\ny', 'V_gj', 'x\n|123456\n123456\n|y')
