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

from NeoVintageous.nv.history import _char2type
from NeoVintageous.nv.history import _HIST_CMD
from NeoVintageous.nv.history import _HIST_DEBUG
from NeoVintageous.nv.history import _HIST_EXPR
from NeoVintageous.nv.history import _HIST_INPUT
from NeoVintageous.nv.history import _HIST_INVALID
from NeoVintageous.nv.history import _HIST_SEARCH
from NeoVintageous.nv.history import _name2type
from NeoVintageous.nv.history import history
from NeoVintageous.nv.history import history_add
from NeoVintageous.nv.history import history_clear
from NeoVintageous.nv.history import history_del
from NeoVintageous.nv.history import history_get
from NeoVintageous.nv.history import history_get_type
from NeoVintageous.nv.history import history_len
from NeoVintageous.nv.history import history_nr
from NeoVintageous.nv.history import history_update

# We need to patch the entries storage dictionary so that out tests don't mess
# up our userland entries, which would obviously be bad.
from NeoVintageous.nv.history import _storage as _storage_struct_


# Reusable mappings test patcher (also passes a clean storage structure to tests).
_patch_storage = unittest.mock.patch('NeoVintageous.nv.history._storage',
                                     new_callable=lambda: {k: {'num': 0, 'items': {}} for k in _storage_struct_})


