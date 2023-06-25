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


class TestHighlightedYank(unittest.FunctionalTestCase):

    def test_highlight_yank(self):
        self.eq('f|iz|z', 'v_y', 'n_f|izz')
        self.assertHighlightedYank('f|iz|z')

    def test_highlight_yank_disabled(self):
        self.view.settings().set('highlightedyank', False)
        self.eq('f|iz|z', 'v_y', 'n_f|izz')
        self.assertNoHighlightedYank()
