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

from NeoVintageous.nv.process_notation import ProcessNotationHandler


class TestProcessNotationHandler(unittest.ViewTestCase):

    def test_can_instantiate(self):
        self.normal('fi|zz')
        handler = ProcessNotationHandler(self.view, 'w', 0, True)
        self.assertIsInstance(handler, ProcessNotationHandler)
        self.assertEqual(self.view, handler.view)
        self.assertEqual(self.view.window(), handler.window)
        self.assertEqual('w', handler.keys)
        self.assertEqual(0, handler.repeat_count)
        self.assertEqual(True, handler.check_user_mappings)

    def test_can_process_escape_key(self):
        self.insert('f|izz')
        ProcessNotationHandler(self.view, '<Esc>l', 0, False).handle()
        self.assertNormal('fi|zz')

    def test_can_process_escape_key_and_insert(self):
        self.insert('f|izz')
        ProcessNotationHandler(self.view, '<Esc>li', 0, False).handle()
        self.assertInsert('fi|zz')
