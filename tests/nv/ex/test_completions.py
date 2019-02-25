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

from NeoVintageous.nv.ex.completions import _wants_fs_completions
from NeoVintageous.nv.ex.completions import _wants_setting_completions


class TestWantsCompletions(unittest.TestCase):

    def test_wants_setting_completions(self):
        self.assertFalse(_wants_setting_completions('foobar'))
        self.assertFalse(_wants_setting_completions(':set'))
        self.assertTrue(_wants_setting_completions(':se '))
        self.assertTrue(_wants_setting_completions(':set '))
        self.assertTrue(_wants_setting_completions(':set '))
        self.assertTrue(_wants_setting_completions(':set name'))
        self.assertTrue(_wants_setting_completions(':setl '))
        self.assertTrue(_wants_setting_completions(':setlocal '))
        self.assertTrue(_wants_setting_completions(':setlocal name'))

    def test_wants_fs_completions(self):
        self.assertFalse(_wants_fs_completions('foobar'))
        self.assertFalse(_wants_fs_completions(':write'))
        self.assertTrue(_wants_fs_completions(':w '))
        self.assertTrue(_wants_fs_completions(':write '))
        self.assertTrue(_wants_fs_completions(':write path'))
