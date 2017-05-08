from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_g_InNormalMode(ViewTestCase):
    def test_can_move_in_normal_mode(self):
        self.write('abc\nabc')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_big_g', {'mode': modes.NORMAL, 'count': 1})
        self.assertEqual(self.R(6, 6), self.first_sel())

    def test_go_to_hard_eof_if_last_line_is_empty(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_big_g', {'mode': modes.NORMAL, 'count': 1})
        self.assertEqual(self.R(8, 8), self.first_sel())


class Test__vi_big_g_InVisualMode(ViewTestCase):
    def test_can_move_in_visual_mode(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(a=0, b=1)

        self.view.run_command('_vi_big_g', {'mode': modes.VISUAL, 'count': 1})
        self.assertEqual(self.R(0, 8), self.first_sel())


class Test__vi_big_g_InInternalNormalMode(ViewTestCase):
    def test_can_move_in_mode_internal_normal(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R(1, 1))

        self.view.run_command('_vi_big_g', {'mode': modes.INTERNAL_NORMAL, 'count': 1})
        self.assertEqual(self.R(0, 8), self.first_sel())

    def test_operates_linewise(self):
        self.write('abc\nabc\nabc\n')
        self.clear_sel()
        self.add_sel(self.R((1, 0), (1, 1)))

        self.view.run_command('_vi_big_g', {'mode': modes.INTERNAL_NORMAL, 'count': 1})
        self.assertEqual(self.R((0, 3), (2, 4)), self.first_sel())


class Test__vi_big_g_InVisualLineMode(ViewTestCase):
    def test_can_move_in_mode_visual_line(self):
        self.write('abc\nabc\n')
        self.clear_sel()
        self.add_sel(a=0, b=4)

        self.view.run_command('_vi_big_g', {'mode': modes.VISUAL_LINE, 'count': 1})
        self.assertEqual(self.R(0, 8), self.first_sel())
