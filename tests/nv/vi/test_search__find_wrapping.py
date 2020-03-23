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

from NeoVintageous.nv.vi.search import find_wrapping


class Test_find_wrapping(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_can_wrap_around_buffer(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(15)
        self.assertEqual(self.Region(0, 3), find_wrapping(self.view, 'xxx', 15, self.view.size()))

    def test_fails_if_search_not_present(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(15)
        self.assertEqual(None, find_wrapping(self.view, 'yyy', 15, self.view.size()))

    def test_can_find_next_occurrence(self):
        self.write('xxx\naaa aaa xxx aaa')
        self.select(4)
        self.assertEqual(self.Region(12, 15), find_wrapping(self.view, 'xxx', 4, self.view.size()))
