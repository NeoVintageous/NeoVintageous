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

import sys

from NeoVintageous.tests import unittest

from NeoVintageous.nv.options import BooleanIsVisibleOption
from NeoVintageous.nv.options import BooleanViewOption
from NeoVintageous.nv.options import NumberOption
from NeoVintageous.nv.options import NumberViewOption
from NeoVintageous.nv.options import Option
from NeoVintageous.nv.options import StringOption
from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.options import get_option_completions
from NeoVintageous.nv.options import set_option
from NeoVintageous.nv.options import set_window_ui_element_visible
from NeoVintageous.nv.options import toggle_option


class TestOption(unittest.ViewTestCase):

    def test_option(self):
        option = Option('fizzbuzz', '')
        self.assertEqual(option.get(self.view), '')
        option.set(self.view, 'x')
        self.assertEqual(option.get(self.view), 'x')
        option.set(self.view, 'all')
        self.assertEqual(option.get(self.view), 'all')
        option.set(self.view, '')
        self.assertEqual(option.get(self.view), '')
        self.assertNotSetting('fizzbuzz')


class TestStringOption(unittest.ViewTestCase):

    def test_set_coerces_boolean_like_values(self):
        option = StringOption('winaltkeys', 'menu')
        option.set(self.view, 'yes')
        self.assertEqual(option.get(self.view), 'yes')
        option.set(self.view, 'no')
        self.assertEqual(option.get(self.view), 'no')
        option.set(self.view, 'yes')
        self.assertEqual(option.get(self.view), 'yes')
        option.set(self.view, 'menu')
        self.assertEqual(option.get(self.view), 'menu')

    def test_set_invalid_values(self):
        option = StringOption('winaltkeys', 'menu', ('all', 'menu'))
        option.set(self.view, 'all')
        self.assertEqual(option.get(self.view), 'all')
        option.set(self.view, 'menu')
        self.assertEqual(option.get(self.view), 'menu')
        for invalid_value in ('foobar', '', None, False):
            with self.assertRaisesRegex(ValueError, 'invalid argument'):
                option.set(self.view, invalid_value)


class TestNumberOption(unittest.ViewTestCase):

    def test_number(self):
        option = NumberOption('fizz', 0)
        option.set(self.view, 0)
        self.assertEqual(option.get(self.view), 0)
        option.set(self.view, 3)
        self.assertEqual(option.get(self.view), 3)
        option.set(self.view, '3')
        self.assertEqual(option.get(self.view), 3)
        option.set(self.view, '42')
        self.assertEqual(option.get(self.view), 42)


class TestNumberViewOption(unittest.ViewTestCase):

    def test_set(self):
        option = NumberViewOption('buzz')
        self.assertEqual(option.get(self.view), None)
        self.assertEqual(self.view.settings().get('buzz'), None)
        option.set(self.view, 3)
        self.assertEqual(option.get(self.view), 3)
        self.assertEqual(self.view.settings().get('buzz'), 3)
        option.set(self.view, 5)
        self.assertEqual(option.get(self.view), 5)
        self.assertEqual(self.view.settings().get('buzz'), 5)

    def test_allows_default(self):
        option = NumberViewOption('buzz', 42)
        self.assertEqual(self.view.settings().get('buzz'), None)
        self.assertEqual(option.get(self.view), 42)


class TestBooleanViewOption(unittest.ViewTestCase):

    def test_set(self):
        self.settings().set('spell_check', False)
        option = BooleanViewOption('spell_check')
        self.assertEqual(option.get(self.view), False)
        self.assertSetting('spell_check', False)
        option.set(self.view, True)
        self.assertEqual(option.get(self.view), True)
        self.assertSetting('spell_check', True)
        option.set(self.view, False)
        self.assertEqual(option.get(self.view), False)
        self.assertSetting('spell_check', False)
        self.assertNotSetting('spell')

    def test_set_false_only_mutates_setting_if_dirty(self):
        self.settings().set('spell_check', False)
        option = BooleanViewOption('spell_check')
        self.view.settings().set = unittest.mock.Mock()

        option.set(self.view, False)
        self.assertEqual(0, self.view.settings().set.call_count)

        option.set(self.view, True)
        self.view.settings().set.assert_called_once_with('spell_check', True)

    def test_set_true_only_mutates_setting_if_dirty(self):
        self.settings().set('spell_check', True)
        option = BooleanViewOption('spell_check')
        self.view.settings().set = unittest.mock.Mock()

        option.set(self.view, True)
        self.assertEqual(0, self.view.settings().set.call_count)

        option.set(self.view, False)
        self.view.settings().set.assert_called_once_with('spell_check', False)

    def test_on_off_values(self):
        self.settings().set('draw_white_space', 'none')
        option = BooleanViewOption('draw_white_space', 'all', 'selection')
        option.set(self.view, True)
        self.assertEqual(option.get(self.view), True)
        self.assertSetting('draw_white_space', 'all')
        option.set(self.view, False)
        self.assertEqual(option.get(self.view), False)
        self.assertSetting('draw_white_space', 'selection')


