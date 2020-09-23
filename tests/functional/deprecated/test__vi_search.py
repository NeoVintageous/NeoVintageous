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


class Test__nv_vi_slash_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_search_begin(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(4)

    def test_search_wrap(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(25)

        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(4)

    def test_search_wrap_mid_match(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(22)

        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(4)

    def test_search_wrap_end(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(27)

        self.view.run_command('nv_vi_slash_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(4)


class Test__nv_vi_question_mark_InNormalMode(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_search_wrap_begin(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(20)

    def test_search_wrap(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(25)

        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(20)

    def test_search_wrap_mid_match(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(12)

        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(4)

    def test_search_end(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(27)

        self.view.run_command('nv_vi_question_mark_impl', {'mode': unittest.NORMAL, 'pattern': 'abc'})

        self.assertSelection(20)
