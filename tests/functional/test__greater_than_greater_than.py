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


class Test_greater_than_greater_than(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('translate_tabs_to_spaces', True)
        self.settings().set('tab_size', 2)

    def test_n(self):
        self.eq('x\n|ab\nx', '>>', 'x\n  |ab\nx')
        self.eq('x\n  fi|zz\nx', '>>', 'x\n    |fizz\nx')
        self.eq('x\n|  fizz\nx', '>>', 'x\n    |fizz\nx')
        self.eq('x\n  fiz|z\nx', '>>', 'x\n    |fizz\nx')
        self.eq('1\n|2\n3\n4\n5\n', '3>>', '1\n  |2\n  3\n  4\n5\n')
        self.eq('1\nfi|zz\n3\n4\n5\n', '3>>', '1\n  |fizz\n  3\n  4\n5\n')
        self.eq('1\nfi|zz\n3\n4\n5\n1\nbu|zz\n3\n4\n5\n', '3>>', '1\n  |fizz\n  3\n  4\n5\n1\n  |buzz\n  3\n  4\n5\n')
