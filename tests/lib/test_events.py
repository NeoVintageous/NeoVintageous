import sublime

from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.events import _Context
from NeoVintageous.lib.state import State


class MockState():
    def __init__(self, mode):
        self.mode = mode


class TestKeyContext(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.context = _Context(self.view)

    def test_doesnt_handle_invalid_keys(self):
        self.assertIsNone(self.context.query('foobar', sublime.OP_EQUAL, True, True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_EQUAL, True, False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_EQUAL, False, False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_EQUAL, False, True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_EQUAL, True, True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_EQUAL, True, False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_EQUAL, False, False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_EQUAL, False, True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_REGEX_MATCH, '.*', True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_REGEX_MATCH, '.*', True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_REGEX_CONTAINS, '.*', True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_REGEX_CONTAINS, '.*', False))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_REGEX_CONTAINS, '.*', True))
        self.assertIsNone(self.context.query('foobar', sublime.OP_NOT_REGEX_CONTAINS, '.*', False))

    def test_vi_mode_normal(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL_INSERT)
        self.assertIsNone(self.context.query('vi_mode_normal', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_normal', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_normal', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_normal', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_normal', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_normal', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_normal', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_normal', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_normal', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_normal', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_normal', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_normal', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_mode_insert(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_insert', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_insert', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_insert', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_insert', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_insert', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_insert', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.INSERT)
        self.assertIsNone(self.context.query('vi_mode_insert', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_insert', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_insert', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_insert', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_insert', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_insert', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_mode_visual(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_visual', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_visual', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_visual', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_visual', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_visual', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_visual', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.VISUAL)
        self.assertIsNone(self.context.query('vi_mode_visual', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_visual', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_visual', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_visual', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_visual', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_visual', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_mode_normal_insert(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_normal_insert', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_normal_insert', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_normal_insert', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_normal_insert', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_normal_insert', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_normal_insert', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.NORMAL_INSERT)
        self.assertIsNone(self.context.query('vi_mode_normal_insert', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_normal_insert', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_normal_insert', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_normal_insert', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_normal_insert', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_normal_insert', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_mode_visual_block(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_visual_block', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_visual_block', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_visual_block', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_visual_block', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_visual_block', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_visual_block', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.VISUAL_BLOCK)
        self.assertIsNone(self.context.query('vi_mode_visual_block', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_visual_block', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_visual_block', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_visual_block', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_visual_block', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_visual_block', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_mode_visual_line(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_visual_line', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_visual_line', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_visual_line', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_visual_line', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_visual_line', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_visual_line', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.VISUAL_LINE)
        self.assertIsNone(self.context.query('vi_mode_visual_line', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_visual_line', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_visual_line', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_visual_line', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_visual_line', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_visual_line', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_mode_select(self):
        self.context.state = MockState(ViewTestCase.modes.NORMAL)
        self.assertIsNone(self.context.query('vi_mode_select', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_select', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertFalse(self.context.query('vi_mode_select', sublime.OP_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_select', sublime.OP_EQUAL, False, False))
        self.assertTrue(self.context.query('vi_mode_select', sublime.OP_NOT_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_select', sublime.OP_NOT_EQUAL, False, False))
        self.context.state = MockState(ViewTestCase.modes.SELECT)
        self.assertIsNone(self.context.query('vi_mode_select', sublime.OP_REGEX_MATCH, '.*', False))
        self.assertIsNone(self.context.query('vi_mode_select', sublime.OP_NOT_REGEX_MATCH, '.*', False))
        self.assertTrue(self.context.query('vi_mode_select', sublime.OP_EQUAL, True, False))
        self.assertFalse(self.context.query('vi_mode_select', sublime.OP_EQUAL, False, False))
        self.assertFalse(self.context.query('vi_mode_select', sublime.OP_NOT_EQUAL, True, False))
        self.assertTrue(self.context.query('vi_mode_select', sublime.OP_NOT_EQUAL, False, False))

    def test_vi_use_ctrl_keys(self):
        self.view.settings().set('vintageous_use_ctrl_keys', False)
        self.assertFalse(self.context.query('vi_use_ctrl_keys', sublime.OP_EQUAL, True, False))
        self.view.settings().set('vintageous_use_ctrl_keys', True)
        self.assertTrue(self.context.query('vi_use_ctrl_keys', sublime.OP_EQUAL, True, False))

    def test_vi_enable_cmdline_mode(self):
        self.view.settings().set('vintageous_enable_cmdline_mode', False)
        self.assertFalse(self.context.query('vi_enable_cmdline_mode', sublime.OP_EQUAL, True, False))
        self.view.settings().set('vintageous_enable_cmdline_mode', True)
        self.assertTrue(self.context.query('vi_enable_cmdline_mode', sublime.OP_EQUAL, True, False))

    def test_vi_is_cmdline(self):
        self.assertFalse(self.context.query('vi_is_cmdline', sublime.OP_EQUAL, True, False))
        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertTrue(self.context.query('vi_is_cmdline', sublime.OP_EQUAL, True, False))

    def test_vi_cmdline_at_fs_completion(self):
        self.assertFalse(self.context.query('vi_cmdline_at_fs_completion', sublime.OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertFalse(self.context.query('vi_cmdline_at_fs_completion', sublime.OP_EQUAL, True, False))

        self.write(':write ')
        self.assertTrue(self.context.query('vi_cmdline_at_fs_completion', sublime.OP_EQUAL, True, False))

    def test_vi_cmdline_at_setting_completion(self):
        self.assertFalse(self.context.query('vi_cmdline_at_setting_completion', sublime.OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertFalse(self.context.query('vi_cmdline_at_setting_completion', sublime.OP_EQUAL, True, False))

        self.write(':set ')
        self.assertTrue(self.context.query('vi_cmdline_at_setting_completion', sublime.OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/tests/fixtures/Command-line mode foobar.sublime-syntax')
        self.assertFalse(self.context.query('vi_cmdline_at_setting_completion', sublime.OP_EQUAL, True, False))

    def test_vi_is_view(self):
        self.assertTrue(self.context.query('vi_is_view', sublime.OP_EQUAL, True, False))

        self.context.state = State(self.view.window().create_output_panel('test'))

        self.assertFalse(self.context.query('vi_is_view', sublime.OP_EQUAL, True, False))

    def test_vi_command_mode_aware(self):
        self.view.settings().set('command_mode', True)
        self.assertTrue(self.context.query('vi_command_mode_aware', sublime.OP_EQUAL, True, False))

        self.view.settings().set('command_mode', False)
        self.assertFalse(self.context.query('vi_command_mode_aware', sublime.OP_EQUAL, True, False))

        self.context.state = State(self.view.window().create_output_panel('test'))

        self.view.settings().set('command_mode', True)
        self.assertFalse(self.context.query('vi_command_mode_aware', sublime.OP_EQUAL, True, False))

        self.view.settings().set('command_mode', False)
        self.assertFalse(self.context.query('vi_command_mode_aware', sublime.OP_EQUAL, True, False))

    def test_vi_insert_mode_aware(self):

        self.view.settings().set('command_mode', True)
        self.assertFalse(self.context.query('vi_insert_mode_aware', sublime.OP_EQUAL, True, False))

        self.view.settings().set('command_mode', False)
        self.assertTrue(self.context.query('vi_insert_mode_aware', sublime.OP_EQUAL, True, False))

        self.context.state = State(self.view.window().create_output_panel('test'))

        self.view.settings().set('command_mode', True)
        self.assertFalse(self.context.query('vi_insert_mode_aware', sublime.OP_EQUAL, True, False))

        self.view.settings().set('command_mode', False)
        self.assertFalse(self.context.query('vi_insert_mode_aware', sublime.OP_EQUAL, True, False))
