from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


# The heavy lifting is done by units.* functions, but we refine some cases in the actual motion
# command, so we need to test for that too here.
class Test__vi_e_InNormalMode(ViewTestCase):
    def test_move_to_end_of_word__on_last_line(self):
        self.write('abc\nabc\nabc')
        self.clear_sel()
        self.add_sel(self.R((2, 0), (2, 0)))

        self.view.run_command('_vi_e', {'mode': modes.NORMAL, 'count': 1})

        self.assertEqual(self.R((2, 2), (2, 2)), self.first_sel())

    def test_move_to_end_of_word__on_middle_line__with_trailing_whitespace(self):
        self.write('abc\nabc   \nabc')
        self.clear_sel()
        self.add_sel(self.R((1, 2), (1, 2)))

        self.view.run_command('_vi_e', {'mode': modes.NORMAL, 'count': 1})

        self.assertEqual(self.R((2, 2), (2, 2)), self.first_sel())

    def test_move_to_end_of_word__on_last_line__with_trailing_whitespace(self):
        self.write('abc\nabc\nabc   ')
        self.clear_sel()
        self.add_sel(self.R((2, 0), (2, 0)))

        self.view.run_command('_vi_e', {'mode': modes.NORMAL, 'count': 1})

        self.assertEqual(self.R((2, 2), (2, 2)), self.first_sel())

        self.view.run_command('_vi_e', {'mode': modes.NORMAL, 'count': 1})

        self.assertEqual(self.R((2, 5), (2, 5)), self.first_sel())


class Test__vi_e_InVisualMode(ViewTestCase):
    def test_move_to_end_of_word__on_last_line2(self):
        self.write('abc abc abc')
        self.clear_sel()
        self.add_sel(self.R(0, 2))
        self.view.run_command('_vi_e', {'mode': modes.VISUAL, 'count': 3})
        self.assertEqual(self.R((0, 0), (0, 11)), self.first_sel())
