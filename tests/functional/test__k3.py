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


class Test_k3(unittest.FunctionalTestCase):

    def test_n(self):
        self.normal('fiz|z buzz')
        self.feed('<k3>')
        self.feed('l')
        self.assertNormal('fizz b|uzz')

    @unittest.mock_mappings((unittest.NORMAL, '<k3>', 'w'))
    def test_can_map_numpad(self):
        self.normal('|fizz buzz')
        self.feedWithUserMappings('<k3>')
        self.assertNormal('fizz |buzz')
