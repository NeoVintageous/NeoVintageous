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


class Test_gu(unittest.FunctionalTestCase):

    def test_guis(self):
        self.eq('FOO. FIZ|Z BUZZ. BAR.', 'guis', 'FOO. |fizz buzz. BAR.')

    def test_gub(self):
        self.eq('|FIZZ', 'gub', '|FIZZ')

    def test_v_gu(self):
        self.eq('FI|ZZ BU|ZZ', 'v_gu', 'n_FI|zz buZZ')
