from NeoVintageous.tests import unittest


class Test__vi_dd_InNormalMode(unittest.ViewTestCase):

    def test_deletes_last_line(self):
        self.write('abc\nabc\nabc')
        self.select(8)

        self.view.run_command('_vi_dd', {'mode': unittest.INTERNAL_NORMAL})

        self.assertContent('abc\nabc')
