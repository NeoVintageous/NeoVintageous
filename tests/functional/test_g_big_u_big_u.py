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


class Test_gUU(unittest.FunctionalTestCase):

    def test_gUU(self):
        self.eq('x\nfiZ|Z Buzz\nx', 'gUU', 'x\n|FIZZ BUZZ\nx')
        self.eq('x\n    fiZ|Z Buzz\nx', 'gUU', 'x\n    |FIZZ BUZZ\nx')
        self.eq('x\n    fiZ|Z\nBuzz\n  three\nx', '3gUU', 'x\n    |FIZZ\nBUZZ\n  THREE\nx')
