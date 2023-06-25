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


class TestGoto(unittest.FunctionalTestCase):

    @unittest.mock.patch('NeoVintageous.nv.goto.goto_prev_change')
    def test_left_bracket_c(self, function):
        self.normal('f|izz')
        self.feed('[c')
        function.assert_called_once_with(self.view, unittest.NORMAL, 1)

    @unittest.mock.patch('NeoVintageous.nv.goto.goto_next_change')
    def test_right_bracket_c(self, function):
        self.normal('f|izz')
        self.feed(']c')
        function.assert_called_once_with(self.view, unittest.NORMAL, 1)

    @unittest.mock.patch('NeoVintageous.nv.goto.goto_prev_mispelled_word')
    def test_left_bracket_s(self, function):
        self.normal('f|izz')
        self.feed('[s')
        function.assert_called_once_with(self.view, unittest.NORMAL, 1)

    @unittest.mock.patch('NeoVintageous.nv.goto.goto_next_mispelled_word')
    def test_right_bracket_s(self, function):
        self.normal('f|izz')
        self.feed(']s')
        function.assert_called_once_with(self.view, unittest.NORMAL, 1)
