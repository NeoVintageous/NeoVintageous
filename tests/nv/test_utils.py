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

from sublime import Region

from NeoVintageous.tests import unittest

from NeoVintageous.nv.utils import extract_file_name
from NeoVintageous.nv.utils import extract_url
from NeoVintageous.nv.utils import resolve_visual_target


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


class TestResolveVisualTarget(unittest.TestCase):

    def test_forward_visual_selection(self):
        self.assertEqual(resolve_visual_target(Region(5, 11), 14), Region(5, 15))
        self.assertEqual(resolve_visual_target(Region(5, 11), 13), Region(5, 14))
        self.assertEqual(resolve_visual_target(Region(5, 11), 12), Region(5, 13))
        self.assertEqual(resolve_visual_target(Region(5, 11), 11), Region(5, 12))
        self.assertEqual(resolve_visual_target(Region(5, 11), 10), Region(5, 11))
        self.assertEqual(resolve_visual_target(Region(5, 11), 9), Region(5, 10))
        self.assertEqual(resolve_visual_target(Region(5, 11), 8), Region(5, 9))
        self.assertEqual(resolve_visual_target(Region(5, 11), 7), Region(5, 8))
        self.assertEqual(resolve_visual_target(Region(5, 11), 6), Region(5, 7))
        self.assertEqual(resolve_visual_target(Region(5, 11), 5), Region(5, 6))
        self.assertEqual(resolve_visual_target(Region(5, 11), 4), Region(6, 4))
        self.assertEqual(resolve_visual_target(Region(5, 11), 3), Region(6, 3))
        self.assertEqual(resolve_visual_target(Region(5, 11), 2), Region(6, 2))
        self.assertEqual(resolve_visual_target(Region(5, 11), 1), Region(6, 1))
        self.assertEqual(resolve_visual_target(Region(5, 11), 0), Region(6, 0))

    def test_backward_visual_selection(self):
        self.assertEqual(resolve_visual_target(Region(11, 5), 0), Region(11, 0))
        self.assertEqual(resolve_visual_target(Region(11, 5), 1), Region(11, 1))
        self.assertEqual(resolve_visual_target(Region(11, 5), 2), Region(11, 2))
        self.assertEqual(resolve_visual_target(Region(11, 5), 3), Region(11, 3))
        self.assertEqual(resolve_visual_target(Region(11, 5), 4), Region(11, 4))
        self.assertEqual(resolve_visual_target(Region(11, 5), 5), Region(11, 5))
        self.assertEqual(resolve_visual_target(Region(11, 5), 6), Region(11, 6))
        self.assertEqual(resolve_visual_target(Region(11, 5), 7), Region(11, 7))
        self.assertEqual(resolve_visual_target(Region(11, 5), 8), Region(11, 8))
        self.assertEqual(resolve_visual_target(Region(11, 5), 9), Region(11, 9))
        self.assertEqual(resolve_visual_target(Region(11, 5), 10), Region(11, 10))
        self.assertEqual(resolve_visual_target(Region(11, 5), 11), Region(11, 12))
        self.assertEqual(resolve_visual_target(Region(11, 5), 12), Region(10, 13))
        self.assertEqual(resolve_visual_target(Region(11, 5), 13), Region(10, 14))
        self.assertEqual(resolve_visual_target(Region(11, 5), 14), Region(10, 15))

    def test_invalid_visual_selection_point_is_corrected(self):
        self.assertEqual(resolve_visual_target(Region(5, 5), 3), Region(5, 3))
        self.assertEqual(resolve_visual_target(Region(5, 5), 4), Region(5, 4))
        self.assertEqual(resolve_visual_target(Region(5, 5), 5), Region(5, 6))
        self.assertEqual(resolve_visual_target(Region(5, 5), 6), Region(5, 6))
        self.assertEqual(resolve_visual_target(Region(5, 5), 7), Region(5, 7))
