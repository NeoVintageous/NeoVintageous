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


class Test_ab(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_vab(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)x', 'v_a' + target, 'x|(fizz)|x')
            self.eq('x(\nfi|zz\n)x', 'v_a' + target, 'x|(\nfizz\n)|x')
            self.eq('x(\n\n  \n    fi|zz\n\n\n)x', 'v_a' + target, 'x|(\n\n  \n    fizz\n\n\n)|x')
            self.eq('(hello, (w|orl|d))', 'v_a' + target, '(hello, |(world)|)')
            self.eq('r_(hello, (w|orl|d))', 'v_a' + target, '(hello, |(world)|)')

    def test_vab_when_on_cursor_on_open_target(self):
        for target in ('(', ')', 'b'):
            self.eq('(hello, |(wor|ld))', 'v_a' + target, '(hello, |(world)|)')
            self.eq('r_(hello, |(wor|ld))', 'v_a' + target, '(hello, |(world)|)')
            self.eq('fizz (hello, |(wor|ld)) buzz', 'v_a' + target, 'fizz (hello, |(world)|) buzz')
            self.eq('(fizz (hello, |(wor|ld)) buzz)', 'v_a' + target, '(fizz (hello, |(world)|) buzz)')
            self.eq('(fizz |(hel|lo, (world)) buzz)', 'v_a' + target, '(fizz |(hello, (world))| buzz)')
            self.eq('r_(fizz |(hel|lo, (world)) buzz)', 'v_a' + target, '(fizz |(hello, (world))| buzz)')

    def test_cab(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'ca' + target, 'i_x|y')
            self.assertRegisters('"-', '(fizz)', '01')
            self.resetRegisters()

            self.eq('x(\nfi|zz\n)y', 'ca' + target, 'i_x|y')
            self.assertLinewiseRegisters('"1', '(\nfizz\n)', '-0')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n)y', 'ca' + target, 'i_x|y')
            self.eq('x(\n    |fizz\n)y', 'ca' + target, 'i_x|y')
            self.eq('x(\n    fi|zz\n)y', 'ca' + target, 'i_x|y')
            self.eq('x(\n    fiz|z\n)y', 'ca' + target, 'i_x|y')
            self.assertLinewiseRegisters('"1', '(\n    fizz\n)', '-0')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n    buzz\n)y', 'ca' + target, 'i_x|y')
            self.eq('x(\n    |fizz\n    buzz\n)y', 'ca' + target, 'i_x|y')
            self.eq('x(\n    fi|zz\n    buzz\n)y', 'ca' + target, 'i_x|y')
            self.eq('x(\n    fiz|z\n    buzz\n)y', 'ca' + target, 'i_x|y')
            self.assertLinewiseRegisters('"1', '(\n    fizz\n    buzz\n)', '-0')
            self.resetRegisters()

    def test_dab(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'da' + target, 'x|y')
            self.assertRegisters('"-', '(fizz)', '01')
            self.resetRegisters()

            self.eq('x(\nfi|zz\n)y', 'da' + target, 'x|y')
            self.assertLinewiseRegisters('"1', '(\nfizz\n)', '-0')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n)y', 'da' + target, 'x|y')
            self.eq('x(\n    |fizz\n)y', 'da' + target, 'x|y')
            self.eq('x(\n    fi|zz\n)y', 'da' + target, 'x|y')
            self.eq('x(\n    fiz|z\n)y', 'da' + target, 'x|y')
            self.assertLinewiseRegisters('"1', '(\n    fizz\n)', '-0')
            self.resetRegisters()

            self.eq('x(\n|    fizz\n    buzz\n)y', 'da' + target, 'x|y')
            self.eq('x(\n    |fizz\n    buzz\n)y', 'da' + target, 'x|y')
            self.eq('x(\n    fi|zz\n    buzz\n)y', 'da' + target, 'x|y')
            self.eq('x(\n    fiz|z\n    buzz\n)y', 'da' + target, 'x|y')
            self.assertLinewiseRegisters('"1', '(\n    fizz\n    buzz\n)', '-0')
            self.resetRegisters()

    def test_yab(self):
        for target in ('(', ')', 'b'):
            self.eq('x(fi|zz)y', 'ya' + target, 'x|(fizz)y')
            self.assertRegisters('"0', '(fizz)', '-1')
            self.resetRegisters()

            self.eq('x(\nfi|zz\n)y', 'ya' + target, 'x|(\nfizz\n)y')
            self.assertLinewiseRegisters('"0', '(\nfizz\n)', '-1')
            self.resetRegisters()

            self.eq('x(\nfi|zz\nbuzz\n)y', 'ya' + target, 'x|(\nfizz\nbuzz\n)y')
            self.assertLinewiseRegisters('"0', '(\nfizz\nbuzz\n)', '-1')
            self.resetRegisters()
