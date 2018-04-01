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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.settings import _opt_bool_parser
from NeoVintageous.nv.vi.settings import _opt_rulers_parser
from NeoVintageous.nv.vi.settings import _SCOPE_VI_VIEW
from NeoVintageous.nv.vi.settings import _SCOPE_VI_WINDOW
from NeoVintageous.nv.vi.settings import _SCOPE_VIEW
from NeoVintageous.nv.vi.settings import _SCOPE_WINDOW
from NeoVintageous.nv.vi.settings import _set_generic_view_setting
from NeoVintageous.nv.vi.settings import _set_list
from NeoVintageous.nv.vi.settings import _set_minimap
from NeoVintageous.nv.vi.settings import _set_sidebar
from NeoVintageous.nv.vi.settings import _SublimeSettings
from NeoVintageous.nv.vi.settings import _VI_OPTIONS
from NeoVintageous.nv.vi.settings import _vi_user_setting
from NeoVintageous.nv.vi.settings import _VintageSettings
from NeoVintageous.nv.vi.settings import SettingsManager


class TestSublimeSettings(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('foo')
        self.setts = _SublimeSettings(view=self.view)

    def test_can_initialize_class(self):
        self.assertEqual(self.setts.view, self.view)

    def test_can_set_setting(self):
        self.assertEqual(self.view.settings().get('foo'), None)
        self.assertEqual(self.setts['foo'], None)

        self.setts['foo'] = 100
        self.assertEqual(self.view.settings().get('foo'), 100)

    def test_can_get_setting(self):
        self.setts['foo'] = 100
        self.assertEqual(self.setts['foo'], 100)

    def test_can_get_nonexisting_key(self):
        self.assertEqual(self.setts['foo'], None)


class TestVintageSettings(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.setts = _VintageSettings(view=self.view)

    def test_can_initialize_class(self):
        self.assertEqual(self.setts.view, self.view)
        self.assertEqual(self.view.settings().get('vintage'), {})

    def test_can_set_setting(self):
        self.assertEqual(self.setts['foo'], None)

        self.setts['foo'] = 100
        self.assertEqual(self.view.settings().get('vintage')['foo'], 100)

    def test_can_get_setting(self):
        self.setts['foo'] = 100
        self.assertEqual(self.setts['foo'], 100)

    def test_can_get_nonexisting_key(self):
        self.assertEqual(self.setts['foo'], None)


class TestSettingsManager(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.settsman = SettingsManager(view=self.view)

    def test_can_initialize_class(self):
        self.assertEqual(self.view, self.settsman.v)

    def test_can_access_vi_ssettings(self):
        self.settsman.vi['foo'] = 100
        self.assertEqual(self.settsman.vi['foo'], 100)

    def test_can_access_view_settings(self):
        self.settsman.view['foo'] = 100
        self.assertEqual(self.settsman.view['foo'], 100)


class TestViEditorSettings(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_hlsearch')
        self.view.settings().erase('vintageous_foo')
        self.view.window().settings().erase('vintageous_foo')
        self.settsman = _VintageSettings(view=self.view)

    def test_knows_all_settings(self):
        all_settings = [
            'hlsearch',
            'magic',
            'incsearch',
            'ignorecase',
            'autoindent',
            'list',
            'showminimap',
            'rulers',
            'showsidebar',
            'visualbell',
        ]

        self.assertEqual(sorted(all_settings), sorted(list(_VI_OPTIONS.keys())))

    def test_settings_are_correctly_defined(self):
        KNOWN_OPTIONS = {
            'hlsearch': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True,
                                         parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),
            'magic': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True,
                                      parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),
            'incsearch': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True,
                                          parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),
            'ignorecase': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=False,
                                           parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),
            'autoindent': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True,
                                           parser=None, action=_set_generic_view_setting, negatable=False),
            'showminimap': _vi_user_setting(scope=_SCOPE_WINDOW, values=(True, False, '0', '1'), default=True,
                                            parser=None, action=_set_minimap, negatable=True),
            'list': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=False,
                                     parser=None, action=_set_list, negatable=True),
            'visualbell': _vi_user_setting(scope=_SCOPE_VI_WINDOW, values=(True, False, '0', '1'), default=True,
                                           parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),
            'rulers': _vi_user_setting(scope=_SCOPE_VIEW, values=None, default=[],
                                       parser=_opt_rulers_parser, action=_set_generic_view_setting, negatable=False),
            'showsidebar': _vi_user_setting(scope=_SCOPE_WINDOW, values=(True, False, '0', '1'), default=True,
                                            parser=None, action=_set_sidebar, negatable=True),
        }

        self.assertEqual(len(KNOWN_OPTIONS), len(_VI_OPTIONS))
        for (k, v) in KNOWN_OPTIONS.items():
            self.assertEqual(_VI_OPTIONS[k], v)

    def test_can_retrieve_default_value(self):
        self.assertEqual(self.settsman['hlsearch'], True)

    def test_can_retrieve_default_value_if_set_value_is_invalid(self):
        self.settsman.view.settings().set('vintageous_hlsearch', 100)
        self.assertEqual(self.settsman['hlsearch'], True)

    def test_can_retrieve_window_level_settings(self):
        # TODO: use mock to patch dict
        _VI_OPTIONS['foo'] = _vi_user_setting(
            scope=_SCOPE_WINDOW,
            values=(100,),
            default='bar',
            parser=None,
            action=None,
            negatable=False
        )
        self.settsman.view.window().settings().set('vintageous_foo', 100)
        self.assertEqual(self.settsman['foo'], 100)
        del _VI_OPTIONS['foo']
