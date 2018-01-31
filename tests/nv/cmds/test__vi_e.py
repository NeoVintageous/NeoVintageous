from NeoVintageous.tests import unittest


class Test__vi_e_InNormalMode(unittest.ViewTestCase):

    def test_move_to_end_of_word__on_last_line(self):
        self.write('abc\nabc\nabc')
        self.select(8)

        self.view.run_command('_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(10)

    def test_move_to_end_of_word__on_middle_line__with_trailing_whitespace(self):
        self.write('abc\nabc   \nabc')
        self.select(6)

        self.view.run_command('_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(13)

    def test_move_to_end_of_word__on_last_line__with_trailing_whitespace(self):
        self.write('abc\nabc\nabc   ')
        self.select(8)

        self.view.run_command('_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(10)

        self.view.run_command('_vi_e', {'mode': unittest.NORMAL, 'count': 1})

        self.assertSelection(13)


class Test__vi_e_InVisualMode(unittest.ViewTestCase):

    def test_move_to_end_of_word__on_last_line2(self):
        self.write('abc abc abc')
        self.select((0, 2))

        self.view.run_command('_vi_e', {'mode': unittest.VISUAL, 'count': 3})

        self.assertSelection((0, 11))
