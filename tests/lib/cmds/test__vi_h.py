from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


def first_sel(self):
    return self.view.sel()[0]


test_data = namedtuple('test_data', 'cmd initial_text regions cmd_params expected actual_func msg')
region_data = namedtuple('region_data', 'regions')


TESTS_MODES = (
    # NORMAL mode
    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 1]], cmd_params={'mode': ViewTestCase.modes.NORMAL},
              expected=region_data([0, 0]), actual_func=first_sel, msg='should move back one char (normal mode)'),
    test_data(cmd='_vi_h', initial_text='foo bar baz', regions=[[1, 1]], cmd_params={'mode': ViewTestCase.modes.NORMAL, 'count': 10},  # noqa: E501, E241
              expected=region_data([0, 0]), actual_func=first_sel, msg='should move back one char with count (normal mode)'),  # noqa: E501, E241
    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 1]], cmd_params={'mode': ViewTestCase.modes.NORMAL, 'count': 10000},  # noqa: E501, E241
              expected=region_data([0, 0]), actual_func=first_sel, msg='should move back one char with large count (normal mode)'),  # noqa: E501, E241

    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 1]], cmd_params={'mode': ViewTestCase.modes.INTERNAL_NORMAL},  # noqa: E501, E241
              expected=region_data([1, 0]), actual_func=first_sel, msg='should select one char (internal normal mode)'),  # noqa: E501, E241
    test_data(cmd='_vi_h', initial_text='foo bar baz', regions=[[10, 10]], cmd_params={'mode': ViewTestCase.modes.INTERNAL_NORMAL},  # noqa: E501, E241
              expected=region_data([10, 9]), actual_func=first_sel, msg='should select one char from eol (internal normal mode)'),  # noqa: E501, E241
    test_data(cmd='_vi_h', initial_text='foo bar baz', regions=[[1, 1]], cmd_params={'mode': ViewTestCase.modes.INTERNAL_NORMAL, 'count': 10000},  # noqa: E501, E241
              expected=region_data([1, 0]), actual_func=first_sel, msg='should select one char large count (internal normal mode)'),  # noqa: E501, E241

    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 2]], cmd_params={'mode': ViewTestCase.modes.VISUAL},
              expected=region_data([2, 0]), actual_func=first_sel, msg='should select one char (visual mode)'),
    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 3]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 1},  # noqa: E501, E241
              expected=region_data([1, 2]), actual_func=first_sel, msg='should deselect one char (visual mode)'),
    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 3]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 2},  # noqa: E501, E241
              expected=region_data([2, 0]), actual_func=first_sel, msg='should go back two chars (visual mode) crossing over'),  # noqa: E501, E241

    test_data(cmd='_vi_h', initial_text='abc', regions=[[1, 3]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 100},  # noqa: E501, E241
              expected=region_data([2, 0]), actual_func=first_sel, msg='can move reversed cross over large count visual mode'),  # noqa: E501, E241
    test_data(cmd='_vi_h', initial_text='foo bar fuzz buzz', regions=[[11, 12]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 10},  # noqa: E501, E241
              expected=region_data([12, 1]), actual_func=first_sel, msg='can move with count visual mode'),
    test_data(cmd='_vi_h', initial_text='abc\n', regions=[[1, 2]], cmd_params={'mode': ViewTestCase.modes.VISUAL, 'count': 10000},  # noqa: E501, E241
              expected=region_data([2, 0]), actual_func=first_sel, msg='stops at left end'),

)


TESTS = TESTS_MODES


class Test__vi_h(ViewTestCase):

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