_patch_max_items = lambda n: unittest.mock.patch('NeoVintageous.nv.history._MAX_ITEMS', n)  # noqa: E731


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
@unittest.mock.patch('NeoVintageous.nv.session.save_session', unittest.mock.Mock())
class TestHistory(unittest.TestCase):
    histories = ('cmd', ':', 'search', '/', '?', 'expr', '=', 'input', '@', 'debug', '>')

    def test_history_get_type(self):
        self.assertEquals(history_get_type(' '), _HIST_INVALID)
        self.assertEquals(history_get_type(''), _HIST_INVALID)
        self.assertEquals(history_get_type('foobar'), _HIST_INVALID)
        self.assertEquals(history_get_type('x'), _HIST_INVALID)
        self.assertEquals(history_get_type(':'), _HIST_CMD)
        self.assertEquals(history_get_type('='), _HIST_EXPR)
        self.assertEquals(history_get_type('>'), _HIST_DEBUG)
        self.assertEquals(history_get_type('?'), _HIST_SEARCH)
        self.assertEquals(history_get_type('/'), _HIST_SEARCH)
        self.assertEquals(history_get_type('@'), _HIST_INPUT)
        self.assertEquals(history_get_type('cmd'), _HIST_CMD)
        self.assertEquals(history_get_type('debug'), _HIST_DEBUG)
        self.assertEquals(history_get_type('expr'), _HIST_EXPR)
        self.assertEquals(history_get_type('input'), _HIST_INPUT)
        self.assertEquals(history_get_type('search'), _HIST_SEARCH)

    def test_char2type(self):
        self.assertEquals(_char2type(':'), _HIST_CMD)
        self.assertEquals(_char2type('>'), _HIST_DEBUG)
        self.assertEquals(_char2type('='), _HIST_EXPR)
        self.assertEquals(_char2type('@'), _HIST_INPUT)
        self.assertEquals(_char2type('/'), _HIST_SEARCH)
        self.assertEquals(_char2type('?'), _HIST_SEARCH)
        self.assertEquals(_char2type(''), _HIST_INVALID)
        self.assertEquals(_char2type(' '), _HIST_INVALID)
        self.assertEquals(_char2type('x'), _HIST_INVALID)
        self.assertEquals(_char2type('foobar'), _HIST_INVALID)

    def test_name2type(self):
        self.assertEquals(_name2type('cmd'), _HIST_CMD)
        self.assertEquals(_name2type('debug'), _HIST_DEBUG)
        self.assertEquals(_name2type('expr'), _HIST_EXPR)
        self.assertEquals(_name2type('input'), _HIST_INPUT)
        self.assertEquals(_name2type('search'), _HIST_SEARCH)
        self.assertEquals(_name2type(''), _HIST_INVALID)
        self.assertEquals(_name2type(' '), _HIST_INVALID)
        self.assertEquals(_name2type('x'), _HIST_INVALID)
        self.assertEquals(_name2type('foobar'), _HIST_INVALID)

    @_patch_storage
    def test_history_add_defaults(self, _storage):
        for name in self.histories:
            self.assertTrue(history_add(name, name + 'item'))

    @_patch_storage
    def test_history_add(self, _storage):
        self.assertTrue(history_add(':', 'test_cmd_1'))
        self.assertEqual(1, history_nr(':'))
        self.assertEqual('test_cmd_1', history_get(':'))
        self.assertTrue(history_add(':', 'test_cmd_2'))
        self.assertEqual(2, history_nr(':'))
        self.assertEqual('test_cmd_2', history_get(':'))
        self.assertTrue(history_add(':', 'test_cmd_3'))
        self.assertEqual('test_cmd_3', history_get(':'))
        self.assertEqual(3, history_nr(':'))

        for name in self.histories:
            if name not in ('cmd', ':'):
                self.assertEqual(-1, history_nr(name))
                self.assertEqual('', history_get(name))

        self.assertTrue(history_add('@', 'test_input_1'))
        self.assertEqual(1, history_nr('@'))
        self.assertEqual('test_input_1', history_get('@'))

        for name in self.histories:
            if name not in ('cmd', ':', 'input', '@'):
                self.assertEqual(-1, history_nr(name))
                self.assertEqual('', history_get(name))

        self.assertEqual(1, history_nr('input'))
        self.assertEqual(1, history_nr('@'))
        self.assertEqual('test_input_1', history_get('@'))
        self.assertEqual('test_input_1', history_get('input'))
        self.assertEqual(3, history_nr(':'))
        self.assertEqual(3, history_nr('cmd'))
        self.assertEqual('test_cmd_3', history_get(':'))
        self.assertEqual('test_cmd_3', history_get('cmd'))

    @_patch_storage
    def test_history_add_get_del_nr(self, _storage):
        self.assertTrue(history_add(':', 'a'))
        self.assertTrue(history_add(':', 'b'))
        self.assertEqual('b', history_get(':'))
        self.assertEqual(2, history_nr(':'))
        self.assertTrue(history_add(':', 'a'))
        self.assertEqual('a', history_get(':'))
        self.assertEqual(3, history_nr(':'))
        self.assertTrue(history_del(':', 3))
        self.assertEqual('b', history_get(':'))
        self.assertEqual(2, history_nr(':'))
        self.assertTrue(history_del(':', 2))
        self.assertEqual('', history_get(':'))
        self.assertEqual(-1, history_nr(':'))

    @_patch_storage
    def test_history_get_defaults(self, _storage):
        for name in self.histories:
            self.assertEqual('', history_get(name, 0))
            self.assertEqual('', history_get(name, 1))
            self.assertEqual('', history_get(name, 2))
            self.assertEqual('', history_get(name, -1))
            self.assertEqual('', history_get(name, -2))
            self.assertEqual('', history_get(name))

    @_patch_storage
    def test_history_del_defaults(self, _storage):
        for name in self.histories:
            self.assertFalse(history_del(name, 0))
            self.assertFalse(history_del(name, 1))
            self.assertFalse(history_del(name, 2))
            self.assertFalse(history_del(name, -1))
            self.assertFalse(history_del(name, -2))
            self.assertTrue(history_del(name))

    @_patch_storage
    def test_history_del(self, _storage):
        _storage[_HIST_SEARCH]['num'] = 9
        _storage[_HIST_SEARCH]['items'] = {1: 'a', 2: 'b', 3: 'c', 7: 'g', 9: 'i'}

        self.assertEqual(9, history_nr('/'))
        self.assertTrue(history_del('/', 2))
        self.assertEqual(9, history_nr('/'))
        self.assertTrue(history_del('/', 9))
        self.assertEqual(7, history_nr('/'))
        self.assertTrue(history_del('/', 7))
        self.assertEqual(3, history_nr('/'))
        self.assertTrue(history_add('/', 'j'))
        self.assertEqual(10, history_nr('/'))
        self.assertTrue(history_add('/', 'k'))
        self.assertEqual(11, history_nr('/'))
        self.assertTrue(history_del('/', -2))
        self.assertEqual(11, history_nr('/'))
        self.assertFalse(history_del('/', 0))
        self.assertEqual(11, history_nr('/'))
        self.assertTrue(history_del('/', -1))
        self.assertEqual(3, history_nr('/'))
        self.assertTrue(history_add('/', 'l'))
        self.assertEqual(12, history_nr('/'))
        self.assertTrue(history_del('/', 12))
        self.assertEqual(3, history_nr('/'))
        self.assertTrue(history_del('/'))
        self.assertEqual(-1, history_nr('/'))
        self.assertEqual('', history_get('/'))
        self.assertTrue(history_add('/', 'm'))
        self.assertEqual(1, history_nr('/'))
        self.assertEqual('m', history_get('/'))
        self.assertTrue(history_del('/', 1))
        self.assertEqual(-1, history_nr('/'))
        self.assertEqual('', history_get('/'))
        self.assertTrue(history_add('/', 'n'))
        self.assertEqual(2, history_nr('/'))
        self.assertEqual('n', history_get('/'))
        self.assertTrue(history_del('/', -1))
        self.assertEqual(-1, history_nr('/'))
        self.assertEqual('', history_get('/'))
        self.assertTrue(history_add('/', 'o'))
        self.assertEqual(3, history_nr('/'))
        self.assertEqual('o', history_get('/'))

    @_patch_storage
    def test_history_nr_defaults(self, _storage):
        for name in self.histories:
            self.assertEqual(-1, history_nr(name))

    @_patch_storage
    def test_history_clear(self, _storage):
        _storage[_HIST_CMD]['items'][1] = 'a'
        _storage[_HIST_CMD]['items'][2] = 'b'
        _storage[_HIST_CMD]['num'] = 7

        history_clear()

        self.assertEqual(_storage, {
            _HIST_CMD: {'num': 0, 'items': {}},
            _HIST_SEARCH: {'num': 0, 'items': {}},
            _HIST_EXPR: {'num': 0, 'items': {}},
            _HIST_INPUT: {'num': 0, 'items': {}},
            _HIST_DEBUG: {'num': 0, 'items': {}}
        })

    @_patch_storage
    def test_history_len(self, _storage):
        _storage[_HIST_CMD]['items'][1] = 'a'
        _storage[_HIST_CMD]['items'][2] = 'b'
        _storage[_HIST_CMD]['items'][3] = 'c'
        _storage[_HIST_CMD]['num'] = 7

        self.assertEqual(history_len(':'), 3)

        _storage[_HIST_CMD]['items'][4] = 'd'
        _storage[_HIST_CMD]['items'][5] = 'd'
        _storage[_HIST_CMD]['num'] = 10

        self.assertEqual(history_len(':'), 5)

    @_patch_storage
    def test_history_update(self, _storage):
        self.assertEqual(history_get(':'), '')
        history_update(':fizz')
        self.assertEqual(history_get(':'), 'fizz')
        history_update(':buzz')
        self.assertEqual(history_get(':'), 'buzz')
        history_update(':foo')
        self.assertEqual(history_get(':'), 'foo')
        history_update('/bar')
        self.assertEqual(history_get(':'), 'foo')
        self.assertEqual(history_get('/'), 'bar')
        history_update('/bat')
        self.assertEqual(history_get(':'), 'foo')
        self.assertEqual(history_get('/'), 'bat')

    @_patch_storage
    def test_all(self, _storage):
        for test in self.histories:
            self.assertTrue(history_add(test, 'dummy'))
            self.assertTrue(history_del(test))
            self.assertEqual(-1, history_nr(test))
            self.assertEqual('', history_get(test))

            self.assertTrue(history_add(test, 'ls'))
            self.assertTrue(history_add(test, 'buffers'))
            self.assertEqual('buffers', history_get(test))
            self.assertEqual('ls', history_get(test, -2))
            self.assertEqual('ls', history_get(test, 1))
            self.assertEqual('', history_get(test, 5))
            self.assertEqual('', history_get(test, -5))
            self.assertEqual(2, history_nr(test))
            self.assertTrue(history_del(test, 2))
            self.assertFalse(history_del(test, 7))
            self.assertEqual(1, history_nr(test))
            self.assertEqual('ls', history_get(test, -1))

            self.assertTrue(history_add(test, 'buffers'))
            self.assertTrue(history_add(test, 'ls'))
            self.assertEqual('ls', history_get(test, -1))
            self.assertEqual(4, history_nr(test))

            self.assertRegex(history(test), "^     #  [a-z]+ history\n     3  buffers\n>    4  ls$")
            self.assertRegex(history('all'), "     #  [a-z]+ history\n     3  buffers\n>    4  ls")
            # TODO test history ranges e.g. `:history : 3,4`

            # TODO Test for removing entries matching a pattern
            # for i in range(1, 3):
            #     history_add(test, 'text_' + str(i))
            # self.assertTrue(history_del(test, 'text_\\d\\+'))
            # self.assertEqual('ls', history_get(test, -1))

            # Test for freeing the entire history list
            for i in range(1, 7):
                self.assertTrue(history_add(test, 'text_' + str(i)))
            self.assertTrue(history_del(test))
            for i in range(1, 7):
                self.assertEqual('', history_get(test, i))
                self.assertEqual('', history_get(test, i - 7 - 1))

        # Negative tests
        self.assertFalse(history_del('abc'))
        self.assertEqual('', history_get('abc'))
        with self.assertRaises(TypeError):
            history_get([])  # type: ignore
        self.assertEqual('', history_get(10))  # type: ignore
        self.assertEqual(-1, history_nr('abc'))

    @_patch_max_items(0)
    @_patch_storage
    def test_history_option_size_0(self, _storage):
        self.assertFalse(history_add(':', 'c1'))
        self.assertEqual(_storage, {
            _HIST_CMD: {'num': 0, 'items': {}},
            _HIST_SEARCH: {'num': 0, 'items': {}},
            _HIST_EXPR: {'num': 0, 'items': {}},
            _HIST_INPUT: {'num': 0, 'items': {}},
            _HIST_DEBUG: {'num': 0, 'items': {}}
        })

    @_patch_max_items(1)
    @_patch_storage
    def test_history_option_size_1(self, _storage):
        self.assertTrue(history_add(':', 'c1'))
        self.assertTrue(history_add(':', 'c2'))
        self.assertTrue(history_add(':', 'c3'))
        self.assertTrue(history_add(':', 'c4'))
        self.assertTrue(history_add('/', 's1'))
        self.assertTrue(history_add('/', 's2'))
        self.assertTrue(history_add('/', 's3'))
        self.assertEqual(_storage, {
            _HIST_CMD: {'num': 4, 'items': {4: 'c4'}},
            _HIST_SEARCH: {'num': 3, 'items': {3: 's3'}},
            _HIST_EXPR: {'num': 0, 'items': {}},
            _HIST_INPUT: {'num': 0, 'items': {}},
            _HIST_DEBUG: {'num': 0, 'items': {}}
        })

    @_patch_max_items(2)
    @_patch_storage
    def test_history_option_size_2(self, _storage):
        self.assertTrue(history_add(':', 'c1'))
        self.assertTrue(history_add(':', 'c2'))
        self.assertTrue(history_add(':', 'c3'))
        self.assertTrue(history_add(':', 'c4'))
        self.assertTrue(history_add('?', 's1'))
        self.assertTrue(history_add('?', 's2'))
        self.assertTrue(history_add('?', 's3'))
        self.assertEqual(_storage, {
            _HIST_CMD: {'num': 4, 'items': {3: 'c3', 4: 'c4'}},
            _HIST_SEARCH: {'num': 3, 'items': {2: 's2', 3: 's3'}},
            _HIST_EXPR: {'num': 0, 'items': {}},
            _HIST_INPUT: {'num': 0, 'items': {}},
            _HIST_DEBUG: {'num': 0, 'items': {}}
        })

    @_patch_storage
    def test_history(self, _storage):
        self.assertTrue(history_add(':', 'a'))
        self.assertTrue(history_add(':', 'b'))
        self.assertTrue(history_add('/', 's1'))
        self.assertTrue(history_add('/', 's2'))
        self.assertTrue(history_add('/', 's3'))
        self.assertTrue(history_add('/', 's4'))
        self.assertTrue(history_add('@', 'i1'))
        self.assertTrue(history_add('@', 'i2'))
        self.assertTrue(history_add('@', 'i3'))

        self.assertEqual((
            "     #  cmd history\n"
            "     1  a\n"
            ">    2  b"
        ), history(':'))

        self.assertEqual((
            "     #  search history\n"
            "     1  s1\n"
            "     2  s2\n"
            "     3  s3\n"
            ">    4  s4"
        ), history('/'))

        self.assertEqual((
            "     #  expr history"
        ), history('='))

        self.assertEqual((
            "     #  input history\n"
            "     1  i1\n"
            "     2  i2\n"
            ">    3  i3"
        ), history('@'))

        self.assertEqual((
            "     #  debug history"
        ), history('>'))

        self.assertEqual((
            "     #  cmd history\n"
            "     1  a\n"
            ">    2  b\n"
            "     #  search history\n"
            "     1  s1\n"
            "     2  s2\n"
            "     3  s3\n"
            ">    4  s4\n"
            "     #  expr history\n"
            "     #  input history\n"
            "     1  i1\n"
            "     2  i2\n"
            ">    3  i3\n"
            "     #  debug history"
        ), history('all'))

        self.assertEqual('', history('foobar'))
