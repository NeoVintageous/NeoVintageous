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


class Test_ex_spellgood(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('add_word')
    def test_n(self):
        self.eq('fi|zz', ':spellgood buzz', 'fi|zz')
        self.assertRunCommand('add_word', {'word': 'buzz'})
        self.feed(':spellgood kapow')
        self.assertRunCommand('add_word', {'word': 'kapow'})
