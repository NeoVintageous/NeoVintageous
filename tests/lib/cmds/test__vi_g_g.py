from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_g_g_InNormalMode(ViewTestCase):
    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.clear_sel()
        self.add_sel(self.R(5, 5))

        self.view.run_command('_vi_gg', {'mode': modes.NORMAL})
        self.assertEqual(self.R(0, 0), self.first_sel())

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R(5, 5))

        self.view.run_command('_vi_gg', {'mode': modes.NORMAL})
        self.assertEqual(self.R(0, 0), self.first_sel())


class Test__vi_g_g_InVisualMode(ViewTestCase):
    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R((0, 1), (0, 2)))

        self.view.run_command('_vi_gg', {'mode': modes.VISUAL})
        self.assertEqual(self.R((0, 2), (0, 0)), self.first_sel())

    def test_can_move_in_visual_mode__reversed(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R((0, 2), (0, 1)))

        self.view.run_command('_vi_gg', {'mode': modes.VISUAL})
        self.assertEqual(self.R((0, 2), (0, 0)), self.first_sel())


class Test__vi_g_g_InInternalNormalMode(ViewTestCase):
    def test_can_move_in_mode_internal_normal(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R(1, 1))

        self.view.run_command('_vi_gg', {'mode': modes.INTERNAL_NORMAL})
        self.assertEqual(self.R(4, 0), self.first_sel())


class Test__vi_g_g_InVisualLineMode(ViewTestCase):
    def test_can_move_in_mode_visual_line(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R((0, 0), (0, 4)))

        self.view.run_command('_vi_gg', {'mode': modes.VISUAL_LINE})
        self.assertEqual(self.R((0, 0), (0, 4)), self.first_sel())

    def test_extends_selection(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R((0, 4), (0, 8)))

        self.view.run_command('_vi_gg', {'mode': modes.VISUAL_LINE})
        self.assertEqual(self.R((0, 0), (0, 8)), self.first_sel())
