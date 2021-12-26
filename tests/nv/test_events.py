# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from sublime import OP_EQUAL
from sublime import OP_NOT_EQUAL
from sublime import OP_NOT_REGEX_CONTAINS
from sublime import OP_NOT_REGEX_MATCH
from sublime import OP_REGEX_CONTAINS
from sublime import OP_REGEX_MATCH

from NeoVintageous.tests import unittest

from NeoVintageous.nv.cmdline import CmdlineOutput
from NeoVintageous.nv.events import NeoVintageousEvents


class TestCommandModeAware(unittest.ViewTestCase):

    KEYS = ['vi_command_mode_aware', 'nv_command_or_insert']

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_is_command_mode_true(self):
        self.settings().set('command_mode', True)
        for key in self.KEYS:
            self.assertEqual(True, self.events.on_query_context(self.view, key, OP_EQUAL, True, True))
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_EQUAL, False, True))
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_NOT_EQUAL, True, True))  # noqa: E501
            self.assertEqual(True, self.events.on_query_context(self.view, key, OP_NOT_EQUAL, False, True))  # noqa: E501

    def test_is_command_mode_false(self):
        self.settings().set('command_mode', False)
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_EQUAL, False, True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_EQUAL, True, True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_EQUAL, False, True))  # noqa: E501
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_EQUAL, True, True))  # noqa: E501

    def test_is_command_mode_true_for_cmdline_output(self):
        panel = CmdlineOutput(self.view.window())._output
        panel.settings().set('command_mode', True)
        for key in self.KEYS:
            self.assertEqual(False, self.events.on_query_context(panel, key, OP_EQUAL, True, True))
            self.assertEqual(True, self.events.on_query_context(panel, key, OP_EQUAL, False, True))

    def test_is_command_mode_false_for_cmdline_output(self):
        panel = CmdlineOutput(self.view.window())._output
        panel.settings().set('command_mode', False)
        for key in self.KEYS:
            self.assertEqual(True, self.events.on_query_context(panel, key, OP_EQUAL, False, True))
            self.assertEqual(False, self.events.on_query_context(panel, key, OP_EQUAL, True, True))

    @unittest.mock.patch('NeoVintageous.nv.events.is_view')
    def test_is_command_mode_should_return_early_if_not_in_command_mode(self, is_view):
        self.settings().set('command_mode', True)
        for key in self.KEYS:
            self.events.on_query_context(self.view, key, OP_EQUAL, True, True)
        self.assertEqual(is_view.call_count, 2)
        self.settings().set('command_mode', False)
        for key in self.KEYS:
            self.events.on_query_context(self.view, key, OP_EQUAL, True, True)
        self.assertEqual(is_view.call_count, 3)


