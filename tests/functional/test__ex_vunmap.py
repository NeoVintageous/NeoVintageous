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


class Test_ex_vunmap(unittest.FunctionalTestCase):

    @unittest.mock_mappings()
    @unittest.mock_status_message()
    def test_no_such_mapping(self):
        self.feed(':vunmap x')
        self.assertStatusMessage('E31: No such mapping', 4)

    @unittest.mock_mappings(
        (unittest.SELECT, 'x', 'y'),
        (unittest.VISUAL, 'x', 'y'),
        (unittest.VISUAL_BLOCK, 'x', 'y'),
        (unittest.VISUAL_LINE, 'x', 'y'))
    @unittest.mock_status_message()
    def test_vunmap(self):
        self.feed(':vunmap x')
        self.assertNotMapping('x')
        self.assertNoStatusMessage()

    @unittest.mock_mappings((unittest.VISUAL, 'x', 'y'))
    @unittest.mock_status_message()
    def test_no_status_message_when_at_least_one_mode_mapping_is_found(self):
        self.feed(':vunmap x')
        self.assertNotMapping('x')
        self.assertStatusMessage('E31: No such mapping', 3)
