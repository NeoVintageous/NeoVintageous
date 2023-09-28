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


class Test_ex_bprevious(unittest.FunctionalTestCase):

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.window_buffer_control')
    def test_n_bprevious(self, control):
        self.eq('f|izz', ':bprevious', 'f|izz')
        control.assert_called_once_with(self.view.window(), 'previous', count=1)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.window_buffer_control')
    def test_n_with_count(self, control):
        self.eq('f|izz', ':bprevious 11', 'f|izz')
        control.assert_called_once_with(self.view.window(), 'previous', count=11)