class TestInsertModeAware(unittest.ViewTestCase):

    KEYS = ['vi_insert_mode_aware', 'nv_command_or_insert']

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_is_insert_mode_true(self):
        self.settings().set('command_mode', False)

        for key in self.KEYS:
            self.assertEqual(True, self.events.on_query_context(self.view, key, OP_EQUAL, True, True))
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_EQUAL, False, True))
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_NOT_EQUAL, True, True))  # noqa: E501
            self.assertEqual(True, self.events.on_query_context(self.view, key, OP_NOT_EQUAL, False, True))  # noqa: E501

    def test_is_insert_mode_false(self):
        self.settings().set('command_mode', True)
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_EQUAL, False, True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_EQUAL, True, True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_EQUAL, False, True))  # noqa: E501
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_EQUAL, True, True))  # noqa: E501

    def test_is_insert_mode_true_for_cmdline_output(self):
        panel = CmdlineOutput(self.view.window())._output
        panel.settings().set('command_mode', False)
        for key in self.KEYS:
            self.assertEqual(True, self.events.on_query_context(panel, key, OP_EQUAL, False, True))
            self.assertEqual(False, self.events.on_query_context(panel, key, OP_EQUAL, True, True))

    def test_is_insert_mode_false_for_cmdline_output(self):
        panel = CmdlineOutput(self.view.window())._output
        panel.settings().set('command_mode', True)
        for key in self.KEYS:
            self.assertEqual(False, self.events.on_query_context(panel, key, OP_EQUAL, True, True))
            self.assertEqual(True, self.events.on_query_context(panel, key, OP_EQUAL, False, True))

    def test_is_insert_mode_false_by_default(self):
        for key in self.KEYS:
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_REGEX_MATCH, True, True))  # noqa: E501
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_REGEX_MATCH, False, True))  # noqa: E501

    @unittest.mock.patch('NeoVintageous.nv.events.is_view')
    def test_is_insert_mode_should_return_early_if_not_command_mode(self, is_view):
        self.settings().set('command_mode', False)
        for key in self.KEYS:
            self.events.on_query_context(self.view, key, OP_EQUAL, True, False)
        self.assertEqual(is_view.call_count, 2)
        self.settings().set('command_mode', True)
        for key in self.KEYS:
            self.events.on_query_context(self.view, key, OP_EQUAL, True, False)
        self.assertEqual(is_view.call_count, 3)

    def test_query_contexts_can_be_disabled_by_external_plugins(self):
        self.settings().set('command_mode', True)
        self.settings().set('is_widget', False)
        self.settings().set('__vi_external_disable', True)
        for key in self.KEYS:
            self.assertEqual(False, self.events.on_query_context(self.view, key, OP_EQUAL, True, True))
            self.assertEqual(True, self.events.on_query_context(self.view, key, OP_EQUAL, False, True))


class TestCommandOrInsert(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_command_mode(self):
        self.normal('fi|zz')
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_command_or_insert', OP_EQUAL, True, False))
        self.visual('f|iz|z')
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_command_or_insert', OP_EQUAL, True, False))
        self.vline('|fizz\n|x')
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_command_or_insert', OP_EQUAL, True, False))
        self.vblock('f|iz|z\nx')
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_command_or_insert', OP_EQUAL, True, False))

    def test_insert_mode(self):
        self.insert('fi|zz')
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_command_or_insert', OP_EQUAL, True, False))


class TestOnQueryContextDisabledOrIgnored(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_can_be_disabled_by_external_plugins(self):
        self.settings().set('command_mode', True)
        self.settings().set('is_widget', False)
        self.settings().set('__vi_external_disable', True)
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_EQUAL, True, True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_EQUAL, False, True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_EQUAL, True, True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_EQUAL, False, True))

    def test_query_contexts_are_disabled_for_widgets(self):
        self.settings().set('command_mode', True)
        self.settings().set('is_widget', True)
        self.settings().set('__vi_external_disable', False)
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_EQUAL, True, True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_EQUAL, False, True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_EQUAL, True, True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_EQUAL, False, True))

    def test_returns_none_for_unknown_key(self):
        self.assertEqual(None, self.events.on_query_context(self.view, 'foo', OP_EQUAL, True, True))
        self.assertEqual(None, self.events.on_query_context(self.view, 'foo', OP_NOT_EQUAL, True, True))
        self.assertEqual(None, self.events.on_query_context(self.view, 'foo', OP_EQUAL, False, True))
        self.assertEqual(None, self.events.on_query_context(self.view, 'foo', OP_NOT_EQUAL, False, True))


class TestOnQueryContextHandleKey(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_can_disable_handled_keys(self):
        self.normal('fi|zz')
        self.set_setting('handle_keys', {})
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))
        self.set_setting('handle_keys', {'<C-u>': False})
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))
        self.set_setting('handle_keys', {'v_<C-u>': False})
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))
        self.visual('fi|zz')
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))
        self.insert('fi|zz')
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))
        self.set_setting('handle_keys', {'i_<C-u>': False})
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))
        self.set_setting('handle_keys', {'V_<C-u>': False})
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_handle_key', OP_EQUAL, '<C-u>', True))


