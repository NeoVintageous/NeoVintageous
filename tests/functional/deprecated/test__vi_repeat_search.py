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


class Test__nv_vi_repeat_star_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')

    def test_repeat_forward_twice(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_repeat_reverse(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_repeat_reverse_twice(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.assertNormal('foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')

    def test_repeat_forward_reverse_twice_forward_thrice(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_repeat_no_partial(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabcxend')
        self.view.run_command('nv_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabcxend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend')


class Test__nv_vi_repeat_octothorp_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\nabc\nbar\n|abc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')

    def test_repeat_reverse(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_repeat_no_partial(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabcxend')
        self.view.run_command('nv_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabcxend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend')


class Test__nv_vi_repeat_slash_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})
        self.setLastSearchCommand('nv_vi_slash')
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\nabc\nbar\n|abc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')

    def test_repeat_reverse(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})
        self.setLastSearchCommand('nv_vi_slash')
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.assertNormal('foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')

    def test_repeat_partial(self):
        self.normal('|foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})
        self.setLastSearchCommand('nv_vi_slash')
        self.assertNormal('foo\n|abc\nbar\nabcxmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcxmoo\nabc\nend')
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\nabc\nbar\n|abcxmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|xmoo\nabc\nend')


class Test__nv_vi_repeat_question_mark_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})
        self.setLastSearchCommand('nv_vi_question_mark')
        self.assertNormal('foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\nabc\nbar\n|abc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')

    def test_repeat_reverse(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})
        self.setLastSearchCommand('nv_vi_question_mark')
        self.assertNormal('foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.assertNormal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_repeat_partial(self):
        self.normal('|foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})
        self.setLastSearchCommand('nv_vi_question_mark')
        self.assertNormal('foo\nabc\nbar\nabcxmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabcxmoo\n|abc|\nend')
        self.view.run_command('nv_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.assertNormal('foo\nabc\nbar\n|abcxmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|xmoo\nabc\nend')
