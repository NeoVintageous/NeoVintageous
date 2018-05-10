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


class Test_b(unittest.FunctionalTestCase):

    def test_b(self):
        self.fixture('Gui|de to the Galaxy')

        self.feed('b')
        self.expects('|Guide to the Galaxy')

        self.select(5)
        self.feed('b')
        self.expects('|Guide to the Galaxy')

        self.select(7)
        self.feed('b')
        self.expects('Guide |to the Galaxy')

        self.select(11)
        self.feed('b')
        self.expects('Guide to |the Galaxy')

        self.select(13)
        self.feed('b')
        self.expects('Guide to |the Galaxy')

        self.select(17)
        self.feed('b')
        self.expects('Guide to the |Galaxy')

    def test_v_b(self):
        self.vFixture('Gui|de| to the Galaxy')

        self.feed('v_b')
        self.expectsV('|Guid|e to the Galaxy')

        self.select((5, 7))
        self.feed('v_b')
        self.expectsV('|Guide |to the Galaxy')

        self.select((7, 11))
        self.feed('v_b')
        self.expectsV('Guide t|o t|he Galaxy')

        self.select((7, 13))
        self.feed('v_b')
        self.expectsV('Guide t|o t|he Galaxy')

        self.select((7, 17))
        self.feed('v_b')
        self.expectsV('Guide t|o the G|alaxy')
