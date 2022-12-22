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

from NeoVintageous.nv import macros


@unittest.mock_session()
class TestMacros(unittest.ViewTestCase):

    def test_is_readable(self):
        self.assertTrue(macros.is_readable('0'))
        self.assertTrue(macros.is_readable('a'))
        self.assertTrue(macros.is_readable('.'))
        self.assertTrue(macros.is_readable('='))

    def test_is_not_readable(self):
        self.assertFalse(macros.is_readable('$'))

    def test_is_writable(self):
        self.assertTrue(macros.is_writable('0'))
        self.assertTrue(macros.is_writable('a'))

    def test_is_not_writable(self):
        self.assertFalse(macros.is_writable('.'))
        self.assertFalse(macros.is_writable('='))
        self.assertFalse(macros.is_writable('$'))

    def test_record_macro(self):
        self.assertFalse(macros.is_recording())
        self.assertStatusLineIsNormal()

        macros.start_recording('a')
        self.assertTrue(macros.is_recording())
        self.assertStatusLineEqual('recording @a')

        macros.add_macro_step(self.view, 'a', {'b': 'c'})

        macros.stop_recording()
        self.assertFalse(macros.is_recording())
        self.assertStatusLineIsNormal()

        self.assertIsNone(macros.get_recorded('x'))
        self.assertEqual([('a', {'b': 'c'})], macros.get_recorded('a'))
