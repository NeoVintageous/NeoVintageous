from NeoVintageous.tests import unittest

from NeoVintageous.lib.state import State


class Test_ex_copy_Copying_InNormalMode_SingleLine_DefaultStart(unittest.ViewTestCase):

    def test_can_copy_default_line_range(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': 'copy3'})

        self.assertContent('abc\nxxx\nabc\nxxx\nabc')

    def test_can_copy_to_eof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': 'copy4'})

        self.assertContent('abc\nxxx\nabc\nabc\nxxx')

    def test_can_copy_to_bof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': 'copy0'})

        self.assertContent('xxx\nabc\nxxx\nabc\nabc')

    def test_can_copy_to_empty_line(self):
        self.write('abc\nxxx\nabc\n\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': 'copy4'})

        self.assertContent('abc\nxxx\nabc\n\nxxx\nabc')

    def test_can_copy_to_same_line(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': 'copy2'})

        self.assertContent('abc\nxxx\nxxx\nabc\nabc')


class Test_ex_copy_Copying_InNormalMode_MultipleLines(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.range = {'left_ref': '.', 'left_offset': 0, 'left_search_offsets': [],
                      'right_ref': '.', 'right_offset': 1, 'right_search_offsets': []}

    def test_can_copy_default_line_range(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': '.,.+1copy4'})

        self.assertContent('abc\nxxx\nxxx\nabc\nxxx\nxxx\nabc')

    def test_can_copy_to_eof(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': '.,.+1copy5'})

        self.assertContent('abc\nxxx\nxxx\nabc\nabc\nxxx\nxxx')

    def test_can_copy_to_bof(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': '.,.+1copy0'})

        self.assertContent('xxx\nxxx\nabc\nxxx\nxxx\nabc\nabc')

    def test_can_copy_to_empty_line(self):
        self.write('abc\nxxx\nxxx\nabc\n\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': '.,.+1copy5'})

        self.assertContent('abc\nxxx\nxxx\nabc\n\nxxx\nxxx\nabc')

    def test_can_copy_to_same_line(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': '.,.+1copy2'})

        self.assertContent('abc\nxxx\nxxx\nxxx\nxxx\nabc\nabc')


class Test_ex_copy_InNormalMode_CaretPosition(unittest.ViewTestCase):

    def test_can_reposition_caret(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        self.view.run_command('ex_copy', {'command_line': 'copy3'})

        self.assertSelection(12)


class Test_ex_copy_ModeTransition(unittest.ViewTestCase):

    def test_from_normal_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)

        state = State(self.view)
        state.enter_normal_mode()

        self.view.run_command('vi_enter_normal_mode')
        prev_mode = state.mode

        self.view.run_command('ex_copy', {'address': '3'})

        state = State(self.view)
        new_mode = state.mode
        self.assertEqual(prev_mode, new_mode, unittest.NORMAL_MODE)

    def test_from_visual_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select((4, 5))

        state = State(self.view)
        state.enter_visual_mode()
        prev_mode = state.mode

        self.view.run_command('ex_copy', {'command_line': 'copy3'})

        state = State(self.view)
        new_mode = state.mode
        self.assertNotEqual(prev_mode, new_mode)
        self.assertEqual(new_mode, unittest.NORMAL_MODE)
