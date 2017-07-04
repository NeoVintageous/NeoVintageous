from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_dd_InNormalMode(ViewTestCase):

    def test_deletes_last_line(self):
        self.write('abc\nabc\nabc')
        self.select(8)

        self.view.run_command('_vi_dd', {'mode': self.INTERNAL_NORMAL_MODE})

        self.assertContent('abc\nabc')
