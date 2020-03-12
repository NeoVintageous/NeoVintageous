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


class Test_gU(unittest.FunctionalTestCase):

    def test_gUip(self):
        self.eq('ab|c def', 'gUip', '|ABC DEF')
        self.eq('xyz\n\nab|c\ndef\n\nxyz', 'gUip', 'xyz\n\n|ABC\nDEF\n\nxyz')
        self.eq('ab|c def', 'gUip', '|ABC DEF')

    def test_gUb(self):
        self.eq('|ab', 'gUb', '|ab')

    def test_v_gU(self):
        self.eq('f|IZZ B|uzz', 'v_gU', 'n_f|IZZ Buzz')

    def test_V_gU(self):
        self.eq('x\n|one\n|y', 'V_gU', 'n_x\n|ONE\ny')
