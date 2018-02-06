from NeoVintageous.tests import unittest


class Test_ex_delete_Deleting_InNormalMode_SingleLine_DefaultStart(unittest.ViewTestCase):

    def test_can_delete_default_line_range(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_delete', {'command_line': 'delete'})

        self.assertContent('abc\nabc\nabc')

    def test_can_delete_at_eof__no_new_line(self):
        self.write('abc\nabc\nabc\nxxx')
        self.select(12)

        self.view.run_command('ex_delete', {'command_line': '4delete'})

        self.assertContent('abc\nabc\nabc\n')

    def test_can_delete_at_eof__new_line(self):
        self.write('abc\nabc\nabc\nxxx\n')
        self.select(12)

        self.view.run_command('ex_delete', {'command_line': 'delete'})

        self.assertContent('abc\nabc\nabc\n')

    def test_can_delete_zero_line_range(self):
        self.write('xxx\nabc\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_delete', {'command_line': '0delete'})

        self.assertContent('abc\nabc\nabc')

    def test_can_delete_empty_line(self):
        self.write('abc\nabc\n\nabc')
        self.select(4)

        self.view.run_command('ex_delete', {'command_line': '3delete'})

        self.assertContent('abc\nabc\nabc')


class Test_ex_delete_Deleting_InNormalMode_MultipleLines(unittest.ViewTestCase):

    def test_can_delete_two_lines(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(0)

        self.view.run_command('ex_delete', {'command_line': '2,3delete'})

        self.assertContent('abc\nabc\nabc')

    def test_can_delete_three_lines(self):
        self.write('abc\nxxx\nxxx\nxxx\nabc\nabc')
        self.select(0)

        self.view.run_command('ex_delete', {'command_line': '2,4delete'})

        self.assertContent('abc\nabc\nabc')

    def test_can_delete_multiple_empty_lines(self):
        self.write('abc\n\n\n\nabc\nabc')
        self.select(0)

        self.view.run_command('ex_delete', {'command_line': '2,4delete'})

        self.assertContent('abc\nabc\nabc')


# TODO: test with multiple selections.
class Test_ex_delete_InNormalMode_CaretPosition(unittest.ViewTestCase):

    def test_can_reposition_caret(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(12)

        self.view.run_command('ex_delete', {'command_line': '2,4delete'})

        self.assertSelection(4)


class Test_ex_delete_ModeTransition(unittest.ViewTestCase):

    def test_from_normal_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_delete', {'command_line': '2delete'})

        self.assertNormalMode()

    def test_from_visual_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select((4, 5))

        self.view.run_command('ex_delete', {'command_line': "'<,'>delete"})

        self.assertNormalMode()
