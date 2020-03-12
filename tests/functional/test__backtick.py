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


class Test_backtick(unittest.FunctionalTestCase):

    def test_n(self):
        self.normal('fizz\n|2\nbuzz\n')
        self.feed('mx')
        self.assertNormal('fizz\n|2\nbuzz\n')
        self.select(0)
        self.feed('n_`x')
        self.assertNormal('fizz\n|2\nbuzz\n')
        self.select(1)
        self.feed('n_`a')
        self.assertNormal('f|izz\n2\nbuzz\n')

    def test_n_jumps_to_specific_location(self):
        self.normal('fizz\n    fizz b|uzz\nbuzz\n')
        self.feed('mx')
        self.assertNormal('fizz\n    fizz b|uzz\nbuzz\n')
        for pt in (0, 5, 7, 9, 15, 20):
            self.select(pt)
            self.feed('n_`x')
            self.assertNormal('fizz\n    fizz b|uzz\nbuzz\n', 'at ' + str(pt))

    def test_v(self):
        self.visual('fizz\n    fi|zz bu|zz\nfizz\n')
        self.feed('mx')
        self.feed('<Esc>')
        self.select(0)
        self.feed('n_`x')
        self.assertNormal('fizz\n    fizz b|uzz\nfizz\n')
        self.visual('fizz\n    fi|zz bu|zz\nfizz\n')
        self.feed('mx')
        self.select(0)
        self.feed('v_`x')
        self.assertVisual('|fizz\n    fizz b|uzz\nfizz\n')
        self.select((20, 22))
        self.feed('v_`x')
        self.assertRVisual('fizz\n    fizz b|uzz\nfi|zz\n')
        self.select((13, 2))
        self.feed('v_`x')
        self.assertVisual('fizz\n    fiz|z bu|zz\nfizz\n')
        self.select((21, 2))
        self.feed('v_`x')
        self.assertRVisual('fizz\n    fizz b|uzz\nfi|zz\n')
        self.select((6, 8))
        self.feed('v_`x')
        self.assertVisual('fizz\n |   fizz bu|zz\nfizz\n')

    def test_V(self):
        self.normal('fizz\n    bu|zz\nfizz\nbuzz\n')
        self.feed('mx')
        self.feed('gg')
        self.assertNormal('|fizz\n    buzz\nfizz\nbuzz\n')
        self.feed('V')
        self.assertVline('|fizz\n|    buzz\nfizz\nbuzz\n')
        self.feed('V_`x')
        self.assertVline('|fizz\n    buzz\n|fizz\nbuzz\n')

    def test_d(self):
        self.normal('fizz\nfizz b|uzz\nbuzz\n')
        self.feed('mx')
        self.select(0)
        self.feed('d\'x')
        self.assertNormal('|\nbuzz\n')
        self.normal('fizz\nfizz b|uzz\nbuzz\n')
        self.feed('mx')
        self.select(17)
        self.feed('d\'x')
        self.normal('fizz\nfizz b|zz\n')

    @unittest.mock_status_message()
    def test_mark_not_set(self):
        self.eq('fi|zz', 'n_`p', 'fi|zz')
        self.assertStatusMessage('E20: mark not set')
