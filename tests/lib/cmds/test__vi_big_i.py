from collections import namedtuple

from NeoVintageous.tests import unittest


def first_sel(self):
    return self.view.sel()[0]


def second_sel(self):
    return self.view.sel()[1]


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')

TESTS = (
    test_data('abc',           [[(0, 0), (0, 2)]],                   {'mode': unittest.INTERNAL_NORMAL_MODE}, [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 1)], [(1, 1), (1, 1)]], {'mode': unittest.INTERNAL_NORMAL_MODE}, [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 1)], [(1, 1), (1, 1)]], {'mode': unittest.INTERNAL_NORMAL_MODE}, [(1, 0), (1, 0)], second_sel, ''),  # noqa: E241,E501
    test_data('abc',           [[(0, 0), (0, 2)]],                   {'mode': unittest.VISUAL_MODE},           [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 2)], [(1, 1), (1, 2)]], {'mode': unittest.VISUAL_MODE},           [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 1), (0, 2)], [(1, 1), (1, 2)]], {'mode': unittest.VISUAL_MODE},           [(1, 0), (1, 0)], second_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc\nabc', [[(0, 0), (1, 4)]],                   {'mode': unittest.VISUAL_LINE_MODE},      [(0, 0), (0, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc\nabc', [[(1, 0), (2, 4)]],                   {'mode': unittest.VISUAL_LINE_MODE},      [(1, 0), (1, 0)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 2), (0, 3)], [(1, 2), (1, 3)]], {'mode': unittest.VISUAL_BLOCK_MODE},     [(0, 2), (0, 2)], first_sel, ''),  # noqa: E241,E501
    test_data('abc\nabc',      [[(0, 2), (0, 3)], [(1, 2), (1, 3)]], {'mode': unittest.VISUAL_BLOCK_MODE},     [(1, 2), (1, 2)], second_sel, ''),  # noqa: E241,E501
)


class Test__vi_big_i(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('_vi_big_i', data.cmd_params)
            actual = data.actual_func(self)

            self.assertEqual(self._R(*data.expected), actual, "[{0}] {1}".format(i, data.msg))
