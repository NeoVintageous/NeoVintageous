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
# along with NeoVintageous.  If not, see <https://www.gnu.org/licensesubstitute/>.

from NeoVintageous.tests import unittest


class Test_ex_delmarks(unittest.ResetMarks, unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_can_delmarks(self):
        self.normal('fi|zz')
        self.feed('m')
        self.feed('a')
        self.assertHasMarks('a')
        self.feed(':marks')
        self.assertMarksOutput(' a      1    2       fizz')
        self.feed(':delmarks!')
        self.assertNoMark('a')
        self.feed(':marks')
        self.assertNoMarksOutput()

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_only_delete_current_buffer_marks(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        self.feed('m')
        self.feed('a')
        self.feed('m')
        self.feed('b')
        self.feed('m')
        self.feed('A')
        self.assertHasMarks('Aab')
        self.feed(':delmarks!')
        self.assertHasMarks('A')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_can_delete_mark(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        self.feed('m')
        self.feed('a')
        self.feed('m')
        self.feed('b')
        self.feed('m')
        self.feed('B')
        self.assertHasMarks('Bab')
        self.feed(':delmarks b')
        self.assertHasMarks('Ba')
        self.feed(':delmarks B')
        self.assertHasMarks('a')
        self.feed(':delmarks a')
        self.assertNoMarks()

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_can_delete_range_lowercase(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        for mark in 'abcdefgh':
            self.feed('m')
            self.feed(mark)
        self.feed('m')
        self.feed('C')
        self.assertHasMarks('Cabcdefgh')
        self.feed(':delmarks c-f')
        self.assertHasMarks('Cabgh')
        self.feed(':delmarks a-g')
        self.assertHasMarks('Ch')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_can_delete_range_uppercase_when_only_some_defined(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        for mark in 'ABDGH':
            self.feed('m')
            self.feed(mark)
        self.assertHasMarks('ABDGH')
        self.feed(':delmarks B-G')
        self.assertHasMarks('AH')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_can_delete_range_uppercase(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        for mark in 'ABCDEFGH':
            self.feed('m')
            self.feed(mark)
        self.feed('m')
        self.feed('c')
        self.assertHasMarks('ABCDEFGHc')
        self.feed(':delmarks B-D')
        self.assertHasMarks('AEFGHc')
        self.feed(':delmarks EG-HcF')
        self.assertHasMarks('A')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_can_delete_ranges_and_regular_marks(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        for mark in 'ABCDEFGH':
            self.feed('m')
            self.feed(mark)
        for mark in 'abcdefgh':
            self.feed('m')
            self.feed(mark)
        self.assertHasMarks('ABCDEFGHabcdefgh')
        self.feed(':delmarks BeDgF-Hb-dA')
        self.assertHasMarks('CEafh')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_allow_spaces(self, fn, opener):
        fn.return_value = '/tmp/fizz.txt'
        opener.return_value = self.view
        self.normal('fi|zz')
        for mark in 'ABCDEFGH':
            self.feed('m')
            self.feed(mark)
        for mark in 'abcdefgh':
            self.feed('m')
            self.feed(mark)
        self.assertHasMarks('ABCDEFGHabcdefgh')
        self.feed(':delmarks B      eD g F-H    b-dA')
        self.assertHasMarks('CEafh')

    @unittest.mock_bell()
    def test_emit_bell_on_invalid_marks(self):
        self.normal('fi|zz')
        self.feed('m')
        self.feed('a')
        self.feed(':delmarks z-a')
        self.assertBell('E475: Invalid argument: %s', 'z-a')
        self.feed(':delmarks G-C')
        self.assertBell('E475: Invalid argument: %s', 'G-C')

    @unittest.mock_bell()
    def test_emit_bell_on_invalid_forced_delete(self):
        self.normal('fi|zz')
        self.feed('m')
        self.feed('a')
        self.feed(':delmarks! a')
        self.assertBell('E475: Invalid argument')

    @unittest.mock_bell()
    def test_emit_bell_because_requires_argument(self):
        self.normal('fi|zz')
        self.feed('m')
        self.feed('a')
        self.feed(':delmarks')
        self.assertBell('E471: Argument required')
