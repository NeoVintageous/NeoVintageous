from NeoVintageous.tests import unittest

from NeoVintageous.lib.state import State


class TestViEnterNormalModeSingleSelectionLeftRoRight(unittest.ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select((8, 11))
        State(self.view).mode = unittest.VISUAL_MODE

        self.view.run_command('_enter_normal_mode', {'mode': unittest.VISUAL_MODE})

        self.assertSelection(10)


class TestViEnterNormalModeSingleSelectionRightToLeft(unittest.ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select((11, 8))
        self.state.mode = unittest.VISUAL_MODE

        self.view.run_command('_enter_normal_mode', {'mode': unittest.VISUAL_MODE})

        self.assertSelection(8)


class TestViEnterNormalModeMulipleSelectionsFromSelectMode(unittest.ViewTestCase):

    def test_carets_end_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([(8, 11), (16, 19)])
        State(self.view).mode = unittest.SELECT_MODE

        self.view.run_command('_enter_normal_mode', {'mode': unittest.SELECT_MODE})

        self.assertSelection([self.Region(8), self.Region(16)])


class TestViEnterNormalModeMulipleSelectionsFromNormalMode(unittest.ViewTestCase):

    def test_caret_ends_in_expected_region(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([8, 16])
        State(self.view).mode = unittest.NORMAL_MODE

        self.view.run_command('_enter_normal_mode', {'mode': unittest.NORMAL_MODE})

        self.assertSelection(8)
