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


class Test_W(unittest.FunctionalTestCase):

    def test_W(self):
        self.eq('one |two. three', 'n_W', 'one two. |three')
        self.eq('|one, t.- three', 'n_2W', 'one, t.- |three')
        self.eq('|on.e t.wo', 'n_2W', 'on.e t.w|o')

    def test_v_w(self):
        self.eq('one |t=- three', 'v_W', 'one |t=- t|hree')
        self.eq('|one_ two$ three', 'v_2W', '|one_ two$ t|hree')
        self.eqr('r_|on|e_ two$ three', 'v_3W', '|on|e_ two$ three')
