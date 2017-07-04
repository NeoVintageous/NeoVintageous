from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_e_InNormalMode(ViewTestCase):

    def test_move_to_end_of_word__on_last_line(self):
        self.write('abc\nabc\nabc')
        self.select(8)

        self.view.run_command('_vi_e', {'mode': self.NORMAL_MODE, 'count': 1})

        self.assertSelection(10)

    def test_move_to_end_of_word__on_middle_line__with_trailing_whitespace(self):
        self.write('abc\nabc   \nabc')
        self.select(6)

        self.view.run_command('_vi_e', {'mode': self.NORMAL_MODE, 'count': 1})

        self.assertSelection(13)

    def test_move_to_end_of_word__on_last_line__with_trailing_whitespace(self):
        self.write('abc\nabc\nabc   ')
        self.select(8)

        self.view.run_command('_vi_e', {'mode': self.NORMAL_MODE, 'count': 1})

        self.assertSelection(10)

        self.view.run_command('_vi_e', {'mode': self.NORMAL_MODE, 'count': 1})

        self.assertSelection(13)


class Test__vi_e_InVisualMode(ViewTestCase):

    def test_move_to_end_of_word__on_last_line2(self):
        self.write('abc abc abc')
        self.select((0, 2))

        self.view.run_command('_vi_e', {'mode': self.VISUAL_MODE, 'count': 3})

        self.assertSelection((0, 11))
