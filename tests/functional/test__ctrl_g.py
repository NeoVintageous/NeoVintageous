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


class Test_ctrl_g(unittest.FunctionalTestCase):

    @unittest.mock_status_message()
    def test_n(self):
        self.eq('|', 'n_<C-g>', '|')
        self.assertStatusMessage('"[No Name]" [Modified] --No lines in buffer--')
        self.eq('a|bc', 'n_<C-g>', 'a|bc')
        self.assertStatusMessage('"[No Name]" [Modified] 1 line --100%--')
        self.eq('|1\n2\n3', 'n_<C-g>', '|1\n2\n3')
        self.assertStatusMessage('"[No Name]" [Modified] 3 lines --33%--')
        self.eq('1\n|2\n3', 'n_<C-g>', '1\n|2\n3')
        self.assertStatusMessage('"[No Name]" [Modified] 3 lines --66%--')
        self.eq('1\n2\n|3', 'n_<C-g>', '1\n2\n|3')
        self.assertStatusMessage('"[No Name]" [Modified] 3 lines --100%--')
        self.eq('1\n|2\n3\n4', 'n_<C-g>', '1\n|2\n3\n4')
        self.assertStatusMessage('"[No Name]" [Modified] 4 lines --50%--')

    @unittest.mock_status_message()
    def test_n_readonly(self):
        self.normal('1\n|2\n3')
        self.view.set_read_only(True)
        self.feed('n_<C-g>')
        self.assertStatusMessage('"[No Name]" [readonly] 3 lines --66%--')
