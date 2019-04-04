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

from unittest import mock
import unittest

from NeoVintageous.nv.variables import _defaults as _defaults_struct_
from NeoVintageous.nv.variables import _special_strings as _special_strings_struct_
from NeoVintageous.nv.variables import _variables as _variables_struct_
from NeoVintageous.nv.variables import expand_keys
from NeoVintageous.nv.variables import get
from NeoVintageous.nv.variables import is_key_name
from NeoVintageous.nv.variables import variables_clear


class TestVariables(unittest.TestCase):

    def test_special_keys_includes_leader_default(self):
        self.assertTrue(is_key_name('<Leader>'))
        self.assertEqual(_defaults_struct_[_special_strings_struct_['<leader>']], '<bslash>')

    def test_special_keys_includes_local_leader_default(self):
        self.assertTrue(is_key_name('<LocalLeader>'))
        self.assertEqual(_defaults_struct_[_special_strings_struct_['<localleader>']], '<bslash>')

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testpresent>': 'testpresentvalue'})
    def test_is_key_name_returns_true_when_present(self):
        self.assertTrue(is_key_name('<testpresent>'))

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testpresent>': 'testpresentvalue'})
    def test_is_key_name_is_case_insensitive(self):
        self.assertTrue(is_key_name('<testpresent>'))
        self.assertTrue(is_key_name('<TESTPRESENT>'))
        self.assertTrue(is_key_name('<TestPresent>'))
        self.assertTrue(is_key_name('<TeStPrESEnT>'))

    def test_is_key_name_returns_false_when_not_present(self):
        self.assertFalse(is_key_name('<testnotpresent>'))

    def test_get_returns_none_if_key_is_not_present(self):
        self.assertIsNone(get('<TestNotPresent>'))

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testget>': 'x'})
    @mock.patch.dict('NeoVintageous.nv.variables._defaults', {'x': 'y'})
    def test_get_returns_default_value(self):
        self.assertEqual(get('<TestGet>'), 'y')

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testget>': 'x'})
    @mock.patch.dict('NeoVintageous.nv.variables._defaults', {'x': 'foobar'})
    @mock.patch.dict('NeoVintageous.nv.variables._variables', {'x': 'y'})
    def test_get_returns_variable_value_if_set(self):
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

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testget>': 'x'})
    @mock.patch.dict('NeoVintageous.nv.variables._defaults', {}, clear=True)
    @mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
    def test_expand_keys_protect_against_infinite_loop(self):
        self.assertEqual('<TestGet>', expand_keys('<TestGet>'))

    @mock.patch.dict('NeoVintageous.nv.variables._defaults', {'x': 'y'})
    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testget>': 'x'})
    def test_expand_keys_expands_to_default(self):
        self.assertEqual('y', expand_keys('<TestGet>'))
        self.assertEqual('yz', expand_keys('<TestGet>z'))
        self.assertEqual('xy', expand_keys('x<TestGet>'))
        self.assertEqual('xyz', expand_keys('x<TestGet>z'))
        self.assertEqual('yy', expand_keys('<TestGet><TestGet>'))
        self.assertEqual('1y2y3', expand_keys('1<TestGet>2<TestGet>3'))
        self.assertEqual('42Gyy:Fizz<Enter>ysiw', expand_keys('42G<TestGet><TestGet>:Fizz<Enter><TestGet>siw'))

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testget>': 'x'})
    @mock.patch.dict('NeoVintageous.nv.variables._defaults', {'x': 'foobar'})
    @mock.patch.dict('NeoVintageous.nv.variables._variables', {'x': 'y'})
    def test_expand_keys_expands_to_variable_if_set(self):
        self.assertEqual('y', expand_keys('<TestGet>'))
        self.assertEqual('yz', expand_keys('<TestGet>z'))
        self.assertEqual('xy', expand_keys('x<TestGet>'))
        self.assertEqual('xyz', expand_keys('x<TestGet>z'))
        self.assertEqual('yy', expand_keys('<TestGet><TestGet>'))
        self.assertEqual('1y2y3', expand_keys('1<TestGet>2<TestGet>3'))
        self.assertEqual('42Gyy:Fizz<Enter>ysiw', expand_keys('42G<TestGet><TestGet>:Fizz<Enter><TestGet>siw'))

    @mock.patch.dict('NeoVintageous.nv.variables._special_strings', {'<testx>': 'testx', '<testy>': 'testy'})
    @mock.patch.dict('NeoVintageous.nv.variables._defaults', {'testx': 'foobar'})
    @mock.patch.dict('NeoVintageous.nv.variables._variables', {'testx': 'x', 'testy': 'y'})
    def test_expand_keys_expands_all_keys_in_seq(self):
        self.assertEqual('x', expand_keys('<TestX>'))
        self.assertEqual('y', expand_keys('<TestY>'))
        self.assertEqual('xy', expand_keys('<TestX><TestY>'))
        self.assertEqual('1x2y3', expand_keys('1<TestX>2<TestY>3'))
        self.assertEqual('42Gyy:w<Enter>xggp', expand_keys('42G<TestY><TestY>:w<Enter><TestX>ggp'))

    @mock.patch.dict('NeoVintageous.nv.variables._variables', {'x': 'y'})
    def test_clear(self):
        variables_clear()
        self.assertEquals({}, _variables_struct_)
