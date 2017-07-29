from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


def first_sel(self):
    return self.view.sel()[0]


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')

TESTS = (
    test_data('abc (abc) abc', [[(0, 6), (0, 7)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 7), (0, 4)], first_sel, 'visual not on bracket A'),  # FIXME # noqa: E501,E241
    test_data('abc (abc) abc', [[(0, 7), (0, 6)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 7), (0, 4)], first_sel, 'visual not on bracket B'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 0), (0, 2)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 0), (0, 4)], first_sel, 'visual right A'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 1), (0, 2)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 1), (0, 4)], first_sel, 'visual right B'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 5), (0, 3)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 5), (0, 1)], first_sel, 'visual left A'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 4), (0, 3)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 4), (0, 1)], first_sel, 'visual left B'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 2), (0, 4)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 3), (0, 1)], first_sel, 'visual right->left A'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 3), (0, 4)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 4), (0, 1)], first_sel, 'visual right->left B'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 3), (0, 1)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 2), (0, 4)], first_sel, 'visual left->right A'),  # FIXME # noqa: E501,E241
    test_data('0(2)4',         [[(0, 2), (0, 1)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 1), (0, 4)], first_sel, 'visual left->right B'),  # FIXME # noqa: E501,E241
    test_data('()',            [[(0, 0), (0, 1)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 0), (0, 2)], first_sel, 'visual off by one right'),  # FIXME # noqa: E501,E241
    test_data('()',            [[(0, 2), (0, 1)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 2), (0, 0)], first_sel, 'visual off by one left'),  # FIXME # noqa: E501,E241
    test_data('()',            [[(0, 1), (0, 2)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 2), (0, 0)], first_sel, 'visual off by one right->left'),  # FIXME # noqa: E501,E241
    test_data('()',            [[(0, 1), (0, 0)]], {'mode': ViewTestCase.VISUAL_MODE},           [(0, 0), (0, 2)], first_sel, 'visual off by one left->right'),  # FIXME # noqa: E501,E241
    test_data('abc (abc) abc', [[(0, 6), (0, 6)]], {'mode': ViewTestCase.INTERNAL_NORMAL_MODE},  [(0, 7), (0, 4)], first_sel, ''),  # FIXME # noqa: E501,E241
    test_data('abc (abc) abc', [[(0, 8), (0, 8)]], {'mode': ViewTestCase.INTERNAL_NORMAL_MODE},  [(0, 9), (0, 4)], first_sel, ''),  # FIXME # noqa: E501,E241
    test_data('abc (abc) abc', [[(0, 4), (0, 4)]], {'mode': ViewTestCase.INTERNAL_NORMAL_MODE},  [(0, 4), (0, 9)], first_sel, ''),  # FIXME # noqa: E501,E241
    test_data('abc (abc) abc', [[(0, 0), (0, 0)]], {'mode': ViewTestCase.INTERNAL_NORMAL_MODE},  [(0, 0), (0, 9)], first_sel, ''),  # FIXME # noqa: E501,E241
    # TODO: test multiline brackets, etc.
)


class Test__vi_percent(ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.view.sel().clear()

            self.write(data.initial_text)
            for region in data.regions:
                self.select(self._R(*region))

            self.view.run_command('_vi_percent', data.cmd_params)

            msg = "[{0}] {1}".format(i, data.msg)
            actual = data.actual_func(self)
            self.assertEqual(self._R(*data.expected), actual, msg)
