from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_octothorp_InNormalMode(ViewTestCase):

    def test_select_match(self):
        self.write('abc\nabc')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(0, 0))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(0, 3), self.R(4, 7)])

    def test_select_match_middle(self):
        self.write('abc\nabc')
        self.select(self.R(5, 5))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(0, 0))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(0, 3), self.R(4, 7)])

    def test_select_match_end(self):
        self.write('abc\nabc')
        self.select(self.R(6, 6))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(0, 0))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(0, 3), self.R(4, 7)])

    def test_select_repeat_match(self):
        self.write('abc\nabc\nfoo\nabc\nbar')
        self.select(self.R(12, 12))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})
        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(0, 0))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(0, 3), self.R(4, 7), self.R(12, 15)])

    def test_select_wrap_match(self):
        self.write('boo\nabc\nfoo\nabc\nbar')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(12, 12))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15)])

    def test_select_no_partial_match(self):
        self.write('boo\nabc\nabcxabc\nabc\nbar')
        self.select(self.R(16, 16))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(16, 19)])

    def test_select_no_match(self):
        self.write('boo\nabc\nfoo\nabc\nbar')
        self.select(self.R(9, 9))

        self.view.run_command('_vi_octothorp', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(8, 8))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(8, 11)])
