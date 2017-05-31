from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_g_InNormalMode(ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.selectRegion(a=0, b=0)

        self.view.run_command('_vi_big_g', {'mode': self.modes.NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(6, 6))

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.selectRegion(a=0, b=0)

        self.view.run_command('_vi_big_g', {'mode': self.modes.NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(8, 8))


class Test__vi_big_g_InVisualMode(ViewTestCase):

    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.selectRegion(a=0, b=1)

        self.view.run_command('_vi_big_g', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(0, 8))


class Test__vi_big_g_InInternalNormalMode(ViewTestCase):

    def test_can_move_in_mode_internal_normal(self):
        self.write('abc\nabc\n')
        self.select(self.R(1, 1))

        self.view.run_command('_vi_big_g', {'mode': self.modes.INTERNAL_NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(0, 8))

    def test_operates_linewise(self):
        self.write('abc\nabc\nabc\n')
        self.select(self.R((1, 0), (1, 1)))

        self.view.run_command('_vi_big_g', {'mode': self.modes.INTERNAL_NORMAL, 'count': 1})

        self.assertFirstSelection(self.R((0, 3), (2, 4)))


class Test__vi_big_g_InVisualLineMode(ViewTestCase):

    def test_can_move_in_mode_visual_line(self):
        self.write('abc\nabc\n')
        self.selectRegion(a=0, b=4)

        self.view.run_command('_vi_big_g', {'mode': self.modes.VISUAL_LINE, 'count': 1})

        self.assertFirstSelection(self.R(0, 8))
