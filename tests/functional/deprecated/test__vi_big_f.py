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

from collections import namedtuple

from NeoVintageous.tests import unittest


test_data = namedtuple('test_data', 'text startRegion findChar mode expectedRegion msg')

NORMAL_CASES = (
    test_data('0x23a5', (4, 4), 'x', unittest.NORMAL, (1, 1), 'Find behind'),
    test_data('012xa5', (4, 4), 'x', unittest.NORMAL, (3, 3), 'Find previous'),
    test_data('0123x5', (4, 4), 'x', unittest.NORMAL, (4, 4), 'Find self'),
    test_data('0xx3a5', (4, 4), 'x', unittest.NORMAL, (2, 2), 'Find multiple'),
    test_data('01x3x5', (4, 4), 'x', unittest.NORMAL, (2, 2), 'Find self multiple'),
)

INTERNAL_NORMAL_CASES = (
    test_data('0x23a5', (4, 4), 'x', unittest.INTERNAL_NORMAL, (4, 1), 'Find behind'),
    test_data('012xa5', (4, 4), 'x', unittest.INTERNAL_NORMAL, (4, 3), 'Find previous'),
    test_data('0123x5', (4, 4), 'x', unittest.INTERNAL_NORMAL, (4, 4), 'Find self'),
    test_data('0xx3a5', (4, 4), 'x', unittest.INTERNAL_NORMAL, (4, 2), 'Find multiple'),
    test_data('01x3x5', (4, 4), 'x', unittest.INTERNAL_NORMAL, (4, 2), 'Find self multiple'),
)

VISUAL_MULTI_CHAR_CASES = (
    test_data('0x2ba5', (5, 3), 'x', unittest.VISUAL, (5, 1), 'Reverse'),
    test_data('0x23a5', (5, 1), 'x', unittest.VISUAL, (5, 1), 'Reverse find b'),
    test_data('0ax3b5', (1, 5), 'x', unittest.VISUAL, (1, 3), 'Forward no crossover'),
    test_data('0x2ab5', (3, 5), 'x', unittest.VISUAL, (4, 1), 'Forward crossover'),
    test_data('01x3b5', (2, 5), 'x', unittest.VISUAL, (2, 3), 'Forward find a'),
    test_data('01a3x5', (2, 5), 'x', unittest.VISUAL, (2, 5), 'Forward find b'),
)

VISUAL_ONE_CHAR_CASES = (
    test_data('xa', (2, 0), 'x', unittest.VISUAL, (2, 0), 'Reverse find b'),
    test_data('xb', (0, 2), 'x', unittest.VISUAL, (0, 1), 'Forward find a'),
    test_data('xr', (2, 1), 'x', unittest.VISUAL, (2, 0), 'Reverse find previous'),
    test_data('xf', (1, 2), 'x', unittest.VISUAL, (2, 0), 'Forward find previous'),
    test_data('r', (1, 0), 'r', unittest.VISUAL, (1, 0), 'Reverse find self'),
    test_data('f', (0, 1), 'f', unittest.VISUAL, (0, 1), 'Forward find self'),
)

VISUAL_MULTI_MATCHES_CASES = (
    test_data('0xxba5', (5, 3), 'x', unittest.VISUAL, (5, 2), 'Reverse find first'),
    test_data('01xxa5', (5, 3), 'x', unittest.VISUAL, (5, 2), 'Reverse find b'),
    test_data('01xxb5', (3, 5), 'x', unittest.VISUAL, (3, 4), 'Forward find a'),
    test_data('01xxb5', (2, 5), 'x', unittest.VISUAL, (2, 4), 'Forward find a'),
    test_data('01xax5', (3, 5), 'x', unittest.VISUAL, (4, 2), 'Forward find b'),
)

VISUAL_MULTI_LINE_CASES = (
    test_data('012\n456', (2, 7), '0', unittest.VISUAL, (2, 7), 'Select L1->L2, find on L1'),
    test_data('012\n456', (2, 7), '4', unittest.VISUAL, (2, 5), 'Select L1->L2, find on L2'),
    test_data('012\n456', (2, 4), '0', unittest.VISUAL, (3, 0), 'Select L1->LF, find on L1'),
    test_data('012\n456', (2, 4), '5', unittest.VISUAL, (2, 4), 'Select L1->LF, find on L2'),
    test_data('012\n456', (7, 2), '0', unittest.VISUAL, (7, 0), 'Select L2->L1, find on L1'),
    test_data('012\n456', (7, 2), '4', unittest.VISUAL, (7, 2), 'Select L2->L1, find on L2'),
    test_data('012\n456', (7, 3), '0', unittest.VISUAL, (7, 0), 'Select L2->LF, find on L1'),
    test_data('012\n456', (7, 3), '4', unittest.VISUAL, (7, 3), 'Select L2->LF, find on L2'),
    test_data('0123\n5678', (2, 4), '0', unittest.VISUAL, (3, 0), 'Select L1->LF-1, find on L1'),
)


class Test__nv_vi_big_f(unittest.ViewTestCase):

    def runTests(self, data):
        for (i, data) in enumerate(data):
            self.write(data.text)
            self.select(self._R(*data.startRegion))

            self.view.run_command('nv_vi_reverse_find_in_line', {
                'mode': data.mode,
                'count': 1,
                'char': data.findChar,
                'inclusive': True
            })

            self._assertRegionsEqual(
                self._R(*data.expectedRegion),
                self.view.sel()[0],
                "Failed on index {} {} : Text:\"{}\" Region:{} Find:'{}'"
                .format(i, data.msg, data.text, data.startRegion, data.findChar)
            )

    def test_normal_cases(self):
        self.runTests(NORMAL_CASES)

    def test_internal_normal_cases(self):
        self.runTests(INTERNAL_NORMAL_CASES)

    def test_visual_multiple_character_cases(self):
        self.runTests(VISUAL_MULTI_CHAR_CASES)

    def test_visual_single_character_cases(self):
        self.runTests(VISUAL_ONE_CHAR_CASES)

    def test_visual_multiple_matches_cases(self):
        self.runTests(VISUAL_MULTI_MATCHES_CASES)

    def test_visual_multiple_lines_cases(self):
        self.runTests(VISUAL_MULTI_LINE_CASES)
