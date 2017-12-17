from NeoVintageous.tests import unittest

from NeoVintageous.lib.state import State


class Test_ex_move_Moving_InNormalMode_SingleLine_DefaultStart(unittest.ViewTestCase):

    def test_can_move_default_line_range(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move3'})

        self.assertContent('abc\nabc\nxxx\nabc')

    def test_can_move_to_eof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move4'})

        self.assertContent('abc\nabc\nabc\nxxx')

    def test_can_move_to_bof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move0'})

        self.assertContent('xxx\nabc\nabc\nabc')

    def test_can_move_to_empty_line(self):
        self.write('abc\nxxx\nabc\n\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move4'})

        self.assertContent('abc\nabc\n\nxxx\nabc')

    def test_can_move_to_same_line(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'address': '2'})

        self.assertContent('abc\nxxx\nabc\nabc')


class Test_ex_move_Moveing_InNormalMode_MultipleLines(unittest.ViewTestCase):

    def test_can_move_default_line_range(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move4'})

        self.assertContent('abc\nxxx\nabc\nxxx\nabc')

    def test_can_move_to_eof(self):
        self.write('aaa\nxxx\nxxx\naaa\naaa')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move5'})

        self.assertContent('aaa\nxxx\naaa\naaa\nxxx')

    def test_can_move_to_bof(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move0'})

        self.assertContent('xxx\nabc\nxxx\nabc\nabc')

    def test_can_move_to_empty_line(self):
        self.write('aaa\nxxx\nxxx\naaa\n\naaa')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move5'})

        self.assertContent('aaa\nxxx\naaa\n\nxxx\naaa')


# TODO: test with multiple selections.
class Test_ex_move_InNormalMode_CaretPosition(unittest.ViewTestCase):

    def test_can_reposition_caret(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_move', {'command_line': 'move3'})

        self.assertSelection(8)


class Test_ex_move_ModeTransition(unittest.ViewTestCase):

    def test_from_normal_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        state = State(self.view)
        state.enter_normal_mode()

        self.view.run_command('vi_enter_normal_mode')
        prev_mode = state.mode

        self.view.run_command('ex_move', {'address': '3'})

        state = State(self.view)
        new_mode = state.mode
        self.assertEqual(prev_mode, new_mode)

    def test_from_visual_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select((4, 5))

        state = State(self.view)
        state.enter_visual_mode()
        prev_mode = state.mode

        self.view.run_command('ex_move', {'command_line': 'move3'})

        state = State(self.view)
        new_mode = state.mode
        self.assertNotEqual(prev_mode, new_mode)
