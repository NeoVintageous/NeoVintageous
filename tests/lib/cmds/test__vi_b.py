from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


def first_sel(self):
    return self.view.sel()[0]


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')


TESTS_NORMAL_MODE_SINGLE_SEL = (
    test_data(initial_text='abc',     regions=[[(0, 2), (0, 2)]], cmd_params={'mode': ViewTestCase.modes.NORMAL},  expected=[(0, 0), (0, 0)], actual_func=first_sel,  msg=''),
    test_data(initial_text='abc abc', regions=[[(0, 4), (0, 4)]], cmd_params={'mode': ViewTestCase.modes.NORMAL},  expected=[(0, 0), (0, 0)], actual_func=first_sel,  msg=''),
    test_data(initial_text='abc a',   regions=[[(0, 4), (0, 4)]], cmd_params={'mode': ViewTestCase.modes.NORMAL},  expected=[(0, 0), (0, 0)], actual_func=first_sel,  msg=''),
)

TESTS_VISUAL_MODE_SINGLE_SEL_START_LEN_1 = (
    test_data(initial_text='abc',   regions=[[(0, 2), (0, 3)]], cmd_params={'mode': ViewTestCase.modes.VISUAL},  expected=[(0, 3), (0, 0)], actual_func=first_sel,  msg=''),
    test_data(initial_text='abc a', regions=[[(0, 4), (0, 5)]], cmd_params={'mode': ViewTestCase.modes.VISUAL},  expected=[(0, 5), (0, 0)], actual_func=first_sel,  msg=''),
)

TESTS = TESTS_NORMAL_MODE_SINGLE_SEL + TESTS_VISUAL_MODE_SINGLE_SEL_START_LEN_1


class Test__vi_b(ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.initial_text)
            self.select([self.R(*region) for region in data.regions])

            self.view.run_command('_vi_b', data.cmd_params)
            actual = data.actual_func(self)

            self.assertEqual(self.R(*data.expected), actual, "failed at test index {0} {1}".format(i, data.msg))
