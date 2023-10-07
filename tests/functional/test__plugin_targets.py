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


class TestTargets(unittest.FunctionalTestCase):

    def test_viB(self):
        for t in ('{', '}', 'B'):
            self.eq('f|izz{\nbuzz\n}xx', 'v_i' + t, 'v_fizz{\n|buzz\n|}xx')
            self.eq('f|izz({\nbuzz\n})xx', 'v_i' + t, 'v_fizz({\n|buzz\n|})xx')

    def test_vaB(self):
        for t in ('{', '}', 'B'):
            self.eq('f|izz{\nbuzz\n}xx', 'v_a' + t, 'v_fizz|{\nbuzz\n}|xx')
            self.eq('f|izz({\nbuzz\n})xx', 'v_a' + t, 'v_fizz(|{\nbuzz\n}|)xx')

    def test_vib(self):
        for t in ('(', ')', 'b'):
            self.eq('fi|zz (   ) buzz', 'v_i' + t, 'fizz (|   |) buzz')
            self.eq('fi|zz\n(\n\n\n\n)\nbuzz', 'v_i' + t, 'fizz\n(\n|\n\n\n|)\nbuzz')

    def test_vab(self):
        for t in ('(', ')', 'b'):
            self.eq('fi|zz (   ) buzz', 'v_a' + t, 'fizz |(   )| buzz')
            self.eq('fi|zz\n(\n\n\n\n)\nbuzz', 'v_a' + t, 'fizz\n|(\n\n\n\n)|\nbuzz')
