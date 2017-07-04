from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_g_g_InNormalMode(ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.select(5)

        self.view.run_command('_vi_gg', {'mode': self.NORMAL_MODE})

        self.assertSelection(0)

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.select(5)

        self.view.run_command('_vi_gg', {'mode': self.NORMAL_MODE})

        self.assertSelection(0)


class Test__vi_g_g_InVisualMode(ViewTestCase):

    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.select((1, 2))

        self.view.run_command('_vi_gg', {'mode': self.VISUAL_MODE})

        self.assertSelection((2, 0))

    def test_can_move_in_visual_mode__reversed(self):
        self.write('abc\nabc\n')
        self.select((2, 1))

        self.view.run_command('_vi_gg', {'mode': self.VISUAL_MODE})

        self.assertSelection((2, 0))


class Test__vi_g_g_InInternalNormalMode(ViewTestCase):

    def test_can_move_in_mode_internal_normal(self):
        self.write('abc\nabc\n')
        self.select(1)

        self.view.run_command('_vi_gg', {'mode': self.INTERNAL_NORMAL_MODE})

        self.assertSelection((4, 0))


class Test__vi_g_g_InVisualLineMode(ViewTestCase):

    def test_can_move_in_mode_visual_line(self):
        self.write('abc\nabc\n')
        self.select((0, 4))

        self.view.run_command('_vi_gg', {'mode': self.VISUAL_LINE_MODE})

        self.assertSelection((0, 4))

    def test_extends_selection(self):
        self.write('abc\nabc\n')
        self.select((4, 8))

        self.view.run_command('_vi_gg', {'mode': self.VISUAL_LINE_MODE})

        self.assertSelection((0, 8))
