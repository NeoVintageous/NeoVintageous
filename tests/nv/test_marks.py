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

from NeoVintageous.nv.marks import _marks
from NeoVintageous.nv.marks import add_mark
from NeoVintageous.nv.marks import get_mark_as_encoded_address


class View():
    def __init__(self, id_, fname, buffer_id=0):
        self.view_id = id_
        self.fname = fname
        self._buffer_id = buffer_id

    def file_name(self):
        return self.fname

    def buffer_id(self):
        return self._buffer_id


class Window():
    pass


class MarksTests(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        _marks.clear()
        self.view.sel().clear()
        self.view.sel().add(self.Region(0, 0))

    def test_can_set_mark(self):
        add_mark(self.view, 'a')
        expected_win, expected_view, expected_region = (self.view.window(), self.view, (0, 0))
        actual_win, actual_view, actual_region = _marks['a']
        self.assertEqual((actual_win.id(), actual_view.view_id, actual_region),
                         (expected_win.id(), expected_view.view_id, expected_region))

    def test_can_retrieve_mark_in_the_current_buffer_as_tuple(self):
        add_mark(self.view, 'a')
        # The caret's at the beginning of the buffer.
        self.assertEqual(get_mark_as_encoded_address(self.view, 'a'), self.Region(0, 0))

    def test_can_retrieve_mark_in_the_current_buffer_as_tuple2(self):
        self.write(''.join(('foo bar\n') * 10))
        self.view.sel().clear()
        self.view.sel().add(self.Region(30, 30))
        add_mark(self.view, 'a')
        self.assertEqual(get_mark_as_encoded_address(self.view, 'a'), self.Region(24, 24))

    def test_can_retrieve_mark_in_a_different_buffer_as_encoded_mark(self):
        view = View(id_=self.view.view_id + 1, fname=r'C:\foo.txt')

        _marks['a'] = (Window(), view, (0, 0))
        expected = "{0}:{1}".format(r'C:\foo.txt', "0:0")
        self.assertEqual(get_mark_as_encoded_address(self.view, 'a'), expected)

    def test_can_retrieve_mark_in_an_untitled_buffer_as_encoded_mark(self):
        view = View(id_=self.view.view_id + 1, fname='', buffer_id=999)

        _marks['a'] = (Window(), view, (0, 0))
        expected = "<untitled {0}>:{1}".format(999, "0:0")
        self.assertEqual(get_mark_as_encoded_address(self.view, 'a'), expected)

    @unittest.mock.patch('NeoVintageous.nv.marks.jumplist_back')
    def test_can_retrieve_quote_mark(self, mock_jumplist_back):
        # Single quote mark should call jumplist_back for its region ignoring
        # any mark set for "'".
        _marks['\''] = (Window(), self.view, (0, 0))
        mock_jumplist_back.return_value = (self.view, [self.Region(30, 30)])
        self.write(''.join(('foo bar\n') * 10))

        location = get_mark_as_encoded_address(self.view, "'")
        self.assertEqual(location, self.Region(24, 24))

    @unittest.mock.patch('NeoVintageous.nv.marks.jumplist_back')
    def test_can_retrieve_backtick_mark(self, mock_jumplist_back):
        # Backtick mark should call jumplist_back for its region ignoring any
        # mark set for "`". Here we set exact to true, emulating ``.
        _marks['`'] = (Window(), self.view, (0, 0))
        mock_jumplist_back.return_value = (self.view, [self.Region(30, 30)])
        self.write(''.join(('foo bar\n') * 10))

        location = get_mark_as_encoded_address(self.view, "`", exact=True)
        self.assertEqual(location, self.Region(30, 30))
