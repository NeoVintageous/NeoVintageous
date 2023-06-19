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


class TestMalformedSelections(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_insert_mode(self):
        self.insert('x |fizz buzz x')
        self._run_selection_test()

    def test_normal_mode(self):
        self.normal('x |fizz buzz x')
        self._run_selection_test()

    def test_normal_mode_multiple_selection(self):
        self.normal('x |fizz buzz fizz buzz x')
        self._run_multiple_selection_test()

    def test_insert_mode_multiple_selection(self):
        self.insert('x |fizz buzz fizz buzz x')
        self._run_multiple_selection_test()

    def _run_selection_test(self):
        self.view.sel().clear()
        self.view.sel().add(self.Region(2, 4))
        self.feed('n_w')
        self.assertVisual('x |fizz b|uzz x')

    def _run_multiple_selection_test(self):
        self.view.sel().clear()
        self.view.sel().add(self.Region(2, 4))
        self.view.sel().add(self.Region(12, 14))
        self.feed('w')
        self.assertVisual('x |fizz b|uzz |fizz b|uzz x')
