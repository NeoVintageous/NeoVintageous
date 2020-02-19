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


class Test_u(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('undo')
    @unittest.mock_bell()
    def test_n_u_invokes_bell_when_nothing_to_redo(self):
        self.eq('fi|zz', 'n_u', 'fi|zz')
        self.assertRunCommand('undo')
        self.assertBell('Already at oldest change')

    @unittest.mock_run_commands('undo')
    @unittest.mock_bell()
    def test_n_u_count(self):
        self.eq('fi|zz', 'n_3u', 'fi|zz')
        self.assertRunCommand('undo', count=3)
        self.assertBell('Already at oldest change')

    def test_v_u(self):
        self.eq('F|IZZ B|UZZ', 'v_u', 'n_F|izz bUZZ')
