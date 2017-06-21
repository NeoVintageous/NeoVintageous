from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_g_g_InNormalMode(ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.select(self.R(5, 5))

        self.view.run_command('_vi_gg', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(0, 0))

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.select(self.R(5, 5))

        self.view.run_command('_vi_gg', {'mode': self.modes.NORMAL})

        self.assertFirstSelection(self.R(0, 0))


class Test__vi_g_g_InVisualMode(ViewTestCase):

    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.select(self.R((0, 1), (0, 2)))

        self.view.run_command('_vi_gg', {'mode': self.modes.VISUAL})

        self.assertFirstSelection(self.R((0, 2), (0, 0)))

    def test_can_move_in_visual_mode__reversed(self):
        self.write('abc\nabc\n')
        self.select(self.R((0, 2), (0, 1)))

        self.view.run_command('_vi_gg', {'mode': self.modes.VISUAL})

        self.assertFirstSelection(self.R((0, 2), (0, 0)))


class Test__vi_g_g_InInternalNormalMode(ViewTestCase):

    def test_can_move_in_mode_internal_normal(self):
        self.write('abc\nabc\n')
        self.select(self.R(1, 1))

        self.view.run_command('_vi_gg', {'mode': self.modes.INTERNAL_NORMAL})

        self.assertFirstSelection(self.R(4, 0))


class Test__vi_g_g_InVisualLineMode(ViewTestCase):

    def test_can_move_in_mode_visual_line(self):
        self.write('abc\nabc\n')
        self.select(self.R((0, 0), (0, 4)))

        self.view.run_command('_vi_gg', {'mode': self.modes.VISUAL_LINE})

        self.assertFirstSelection(self.R((0, 0), (0, 4)))

    def test_extends_selection(self):
        self.write('abc\nabc\n')
        self.select(self.R((0, 4), (0, 8)))

        self.view.run_command('_vi_gg', {'mode': self.modes.VISUAL_LINE})

        self.assertFirstSelection(self.R((0, 0), (0, 8)))
