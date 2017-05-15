from NeoVintageous.lib.state import State

from NeoVintageous.tests.utils import ViewTestCase


class Test_ex_move_Moving_InNormalMode_SingleLine_DefaultStart(ViewTestCase):
    def test_can_move_default_line_range(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move3'})

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'abc\nabc\nxxx\nabc'
        self.assertEqual(expected, actual)

    def test_can_move_to_eof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move4'})

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'abc\nabc\nabc\nxxx'
        self.assertEqual(expected, actual)

    def test_can_move_to_bof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move0'})

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'xxx\nabc\nabc\nabc'
        self.assertEqual(expected, actual)

    def test_can_move_to_empty_line(self):
        self.write('abc\nxxx\nabc\n\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move4'})

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'abc\nabc\n\nxxx\nabc'
        self.assertEqual(expected, actual)

    def test_can_move_to_same_line(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'address': '2'})

        actual = self.view.substr(self.R(0, self.view.size()))
        expected = 'abc\nxxx\nabc\nabc'
        self.assertEqual(expected, actual)


class Test_ex_move_Moveing_InNormalMode_MultipleLines(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.range = {'left_ref': '.', 'left_offset': 0, 'left_search_offsets': [],
                      'right_ref': '.', 'right_offset': 1, 'right_search_offsets': []}

    def test_can_move_default_line_range(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move4'})

        expected = 'abc\nxxx\nabc\nxxx\nabc'
        actual = self.view.substr(self.R(0, self.view.size()))
        self.assertEqual(expected, actual)

    def test_can_move_to_eof(self):
        self.write('aaa\nxxx\nxxx\naaa\naaa')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move5'})

        expected = 'aaa\nxxx\naaa\naaa\nxxx'
        actual = self.view.substr(self.R(0, self.view.size()))
        self.assertEqual(expected, actual)

    def test_can_move_to_bof(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move0'})

        expected = 'xxx\nabc\nxxx\nabc\nabc'
        actual = self.view.substr(self.R(0, self.view.size()))
        self.assertEqual(expected, actual)

    def test_can_move_to_empty_line(self):
        self.write('aaa\nxxx\nxxx\naaa\n\naaa')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move5'})

        expected = 'aaa\nxxx\naaa\n\nxxx\naaa'
        actual = self.view.substr(self.R(0, self.view.size()))
        self.assertEqual(expected, actual)


class Test_ex_move_InNormalMode_CaretPosition(ViewTestCase):
    def test_can_reposition_caret(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

        self.view.run_command('ex_move', {'command_line': 'move3'})

        actual = list(self.view.sel())
        expected = [self.R((2, 0), (2, 0))]
        self.assertEqual(expected, actual)

    # TODO: test with multiple selections.


class Test_ex_move_ModeTransition(ViewTestCase):
    def test_from_normal_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(self.R((1, 0), (1, 0)))

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
        self.select(self.R((1, 0), (1, 1)))

        state = State(self.view)
        state.enter_visual_mode()
        prev_mode = state.mode

        self.view.run_command('ex_move', {'command_line': 'move3'})

        state = State(self.view)
        new_mode = state.mode
        self.assertNotEqual(prev_mode, new_mode)
