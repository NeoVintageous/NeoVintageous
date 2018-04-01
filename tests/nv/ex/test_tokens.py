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

from NeoVintageous.nv.ex.tokens import Token
from NeoVintageous.nv.ex.tokens import TokenCommand
from NeoVintageous.nv.ex.tokens import TokenOfCommand
from NeoVintageous.nv.ex.tokens import TokenOfRange


class TestToken(unittest.TestCase):

    def test_can_instantiate(self):
        token = Token(42, 'content val')
        self.assertEqual(token.token_type, 42)
        self.assertEqual(token.content, 'content val')

    def test_eq(self):
        token_a = Token(42, 'content val')
        token_b = Token(42, 'content val')

        self.assertTrue(token_a == token_b)
        self.assertTrue(token_a.__eq__(token_b))

        self.assertTrue(token_b == token_a)
        self.assertTrue(token_b.__eq__(token_a))

    def test_not_eq(self):
        token_a = Token(42, 'a')

        self.assertTrue(token_a == Token(42, 'a'), 'protected against false-positive')
        self.assertFalse(token_a == Token(None, None))
        self.assertFalse(token_a == Token(None, 'a'))
        self.assertFalse(token_a == Token(42, None))
        self.assertFalse(token_a == Token(42, ''))
        self.assertFalse(token_a == Token(42, 'foo'))
        self.assertFalse(token_a == Token(-7, 'a'))
        self.assertFalse(token_a == Token(0, 'a'))
        self.assertFalse(token_a == Token(7, 'a'))

        class UnknownTokenType:
            def __init__(self, token_type, content):
                self.token_type = token_type
                self.content = content

        self.assertFalse(token_a == UnknownTokenType(42, 'a'))
        self.assertFalse(token_a.__eq__(UnknownTokenType(42, 'a')))


class TestCommandToken(unittest.TestCase):

    def test_requires_name(self):
        with self.assertRaisesRegex(TypeError, 'name'):
            TokenCommand()

    def test_can_create_with_name(self):
        command = TokenCommand('only')
        self.assertEqual(command.name, 'only')

        command = TokenCommand(name='only')
        self.assertEqual(command.name, 'only')

    def test_is_instance_of_token(self):
        self.assertIsInstance(TokenCommand('only'), Token)

    def test_create_with_name_sets_target(self):
        command = TokenCommand('only')
        self.assertEqual(command.name, 'only')
        self.assertEqual(command.target, 'ex_only')

    def test_create_with_name_sets_content(self):
        command = TokenCommand('only')
        self.assertEqual(command.name, 'only')
        self.assertEqual(command.content, 'only')

    def test_can_set_target(self):
        command = TokenCommand('a', target='b')
        self.assertEqual(command.name, 'a')
        self.assertEqual(command.target, 'b')

    def test_default_attributes(self):
        command = TokenCommand('only')
        self.assertEqual(command.name, 'only')
        self.assertEqual(command.target, 'ex_only')
        self.assertEqual(command.params, {})
        self.assertEqual(command.forced, False)
        self.assertEqual(command.addressable, False)
        self.assertEqual(command.cooperates_with_global, False)

    def test_can_set_forced(self):
        self.assertTrue(TokenCommand('x', forced=True).forced)
        self.assertFalse(TokenCommand('x', forced=False).forced)

        command = TokenCommand('x', forced=False)
        command.forced = True
        self.assertTrue(command.forced)
        command.forced = False
        self.assertFalse(command.forced)

    def test_can_set_addressable(self):
        self.assertTrue(TokenCommand('x', addressable=True).addressable)
        self.assertFalse(TokenCommand('x', addressable=False).addressable)

        command = TokenCommand('x', addressable=False)
        command.addressable = True
        self.assertTrue(command.addressable)
        command.addressable = False
        self.assertFalse(command.addressable)

    def test_can_set_cooperates_with_global(self):
        self.assertTrue(TokenCommand('x', cooperates_with_global=True).cooperates_with_global)
        self.assertFalse(TokenCommand('x', cooperates_with_global=False).cooperates_with_global)

        command = TokenCommand('x', cooperates_with_global=False)
        command.cooperates_with_global = True
        self.assertTrue(command.cooperates_with_global)
        command.cooperates_with_global = False
        self.assertFalse(command.cooperates_with_global)

    def test_compare(self):
        command_a1 = TokenCommand('a')
        command_a2 = TokenCommand('a')

        self.assertTrue(command_a1 == command_a2)
        self.assertTrue(command_a2 == command_a1)
        self.assertTrue(command_a1.__eq__(command_a2))
        self.assertTrue(command_a2.__eq__(command_a1))

        command_a = TokenCommand('a')
        command_b = TokenCommand('b')

        self.assertFalse(command_a == command_b)
        self.assertFalse(command_b == command_a)
        self.assertFalse(command_a.__eq__(command_b))
        self.assertFalse(command_b.__eq__(command_a))

        command_a = TokenCommand('a', target='x')
        command_b = TokenCommand('a', target='y')

        self.assertFalse(command_a == command_b)

        command_a1 = TokenCommand('a', forced=False, addressable=True)
        command_a2 = TokenCommand('a', forced=False, addressable=True)

        self.assertTrue(command_a1 == command_a2)

        command_a1 = TokenCommand('a', forced=True, addressable=True)
        command_a2 = TokenCommand('a', forced=False, addressable=True)

        self.assertFalse(command_a1 == command_a2)


