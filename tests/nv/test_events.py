from sublime import OP_EQUAL
from sublime import OP_NOT_EQUAL
from sublime import OP_NOT_REGEX_CONTAINS
from sublime import OP_NOT_REGEX_MATCH
from sublime import OP_REGEX_CONTAINS
from sublime import OP_REGEX_MATCH

from NeoVintageous.tests import unittest

from NeoVintageous.nv.events import _Context


class TestKeyContext(unittest.ViewTestCase):

    def test_should_not_handle_invalid_key(self):
        context = _Context(self.view)
        self.assertEqual(None, context.query('foobar', OP_EQUAL, True, True))
        self.assertEqual(None, context.query('foobar', OP_EQUAL, True, False))
        self.assertEqual(None, context.query('foobar', OP_EQUAL, False, False))
        self.assertEqual(None, context.query('foobar', OP_EQUAL, False, True))
        self.assertEqual(None, context.query('foobar', OP_NOT_EQUAL, True, True))
        self.assertEqual(None, context.query('foobar', OP_NOT_EQUAL, True, False))
        self.assertEqual(None, context.query('foobar', OP_NOT_EQUAL, False, False))
        self.assertEqual(None, context.query('foobar', OP_NOT_EQUAL, False, True))
        self.assertEqual(None, context.query('foobar', OP_REGEX_MATCH, '.*', True))
        self.assertEqual(None, context.query('foobar', OP_REGEX_MATCH, '.*', False))
        self.assertEqual(None, context.query('foobar', OP_NOT_REGEX_MATCH, '.*', True))
        self.assertEqual(None, context.query('foobar', OP_NOT_REGEX_MATCH, '.*', False))
        self.assertEqual(None, context.query('foobar', OP_REGEX_CONTAINS, '.*', True))
        self.assertEqual(None, context.query('foobar', OP_REGEX_CONTAINS, '.*', False))
        self.assertEqual(None, context.query('foobar', OP_NOT_REGEX_CONTAINS, '.*', True))
        self.assertEqual(None, context.query('foobar', OP_NOT_REGEX_CONTAINS, '.*', False))

    def test_vi_is_cmdline(self):
        self.assertFalse(_Context(self.view).query('vi_is_cmdline', OP_EQUAL, True, False))
        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertTrue(_Context(self.view).query('vi_is_cmdline', OP_EQUAL, True, False))

    def test_vi_cmdline_at_fs_completion(self):
        self.assertFalse(_Context(self.view).query('vi_cmdline_at_fs_completion', OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertFalse(_Context(self.view).query('vi_cmdline_at_fs_completion', OP_EQUAL, True, False))

        self.write(':write ')
        self.assertTrue(_Context(self.view).query('vi_cmdline_at_fs_completion', OP_EQUAL, True, False))

    def test_vi_cmdline_at_setting_completion(self):
        self.assertFalse(_Context(self.view).query('vi_cmdline_at_setting_completion', OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertFalse(_Context(self.view).query('vi_cmdline_at_setting_completion', OP_EQUAL, True, False))

        self.write(':set ')
        self.assertTrue(_Context(self.view).query('vi_cmdline_at_setting_completion', OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/tests/fixtures/Command-line mode foobar.sublime-syntax')
        self.assertFalse(_Context(self.view).query('vi_cmdline_at_setting_completion', OP_EQUAL, True, False))

    def test_vi_command_mode_aware_can_return_true(self):
        self.settings().set('command_mode', True)
        self.assertTrue(_Context(self.view).query('vi_command_mode_aware', OP_EQUAL, True, True))
        self.settings().set('command_mode', False)
        self.assertTrue(_Context(self.view).query('vi_command_mode_aware', OP_EQUAL, False, True))

    def test_vi_command_mode_aware_can_return_false(self):
        self.settings().set('command_mode', False)
        self.assertFalse(_Context(self.view).query('vi_command_mode_aware', OP_EQUAL, True, True))
        self.settings().set('command_mode', True)
        self.assertFalse(_Context(self.view).query('vi_command_mode_aware', OP_EQUAL, False, True))

    def test_vi_command_mode_aware_can_return_false_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertFalse(_Context(panel).query('vi_command_mode_aware', OP_EQUAL, True, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertFalse(_Context(panel).query('vi_command_mode_aware', OP_EQUAL, True, True))

    def test_vi_command_mode_aware_can_return_true_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertTrue(_Context(panel).query('vi_command_mode_aware', OP_EQUAL, False, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertTrue(_Context(panel).query('vi_command_mode_aware', OP_EQUAL, False, True))

    def test_vi_insert_mode_aware_can_return_true(self):
        self.settings().set('command_mode', False)
        self.assertTrue(_Context(self.view).query('vi_insert_mode_aware', OP_EQUAL, True, True))
        self.settings().set('command_mode', True)
        self.assertTrue(_Context(self.view).query('vi_insert_mode_aware', OP_EQUAL, False, True))

    def test_vi_insert_mode_aware_can_return_false(self):
        self.settings().set('command_mode', True)
        self.assertFalse(_Context(self.view).query('vi_insert_mode_aware', OP_EQUAL, True, True))
        self.settings().set('command_mode', False)
        self.assertFalse(_Context(self.view).query('vi_insert_mode_aware', OP_EQUAL, False, True))

    def test_vi_insert_mode_aware_can_return_false_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertFalse(_Context(panel).query('vi_insert_mode_aware', OP_EQUAL, True, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertFalse(_Context(panel).query('vi_insert_mode_aware', OP_EQUAL, True, True))

    def test_vi_insert_mode_aware_can_return_true_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertTrue(_Context(panel).query('vi_insert_mode_aware', OP_EQUAL, False, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertTrue(_Context(panel).query('vi_insert_mode_aware', OP_EQUAL, False, True))
