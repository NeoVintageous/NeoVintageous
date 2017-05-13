from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_dd_InNormalMode(ViewTestCase):
    def test_deletes_last_line(self):
        self.write('abc\nabc\nabc')
        self.select(self.R((2, 0), (2, 0)))

        self.view.run_command('_vi_dd', {'mode': modes.INTERNAL_NORMAL})

        expected = self.view.substr(self.R(0, self.view.size()))
        self.assertEqual(expected, 'abc\nabc')