class TestTokenOfCommand(unittest.TestCase):

    def test_can_instantiate(self):
        token = TokenOfCommand({}, 42, 'c')
        self.assertEqual(token.params, {})
        self.assertEqual(token.forced, False)
        self.assertEqual(token.addressable, False)
        self.assertEqual(token.cooperates_with_global, False)
        self.assertEqual(token.target_command, None)
        self.assertEqual(token.token_type, 42)
        self.assertEqual(token.content, 'c')

    def test_is_instance_of_token(self):
        self.assertIsInstance(TokenOfCommand({}, 42, 'c'), Token)

    def test_can_set_forced_attribute(self):
        self.assertEqual(TokenOfCommand({}, 42, 'c', forced=True).forced, True)
        self.assertEqual(TokenOfCommand({}, 42, 'c', forced=False).forced, False)

    def test_eq(self):
        token_a = TokenOfCommand({}, 42, 'content val')
        token_b = TokenOfCommand({}, 42, 'content val')

        self.assertTrue(token_a == token_b)
        self.assertTrue(token_a.__eq__(token_b))

        self.assertTrue(token_b == token_a)
        self.assertTrue(token_b.__eq__(token_a))

    def test_eq_params(self):
        token_a = TokenOfCommand({'a': 'b', 'x': 'y'}, 42, 'c')
        token_b = TokenOfCommand({'a': 'b', 'x': 'y'}, 42, 'c')

        self.assertTrue(token_a == token_b)
        self.assertTrue(token_b == token_a)

    def test_not_eq(self):
        token_a = TokenOfCommand({'a': 'b', 'x': 'y'}, 42, 'c')

        self.assertTrue(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 42, 'c'), 'protect against false-positive')
        self.assertFalse(token_a == TokenOfCommand({}, 42, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, None, None))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, None, 'a'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 42, None))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 42, ''))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 42, 'foo'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, -7, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 0, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 7, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'foobar'}, 42, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'foo': 'bar'}, 42, 'c'))

        class UnknownTokenOfCommandType:
            def __init__(self, params, token_type, content):
                self.params = params or {}
                self.token_type = token_type
                self.content = content
                self.forced = False
                self.addressable = False
                self.cooperates_with_global = False
                self.target_command = None

        self.assertFalse(token_a == UnknownTokenOfCommandType({'a': 'b', 'x': 'y'}, 42, 'c'))
        self.assertFalse(token_a.__eq__(UnknownTokenOfCommandType({'a': 'b', 'x': 'y'}, 42, 'c')))

    def test_not_eq_attributes(self):
        token_a = TokenOfCommand({'x': 'y'}, 42, 'c')
        self.assertEqual(token_a.params, {'x': 'y'})
        self.assertEqual(token_a.forced, False)
        self.assertEqual(token_a.addressable, False)
        self.assertEqual(token_a.cooperates_with_global, False)
        self.assertEqual(token_a.target_command, None)
        self.assertEqual(token_a.token_type, 42)
        self.assertEqual(token_a.content, 'c')

        token_b = TokenOfCommand({'x': 'y'}, 42, 'c')
        token_b.forced = True
        self.assertFalse(token_a == token_b)

        token_b = TokenOfCommand({'x': 'y'}, 42, 'c')
        token_b.addressable = True
        self.assertFalse(token_a == token_b)

        token_b = TokenOfCommand({'x': 'y'}, 42, 'c')
        token_b.cooperates_with_global = True
        self.assertFalse(token_a == token_b)

        token_b = TokenOfCommand({'x': 'y'}, 42, 'c')
        token_b.target_command = 'foobar'
        self.assertFalse(token_a == token_b)


class TestTokenOfRange(unittest.TestCase):

    def test_can_instantiate(self):
        token = TokenOfRange(42, 'r')
        self.assertEqual(token.token_type, 42)
        self.assertEqual(token.content, 'r')

    def test_is_instance_of_token(self):
        self.assertIsInstance(TokenOfRange(42, 'c'), Token)