class TestFalseForUnsupportedOperators(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_all(self):
        self.settings().set('command_mode', False)
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_MATCH, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_MATCH, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_MATCH, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_MATCH, False, True))  # noqa: E501
        self.settings().set('command_mode', True)
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_MATCH, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_command_mode_aware', OP_NOT_REGEX_MATCH, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_CONTAINS, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_CONTAINS, False, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_MATCH, True, True))  # noqa: E501
        self.assertEqual(False, self.events.on_query_context(self.view, 'vi_insert_mode_aware', OP_NOT_REGEX_MATCH, False, True))  # noqa: E501


class TestAltKeyEnabled(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.window = unittest.mock.Mock()
        self.events = NeoVintageousEvents()

    def test_winaltkeys_yes(self):
        self.set_option('winaltkeys', 'yes', setting=False)
        self.settings().set('command_mode', True)

        self.view.window().is_menu_visible.return_value = False
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))

        self.view.window().is_menu_visible.return_value = True
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))

    def test_winaltkeys_no(self):
        self.set_option('winaltkeys', 'no', setting=False)
        self.settings().set('command_mode', True)

        self.view.window().is_menu_visible.return_value = False
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))

        self.view.window().is_menu_visible.return_value = True
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))

    def test_winaltkeys_menu(self):
        self.set_option('winaltkeys', 'menu', setting=False)
        self.settings().set('command_mode', True)

        self.view.window().is_menu_visible.return_value = False
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))

        self.view.window().is_menu_visible.return_value = True
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(True, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))

        self.settings().set('command_mode', False)
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'f', True))
        self.assertEqual(False, self.events.on_query_context(self.view, 'nv_winaltkeys', OP_EQUAL, 'x', True))


