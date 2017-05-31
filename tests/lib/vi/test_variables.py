from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.variables import _SPECIAL_STRINGS
from NeoVintageous.lib.vi.variables import _DEFAULTS
from NeoVintageous.lib.vi.variables import is_key_name
from NeoVintageous.lib.vi.variables import set_
from NeoVintageous.lib.vi.variables import get
from NeoVintageous.lib.vi import variables


class Test_special_strings(ViewTestCase):

    def test_includes_leader_string(self):
        self.assertEqual(_SPECIAL_STRINGS['<leader>'], 'mapleader')

    def test_includes_local_leader_string(self):
        self.assertEqual(_SPECIAL_STRINGS['<localleader>'], 'maplocalleader')


class Test_default_values(ViewTestCase):

    def test_has_default_value_for_leader(self):
        self.assertEqual(_DEFAULTS['mapleader'], '\\')

    def test_has_default_value_for_local_leader(self):
        self.assertEqual(_DEFAULTS['maplocalleader'], '\\')


class Test_is_key_name(ViewTestCase):

    def test_succeeds_if_name_present(self):
        self.assertTrue(is_key_name('<Leader>'))
        # test that it's case-insentitive
        self.assertTrue(is_key_name('<leader>'))

    def test_fails_if_name_absent(self):
        self.assertFalse(is_key_name('<Leaderx>'))


class Test_set_(ViewTestCase):

    def test_can_set_value(self):
        set_('dog', 'cat')
        self.assertEqual(variables._VARIABLES['dog'], 'cat')


class Test_get(ViewTestCase):

    def setUp(self):
        super().setUp()
        variables._VARIABLES = {}

    def test_can_get_set_value(self):
        set_('dog', 'cat')
        self.assertEqual(get('dog'), 'cat')
