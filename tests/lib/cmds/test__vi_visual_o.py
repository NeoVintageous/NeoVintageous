from NeoVintageous.tests import unittest


class Test__vi_visual_o_InNormalMode(unittest.ViewTestCase):

    def test_doesnt_do_anything(self):
        self.write('abc')
        self.select((2, 0))

        self.view.run_command('_vi_visual_o', {'mode': unittest.NORMAL_MODE, 'count': 1})

        self.assertSelection((2, 0))


class Test__vi_visual_o_InInternalNormalMode(unittest.ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc')
        self.select((2, 0))

        self.view.run_command('_vi_visual_o', {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1})

        self.assertSelection((2, 0))


class Test__vi_visual_o_InVisualMode(unittest.ViewTestCase):

    def test_can_move(self):
        self.write('abc')
        self.select((0, 2))

        self.view.run_command('_vi_visual_o', {'mode': unittest.VISUAL_MODE, 'count': 1})

        self.assertSelection((2, 0))


class Test__vi_visual_o_InVisualLineMode(unittest.ViewTestCase):

    def test_can_move(self):
        self.write('abc\ndef')
        self.select((0, 4))

        self.view.run_command('_vi_visual_o', {'mode': unittest.VISUAL_LINE_MODE, 'count': 1})

        self.assertSelection((4, 0))
