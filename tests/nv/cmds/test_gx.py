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

import re
import unittest

from NeoVintageous.nv.cmds_vi_actions import _vi_gx


class Test_gx(unittest.TestCase):

    URL_REGEX = re.compile(_vi_gx.URL_REGEX)

    def assertMatch(self, expected, text):
        self.assertEqual(expected, _vi_gx._url(self.URL_REGEX, text))

    def test_invalid(self):
        self.assertMatch(None, '')
        self.assertMatch(None, 'http')
        self.assertMatch(None, 'http://.com')

    def test_basic(self):
        self.assertMatch('http://example.com', 'http://example.com')
        self.assertMatch('https://example.com', 'https://example.com')

        self.assertMatch('http://EXAMPLE.COM', 'http://EXAMPLE.COM _xxx_')
        self.assertMatch('http://www.example.com', 'http://www.example.com _xxx_')
        self.assertMatch('http://sub.example.com', 'http://sub.example.com _xxx_')
        self.assertMatch('http://sub.sub.example.com', 'http://sub.sub.example.com _xxx_')

        self.assertMatch('http://example.com/x/y', 'http://example.com/x/y _xxx_')
        self.assertMatch('http://example.com/x/y.html', 'http://example.com/x/y.html _xxx_')
        self.assertMatch('http://example.com/x/y.html#x', 'http://example.com/x/y.html#x _xxx_')
        self.assertMatch('http://example.com/x/y.html#x-y', 'http://example.com/x/y.html#x-y _xxx_')
        self.assertMatch('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')
        self.assertMatch('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')

    def test_trailing_stop_is_ignored(self):
        self.assertMatch('http://example.com', 'http://example.com.')

    def test_trailing_parens_are_ignored(self):
        self.assertMatch('http://example.com', 'http://example.com)')
        self.assertMatch('http://example.com', 'http://example.com).')

    def test_markdown_links(self):
        self.assertMatch('http://example.com', '[title](http://example.com)')

    def test_markdown_images(self):
        self.assertMatch('https://example.com', '[![Alt](https://example.com)]')

    def test_quoted_urls(self):
        self.assertMatch('http://example.com', '"http://example.com"')
        self.assertMatch('http://example.com', '\'http://example.com\'')

    def test_urls_within_strings_within_lists_with_trailing_comma__inception__(self):
        self.assertMatch('http://example.com', '"http://example.com",')
        self.assertMatch('http://example.com', '\'http://example.com\',')
