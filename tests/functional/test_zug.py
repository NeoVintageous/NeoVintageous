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


class Test_zug(unittest.FunctionalTestCase):

    @unittest.mock.patch('NeoVintageous.nv.utils.spell_undo')
    def test_n(self, spell_undo):
        self.eq('x fi|zz x', 'n_zug', 'x fi|zz x')
        spell_undo.assert_called_once_with('fizz')
        self.eq('x bu|zz x', 'n_zug', 'x bu|zz x')
        spell_undo.assert_called_with('buzz')

    @unittest.mock.patch('NeoVintageous.nv.utils.spell_undo')
    def test_v(self, spell_undo):
        self.eq('x |fiz|z x', 'v_zug', 'x |fiz|z x')
        spell_undo.assert_called_once_with('fiz')
        self.eq('k|apo|w', 'n_zug', 'k|apo|w')
        spell_undo.assert_called_with('kapow')
