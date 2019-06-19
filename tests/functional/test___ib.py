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
            self.assertRegisters('"-', 'fizz', '01')
            self.resetRegisters()

            # XXX Should this be registered as a linewise register?
            self.eq('x(\nfi|zz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.assertRegisters('"-', 'fizz', '01')
            self.resetRegisters()

            # XXX Should this be registered as a linewise register?
            self.eq('x(\n|    fizz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    |fizz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fi|zz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fiz|z\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.assertRegisters('"-', '    fizz', '01')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    |fizz\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fi|zz\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.eq('x(\n    fiz|z\n    buzz\n)y', 'ci' + target, 'i_x(\n|\n)y')
            self.assertLinewiseRegisters('"1', '    fizz\n    buzz', '-0')
            self.resetRegisters()

    def test_dib(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'di' + target, 'x(|)y')
            self.assertRegisters('"-', 'fizz', '01')
            self.resetRegisters()

            self.eq('x(\nfi|zz\n)y', 'di' + target, 'x(\n|)y')
            self.assertLinewiseRegisters('"1', 'fizz\n', '-0')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    |fizz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fi|zz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fiz|z\n)y', 'di' + target, 'x(\n|)y')
            self.assertLinewiseRegisters('"1', '    fizz\n', '-0')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    |fizz\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fi|zz\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.eq('x(\n    fiz|z\n    buzz\n)y', 'di' + target, 'x(\n|)y')
            self.assertLinewiseRegisters('"1', '    fizz\n    buzz\n', '-0')
            self.resetRegisters()

    def test_yib(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'yi' + target, 'x(|fizz)y')
            self.assertRegisters('"0', 'fizz', '-1')
            self.resetRegisters()

            self.eq('x(\nfi|zz\n)y', 'yi' + target, 'x(\n|fizz\n)y')
            self.assertLinewiseRegisters('"0', 'fizz\n', '-1')
            self.resetRegisters()

            self.eq('x(\nfi|zz\nbuzz\n)y', 'yi' + target, 'x(\n|fizz\nbuzz\n)y')
            self.assertLinewiseRegisters('"0', 'fizz\nbuzz\n', '-1')
            self.resetRegisters()
