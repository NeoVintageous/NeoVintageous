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
    test_data('0a23x5', (1, 1), 'x', unittest.NORMAL, (3, 3), 'Find ahead'),
    test_data('0ax345', (1, 1), 'x', unittest.NORMAL, (1, 1), 'Find next'),
    test_data('0x2345', (1, 1), 'x', unittest.NORMAL, (1, 1), 'Find self'),
    test_data('0a2xx5', (1, 1), 'x', unittest.NORMAL, (2, 2), 'Find multiple'),
    test_data('0x2x45', (1, 1), 'x', unittest.NORMAL, (2, 2), 'Find self multiple'),
    test_data('0a23:5', (1, 1), ':', unittest.NORMAL, (3, 3), 'Find ahead (colon)'),
    test_data('0a:345', (1, 1), ':', unittest.NORMAL, (1, 1), 'Find next (colon)'),
    test_data('0:2345', (1, 1), ':', unittest.NORMAL, (1, 1), 'Find self (colon)'),
    test_data('0a2::5', (1, 1), ':', unittest.NORMAL, (2, 2), 'Find multiple (colon)'),
    test_data('0:2:45', (1, 1), ':', unittest.NORMAL, (2, 2), 'Find self multiple (colon)'),
)

INTERNAL_NORMAL_CASES = (
    test_data('0a23x5', (1, 1), 'x', unittest.INTERNAL_NORMAL, (1, 4), 'Find ahead'),
    test_data('0ax345', (1, 1), 'x', unittest.INTERNAL_NORMAL, (1, 2), 'Find next'),
    test_data('0x2345', (1, 1), 'x', unittest.INTERNAL_NORMAL, (1, 1), 'Find self'),
    test_data('0a2xx5', (1, 1), 'x', unittest.INTERNAL_NORMAL, (1, 3), 'Find multiple'),
    test_data('0x2x45', (1, 1), 'x', unittest.INTERNAL_NORMAL, (1, 3), 'Find self multiple'),
)

VISUAL_MULTI_CHAR_CASES = (
    test_data('0ab3x5', (1, 3), 'x', unittest.VISUAL, (1, 4), 'Forward'),
    test_data('0a23x5', (1, 5), 'x', unittest.VISUAL, (1, 5), 'Forward find b'),
    test_data('0b2xa5', (5, 1), 'x', unittest.VISUAL, (5, 2), 'Reverse no crossover'),
    test_data('0ba3x5', (3, 1), 'x', unittest.VISUAL, (2, 4), 'Reverse crossover'),
    test_data('0b2x45', (4, 1), 'x', unittest.VISUAL, (4, 2), 'Reverse find a'),
    test_data('0x2a45', (4, 1), 'x', unittest.VISUAL, (4, 1), 'Reverse find b'),
    test_data('0a2bx5', (1, 4), 'x', unittest.VISUAL, (1, 4), 'Forward find b+1'),
    test_data('0bx3a5', (5, 1), 'x', unittest.VISUAL, (5, 1), 'Reverse find b+1'),
    test_data('0b2ax5', (4, 1), 'x', unittest.VISUAL, (4, 3), 'Reverse find a+1'),
)

VISUAL_ONE_CHAR_CASES = (
    test_data('ax', (0, 2), 'x', unittest.VISUAL, (0, 2), 'Forward find b'),
    test_data('bx', (2, 0), 'x', unittest.VISUAL, (2, 0), 'Reverse find a'),
    test_data('fx', (0, 1), 'x', unittest.VISUAL, (0, 1), 'Forward find next'),
    test_data('rx', (1, 0), 'x', unittest.VISUAL, (1, 0), 'Reverse find next'),
    test_data('f', (0, 1), 'f', unittest.VISUAL, (0, 1), 'Forward find self'),
    test_data('r', (1, 0), 'r', unittest.VISUAL, (1, 0), 'Reverse find self'),
)

VISUAL_MULTI_MATCHES_CASES = (
    test_data('0abxx5', (1, 3), 'x', unittest.VISUAL, (1, 3), 'Forward find first'),
    test_data('0axx45', (1, 3), 'x', unittest.VISUAL, (1, 3), 'Forward find b'),
    test_data('0bxx45', (3, 1), 'x', unittest.VISUAL, (3, 1), 'Reverse find a'),
    test_data('0bxx45', (4, 1), 'x', unittest.VISUAL, (4, 1), 'Reverse find a'),
    test_data('0xax45', (3, 1), 'x', unittest.VISUAL, (3, 2), 'Reverse find b'),
)

VISUAL_MULTI_LINE_CASES = (
    test_data('012\n456', (0, 5), '2', unittest.VISUAL, (0, 5), 'Select L1->L2, find on L1'),
    test_data('012\n456', (0, 5), '6', unittest.VISUAL, (0, 6), 'Select L1->L2, find on L2'),
    test_data('012\n456', (0, 4), '2', unittest.VISUAL, (0, 4), 'Select L1->LF, find on L1'),
    test_data('012\n456', (0, 4), '6', unittest.VISUAL, (0, 4), 'Select L1->LF, find on L2'),
    test_data('012\n456', (5, 0), '2', unittest.VISUAL, (5, 1), 'Select L2->L1, find on L1'),
    test_data('012\n456', (5, 0), '6', unittest.VISUAL, (5, 0), 'Select L2->L1, find on L2'),
    test_data('012\n456', (5, 3), '2', unittest.VISUAL, (5, 3), 'Select L2->LF, find on L1'),
    test_data('012\n456', (5, 3), '6', unittest.VISUAL, (5, 3), 'Select L2->LF, find on L2'),
    test_data('0123\n5678', (7, 5), '8', unittest.VISUAL, (6, 8), 'Select L2->LF+1, find on L2'),
)

SKIP_CASES = (
    test_data('xxxx', (1, 1), 'x', unittest.NORMAL, (2, 2), 'Skip past previous match'),
    test_data('xxxx', (2, 2), 'x', unittest.NORMAL, (2, 2), 'Does not skip past final match'),
)


class Test__nv_vi_t(unittest.ViewTestCase):

    def runTests(self, data, skipping=False):
        for (i, data) in enumerate(data):
            self.write(data.text)
            self.select(self._R(*data.startRegion))

            self.view.run_command('nv_vi_find_in_line', {
                'mode': data.mode,
                'count': 1,
                'char': data.findChar,
                'inclusive': False,
                'skipping': skipping
            })

            self._assertRegionsEqual(
                self._R(*data.expectedRegion),
                self.view.sel()[0],
                "Failed on index {} {} : Text:\"{}\" Region:{} Find:'{}'"
                .format(i, data.msg, data.text, data.startRegion, data.findChar)
            )

    def runTestsWithSkip(self, data):
        self.runTests(data, skipping=True)

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

    def test_skip_cases(self):
        self.runTestsWithSkip(SKIP_CASES)
