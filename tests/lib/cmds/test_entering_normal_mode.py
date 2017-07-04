from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.state import State


class TestViEnterNormalModeSingleSelectionLeftRoRight(ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select((8, 11))
        State(self.view).mode = self.VISUAL_MODE

        self.view.run_command('_enter_normal_mode', {'mode': self.VISUAL_MODE})

        self.assertSelection(10)


class TestViEnterNormalModeSingleSelectionRightToLeft(ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select((11, 8))
        self.state.mode = self.VISUAL_MODE

        self.view.run_command('_enter_normal_mode', {'mode': self.VISUAL_MODE})

        self.assertSelection(8)


class TestViEnterNormalModeMulipleSelectionsFromSelectMode(ViewTestCase):

    def test_carets_end_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([(8, 11), (16, 19)])
        State(self.view).mode = self.SELECT_MODE

        self.view.run_command('_enter_normal_mode', {'mode': self.SELECT_MODE})

        self.assertSelection([self.Region(8), self.Region(16)])


class TestViEnterNormalModeMulipleSelectionsFromNormalMode(ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([8, 16])
        State(self.view).mode = self.NORMAL_MODE

        self.view.run_command('_enter_normal_mode', {'mode': self.NORMAL_MODE})

        self.assertSelection(8)
