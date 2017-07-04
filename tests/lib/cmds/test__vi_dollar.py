from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


def first_sel(self):
    return self.view.sel()[0]


test_data = namedtuple('test_data', 'cmd initial_text regions cmd_params expected actual_func msg')
region_data = namedtuple('region_data', 'regions')

TESTS_INTERNAL_NORMAL = (
    # NORMAL mode
    test_data(cmd='_vi_dollar', initial_text='abc\nabc\n', regions=[[(0, 0), (0, 0)]], cmd_params={'mode': ViewTestCase.modes.NORMAL},  # noqa: E501, E241
              expected=region_data([(0, 2), (0, 2)]), actual_func=first_sel, msg=''),

    test_data(cmd='_vi_dollar', initial_text=('abc\n' * 10), regions=[[(0, 0), (0, 0)]], cmd_params={'mode': ViewTestCase.modes.NORMAL, 'count': 5},  # noqa: E501, E241
              expected=region_data([18, 18]), actual_func=first_sel, msg=''),

    test_data(cmd='_vi_dollar', initial_text=('abc\n\nabc\n'), regions=[[4, 4]], cmd_params={'mode': ViewTestCase.modes.NORMAL, 'count': 1},  # noqa: E501, E241
              expected=region_data([4, 4]), actual_func=first_sel, msg='should not move on empty line'),

    # VISUAL mode
    test_data(cmd='_vi_dollar', initial_text='abc\nabc\n', regions=[[0, 1]], cmd_params={'mode': ViewTestCase.modes.VISUAL},  # noqa: E501, E241
              expected=region_data([0, 4]), actual_func=first_sel, msg=''),

    test_data(cmd='_vi_dollar', initial_text=('abc\n' * 10), regions=[[0, 1]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 5},  # noqa: E501, E241
              expected=region_data([0, 20]), actual_func=first_sel, msg=''),

    test_data(cmd='_vi_dollar', initial_text=('abc\n\nabc\n'), regions=[[4, 5]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 1},  # noqa: E501, E241
              expected=region_data([4, 5]), actual_func=first_sel, msg=''),

    test_data(cmd='_vi_dollar', initial_text=('abc\nabc\n'), regions=[[6, 1]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 1},  # noqa: E501, E241
              expected=region_data([6, 3]), actual_func=first_sel, msg='can move in visual mode with reversed sel no cross over'),  # noqa: E501, E241

    test_data(cmd='_vi_dollar', initial_text=('abc\nabc\n'), regions=[[3, 2]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 1},  # noqa: E501, E241
              expected=region_data([2, 4]), actual_func=first_sel, msg='can move in visual mode with reversed sel at eol'),  # noqa: E501, E241

    test_data(cmd='_vi_dollar', initial_text=('abc\nabc\n'), regions=[[5, 4]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 2},  # noqa: E501, E241
              expected=region_data([4, 8]), actual_func=first_sel, msg='can move in visual mode with revesed sel cross over'),  # noqa: E501, E241

    test_data(cmd='_vi_dollar', initial_text=('abc\nabc\nabc\n'), regions=[[0, 4]], cmd_params={'mode': ViewTestCase.modes.VISUAL_LINE, 'count': 1},  # noqa: E501, E241
              expected=region_data([0, 4]), actual_func=first_sel, msg='can move in visual mode with revesed sel cross over'),  # noqa: E501, E241

    test_data(cmd='_vi_dollar', initial_text='abc\nabc\n', regions=[[0, 0]], cmd_params={'mode': ViewTestCase.modes.INTERNAL_NORMAL},  # noqa: E501, E241
              expected=region_data([0, 4]), actual_func=first_sel, msg=''),

    test_data(cmd='_vi_dollar', initial_text='abc\nabc\nabc\nabc\n', regions=[[0, 0]], cmd_params={'mode': ViewTestCase.modes.INTERNAL_NORMAL, 'count': 3},  # noqa: E501, E241
              expected=region_data([0, 12]), actual_func=first_sel, msg=''),
)


TESTS = TESTS_INTERNAL_NORMAL


class Test__vi_dollar(ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.initial_text)
            self.select([self.R(*region) for region in data.regions])

            self.view.run_command(data.cmd, data.cmd_params)

            msg = "failed at test index {0} {1}".format(i, data.msg)
            actual = data.actual_func(self)

            if isinstance(data.expected, region_data):
                self.assertEqual(self.R(*data.expected.regions), actual, msg)
            else:
                self.assertEqual(data.expected, actual, msg)
