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
from NeoVintageous.nv.ex.tokens import TokenPercent
from NeoVintageous.nv.ex.tokens import TokenDigits
from NeoVintageous.nv.ex.tokens import TokenMark
from NeoVintageous.nv.ex.tokens import TokenDollar
from NeoVintageous.nv.ex.tokens import TokenOfCommand
from NeoVintageous.nv.ex.tokens import TokenOfRange


class TestToken(unittest.TestCase):

    def test_can_instantiate(self):
        token = Token('content val')
        self.assertEqual(token.content, 'content val')

    def test_eq_true(self):
        token_a1 = Token('a')
        token_a2 = Token('a')

        self.assertTrue(token_a1 == token_a2)
        self.assertTrue(token_a1.__eq__(token_a2))
        self.assertTrue(token_a2 == token_a1)
        self.assertTrue(token_a2.__eq__(token_a1))

    def test_eq_false(self):
        token_a = Token('a')

        self.assertTrue(token_a == Token('a'), 'protect against false-positive')
        self.assertFalse(token_a == Token(None))
        self.assertFalse(token_a == Token(''))
        self.assertFalse(token_a == Token('foo'))
        self.assertFalse(token_a == Token('b'))
        self.assertFalse(token_a == Token(True))
        self.assertFalse(token_a == Token(False))

    def test_type_equality(self):
        class Unknown:
            def __init__(self, content):
                self.content = content

        class Foo(Token):
            pass

        class Bar(Foo):
            pass

        a = Token('a')
        unknown = Unknown('a')
        bar = Bar('a')
        foo = Foo('a')

        self.assertFalse(a == unknown)
        self.assertFalse(unknown == a)

        self.assertFalse(a == foo)
        self.assertFalse(foo == a)

        self.assertFalse(a == bar)
        self.assertFalse(bar == a)

        self.assertFalse(foo == bar)
        self.assertFalse(bar == foo)

        self.assertFalse(foo == unknown)
        self.assertFalse(Unknown == foo)

        percent = TokenPercent()
        dollar = TokenDollar()

        self.assertFalse(percent == dollar)
        self.assertFalse(dollar == percent)

        digits = TokenDigits('1')
        mark = TokenMark('1')

        self.assertFalse(digits == mark)
        self.assertFalse(mark == digits)


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
        token = TokenOfCommand({}, 'c')
        self.assertEqual(token.params, {})
        self.assertEqual(token.forced, False)
        self.assertEqual(token.addressable, False)
        self.assertEqual(token.cooperates_with_global, False)
        self.assertEqual(token.target_command, None)
        self.assertEqual(token.content, 'c')

    def test_is_instance_of_token(self):
        self.assertIsInstance(TokenOfCommand({}, 'c'), Token)

    def test_can_set_forced_attribute(self):
        self.assertEqual(TokenOfCommand({}, 'c', forced=True).forced, True)
        self.assertEqual(TokenOfCommand({}, 'c', forced=False).forced, False)

    def test_eq(self):
        token_a = TokenOfCommand({}, 'content val')
        token_b = TokenOfCommand({}, 'content val')

        self.assertTrue(token_a == token_b)
        self.assertTrue(token_a.__eq__(token_b))

        self.assertTrue(token_b == token_a)
        self.assertTrue(token_b.__eq__(token_a))

    def test_eq_params(self):
        token_a = TokenOfCommand({'a': 'b', 'x': 'y'}, 'c')
        token_b = TokenOfCommand({'a': 'b', 'x': 'y'}, 'c')

        self.assertTrue(token_a == token_b)
        self.assertTrue(token_b == token_a)

    def test_not_eq(self):
        token_a = TokenOfCommand({'a': 'b', 'x': 'y'}, 'c')

        self.assertTrue(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 'c'), 'protect against false-positive')
        self.assertFalse(token_a == TokenOfCommand({}, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, None))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 'a'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, None))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, ''))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'y'}, 'foo'))
        self.assertFalse(token_a == TokenOfCommand({'a': 'b', 'x': 'foobar'}, 'c'))
        self.assertFalse(token_a == TokenOfCommand({'foo': 'bar'}, 'c'))

        class NotAToken:
            def __init__(self, params, content):
                self.params = params or {}
                self.content = content
                self.forced = False
                self.addressable = False
                self.cooperates_with_global = False
                self.target_command = None

        self.assertFalse(token_a == NotAToken({'a': 'b', 'x': 'y'}, 'c'))
        self.assertFalse(token_a.__eq__(NotAToken({'a': 'b', 'x': 'y'}, 'c')))

    def test_not_eq_attributes(self):
        token_a = TokenOfCommand({'x': 'y'}, 'c')
        self.assertEqual(token_a.params, {'x': 'y'})
        self.assertEqual(token_a.forced, False)
        self.assertEqual(token_a.addressable, False)
        self.assertEqual(token_a.cooperates_with_global, False)
        self.assertEqual(token_a.target_command, None)
        self.assertEqual(token_a.content, 'c')

        token_b = TokenOfCommand({'x': 'y'}, 'c')
        token_b.forced = True
        self.assertFalse(token_a == token_b)

        token_b = TokenOfCommand({'x': 'y'}, 'c')
        token_b.addressable = True
        self.assertFalse(token_a == token_b)

        token_b = TokenOfCommand({'x': 'y'}, 'c')
        token_b.cooperates_with_global = True
        self.assertFalse(token_a == token_b)

        token_b = TokenOfCommand({'x': 'y'}, 'c')
        token_b.target_command = 'foobar'
        self.assertFalse(token_a == token_b)


class TestTokenOfRange(unittest.TestCase):

    def test_can_instantiate(self):
        token = TokenOfRange('r')
        self.assertEqual(token.content, 'r')

    def test_is_instance_of_token(self):
        self.assertIsInstance(TokenOfRange('c'), Token)
