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


class Test_ex_nnoremap(unittest.FunctionalTestCase):

    @unittest.mock_mappings()
    @unittest.mock_status_message()
    def test_nnoremap(self):
        self.feed(':nnoremap x y')

        self.assertMapping(unittest.NORMAL, 'x', 'y')
        self.assertNotMapping('x', unittest.INSERT)
        self.assertNotMapping('x', unittest.OPERATOR_PENDING)
        self.assertNotMapping('x', unittest.SELECT)
        self.assertNotMapping('x', unittest.VISUAL)
        self.assertNotMapping('x', unittest.VISUAL_BLOCK)
        self.assertNotMapping('x', unittest.VISUAL_LINE)

        self.assertNoStatusMessage()
