from unittest import TestCase

from NeoVintageous.lib.vi.variables import _DEFAULTS
from NeoVintageous.lib.vi.variables import _SPECIAL_STRINGS
from NeoVintageous.lib.vi.variables import _VARIABLES
from NeoVintageous.lib.vi.variables import expand_keys
from NeoVintageous.lib.vi.variables import get
from NeoVintageous.lib.vi.variables import is_key_name


class TestVariables(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._orig_special_strings = _SPECIAL_STRINGS.copy()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        _SPECIAL_STRINGS.clear()
        _SPECIAL_STRINGS.update(cls._orig_special_strings)

    def test_special_keys_includes_leader_default(self):
        self.assertTrue(is_key_name('<Leader>'))
        self.assertEqual(_DEFAULTS[_SPECIAL_STRINGS['<leader>']], '\\')

    def test_special_keys_includes_local_leader_default(self):
        self.assertTrue(is_key_name('<LocalLeader>'))
        self.assertEqual(_DEFAULTS[_SPECIAL_STRINGS['<localleader>']], '\\')

    def test_is_key_name_returns_true_when_present(self):
        _SPECIAL_STRINGS['<testpresent>'] = 'testpresentvalue'
        self.assertTrue(is_key_name('<testpresent>'))

    def test_is_key_name_is_case_insensitive(self):
        _SPECIAL_STRINGS['<testpresent>'] = 'testpresentvalue'
        self.assertTrue(is_key_name('<testpresent>'))
        self.assertTrue(is_key_name('<TESTPRESENT>'))
        self.assertTrue(is_key_name('<TestPresent>'))
        self.assertTrue(is_key_name('<TeStPrESEnT>'))

    def test_is_key_name_returns_false_when_not_present(self):
        self.assertFalse(is_key_name('<testnotpresent>'))

    def test_get_returns_none_if_key_is_not_present(self):
        self.assertIsNone(get('<TestNotPresent>'))

    def test_get_returns_default_value(self):
        _SPECIAL_STRINGS['<testget>'] = 'x'
        _DEFAULTS['x'] = 'y'
        if 'x' in _VARIABLES:
            # Prevents false positive i.e. another test
            # might set the variable which would cause
            # this test fail, pass, or error.
            del _VARIABLES['x']
        self.assertEqual(get('<TestGet>'), 'y')

    def test_get_returns_variable_value_if_set(self):
        _SPECIAL_STRINGS['<testget>'] = 'x'
        _DEFAULTS['x'] = 'foobar'
        _VARIABLES['x'] = 'y'
        self.assertEqual(get('<TestGet>'), 'y')

    def test_expand_keys_does_not_mutate_plain_strings(self):
        self.assertEqual('', expand_keys(''))
        self.assertEqual('xyz', expand_keys('xyz'))

    def test_expand_keys_does_not_expand_unknown_keys(self):
        self.assertEqual('<TestNotPresent>', expand_keys('<TestNotPresent>'))
        self.assertEqual('x<TestNotPresent>', expand_keys('x<TestNotPresent>'))
        self.assertEqual('xy<TestNotPresent>', expand_keys('xy<TestNotPresent>'))
        self.assertEqual('<TestNotPresent>x', expand_keys('<TestNotPresent>x'))
        self.assertEqual('<TestNotPresent>xy', expand_keys('<TestNotPresent>xy'))
        self.assertEqual('x<TestNotPresent>y', expand_keys('x<TestNotPresent>y'))
        self.assertEqual('<TestNotPresent><TestNotPresent>', expand_keys('<TestNotPresent><TestNotPresent>'))

    def test_expand_keys_expands_to_default(self):
        _SPECIAL_STRINGS['<testget>'] = 'x'
        _DEFAULTS['x'] = 'y'
        if 'x' in _VARIABLES:
            # Prevents false positive i.e. another test
            # might set the variable which would cause
            # this test fail, pass, or error.
            del _VARIABLES['x']

        self.assertEqual('y', expand_keys('<TestGet>'))
        self.assertEqual('yz', expand_keys('<TestGet>z'))
        self.assertEqual('xy', expand_keys('x<TestGet>'))
        self.assertEqual('xyz', expand_keys('x<TestGet>z'))
        self.assertEqual('yy', expand_keys('<TestGet><TestGet>'))
        self.assertEqual('1y2y3', expand_keys('1<TestGet>2<TestGet>3'))
        self.assertEqual('42Gyy:Fizz<Enter>ysiw', expand_keys('42G<TestGet><TestGet>:Fizz<Enter><TestGet>siw'))

    def test_expand_keys_expands_to_variable_if_set(self):
        _SPECIAL_STRINGS['<testget>'] = 'x'
        _DEFAULTS['x'] = 'foobar'
        _VARIABLES['x'] = 'y'
        self.assertEqual('y', expand_keys('<TestGet>'))
        self.assertEqual('yz', expand_keys('<TestGet>z'))
        self.assertEqual('xy', expand_keys('x<TestGet>'))
        self.assertEqual('xyz', expand_keys('x<TestGet>z'))
        self.assertEqual('yy', expand_keys('<TestGet><TestGet>'))
        self.assertEqual('1y2y3', expand_keys('1<TestGet>2<TestGet>3'))
        self.assertEqual('42Gyy:Fizz<Enter>ysiw', expand_keys('42G<TestGet><TestGet>:Fizz<Enter><TestGet>siw'))

    def test_expand_keys_expands_all_keys_in_seq(self):

        # test key x
        _SPECIAL_STRINGS['<testx>'] = 'testx'
        _DEFAULTS['testx'] = 'foobar'
        _VARIABLES['testx'] = 'x'

        # test key y (fallback to default value)
        _SPECIAL_STRINGS['<testy>'] = 'testy'
        _DEFAULTS['testy'] = 'y'
        if 'testy' in _VARIABLES:
            # Prevents false positive i.e. another test
            # might set the variable which would cause
            # this test fail, pass, or error.
            del _VARIABLES['testy']

        self.assertEqual('x', expand_keys('<TestX>'))
        self.assertEqual('y', expand_keys('<TestY>'))
        self.assertEqual('xy', expand_keys('<TestX><TestY>'))
        self.assertEqual('1x2y3', expand_keys('1<TestX>2<TestY>3'))
        self.assertEqual('42Gyy:w<Enter>xggp', expand_keys('42G<TestY><TestY>:w<Enter><TestX>ggp'))
