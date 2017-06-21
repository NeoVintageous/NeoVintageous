from NeoVintageous.tests.utils import ViewTestCase


# XXX: Am I using the best way to test this?
class Test__vi_ctrl_r(ViewTestCase):

    def test_does_not_linger_past_soft_eol(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('_vi_dd', {'mode': self.modes.INTERNAL_NORMAL})
        self.view.window().run_command('_vi_u')
        self.view.window().run_command('_vi_ctrl_r')  # passing mode is irrelevant

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'abc\nabc\nabc'
        self.assertEqual(expected, actual)
        actual_sel = self.view.sel()[0]
        self.assertEqual(self.R((1, 0), (1, 0)), actual_sel)

    def test_does_not_linger_past_soft_eol2(self):
        self.write('abc\nxxx foo bar\nabc\nabc')
        self.select(self.R((1, 8), (1, 8)))

        self.view.run_command('_vi_big_d', {'mode': self.modes.INTERNAL_NORMAL})
        self.view.window().run_command('_vi_u')
        self.view.window().run_command('_vi_ctrl_r')  # passing mode is irrelevant

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'abc\nxxx foo \nabc\nabc'
        self.assertEqual(expected, actual)
        actual_sel = self.view.sel()[0]
        self.assertEqual(self.R((1, 7), (1, 7)), actual_sel)
