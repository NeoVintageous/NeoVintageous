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

from NeoVintageous.nv.vi.settings import SettingsManager
from NeoVintageous.nv.vi.settings import _VintageSettings


class TestVintageSettings(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.setts = _VintageSettings(view=self.view)

    def test_can_initialize_class(self):
        self.assertEqual(self.setts.view, self.view)
        self.assertEqual(self.view.settings().get('vintage'), {})

    def test_can_set_setting(self):
        self.assertEqual(self.setts['foo'], None)

        self.setts['foo'] = 100
        self.assertEqual(self.view.settings().get('vintage')['foo'], 100)

    def test_can_get_setting(self):
        self.setts['foo'] = 100
        self.assertEqual(self.setts['foo'], 100)

    def test_can_get_nonexisting_key(self):
        self.assertEqual(self.setts['foo'], None)


class TestSettingsManager(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.manager = SettingsManager(self.view)

    def test_can_access_vi_ssettings(self):
        self.manager.vi['foo'] = 100
        self.assertEqual(self.manager.vi['foo'], 100)
