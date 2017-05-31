from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.settings import SettingsManager
from NeoVintageous.lib.vi.settings import SublimeSettings
from NeoVintageous.lib.vi.settings import VI_OPTIONS
from NeoVintageous.lib.vi.settings import vi_user_setting
from NeoVintageous.lib.vi.settings import VintageSettings
from NeoVintageous.lib.vi.settings import SCOPE_VIEW
from NeoVintageous.lib.vi.settings import SCOPE_VI_VIEW
from NeoVintageous.lib.vi.settings import SCOPE_VI_WINDOW
from NeoVintageous.lib.vi.settings import SCOPE_WINDOW
from NeoVintageous.lib.vi.settings import set_generic_view_setting
from NeoVintageous.lib.vi.settings import opt_bool_parser
from NeoVintageous.lib.vi.settings import set_minimap
from NeoVintageous.lib.vi.settings import set_sidebar
from NeoVintageous.lib.vi.settings import opt_rulers_parser


class TestSublimeSettings(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('foo')
        self.setts = SublimeSettings(view=self.view)

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


class TestVintageSettings(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.setts = VintageSettings(view=self.view)

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


class TestSettingsManager(ViewTestCase):

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


class TestViEditorSettings(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_hlsearch')
        self.view.settings().erase('vintageous_foo')
        self.view.window().settings().erase('vintageous_foo')
        self.settsman = VintageSettings(view=self.view)

    def test_knows_all_settings(self):
        all_settings = [
            'hlsearch',
            'magic',
            'incsearch',
            'ignorecase',
            'autoindent',
            'showminimap',
            'rulers',
            'showsidebar',
            'visualbell',
        ]

        self.assertEqual(sorted(all_settings), sorted(list(VI_OPTIONS.keys())))

    def test_settings_are_correctly_defined(self):
        KNOWN_OPTIONS = {
            'hlsearch':    vi_user_setting(scope=SCOPE_VI_VIEW,    values=(True, False, '0', '1'), default=True,  parser=opt_bool_parser,   action=set_generic_view_setting, negatable=True),
            'magic':       vi_user_setting(scope=SCOPE_VI_VIEW,    values=(True, False, '0', '1'), default=True,  parser=opt_bool_parser,   action=set_generic_view_setting, negatable=True),
            'incsearch':   vi_user_setting(scope=SCOPE_VI_VIEW,    values=(True, False, '0', '1'), default=True,  parser=opt_bool_parser,   action=set_generic_view_setting, negatable=True),
            'ignorecase':  vi_user_setting(scope=SCOPE_VI_VIEW,    values=(True, False, '0', '1'), default=False, parser=opt_bool_parser,   action=set_generic_view_setting, negatable=True),
            'autoindent':  vi_user_setting(scope=SCOPE_VI_VIEW,    values=(True, False, '0', '1'), default=True,  parser=None,              action=set_generic_view_setting, negatable=False),
            'showminimap': vi_user_setting(scope=SCOPE_WINDOW,     values=(True, False, '0', '1'), default=True,  parser=None,              action=set_minimap,              negatable=True),
            'visualbell':  vi_user_setting(scope=SCOPE_VI_WINDOW,  values=(True, False, '0', '1'), default=True,  parser=opt_bool_parser,   action=set_generic_view_setting, negatable=True),
            'rulers':      vi_user_setting(scope=SCOPE_VIEW,       values=None,                    default=[],    parser=opt_rulers_parser, action=set_generic_view_setting, negatable=False),
            'showsidebar': vi_user_setting(scope=SCOPE_WINDOW,     values=(True, False, '0', '1'), default=True,  parser=None,              action=set_sidebar,              negatable=True),
        }

        self.assertEqual(len(KNOWN_OPTIONS), len(VI_OPTIONS))
        for (k, v) in KNOWN_OPTIONS.items():
            self.assertEqual(VI_OPTIONS[k], v)

    def test_can_retrieve_default_value(self):
        self.assertEqual(self.settsman['hlsearch'], True)

    def test_can_retrieve_default_value_if_set_value_is_invalid(self):
        self.settsman.view.settings().set('vintageous_hlsearch', 100)
        self.assertEqual(self.settsman['hlsearch'], True)

    def test_can_retrieve_window_level_settings(self):
        # TODO: use mock to patch dict
        VI_OPTIONS['foo'] = vi_user_setting(scope=SCOPE_WINDOW, values=(100,), default='bar', parser=None, action=None, negatable=False)
        self.settsman.view.window().settings().set('vintageous_foo', 100)
        self.assertEqual(self.settsman['foo'], 100)
        del VI_OPTIONS['foo']
