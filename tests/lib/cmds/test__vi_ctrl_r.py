from NeoVintageous.tests.utils import ViewTestCase


# XXX: Am I using the best way to test this?
class Test__vi_ctrl_r(ViewTestCase):

    def test_does_not_linger_past_soft_eol(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('_vi_dd', {'mode': self.INTERNAL_NORMAL_MODE})
        self.view.window().run_command('_vi_u')
        self.view.window().run_command('_vi_ctrl_r')  # passing mode is irrelevant

        self.assertContent('abc\nabc\nabc')
        self.assertSelection(4)

    def test_does_not_linger_past_soft_eol2(self):
        self.write('abc\nxxx foo bar\nabc\nabc')
        self.select(12)

        self.view.run_command('_vi_big_d', {'mode': self.INTERNAL_NORMAL_MODE})
        self.view.window().run_command('_vi_u')
        self.view.window().run_command('_vi_ctrl_r')  # passing mode is irrelevant

        self.assertContent('abc\nxxx foo \nabc\nabc')
        self.assertSelection(11)