class TestBooleanIsVisibleOption(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.is_menu_visible = self.view.window().is_menu_visible()
        self.is_minimap_visible = self.view.window().is_minimap_visible()
        self.is_sidebar_visible = self.view.window().is_sidebar_visible()
        self.is_status_bar_visible = self.view.window().is_status_bar_visible()

    def tearDown(self):
        self.view.window().set_menu_visible(self.is_menu_visible)
        self.view.window().set_minimap_visible(self.is_minimap_visible)
        self.view.window().set_sidebar_visible(self.is_sidebar_visible)
        self.view.window().set_status_bar_visible(self.is_status_bar_visible)
        super().tearDown()

    def test_is_visible(self):
        toggles = [
            'minimap',
            'sidebar',
            'status_bar'
        ]

        # XXX For some reason toggling the menu breaks for OSX, but possibly
        # only in CI, or maybe a bug in Sublime specific to OSX.
        if not sys.platform.startswith('darwin'):
            toggles.append('menu')

        for name in toggles:
            option = BooleanIsVisibleOption(name, False)
            option.set(self.view, True)
            self.assertEqual(option.get(self.view), True)
            self.assertOption(name.replace('_', ''), True)

            option.set(self.view, False)
            self.assertEqual(option.get(self.view), False)
            self.assertOption(name.replace('_', ''), False)

            option.set(self.view, True)
            self.assertEqual(option.get(self.view), True)
            self.assertOption(name.replace('_', ''), True)

            # Test toggle (used by for example Unimpaired).
            set_window_ui_element_visible(name, window=self.view.window())
            self.assertEqual(option.get(self.view), False)
            self.assertOption(name.replace('_', ''), False)

            # Test toggle (used by for example Unimpaired).
            set_window_ui_element_visible(name, window=self.view.window())
            self.assertEqual(option.get(self.view), True)
            self.assertOption(name.replace('_', ''), True)


class TestGetSetOptions(unittest.ViewTestCase):

    def test_get(self):
        set_option(self.view, 'hlsearch', False)
        self.assertEqual(get_option(self.view, 'hlsearch'), False)
        self.assertEqual(get_option(self.view, 'hls'), False)
        set_option(self.view, 'hlsearch', True)
        self.assertEqual(get_option(self.view, 'hlsearch'), True)
        self.assertEqual(get_option(self.view, 'hls'), True)
        set_option(self.view, 'nohlsearch')
        self.assertEqual(get_option(self.view, 'hlsearch'), False)
        set_option(self.view, 'hlsearch')
        self.assertEqual(get_option(self.view, 'hlsearch'), True)

    def test_toggle(self):
        set_option(self.view, 'hlsearch', True)
        toggle_option(self.view, 'hlsearch')
        self.assertEqual(get_option(self.view, 'hlsearch'), False)
        toggle_option(self.view, 'hlsearch')
        self.assertEqual(get_option(self.view, 'hlsearch'), True)

    def test_set_unknown_raises_exception(self):
        with self.assertRaisesRegex(KeyError, 'foobar'):
            set_option(self.view, 'foobar', False)

        with self.assertRaisesRegex(KeyError, 'nofoobar'):
            set_option(self.view, 'nofoobar', False)


class TestCompletions(unittest.TestCase):

    def test_completions(self):
        completions = list(get_option_completions())

        self.assertTrue('belloff' in completions)
        self.assertTrue('hlsearch' in completions)
        self.assertTrue('ignorecase' in completions)
        self.assertTrue('list' in completions)
        self.assertTrue('modeline' in completions)
        self.assertTrue('modelines' in completions)
        self.assertTrue('scrolloff' in completions)
        self.assertTrue('spell' in completions)
        self.assertTrue('winaltkeys' in completions)

        self.assertFalse('nobelloff' in completions)
        self.assertFalse('nohlsearch' in completions)
        self.assertFalse('noignorecase' in completions)
        self.assertFalse('nolist' in completions)
        self.assertFalse('nomodelines' in completions)
        self.assertFalse('noscrolloff' in completions)
        self.assertFalse('nospell' in completions)
        self.assertFalse('nowinaltkeys' in completions)

        self.assertFalse('invbelloff' in completions)
        self.assertFalse('invhlsearch' in completions)
        self.assertFalse('invignorecase' in completions)
        self.assertFalse('invlist' in completions)
        self.assertFalse('invmodelines' in completions)
        self.assertFalse('invscrolloff' in completions)
        self.assertFalse('invspell' in completions)
        self.assertFalse('invwinaltkeys' in completions)

    def test_completions_prefix(self):
        completions = list(get_option_completions('i'))

        self.assertFalse('invignorecase' in completions)
        self.assertFalse('invincsearch' in completions)
        self.assertFalse('list' in completions)
        self.assertFalse('modeline' in completions)
        self.assertFalse('noignorecase' in completions)
        self.assertFalse('noincsearch' in completions)
        self.assertFalse('spell' in completions)
        self.assertTrue('ignorecase' in completions)
        self.assertTrue('incsearch' in completions)

        completions = list(get_option_completions('noi'))

        self.assertFalse('ignorecase' in completions)
        self.assertFalse('incsearch' in completions)
        self.assertFalse('invignorecase' in completions)
        self.assertFalse('invincsearch' in completions)
        self.assertFalse('list' in completions)
        self.assertFalse('modeline' in completions)
        self.assertFalse('spell' in completions)
        self.assertTrue('noignorecase' in completions)
        self.assertTrue('noincsearch' in completions)

        completions = list(get_option_completions('inv'))

        self.assertFalse('list' in completions)
        self.assertFalse('modeline' in completions)
        self.assertFalse('nolist' in completions)
        self.assertFalse('spell' in completions)
        self.assertTrue('invhlsearch' in completions)
        self.assertTrue('invignorecase' in completions)
        self.assertTrue('invlist' in completions)
