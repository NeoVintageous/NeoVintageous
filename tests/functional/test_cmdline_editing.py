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


class TestNvCmdlineEditing(unittest.ViewTestCase):

    # TODO [refactor] Into usable run test command-line mode command via feed.
    def feed(self, seq):
        self.view.run_command('_nv_cmdline_feed_key', {'key': seq})

    def test_c_ctrl_b(self):
        for test_key in ('<C-b>', '<home>'):
            self.fixture(':abc|')
            self.feed(test_key)
            self.expects(':|abc')

            # shouldn't change if position already correct.
            self.feed(test_key)
            self.expects(':|abc')

            # should work in the middle of words.
            self.fixture(':ab|c')
            self.feed(test_key)
            self.expects(':|abc')

            # shouldn't move cursor when cmdline is empty.
            self.fixture(':|')
            self.feed(test_key)
            self.expects(':|')

    def test_c_ctrl_e(self):
        for test_key in ('<C-e>', '<end>'):
            self.fixture(':|abc')
            self.feed(test_key)
            self.expects(':abc|')

            # shouldn't change if position already correct.
            self.feed(test_key)
            self.expects(':abc|')

            # should work in the middle of words.
            self.fixture(':a|bc')
            self.feed(test_key)
            self.expects(':abc|')

            # shouldn't move cursor when cmdline is empty.
            self.fixture(':|')
            self.feed(test_key)
            self.expects(':|')

    def test_c_ctrl_h(self):
        for test_key in ('<C-h>',):
            self.fixture(':abc|')
            self.feed(test_key)
            self.expects(':ab|')

            self.fixture(':ab|c')
            self.feed(test_key)
            self.expects(':a|c')

            self.fixture(':|')
            self.feed(test_key)
            self.expects(':|')

    def test_c_ctrl_u(self):
        self.fixture(':abc|')
        self.feed('<C-u>')
        self.expects(':|')

        # shouldn't change when cmdline is empty.
        self.feed('<C-u>')
        self.expects(':|')

        # should only remove characters up to cursor position.
        self.fixture(':abc d|ef')
        self.feed('<C-u>')
        self.expects(':|ef')

        # shouldn't change anything if no characters before cursor.
        self.feed('<C-w>')
        self.expects(':|ef')

    def test_c_ctrl_w(self):
        self.fixture(':abc|')
        self.feed('<C-w>')
        self.expects(':|')

        # shouldn't change when cmdline is empty.
        self.feed('<C-w>')
        self.expects(':|')

        # should only remove characters up to cursor position.
        self.fixture(':ab|c')
        self.feed('<C-w>')
        self.expects(':|c')

        # shouldn't change anything if no characters before cursor.
        self.feed('<C-w>')
        self.expects(':|c')

        # should include whitespace.
        self.fixture(':abc def    |')
        self.feed('<C-w>')
        self.expects(':abc |')
        self.feed('<C-w>')
        self.expects(':|')
