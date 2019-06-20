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


class Test_gP(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)

    def test_n(self):
        self.register('"abc')
        self.eq('x|yz', 'gP', 'xabc|yz')
        self.register('"abc\n')
        self.eq('x|yz', 'gP', 'xabc\n|yz')
        self.register('"fizz\nbuzz\nfizz')
        self.eq('x|yz', 'gP', 'xfizz\nbuzz\nfizz|yz')
        self.registerLinewise('"fizz\n')
        self.eq('a\n|b\nc', 'gP', 'a\nfizz\n|b\nc')
        self.registerLinewise('"fizz\nbuzz\n')
        self.eq('a\n|b\nc', 'gP', 'a\nfizz\nbuzz\n|b\nc')
