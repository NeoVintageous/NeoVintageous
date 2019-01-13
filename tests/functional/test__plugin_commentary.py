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


class TestCommentary(unittest.FunctionalTestCase):

    def normal(self, text):
        # Test against a specific syntax, because views that
        # have no syntax applied have no comment behaviours.
        self.view.assign_syntax('Packages/Python/Python.sublime-syntax')
        super().normal(text)

    def test_gcc_comment(self):
        self.eq('|abc', 'gcc', '|# abc')
        self.eq('abc|', 'gcc', '|# abc')

    def test_gcc_uncomment(self):
        self.eq('|# abc', 'gcc', '|abc')
        self.eq('# abc|', 'gcc', '|abc')

    def test_gcc_the_position_of_the_cursor_after_operation_should_be_first_non_whitespace_character(self):
        self.eq('    abc|', 'gcc', '    |# abc')
        self.eq('    a|bc', 'gcc', '    |# abc')
        self.eq('    # abc|', 'gcc', '    |abc')
        self.eq('    # a|bc', 'gcc', '    |abc')

    def test_gcc_empty_lines(self):
        self.eq('|', 'gcc', '|# ')
        self.eq('|#', 'gcc', '|')

    def test_gcc_multiple_cursor_commenting(self):
        self.eq('    a|bc\n    a|bc\n    a|bc\n', 'gcc', '    |# abc\n    # abc\n    # abc\n')

    def test_gcc_multiple_cursor_uncommenting(self):
        self.eq('    # a|bc\n    # a|bc\n    # a|bc\n', 'gcc', '    |abc\n    abc\n    abc\n')

    def test_gcG_comment(self):
        self.eq('|abc\ndef\nghi\n', 'gcG', '|# abc\n# def\n# ghi\n')
        self.eq('1\n2\n|3\n4\n5\n', 'gcG', '1\n2\n|# 3\n# 4\n# 5\n')
        self.eq('1\n2\n    |3\n    4\n    5\n', 'gcG', '1\n2\n    |# 3\n    # 4\n    # 5\n')
        self.eq('1\n2\n|    3\n    4\n    5\n', 'gcG', '1\n2\n    |# 3\n    # 4\n    # 5\n')

    def test_gcG_uncomment(self):
        self.eq('|# abc\n# def\n# ghi\n', 'gcG', '|abc\ndef\nghi\n')
        self.eq('1\n2\n|3\n4\n5\n', 'gcG', '1\n2\n|# 3\n# 4\n# 5\n')
        self.eq('1\n2\n    |#3\n    #4\n    #5\n', 'gcG', '1\n2\n    |3\n    4\n    5\n')
        self.eq('1\n2\n|    #3\n    #4\n    #5\n', 'gcG', '1\n2\n    |3\n    4\n    5\n')
