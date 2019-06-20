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


class Test_gp(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)

    def test_n(self):
        self.register('"fizz')
        self.eq('a|bc', 'gp', 'abfizz|c')
        self.eq('ab|c', 'gp', 'abcfiz|z')
        self.register('"fizz\n')
        self.eq('a|bc', 'gp', 'abfizz\n|c')
        self.registerLinewise('"fizz\n')
        self.eq('a\n|b\nc\n', 'gp', 'a\nb\nfizz\n|c\n')
