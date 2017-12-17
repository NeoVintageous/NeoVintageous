from NeoVintageous.tests import unittest


class Test__vi_big_a_InNormalMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select(2)

        self.view.run_command('_vi_big_a', {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection(3)


class Test__vi_big_a_InNormalMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(1, 1), (5, 5)])

        self.view.run_command('_vi_big_a', {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection([self.Region(3), self.Region(7)])


class Test__vi_big_a_InVisualMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('_vi_big_a', {'mode': unittest.VISUAL_MODE, 'count': 1})

        self.assertSelection(2)


class Test__vi_big_a_InVisualMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 2), (4, 6)])

        self.view.run_command('_vi_big_a', {'mode': unittest.VISUAL_MODE, 'count': 1})

        self.assertSelection([self.Region(2), self.Region(6)])


class Test__vi_big_a_InVisualLineMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 3))

        self.view.run_command('_vi_big_a', {'mode': unittest.VISUAL_LINE_MODE, 'count': 1})

        self.assertSelection(3)


class Test__vi_big_a_InVisualLineMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 4), (4, 7)])

        self.view.run_command('_vi_big_a', {'mode': unittest.VISUAL_LINE_MODE, 'count': 1})

        self.assertSelection([self.Region(3), self.Region(7)])


class Test__vi_big_a_InVisualBlockMode_SingleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('_vi_big_a', {'mode': unittest.VISUAL_BLOCK_MODE, 'count': 1})

        self.assertSelection(2)


class Test__vi_big_a_InVisualBlockMode_MultipleSel(unittest.ViewTestCase):

    def test_moves_caret_to_eol(self):
        self.write('abc\nabc')
        self.select([(0, 2), (4, 6)])

        self.view.run_command('_vi_big_a', {'mode': unittest.VISUAL_BLOCK_MODE, 'count': 1})

        self.assertSelection([self.Region(2), self.Region(6)])
