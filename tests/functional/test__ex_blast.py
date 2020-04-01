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


class Test_ex_blast(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('select_by_index')
    def test_n_blast(self):
        self.eq('f|izz', ':blast', 'f|izz')
        self.assertRunCommand('select_by_index', {'index': len(self.view.window().views_in_group(self.view.window().num_groups() - 1)) - 1})  # noqa: E501
