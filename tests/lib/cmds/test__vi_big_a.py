from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_a_InNormalMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(self.R(0, 2))

        self.view.run_command('_vi_big_a', {'mode': self.modes.INTERNAL_NORMAL, 'count': 1})
        self.assertFirstSelection(self.R(3, 3))


class Test__vi_big_a_InNormalMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.selectMultiple([self.R((0, 1), (0, 1)), self.R((1, 1), (1, 1))])

        self.view.run_command('_vi_big_a', {'mode': self.modes.INTERNAL_NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(3, 3))
        self.assertSecondSelection(self.R((1, 3), (1, 3)))


class Test__vi_big_a_InVisualMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(self.R((0, 0), (0, 2)))

        self.view.run_command('_vi_big_a', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(2, 2))


class Test__vi_big_a_InVisualMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.selectMultiple([self.R((0, 0), (0, 2)), self.R((1, 1), (1, 2))])

        self.view.run_command('_vi_big_a', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(2, 2))
        self.assertSecondSelection(self.R((1, 2), (1, 2)))


class Test__vi_big_a_InVisualLineMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(self.R((0, 0), (0, 3)))

        self.view.run_command('_vi_big_a', {'mode': self.modes.VISUAL_LINE, 'count': 1})

        self.assertFirstSelection(self.R(3, 3))


class Test__vi_big_a_InVisualLineMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.selectMultiple([self.R((0, 0), (0, 4)), self.R((1, 0), (1, 3))])

        self.view.run_command('_vi_big_a', {'mode': self.modes.VISUAL_LINE, 'count': 1})

        self.assertFirstSelection(self.R(3, 3))
        self.assertSecondSelection(self.R((1, 3), (1, 3)))


class Test__vi_big_a_InVisualBlockMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(self.R((0, 0), (0, 2)))

        self.view.run_command('_vi_big_a', {'mode': self.modes.VISUAL_BLOCK, 'count': 1})

        self.assertFirstSelection(self.R(2, 2))


class Test__vi_big_a_InVisualBlockMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.selectMultiple([self.R((0, 0), (0, 2)), self.R((1, 0), (1, 2))])

        self.view.run_command('_vi_big_a', {'mode': self.modes.VISUAL_BLOCK, 'count': 1})

        self.assertFirstSelection(self.R(2, 2))
        self.assertSecondSelection(self.R((1, 2), (1, 2)))
