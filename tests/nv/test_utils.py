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

from NeoVintageous.nv.utils import extract_file_name
from NeoVintageous.nv.utils import extract_url


class TestExtractFileName(unittest.ViewTestCase):

    def assertExtractFileName(self, expected, text):
        self.normal(text)
        self.assertEqual(extract_file_name(self.view), expected)

    def test_extract_file_name(self):
        tests = {
            '|': None,
            'REA|DME.md': 'README.md',
            ' REA|DME.md ': 'README.md',
            '\nREA|DME.md\n': 'README.md',
            'path/to/REA|DME.md': 'path/to/README.md',
            ' pat|h/to/README.md ': 'path/to/README.md',
            '\npath|/to/README.md\n': 'path/to/README.md',
        }

        for text, expected in tests.items():
            self.assertExtractFileName(expected, text)

    def test_invalid(self):
        self.assertExtractFileName(None, '|')
        self.assertExtractFileName(None, '$|$$')


class TestExtractUrl(unittest.ViewTestCase):

    def assertExtractUrl(self, expected, text):
        self.normal(text)
        self.assertEqual(extract_url(self.view), expected)

    def test_extract_uri(self):
        self.assertExtractUrl('http://example.com', 'http://example.com')

    def test_invalid(self):
        self.assertExtractUrl(None, '')
        self.assertExtractUrl(None, 'http')
        self.assertExtractUrl(None, 'http://.com')

    def test_basic(self):
        self.assertExtractUrl('http://example.com', 'http://example.com')
        self.assertExtractUrl('https://example.com', 'https://example.com')

        self.assertExtractUrl('http://EXAMPLE.COM', 'http://EXAMPLE.COM _xxx_')
        self.assertExtractUrl('http://www.example.com', 'http://www.example.com _xxx_')
        self.assertExtractUrl('http://sub.example.com', 'http://sub.example.com _xxx_')
        self.assertExtractUrl('http://sub.sub.example.com', 'http://sub.sub.example.com _xxx_')

        self.assertExtractUrl('http://example.com/x/y', 'http://example.com/x/y _xxx_')
        self.assertExtractUrl('http://example.com/x/y.html', 'http://example.com/x/y.html _xxx_')
        self.assertExtractUrl('http://example.com/x/y.html#x', 'http://example.com/x/y.html#x _xxx_')
        self.assertExtractUrl('http://example.com/x/y.html#x-y', 'http://example.com/x/y.html#x-y _xxx_')
        self.assertExtractUrl('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')
        self.assertExtractUrl('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')

    def test_trailing_stop_is_ignored(self):
        self.assertExtractUrl('http://example.com', 'http://example.com.')

    def test_trailing_parens_are_ignored(self):
        self.assertExtractUrl('http://example.com', 'http://example.com)')
        self.assertExtractUrl('http://example.com', 'http://example.com).')

    def test_markdown_links(self):
        self.assertExtractUrl('http://example.com', '[title](http://example.com)')

    def test_markdown_images(self):
        self.assertExtractUrl('https://example.com', '[![Alt](https://example.com)]')

    def test_quoted_urls(self):
        self.assertExtractUrl('http://example.com', '"http://example.com"')
        self.assertExtractUrl('http://example.com', '\'http://example.com\'')

    def test_urls_within_strings_within_lists_with_trailing_comma__inception__(self):
        self.assertExtractUrl('http://example.com', '"http://example.com",')
        self.assertExtractUrl('http://example.com', '\'http://example.com\',')

    def test_dashes(self):
        self.assertExtractUrl('http://api-v1.example.com', 'http://api-v1.example.com.')
