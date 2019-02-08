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


class Test_t(unittest.FunctionalTestCase):

    def test_n_t(self):
        self.eq('|12x34', 'n_tx', '1|2x34')
        self.eq('|12\\34', 'n_t\\', '1|2\\34')

    def test_n_t_bar(self):
        self.write('12|34')
        self.select(0)
        self.feed('n_t|')
        self.assertContent('12|34')
        self.assertSelection(1)
