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


class Test_gF(unittest.FunctionalTestCase):

    def assertOpened(self, opener, file: str, row: int, col: int) -> None:
        opener.assert_called_with(self.view.window(), file, row, col)
        # Reset to avoid false-positives in subsequent calls.
        opener.reset_mock()

    @unittest.mock_bell()
    @unittest.mock.patch.dict(unittest.os.environ, {"HOME": "/home"})
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_gF(self, opener):
        # (before, after, expected file name)
        tests = [
            ('|parans.txt', '|parans.txt', 'parans.txt', None, None),
            ('|parans.txt(1).', '|parans.txt(1).', 'parans.txt', 1, None),
            ('|row.txt(42)', '|row.txt(42)', 'row.txt', 42, None),
            ('|row.txt:42', '|row.txt:42', 'row.txt', 42, None),
            ('|row.txt@42', '|row.txt@42', 'row.txt', 42, None),
            ('|rowcol.txt:4:2', '|rowcol.txt:4:2', 'rowcol.txt', 4, 2),
        ]

        for test in tests:
            self.eq(test[0], 'n_gF', test[1])
            self.assertOpened(opener, test[2], test[3], test[4])
        self.assertNoBell()

    @unittest.mock_bell()
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_gF_no_file_name_under_cursor(self, opener):
        self.eq('|', 'n_gF', '|')
        self.eq('$|$$', 'n_gF', '$|$$')
        self.assertMockNotCalled(opener)
        self.assertBell('E446: No file name under cursor', count=2)

    @unittest.mock_session()
    @unittest.mock_bell()
    @unittest.mock.patch('sublime.Window.open_file')
    def test_gF_found(self, opener):
        fixture = self.fixturePath('fizz.txt') + ':3'
        self.feed(':cd ' + self.rootPath())
        if unittest.is_windows():
            self.eq('|tests\\fixtures\\fizz.txt:3', 'n_gF', '|tests\\fixtures\\fizz.txt:3')
        else:
            self.eq('|tests/fixtures/fizz.txt:3', 'n_gF', '|tests/fixtures/fizz.txt:3')
        opener.assert_called_with(fixture, 1)
        self.assertNoBell()
