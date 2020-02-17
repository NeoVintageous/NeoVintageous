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

from NeoVintageous.nv.marks import get_mark
from NeoVintageous.nv.marks import set_mark


class TestMarks(unittest.ViewTestCase):

    def test_can_set_mark(self):
        self.normal('fi|zz')
        set_mark(self.view, 'p')
        self.assertRegion(get_mark(self.view, 'p'), 2)

    def test_no_mark(self):
        self.normal('fi|zz')
        self.assertEqual(None, get_mark(self.view, 'u'))

    def test_can_retrieve_mark_in_the_current_buffer(self):
        self.normal('|fizz')
        set_mark(self.view, 'p')
        self.assertRegion(get_mark(self.view, 'p'), 0)

    def test_can_retrieve_mark_in_the_current_buffer_as_tuple2(self):
        self.normal('foo bar\nfoo bar\nfoo bar\n|foo bar\nfoo bar\n')
        set_mark(self.view, 'p')
        self.assertRegion(get_mark(self.view, 'p'), 24)

    def do_can_retrieve_quote_or_backtick_mark_test(self, name, jumplist_back):
        jumplist_back.return_value = (self.view, [self.Region(7)])
        self.normal('|fizz\nbuzz\nfizz\nbuzz')
        self.assertRegion(get_mark(self.view, name), 7)
        jumplist_back.assert_called_once_with(self.view)

    @unittest.mock.patch('NeoVintageous.nv.marks.jumplist_back')
    def test_can_retrieve_quote_mark(self, jumplist_back):
        self.do_can_retrieve_quote_or_backtick_mark_test('`', jumplist_back)

    @unittest.mock.patch('NeoVintageous.nv.marks.jumplist_back')
    def test_can_retrieve_backtick_mark(self, jumplist_back):
        self.do_can_retrieve_quote_or_backtick_mark_test('\'', jumplist_back)

    def do_can_retrieve_quote_or_backtick_mark_from_other_view(self, name, jumplist_back):
        panel = self.view.window().create_output_panel('test_mark', unlisted=True)
        jumplist_back.return_value = (panel, [self.Region(7)])
        self.normal('|fizz\nbuzz\nfizz\nbuzz')
        self.assertEqual(get_mark(self.view, name), (panel, self.Region(7)))
        jumplist_back.assert_called_once_with(self.view)

    @unittest.mock.patch('NeoVintageous.nv.marks.jumplist_back')
    def test_can_retrieve_quote_mark_from_other_view(self, jumplist_back):
        self.do_can_retrieve_quote_or_backtick_mark_from_other_view('`', jumplist_back)

    @unittest.mock.patch('NeoVintageous.nv.marks.jumplist_back')
    def test_can_retrieve_backtick_mark_from_other_view(self, jumplist_back):
        self.do_can_retrieve_quote_or_backtick_mark_from_other_view('\'', jumplist_back)
