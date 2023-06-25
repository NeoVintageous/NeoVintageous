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

from NeoVintageous.nv.feed_key import FeedKeyHandler


class TestFeedKeyHandler(unittest.ViewTestCase):

    def test_can_instantiate(self):
        self.normal('fi|zz')
        handler = FeedKeyHandler(self.view, 'w', None, True, True)
        self.assertIsInstance(handler, FeedKeyHandler)
        self.assertEqual(self.view, handler.view)
        self.assertEqual(self.view.window(), handler.window)
        self.assertEqual('w', handler.key)
        self.assertEqual(None, handler.repeat_count)
        self.assertEqual(True, handler.do_eval)
        self.assertEqual(True, handler.check_user_mappings)
        self.assertEqual(unittest.NORMAL, handler.mode)
