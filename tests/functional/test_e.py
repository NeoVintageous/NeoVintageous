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


class Test_e(unittest.FunctionalTestCase):

    def test_e(self):
        self.eq('one |two three', 'e', 'one tw|o three')
        self.eq('one |two three', '2e', 'one two thre|e')

    def test_v_e(self):
        self.eq('one |two three', 'v_e', 'one |two| three')
        self.eq('one |two three', 'v_2e', 'one |two three|')
