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


class Test__vi_repeat_star_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(20)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_forward_twice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse_twice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})

        self.assertSelection(20)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_forward_reverse_twice_forward_thrice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})
        for i in range(0, 2):
            self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})
        for i in range(0, 3):
            self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_no_partial(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabcxend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(4, 7), self.Region(12, 15)])


class Test__vi_repeat_octothorp_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_no_partial(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabcxend')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(4, 7), self.Region(12, 15)])


class Test__vi_repeat_slash_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': unittest.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertSelection(4)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': unittest.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertSelection(4)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})

        self.assertSelection(20)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_partial(self):
        self.write('foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': unittest.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertSelection(4)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])


class Test__vi_repeat_question_mark_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': unittest.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertSelection(20)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': unittest.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertSelection(20)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_partial(self):
        self.write('foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': unittest.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertSelection(20)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': unittest.NORMAL, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])
