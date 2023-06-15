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


class Test_gn(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.syntax('Packages/Python/Python.sublime-syntax')

    def setupMocks(self, file_name, lookup_symbol_in_index) -> None:
        file_name.return_value = '/tmp/sublime/Packages/NeoVintageous/buzz.py'
        lookup_symbol_in_index.return_value = [
            (
                '/tmp/sublime/Packages/NeoVintageous/buzz.py',
                'NeoVintageous/buzz.py',
                (1, 5)
            )
        ]

    def test_n_noop_when_view_has_no_file_name(self):
        self.normal("def fizz(self):\n    pass\n\n|fizz\n\n")
        self.feed('gd')
        self.assertNormal("def fizz(self):\n    pass\n\n|fizz\n\n")

    @unittest.mock.patch('sublime.Window.lookup_symbol_in_index')
    @unittest.mock.patch('sublime.View.file_name')
    def test_n_noop_when_view_has_no_symbols(self, file_name, lookup_symbol_in_index):
        self.setupMocks(file_name, lookup_symbol_in_index)
        lookup_symbol_in_index.return_value = []
        self.normal("def fizz(self):\n    pass\n\n|fizz\n\n")
        self.feed('gd')
        self.assertNormal("def fizz(self):\n    pass\n\n|fizz\n\n")

    @unittest.mock.patch('sublime.Window.lookup_symbol_in_index')
    @unittest.mock.patch('sublime.View.file_name')
    def test_n(self, file_name, lookup_symbol_in_index):
        self.setupMocks(file_name, lookup_symbol_in_index)
        self.normal("def fizz(self):\n    pass\n\n|fizz\n\n")
        self.feed('gd')
        self.assertNormal("def |fizz(self):\n    pass\n\nfizz\n\n")

    @unittest.mock.patch('sublime.Window.lookup_symbol_in_index')
    @unittest.mock.patch('sublime.View.file_name')
    def test_v(self, file_name, lookup_symbol_in_index):
        self.setupMocks(file_name, lookup_symbol_in_index)
        self.visual("def fizz(self):\n    pass\n\n|fizz\n\n")
        self.feed('gd')
        self.assertRVisual("def |fizz(self):\n    pass\n\nf|izz\n\n")

    @unittest.mock.patch('sublime.Window.lookup_symbol_in_index')
    @unittest.mock.patch('sublime.View.file_name')
    def test_o(self, file_name, lookup_symbol_in_index):
        self.setupMocks(file_name, lookup_symbol_in_index)
        self.normal("def fizz(self):\n    pass\n\n|fizz\n\n")
        self.feed('d')
        self.feed('gd')
        self.assertNormal("def |fizz\n\n")
