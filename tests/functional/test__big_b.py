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


class Test_B(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('fizz b.^%4u|zz', 'n_B', 'fizz |b.^%4uzz')
        self.eq('ab|c', 'n_B', '|abc')
        self.eq('abc a|bc', 'n_B', 'abc |abc')
        self.eq('abc |a', 'n_B', '|abc a')
        self.eq('abc |abc', 'n_B', '|abc abc')

    def test_v(self):
        self.eq('fizz b.^%|4uz|z', 'v_B', 'r_fizz |b.^%4|uzz')
        self.eq('r_fizz b.^%|4u|zz', 'v_B', 'r_fizz |b.^%4u|zz')
        self.eq('r_ab|c', 'v_B', 'r_|abc|')
        self.eq('abc |abc', 'v_B', 'r_|abc a|bc')
        self.eq('abc |a|', 'v_B', 'r_|abc a|')
        self.eq('abc |abc|', 'v_B', 'abc |a|bc')
        self.eq('|abc abc|', 'v_B', '|abc a|bc')

    def test_b(self):
        self.eq('fi|zz buz|z\nfi|zz buz|z\n', 'b_B', 'fi|zz b|uzz\nfi|zz b|uzz\n')

    def test_d(self):
        self.eq('fi|zz', 'dB', '|zz')
        self.eq('fizz bu|zz', 'dB', 'fizz |zz')
        self.eq('fizz bu.,!;|zz', 'dB', 'fizz |zz')
