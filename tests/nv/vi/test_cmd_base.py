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

import unittest

from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef


class TestViCommandDefBase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.command = ViCommandDefBase()

    def test_input_default(self):
        self.assertEqual('', self.command.inp)

    def test_set_input(self):
        self.command.inp = 'x'
        self.assertEqual('x', self.command.inp)

    def test_reset_input(self):
        self.command.inp = 'x'
        self.command.reset()
        self.assertEqual('', self.command.inp)

    def test_accept_input_defaults_to_false(self):
        self.assertFalse(self.command.accept_input)

    def test_input_parser_defaults_to_none(self):
        self.assertIsNone(self.command.input_parser)

    def test_translate_default_raises_not_implemented(self):
        with self.assertRaisesRegex(NotImplementedError, 'ViCommandDefBase must implement translate()'):
            self.command.translate('state stub')

    def test_accept_default_raises_not_implemented(self):
        with self.assertRaisesRegex(NotImplementedError, 'ViCommandDefBase must implement accept()'):
            self.command.accept('state stub')

    def test_serialize_default(self):
        self.assertEqual({'name': 'ViCommandDefBase', 'data': {'_inp': ''}}, self.command.serialize())

    def test_serialize_input(self):
        self.command.inp = 'ab'
        self.assertEqual({'name': 'ViCommandDefBase', 'data': {'_inp': 'ab'}}, self.command.serialize())

    def test_serialize_uses_a_serializable_whitelist(self):
        self.command.inp = 'ab'
        self.command.foo = 'bar'
        self.command.fizz = 'buzz'
        self.assertEqual({'name': 'ViCommandDefBase', 'data': {'_inp': 'ab'}}, self.command.serialize())

    def test_from_json(self):
        command = self.command.from_json({'foo': 'bar', '_inp': 'xyz'})
        self.assertEqual('bar', command.foo)
        self.assertEqual('xyz', command.inp)
        self.assertEqual({'name': 'ViCommandDefBase', 'data': {'_inp': 'xyz'}}, command.serialize())

    def test__str__(self):
        self.assertEqual('<ViCommandDefBase>', str(self.command))
        self.command.command = 'fizz'
        self.assertEqual('<ViCommandDefBase>', str(self.command))


class ViCommandDefBaseImplementation(ViCommandDefBase):
    pass


class TestViCommandDefBaseTestImplementation(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.command = ViCommandDefBaseImplementation()

    def test__str__(self):
        self.assertEqual('<ViCommandDefBaseImplementation>', str(self.command))
        self.command.command = 'buzz'
        self.assertEqual('<ViCommandDefBaseImplementation>', str(self.command))

    def test_serialize_input(self):
        self.command.inp = 'ab'
        self.assertEqual({'name': 'ViCommandDefBaseImplementation', 'data': {'_inp': 'ab'}}, self.command.serialize())


class TestViMissingCommandDef(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.command = ViMissingCommandDef()

    def test_translate_raises_exception(self):
        with self.assertRaisesRegex(TypeError, 'ViMissingCommandDef should not be used as a runnable command'):
            self.command.translate()
