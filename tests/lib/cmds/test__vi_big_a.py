from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_a_InNormalMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(2)

        self.view.run_command('_vi_big_a', {'mode': self.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection(3)


class Test__vi_big_a_InNormalMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(1, 1), (5, 5)])

        self.view.run_command('_vi_big_a', {'mode': self.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection([self.Region(3), self.Region(7)])


class Test__vi_big_a_InVisualMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('_vi_big_a', {'mode': self.VISUAL_MODE, 'count': 1})

        self.assertSelection(2)


class Test__vi_big_a_InVisualMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 2), (4, 6)])

        self.view.run_command('_vi_big_a', {'mode': self.VISUAL_MODE, 'count': 1})

        self.assertSelection([self.Region(2), self.Region(6)])


class Test__vi_big_a_InVisualLineMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 3))

        self.view.run_command('_vi_big_a', {'mode': self.VISUAL_LINE_MODE, 'count': 1})

        self.assertSelection(3)


class Test__vi_big_a_InVisualLineMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 4), (4, 7)])

        self.view.run_command('_vi_big_a', {'mode': self.VISUAL_LINE_MODE, 'count': 1})

        self.assertSelection([self.Region(3), self.Region(7)])


class Test__vi_big_a_InVisualBlockMode_SingleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('_vi_big_a', {'mode': self.VISUAL_BLOCK_MODE, 'count': 1})

        self.assertSelection(2)


class Test__vi_big_a_InVisualBlockMode_MultipleSel(ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 2), (4, 6)])

        self.view.run_command('_vi_big_a', {'mode': self.VISUAL_BLOCK_MODE, 'count': 1})

        self.assertSelection([self.Region(2), self.Region(6)])
