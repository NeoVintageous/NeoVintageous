from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


test_data = namedtuple('test_data', 'text startRegion findChar mode expectedRegion msg')

NORMAL_CASES = (
    test_data('0a23x5', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (4, 4), 'Find ahead'),
    test_data('0ax345', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (2, 2), 'Find next'),
    test_data('0x2345', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (1, 1), 'Find self'),
    test_data('0a2xx5', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (3, 3), 'Find multiple'),
    test_data('0x2x45', (1, 1), 'x', ViewTestCase.NORMAL_MODE, (3, 3), 'Find self multiple'),
)

INTERNAL_NORMAL_CASES = (
    test_data('0a23x5', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 5), 'Find ahead'),
    test_data('0ax345', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 3), 'Find next'),
    test_data('0x2345', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 1), 'Find self'),
    test_data('0a2xx5', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 4), 'Find multiple'),
    test_data('0x2x45', (1, 1), 'x', ViewTestCase.INTERNAL_NORMAL_MODE, (1, 4), 'Find self multiple'),
)

VISUAL_MULTI_CHAR_CASES = (
    test_data('0ab3x5', (1, 3), 'x', ViewTestCase.VISUAL_MODE, (1, 5), 'Forward'),
    test_data('0a23x5', (1, 5), 'x', ViewTestCase.VISUAL_MODE, (1, 5), 'Forward find b'),
    test_data('0b2xa5', (5, 1), 'x', ViewTestCase.VISUAL_MODE, (5, 3), 'Reverse no crossover'),
    test_data('0ba3x5', (3, 1), 'x', ViewTestCase.VISUAL_MODE, (2, 5), 'Reverse crossover'),
    test_data('0b2x45', (4, 1), 'x', ViewTestCase.VISUAL_MODE, (4, 3), 'Reverse find a'),
    test_data('0x2a45', (4, 1), 'x', ViewTestCase.VISUAL_MODE, (4, 1), 'Reverse find b'),
)

VISUAL_ONE_CHAR_CASES = (
    test_data('ax', (0, 2), 'x', ViewTestCase.VISUAL_MODE, (0, 2), 'Forward find b'),
    test_data('bx', (2, 0), 'x', ViewTestCase.VISUAL_MODE, (2, 1), 'Reverse find a'),
    test_data('fx', (0, 1), 'x', ViewTestCase.VISUAL_MODE, (0, 2), 'Forward find next'),
    test_data('rx', (1, 0), 'x', ViewTestCase.VISUAL_MODE, (0, 2), 'Reverse find next'),
    test_data('f', (0, 1), 'f', ViewTestCase.VISUAL_MODE, (0, 1), 'Forward find self'),
    test_data('r', (1, 0), 'r', ViewTestCase.VISUAL_MODE, (1, 0), 'Reverse find self'),
)

VISUAL_MULTI_MATCHES_CASES = (
    test_data('0abxx5', (1, 3), 'x', ViewTestCase.VISUAL_MODE, (1, 4), 'Forward find first'),
    test_data('0axx45', (1, 3), 'x', ViewTestCase.VISUAL_MODE, (1, 4), 'Forward find b'),
    test_data('0bxx45', (3, 1), 'x', ViewTestCase.VISUAL_MODE, (3, 2), 'Reverse find a'),
    test_data('0bxx45', (4, 1), 'x', ViewTestCase.VISUAL_MODE, (4, 2), 'Reverse find a'),
    test_data('0xax45', (3, 1), 'x', ViewTestCase.VISUAL_MODE, (2, 4), 'Reverse find b'),
)

VISUAL_MULTI_LINE_CASES = (
    test_data('012\n456', (0, 5), '2', ViewTestCase.VISUAL_MODE, (0, 5), 'Select L1->L2, find on L1'),
    test_data('012\n456', (0, 5), '6', ViewTestCase.VISUAL_MODE, (0, 7), 'Select L1->L2, find on L2'),
    test_data('012\n456', (0, 4), '2', ViewTestCase.VISUAL_MODE, (0, 4), 'Select L1->LF, find on L1'),
    test_data('012\n456', (0, 4), '6', ViewTestCase.VISUAL_MODE, (0, 4), 'Select L1->LF, find on L2'),
    test_data('012\n456', (5, 0), '2', ViewTestCase.VISUAL_MODE, (5, 2), 'Select L2->L1, find on L1'),
    test_data('012\n456', (5, 0), '6', ViewTestCase.VISUAL_MODE, (5, 0), 'Select L2->L1, find on L2'),
    test_data('012\n456', (5, 3), '2', ViewTestCase.VISUAL_MODE, (5, 3), 'Select L2->LF, find on L1'),
    test_data('012\n456', (5, 3), '6', ViewTestCase.VISUAL_MODE, (5, 3), 'Select L2->LF, find on L2'),
    test_data('0123\n5678', (7, 5), '8', ViewTestCase.VISUAL_MODE, (6, 9), 'Select L2->LF+1, find on L2'),
)


class Test__vi_f(ViewTestCase):

    def runTests(self, data):
        for (i, data) in enumerate(data):
            self.write(data.text)
            self.select(self._R(*data.startRegion))

            self.view.run_command('_vi_find_in_line', {
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