class TestOnLoadDoModeline(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    @unittest.mock.patch('NeoVintageous.nv.events.do_modeline')
    def test_modeline_on(self, do_modeline):
        self.set_option('modeline', True)
        self.events.on_load(self.view)
        do_modeline.assert_called_once_with(self.view)

    @unittest.mock.patch('NeoVintageous.nv.events.do_modeline')
    def test_modeline_off(self, do_modeline):
        self.set_option('modeline', False)
        self.events.on_load(self.view)
        self.assertMockNotCalled(do_modeline)


class TestOnActivated(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_default_mode_enters_normal_mode(self):
        self.insert('fi|zz')
        self.events.on_activated(self.view)
        self.assertNormal('fi|zz')
        self.normal('fi|zz')
        self.events.on_activated(self.view)
        self.assertNormal('fi|zz')

    def test_can_set_default_mode_insert(self):
        self.normal('fi|zz')
        self.set_setting('default_mode', 'insert')
        self.events.on_activated(self.view)
        self.assertInsert('fi|zz')
        self.set_setting('default_mode', '')
        self.events.on_activated(self.view)
        self.assertNormal('fi|zz')

    def test_default_mode_does_not_change_mode_for_visual_modes(self):
        for default_mode in ('insert', ''):
            self.visual('f|iz|z')
            self.set_setting('default_mode', default_mode)
            self.events.on_activated(self.view)
            self.assertVisual('f|iz|z')
            self.vline('|1\n|2')
            self.events.on_activated(self.view)
            self.assertVline('|1\n|2')
            self.vblock('|1|\n|2|\n')
            self.events.on_activated(self.view)
            self.assertVblock('|1|\n|2|\n')

    def test_reset_mode_when_switching_tabs_is_false(self):
        self.normal('fi|zz')
        self.set_setting('reset_mode_when_switching_tabs', False)
        self.events.on_activated(self.view)
        self.assertNormal('fi|zz')
        self.insert('fi|zz')
        self.events.on_activated(self.view)
        self.assertInsert('fi|zz')
        self.visual('f|iz|z')
        self.events.on_activated(self.view)
        self.assertVisual('f|iz|z')

    def test_multiple_cursors_when_reset_mode_when_switching_tabs_is_false(self):
        self.normal('fi|zz bu|zz')
        self.set_setting('reset_mode_when_switching_tabs', False)
        self.events.on_activated(self.view)
        self.assertNormal('fi|zz bu|zz')

    def test_fix_malformed_normal_mode_is_fixed_by_resetting_it(self):
        self.normal('fi|zz')
        self.view.sel().clear()
        self.events.on_activated(self.view)
        self.assertNormal('|fizz')

    def test_fix_malformed_visual_mode_is_fixed_by_resetting_it(self):
        self.visual('fi|zz| buzz')
        self.view.sel().clear()
        self.events.on_activated(self.view)
        self.assertVisual('|fizz buzz')


class TestOnPostSave(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_on_last_char(self):
        self.normal('fiz|z')
        self.events.on_post_save(self.view)
        self.assertNormal('fiz|z')

    def test_fix_eol_cursor(self):
        self.normal('fizz|\n')
        self.events.on_post_save(self.view)
        self.assertNormal('fiz|z\n')
        self.normal('fizz|\nbuzz\n')
        self.events.on_post_save(self.view)
        self.assertNormal('fiz|z\nbuzz\n')

    def test_fix_eof_cursor(self):
        self.normal('fizz|')
        self.events.on_post_save(self.view)
        self.assertNormal('fiz|z')

    def test_disabled_views_are_ingored(self):
        self.normal('x|\n')
        self.view.settings().set('__vi_external_disable', True)
        self.events.on_post_save(self.view)
        self.assertNormal('x|\n')

    def test_widgets_are_ignored(self):
        self.normal('x|\n')
        self.view.settings().set('is_widget', True)
        self.events.on_post_save(self.view)
        self.assertNormal('x|\n')


class TestOnTextCommand(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def on_text_command(self, cmd, args):
        out = self.events.on_text_command(self.view, cmd, args)
        if out:
            self.view.run_command(out[0], out[1])

    def test_double_click_enters_visual(self):
        self.normal('|fizz buzz')
        self.select((2, 5))
        self.on_text_command('drag_select', {'by': 'words'})
        self.assertVisual('fi|zz |buzz')

    def test_extends_enters_visual(self):
        self.normal('|fizz buzz')
        self.select((2, 5))
        self.on_text_command('drag_select', {'by': 'words'})
        self.assertVisual('fi|zz |buzz')

    def test_triple_click_enters_visual_line(self):
        self.visual('1\nf|iz|z\nbuzz\n')
        self.on_text_command('drag_select', {'by': 'lines'})
        self.assertVline('1\n|fizz\n|buzz\n')
        self.visual('1\nf|izz\nbu|zz\n3\n')
        self.on_text_command('drag_select', {'by': 'lines'})
        self.assertVline('1\n|fizz\nbuzz\n|3\n')

    def test_single_click_enters_normal(self):
        self.visual('fi|zz b|uzz')
        self.on_text_command('drag_select', {})
        self.assertNormal('fizz |buzz')

    def test_extend_visual_stays_in_visual(self):
        self.visual('fi|zz b|uzz')
        self.on_text_command('drag_select', {'extend': True})
        self.assertVisual('fi|zz b|uzz')

    def test_additive_visual_stays_in_visual(self):
        self.visual('fi|zz b|uzz')
        self.on_text_command('drag_select', {'additive': True})
        self.assertVisual('fi|zz b|uzz')

    def test_by_words_visual_stays_in_visual(self):
        self.visual('fi|zz b|uzz')
        self.on_text_command('drag_select', {'by': 'words'})
        self.assertVisual('fi|zz b|uzz')


class TestOnPostTextCommand(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.events = NeoVintageousEvents()

    def test_updates_xpos(self):
        self.normal('fizz| buzz')
        self.assertXpos(0)
        self.events.on_post_text_command(self.view, 'drag_select', {
            'event': {'button': 1, 'x': 2, 'y': 4}})
        self.assertXpos(4)

    def test_updates_xposx(self):
        self.normal('fizz| buzz')
        self.assertXpos(0)
        self.events.on_post_text_command(self.view, 'drag_select', {})
        self.events.on_post_text_command(self.view, 'foobar', {})
        self.events.on_post_text_command(self.view, 'drag_select', {'event': {'button': 1}})
        self.events.on_post_text_command(self.view, 'drag_select', {'event': {'button': 2, 'x': 2, 'y': 4}})
        self.assertXpos(0)
