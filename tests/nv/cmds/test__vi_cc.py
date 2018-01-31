from NeoVintageous.tests import unittest


class Test__vi_cc(unittest.ViewTestCase):

    def test_cc(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([self._R(*region) for region in [[(0, 0), (1, 0)]]])

        self.view.run_command('_vi_cc', {'mode': unittest.INTERNAL_NORMAL})

        self.assertContent('foo bar\n\nfoo bar\n')
