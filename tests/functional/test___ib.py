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


class Test_ib(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_vib(self):
        for target in ('(', ')', 'b'):
            self.eq('(fi|zz)', 'v_i' + target, '(|fizz|)')
            self.eq('(\nfi|zz\n)', 'v_i' + target, '(\n|fizz\n|)')
            self.eq('(\n|    fizz\n)', 'v_i' + target, '(\n|    fizz\n|)')
            self.eq('(\n    |fizz\n)', 'v_i' + target, '(\n|    fizz\n|)')
            self.eq('(\n    fiz|z\n)', 'v_i' + target, '(\n|    fizz\n|)')
            self.eq('(\nfi|zz\nbuzz\n)', 'v_i' + target, '(\n|fizz\nbuzz\n|)')
            self.eq('(\n    fi|zz\n    buzz\n)', 'v_i' + target, '(\n|    fizz\n    buzz\n|)')

    def test_cib(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'ci' + target, 'i_x(|)y')
            self.eq('x(\nfi|zz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n|    fizz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    |fizz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fi|zz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fiz|z\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n|    fizz\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    |fizz\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fi|zz\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fiz|z\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')

    def test_dib(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'di' + target, 'x(|)y')
            self.eq('x(\nfi|zz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n|    fizz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    |fizz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fi|zz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fiz|z\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n|    fizz\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    |fizz\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fi|zz\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fiz|z\n    buzz\n)y', 'di' + target, 'x(\n|)y')

    def test_yib(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'yi' + target, 'x(|fizz)y')
            self.eq('x(\nfi|zz\n)y', 'yi' + target, 'x(\n|fizz\n)y')
            self.eq('x(\nfi|zz\nbuzz\n)y', 'yi' + target, 'x(\n|fizz\nbuzz\n)y')
