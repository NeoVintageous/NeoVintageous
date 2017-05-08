from collections import namedtuple

from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


def get_text(self):
    return self.view.substr(self.R(0, self.view.size()))


test_data = namedtuple('test_data', 'cmd initial_text regions cmd_params expected actual_func msg')
region_data = namedtuple('region_data', 'regions')

TESTS_INTERNAL_NORMAL = (
    test_data(cmd='_vi_cc', initial_text='foo bar\nfoo bar\nfoo bar\n', regions=[[(1, 0), (1, 0)]],
              cmd_params={'mode': modes.INTERNAL_NORMAL}, expected='foo bar\n\nfoo bar\n', actual_func=get_text,  msg=''),
)


TESTS = TESTS_INTERNAL_NORMAL


class Test__vi_cc(ViewTestCase):
    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.view.sel().clear()

            self.write(data.initial_text)
            for region in data.regions:
                self.add_sel(self.R(*region))

            self.view.run_command(data.cmd, data.cmd_params)

            msg = "failed at test index {0} {1}".format(i, data.msg)
            actual = data.actual_func(self)

            if isinstance(data.expected, region_data):
                self.assertEqual(self.R(*data.expected.regions), actual, msg)
            else:
                self.assertEqual(data.expected, actual, msg)
