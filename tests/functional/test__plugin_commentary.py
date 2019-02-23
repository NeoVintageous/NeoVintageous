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

    def feed(self, seq):
        # Assign a specific syntax before feed, because our  tests would fail,
        # because views that have no syntax applied have no comment behaviours.
        self.view.assign_syntax('Packages/Python/Python.sublime-syntax')
        super().feed(seq)

    def test_gcc_comment(self):
        self.eq('|abc', 'gcc', '|# abc')
        self.eq('abc|', 'gcc', '|# abc')
        self.eq('|', 'gcc', '|# ')
        self.eq('1\n|2\n3\n4\n5', '3gcc', '1\n|# 2\n# 3\n# 4\n5')
        self.eq('1\n2\n|', 'gcc', '1\n|# 2\n')

    def test_gcc_uncomment(self):
        self.eq('|# abc', 'gcc', '|abc')
        self.eq('# abc|', 'gcc', '|abc')
        self.eq('|#', 'gcc', '|')
        self.eq('# 1\n|# 2\n# 3\n# 4\n# 5\n', '3gcc', '# 1\n|2\n3\n4\n# 5\n')

    def test_gcc_the_position_of_the_cursor_after_operation_should_be_first_non_whitespace_character(self):
        self.eq('    abc|', 'gcc', '    |# abc')
        self.eq('    a|bc', 'gcc', '    |# abc')
        self.eq('    # abc|', 'gcc', '    |abc')
        self.eq('    # a|bc', 'gcc', '    |abc')

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

    def test_v_gc(self):
        self.eq('f|iz|z', 'v_gc', 'n_|# fizz')
        self.eq('1\na|bc\n3\na|bc\nx', 'v_gc', 'n_1\n|# abc\n# 3\n# abc\nx')


class TestCommentaryPHP(unittest.FunctionalTestCase):

    def feed(self, seq):
        # Assign a specific syntax before feed, because our  tests would fail,
        # because views that have no syntax applied have no comment behaviours.
        self.view.assign_syntax('Packages/PHP/PHP.sublime-syntax')
        super().feed(seq)

    def test_v_gc(self):
        self.eq('<?php\nf|iz|z', 'v_gc', 'n_<?php\n|// fizz')

    def test_v_gC(self):
        self.eq('<?php\nf|iz|z', 'v_gC', 'n_<?php\nf/*|iz*/z')

    def test_n_gC_right_brace(self):
        self.eq('<?php\n|fizz\nbuzz\n\nx\ny', 'gC}', 'n_<?php\n/*|fizz\nbuzz\n*/\nx\ny')

    def test_n_gC_should_do_nothing(self):
        self.eq('<?php\nf|izz', 'n_gC', 'n_<?php\nf|izz')
