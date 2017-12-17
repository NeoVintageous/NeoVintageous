from collections import namedtuple

from NeoVintageous.tests import unittest


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected msg')

TESTS = (
    test_data('    abc',                   [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1}, 'abc',               'failed in {0}'),  # noqa: E241,E501
    test_data('        abc',               [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1}, '    abc',           'failed in {0}'),  # noqa: E241,E501
    test_data('    abc\n    abc',          [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 2}, 'abc\nabc',          'failed in {0}'),  # noqa: E241,E501
    test_data('    abc\n    abc\n    abc', [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 3}, 'abc\nabc\nabc',     'failed in {0}'),  # noqa: E241,E501
    test_data('    abc\n    abc\n    abc', [[(0, 0), (0, 0)], [(1, 0), (1, 0)]], {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1}, 'abc\nabc\n    abc', 'failed in {0}'),  # noqa: E241,E501
)


class Test__vi_double_antilambda(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('_vi_less_than_less_than', data.cmd_params)

            self.assertEqual(data.expected, self.content(), "[{0}] {1}".format(i, data.msg).format(i))
