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
            self.normal(':abc|')
            self.feed(test_key)
            self.assertNormal(':|abc')

            # shouldn't change if position already correct.
            self.feed(test_key)
            self.assertNormal(':|abc')

            # should work in the middle of words.
            self.normal(':ab|c')
            self.feed(test_key)
            self.assertNormal(':|abc')

            # shouldn't move cursor when cmdline is empty.
            self.normal(':|')
            self.feed(test_key)
            self.assertNormal(':|')

    def test_c_ctrl_e(self):
        for test_key in ('<C-e>', '<end>'):
            self.normal(':|abc')
            self.feed(test_key)
            self.assertNormal(':abc|')

            # shouldn't change if position already correct.
            self.feed(test_key)
            self.assertNormal(':abc|')

            # should work in the middle of words.
            self.normal(':a|bc')
            self.feed(test_key)
            self.assertNormal(':abc|')

            # shouldn't move cursor when cmdline is empty.
            self.normal(':|')
            self.feed(test_key)
            self.assertNormal(':|')

    def test_c_ctrl_h(self):
        for test_key in ('<C-h>',):
            self.normal(':abc|')
            self.feed(test_key)
            self.assertNormal(':ab|')

            self.normal(':ab|c')
            self.feed(test_key)
            self.assertNormal(':a|c')

            self.normal(':|')
            self.feed(test_key)
            self.assertNormal(':|')

    def test_c_ctrl_u(self):
        self.normal(':abc|')
        self.feed('<C-u>')
        self.assertNormal(':|')

        # shouldn't change when cmdline is empty.
        self.feed('<C-u>')
        self.assertNormal(':|')

        # should only remove characters up to cursor position.
        self.normal(':abc d|ef')
        self.feed('<C-u>')
        self.assertNormal(':|ef')

        # shouldn't change anything if no characters before cursor.
        self.feed('<C-w>')
        self.assertNormal(':|ef')

    def test_c_ctrl_w(self):
        self.normal(':abc|')
        self.feed('<C-w>')
        self.assertNormal(':|')

        # shouldn't change when cmdline is empty.
        self.feed('<C-w>')
        self.assertNormal(':|')

        # should only remove characters up to cursor position.
        self.normal(':ab|c')
        self.feed('<C-w>')
        self.assertNormal(':|c')

        # shouldn't change anything if no characters before cursor.
        self.feed('<C-w>')
        self.assertNormal(':|c')

        # should include whitespace.
        self.normal(':abc def    |')
        self.feed('<C-w>')
        self.assertNormal(':abc |')
        self.feed('<C-w>')
        self.assertNormal(':|')
