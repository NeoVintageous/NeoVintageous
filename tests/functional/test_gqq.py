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


@unittest.skipIf(unittest.ST_VERSION >= 4000, 'broken in ST4 see https://github.com/sublimehq/sublime_text/issues/3177')
class Test_gqq(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('WrapPlus.include_line_endings', None)
        self.settings().set('wrap_width', 5)

    def test_n(self):
        self.eq('f i z z\n|1 2 3 4 5 6 7 8 9 0\nb u z z\n', 'gqq', 'f i z z\n1 2 3\n4 5 6\n7 8 9\n|0\nb u z z\n')
        self.eq('f i z z\n1 2 3 4 |5 6 7 8 9 0\nb u z z\n', 'gqq', 'f i z z\n1 2 3\n4 5 6\n7 8 9\n|0\nb u z z\n')
        self.eq('f i z z\n1 2 3 4 5 6 7 8 9 |0\nb u z z\n', 'gqq', 'f i z z\n1 2 3\n4 5 6\n7 8 9\n|0\nb u z z\n')
        self.eq('|f i z z\n1 2 3 4 5 6 7 8 9 0\nb u z z\n', '2gqq', 'f i z\nz 1 2\n3 4 5\n6 7 8\n|9 0\nb u z z\n')
        self.eq('|f i z z\n1 2 3 4 5 6 7 8 9 0\na b c\nd e f', '3gqq', 'f i z\nz 1 2\n3 4 5\n6 7 8\n9 0 a\n|b c\nd e f')
