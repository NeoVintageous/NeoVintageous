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


class Test_d(unittest.FunctionalTestCase):

    def test_de(self):
        self.eq('one |two three', 'de', 'one | three')
        self.eq('one t|wo three', 'de', 'one t| three')

    def test_df(self):
        self.eq('one |two three', 'dft', 'one |hree')
        self.eq('one |two three three', 'd2ft', 'one |hree')
        self.eq('|a = 1', 'df=', '| 1')

    def test_dw(self):
        self.eq('one |two three', 'dw', 'one |three')
        self.eq('one t|wo three', 'dw', 'one t|three')

    def test_d__dollar(self):
        self.eq('one |two three', 'd$', 'one| ')
        self.eq('one t|wo three', 'd$', 'one |t')
