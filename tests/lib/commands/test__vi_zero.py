from collections import namedtuple

from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


def first_sel(self):
    return self.first_sel()


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')

TESTS = (
    test_data('abc',      [[(0, 2), (0, 2)]], {'mode': modes.NORMAL}, [(0, 0), (0, 0)], first_sel, ''),
    test_data('abc',      [[(0, 2), (0, 2)]], {'mode': modes.INTERNAL_NORMAL}, [(0, 2), (0, 0)], first_sel, ''),
    test_data('abc\nabc', [[(0, 2), (1, 3)]], {'mode': modes.VISUAL},           [(0, 2), (1, 1)], first_sel, ''),
    test_data('abc\nabc', [[(1, 3), (0, 2)]], {'mode': modes.VISUAL},           [(1, 3), (0, 0)], first_sel, ''),

    # TODO: Test multiple sels.
)


class Test__vi_zero(ViewTestCase):
    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.view.sel().clear()

            self.write(data.initial_text)
            for region in data.regions:
                self.add_sel(self.R(*region))

            self.view.run_command('_vi_zero', data.cmd_params)

            msg = "[{0}] {1}".format(i, data.msg)
            actual = data.actual_func(self)
            self.assertEqual(self.R(*data.expected), actual, msg)
