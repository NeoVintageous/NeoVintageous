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


class TestUnimpairedCommands(unittest.FunctionalTestCase):

    def test_blank_down(self):
        self.eq('aaa\nbb|b\nccc', '] ', 'aaa\n|bbb\n\nccc')
        self.eq('aaa\n    bb|b\nccc', '] ', 'aaa\n    |bbb\n\nccc')
        self.eq('aaa\nbb|b\nccc', '2] ', 'aaa\n|bbb\n\n\nccc')
        self.eq('aaa\nbb|b\nccc', '5] ', 'aaa\n|bbb\n\n\n\n\n\nccc')
        self.eq('aaa\nbb|b\nccc', '5] ', 'aaa\n|bbb\n\n\n\n\n\nccc')
        self.eq('aaa\n    bb|b\nccc', '5] ', 'aaa\n    |bbb\n\n\n\n\n\nccc')
        self.eq('\n\n|\n\n\n    fizz', '] ', '\n\n|\n\n\n\n    fizz')
        self.eq('\n\n|\n\n\n    fizz', '3] ', '\n\n|\n\n\n\n\n\n    fizz')

    def test_blank_up(self):
        self.eq('aaa\nbb|b\nccc', '[ ', 'aaa\n\n|bbb\nccc')
        self.eq('aaa\n    bb|b\nccc', '[ ', 'aaa\n\n    |bbb\nccc')
        self.eq('aaa\nbb|b\nccc', '3[ ', 'aaa\n\n\n\n|bbb\nccc')
        self.eq('aaa\n    bb|b\nccc', '3[ ', 'aaa\n\n\n\n    |bbb\nccc')
        self.eq('\n\n|\n\n\n    fizz', '[ ', '\n\n\n|\n\n\n    fizz')
        self.eq('\n\n|\n\n\n    fizz', '3[ ', '\n\n\n\n\n|\n\n\n    fizz')

    def test_move_down(self):
        self.eq('111\n22|2\n333\n444', ']e', '111\n333\n22|2\n444')
        self.eq('111\n22|2\n333\n444\n555\n666\n777\n888', '5]e', '111\n333\n444\n555\n666\n777\n22|2\n888')

    def test_move_up(self):
        self.eq('111\n222\n33|3\n444', '[e', '111\n33|3\n222\n444')
        self.eq('111\n222\n333\n444\n555\n666\n77|7\n888', '3[e', '111\n222\n333\n77|7\n444\n555\n666\n888')


class TestUnimpairedToggles(unittest.FunctionalTestCase):

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

    def test_toggle_basic_options(self):
        toggles = {
            'e': 'statusbar',
            'h': 'hlsearch',
            'i': 'ignorecase',
            'l': 'list',
            'm': 'minimap',
            'n': 'number',
            't': 'sidebar',
            'w': 'wrap',
        }

        # XXX For some reason toggling the menu breaks for OSX, but possibly
        # only in CI, or maybe a bug in Sublime specific to OSX.
        if not sys.platform.startswith('darwin'):
            toggles.update({
                'a': 'menu',
            })

        for key, name in toggles.items():
            self.feed(']o%s' % key)
            self.assertOption(name, False, msg=name)
            self.feed('[o%s' % key)
            self.assertOption(name, True, msg=name)
            self.feed('[o%s' % key)
            self.assertOption(name, True, msg=name)
            self.feed(']o%s' % key)
            self.assertOption(name, False, msg=name)
            self.feed(']o%s' % key)
            self.assertOption(name, False, msg=name)
            self.feed('yo%s' % key)
            self.assertOption(name, True, msg=name)
            self.feed('yo%s' % key)
            self.assertOption(name, False, msg=name)
            self.feed('yo%s' % key)
            self.assertOption(name, True, msg=name)
