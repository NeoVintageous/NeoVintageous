from NeoVintageous.lib.state import State

from NeoVintageous.tests.utils import ViewTestCase


class TestViEnterNormalModeSingleSelectionLeftRoRight(ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.clear_sel()
        self.add_sel(self.R((1, 0), (1, 3)))

        State(self.view).mode = self.modes.VISUAL

        self.view.run_command('_enter_normal_mode', {'mode': self.modes.VISUAL})
        self.assertEqual(self.R((1, 2), (1, 2)), self.first_sel())


class TestViEnterNormalModeSingleSelectionRightToLeft(ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write(''.join(('foo bar\nfoo bar\nfoo bar\n',)))
        self.clear_sel()
        self.add_sel(self.R((1, 3), (1, 0)))

        self.state.mode = self.modes.VISUAL

        self.view.run_command('_enter_normal_mode', {'mode': self.modes.VISUAL})
        self.assertEqual(self.R((1, 0), (1, 0)), self.first_sel())


class TestViEnterNormalModeMulipleSelectionsFromSelectMode(ViewTestCase):

    def test_carets_end_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.clear_sel()
        self.add_sel(self.R((1, 0), (1, 3)))
        self.add_sel(self.R((2, 0), (2, 3)))

        State(self.view).mode = self.modes.SELECT

        self.view.run_command('_enter_normal_mode', {'mode': self.modes.SELECT})
        self.assertEqual(self.R((1, 0), (1, 0)), self.first_sel())
        self.assertEqual(self.R((2, 0), (2, 0)), self.second_sel())
        self.assertEqual(2, self.num_sels())


class TestViEnterNormalModeMulipleSelectionsFromNormalMode(ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.clear_sel()
        self.add_sel(self.R((1, 0), (1, 0)))
        self.add_sel(self.R((2, 0), (2, 0)))

        State(self.view).mode = self.modes.NORMAL

        self.view.run_command('_enter_normal_mode', {'mode': self.modes.NORMAL})
        self.assertEqual(self.R((1, 0), (1, 0)), self.first_sel())
        self.assertEqual(1, self.num_sels())
