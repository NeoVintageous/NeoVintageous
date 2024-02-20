# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from NeoVintageous.nv.utils import VisualBlockSelection
from NeoVintageous.nv.utils import extract_url
from NeoVintageous.nv.utils import resolve_visual_line_target
from NeoVintageous.nv.utils import resolve_visual_target
from NeoVintageous.nv.utils import sel_observer
from NeoVintageous.nv.utils import translate_char
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import DIRECTION_UP


class TestTranslateChar(unittest.TestCase):

    def test_tranlsate_char(self):
        self.assertEqual(translate_char('<bar>'), '|')
        self.assertEqual(translate_char('<bslash>'), '\\')
        self.assertEqual(translate_char('<cr>'), '\n')
        self.assertEqual(translate_char('<enter>'), '\n')
        self.assertEqual(translate_char('<k0>'), '0')
        self.assertEqual(translate_char('<k3>'), '3')
        self.assertEqual(translate_char('<kdivide>'), '/')
        self.assertEqual(translate_char('<kenter>'), '\n')
        self.assertEqual(translate_char('<lt>'), '<')
        self.assertEqual(translate_char('<sp>'), ' ')
        self.assertEqual(translate_char('<space>'), ' ')
        self.assertEqual(translate_char('<tab>'), '\t')
        self.assertEqual(translate_char('a'), 'a')
        self.assertEqual(translate_char('w'), 'w')


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
        self.assertExtractUrl('http://example.com', '[title](http://example.com):')

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

    def test_localhost(self):
        self.assertExtractUrl('http://localhost', 'http://localhost')

    def test_port(self):
        self.assertExtractUrl('http://example.com:5173', 'http://example.com:5173')
        self.assertExtractUrl('http://localhost:5173', 'http://localhost:5173')


class TestResolveVisualTarget(unittest.TestCase):

    def assertResolveVisualTarget(self, s, target, expected):
        resolve_visual_target(s, target)
        self.assertEqual(s, expected)

    def test_forwards(self):
        self.assertResolveVisualTarget(Region(5, 11), 14, Region(5, 15))
        self.assertResolveVisualTarget(Region(5, 11), 13, Region(5, 14))
        self.assertResolveVisualTarget(Region(5, 11), 12, Region(5, 13))
        self.assertResolveVisualTarget(Region(5, 11), 11, Region(5, 12))
        self.assertResolveVisualTarget(Region(5, 11), 10, Region(5, 11))
        self.assertResolveVisualTarget(Region(5, 11), 9, Region(5, 10))
        self.assertResolveVisualTarget(Region(5, 11), 8, Region(5, 9))
        self.assertResolveVisualTarget(Region(5, 11), 7, Region(5, 8))
        self.assertResolveVisualTarget(Region(5, 11), 6, Region(5, 7))
        self.assertResolveVisualTarget(Region(5, 11), 5, Region(5, 6))
        self.assertResolveVisualTarget(Region(5, 11), 4, Region(6, 4))
        self.assertResolveVisualTarget(Region(5, 11), 3, Region(6, 3))
        self.assertResolveVisualTarget(Region(5, 11), 2, Region(6, 2))
        self.assertResolveVisualTarget(Region(5, 11), 1, Region(6, 1))
        self.assertResolveVisualTarget(Region(5, 11), 0, Region(6, 0))

    def test_backwards(self):
        self.assertResolveVisualTarget(Region(11, 5), 0, Region(11, 0))
        self.assertResolveVisualTarget(Region(11, 5), 1, Region(11, 1))
        self.assertResolveVisualTarget(Region(11, 5), 2, Region(11, 2))
        self.assertResolveVisualTarget(Region(11, 5), 3, Region(11, 3))
        self.assertResolveVisualTarget(Region(11, 5), 4, Region(11, 4))
        self.assertResolveVisualTarget(Region(11, 5), 5, Region(11, 5))
        self.assertResolveVisualTarget(Region(11, 5), 6, Region(11, 6))
        self.assertResolveVisualTarget(Region(11, 5), 7, Region(11, 7))
        self.assertResolveVisualTarget(Region(11, 5), 8, Region(11, 8))
        self.assertResolveVisualTarget(Region(11, 5), 9, Region(11, 9))
        self.assertResolveVisualTarget(Region(11, 5), 10, Region(11, 10))
        self.assertResolveVisualTarget(Region(11, 5), 11, Region(10, 12))
        self.assertResolveVisualTarget(Region(11, 5), 12, Region(10, 13))
        self.assertResolveVisualTarget(Region(11, 5), 13, Region(10, 14))
        self.assertResolveVisualTarget(Region(11, 5), 14, Region(10, 15))

    def test_malformed_visual_selections_are_corrected(self):
        self.assertResolveVisualTarget(Region(5, 5), 3, Region(5, 3))
        self.assertResolveVisualTarget(Region(5, 5), 4, Region(5, 4))
        self.assertResolveVisualTarget(Region(5, 5), 5, Region(5, 6))
        self.assertResolveVisualTarget(Region(5, 5), 6, Region(5, 6))
        self.assertResolveVisualTarget(Region(5, 5), 7, Region(5, 7))


class TestResolveVisualLineTarget(unittest.ViewTestCase):

    def assertResolveVisualLineTarget(self, view, s, target, expected):
        resolve_visual_line_target(view, s, target)
        self.assertEqual(s, expected)

    def test_forwards(self):
        self.vline('12\nabc\n|fizz\n|abc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 0, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 1, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 2, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 3, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 4, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 5, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 6, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 7, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 8, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 9, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 10, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 11, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 12, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 13, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 14, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 15, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 16, Region(7, 18))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 17, Region(7, 18))
        self.assertResolveVisualLineTarget(self.view, Region(7, 12), 18, Region(7, 18))

    def test_forwards_multiline(self):
        self.vline('12\nabc\n|fizz\nbuzz\n|abc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 0, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 1, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 2, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 3, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 4, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 5, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 6, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 7, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 8, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 9, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 10, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 11, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 12, Region(7, 17))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 13, Region(7, 17))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 14, Region(7, 17))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 15, Region(7, 17))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 16, Region(7, 17))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 17, Region(7, 21))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 18, Region(7, 21))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 19, Region(7, 21))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 20, Region(7, 21))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 21, Region(7, 23))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 22, Region(7, 23))
        self.assertResolveVisualLineTarget(self.view, Region(7, 17), 23, Region(7, 23))

    def test_backwards(self):
        self.rvline('12\nabc\n|fizz\n|abc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 0, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 1, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 2, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 3, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 4, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 5, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 6, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 7, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 8, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 9, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 10, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 11, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 12, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 13, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 14, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 15, Region(7, 16))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 16, Region(7, 18))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 17, Region(7, 18))
        self.assertResolveVisualLineTarget(self.view, Region(12, 7), 18, Region(7, 18))

    def test_backwards_muliline(self):
        self.rvline('12\nabc\n|fizz\nbuzz\n|abc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 0, Region(17, 0))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 1, Region(17, 0))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 2, Region(17, 0))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 3, Region(17, 3))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 4, Region(17, 3))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 5, Region(17, 3))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 6, Region(17, 3))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 7, Region(17, 7))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 8, Region(17, 7))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 9, Region(17, 7))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 10, Region(17, 7))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 11, Region(17, 7))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 12, Region(17, 12))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 13, Region(17, 12))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 14, Region(17, 12))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 15, Region(17, 12))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 16, Region(17, 12))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 17, Region(12, 21))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 18, Region(12, 21))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 19, Region(12, 21))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 20, Region(12, 21))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 21, Region(12, 23))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 22, Region(12, 23))
        self.assertResolveVisualLineTarget(self.view, Region(17, 7), 23, Region(12, 23))

    def test_normal(self):
        self.normal('12\nabc\n|fizz\nabc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(7), 0, Region(12, 0))
        self.assertResolveVisualLineTarget(self.view, Region(7), 4, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7), 5, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7), 6, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(7), 7, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7), 8, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7), 11, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(7), 12, Region(7, 16))
        self.normal('12\nabc\nfi|zz\nabc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(9), 5, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(9), 6, Region(12, 3))
        self.assertResolveVisualLineTarget(self.view, Region(9), 7, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(9), 8, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(9), 9, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(9), 10, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(9), 11, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(9), 12, Region(7, 16))
        self.normal('12\nabc\nfizz|\nabc\n12')
        self.assertResolveVisualLineTarget(self.view, Region(11), 10, Region(12, 7))
        self.assertResolveVisualLineTarget(self.view, Region(11), 11, Region(7, 12))
        self.assertResolveVisualLineTarget(self.view, Region(11), 12, Region(7, 16))


class TestVisualBlockSelection(unittest.ViewTestCase):

    def test_single_line_forward_down(self):
        self.vblock('fi|zz bu|zz\n', DIRECTION_DOWN)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).a, 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).ab, 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).b, 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).ba, 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).begin(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).end(), 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).is_direction_down(), True)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).is_direction_up(), False)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).insertion_point_b(), 6)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).insertion_point_a(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).rowcolb(), (0, 6))

    def test_single_line_forward_up(self):
        self.rvblock('fi|zz bu|zz\n', DIRECTION_UP)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).a, 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).ab, 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).b, 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).ba, 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).begin(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).end(), 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).is_direction_down(), False)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).is_direction_up(), True)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).insertion_point_b(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).insertion_point_a(), 6)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).rowcolb(), (0, 2))

    def test_multi_line_forward_down(self):
        self.vblock('fi|zz bu|zz\nfi|zz bu|zz\n', DIRECTION_DOWN)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).a, 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).ab, 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).b, 17)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).ba, 12)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).begin(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).end(), 17)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).is_direction_down(), True)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).is_direction_up(), False)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).insertion_point_b(), 16)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).insertion_point_a(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_DOWN).rowcolb(), (1, 6))

    def test_multi_line_forward_up(self):
        self.rvblock('fi|zz bu|zz\nfi|zz bu|zz\n', DIRECTION_UP)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).a, 17)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).ab, 12)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).b, 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).ba, 7)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).begin(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).end(), 17)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).is_direction_down(), False)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).is_direction_up(), True)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).insertion_point_b(), 2)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).insertion_point_a(), 16)
        self.assertEqual(VisualBlockSelection(self.view, DIRECTION_UP).rowcolb(), (0, 2))

    def assertResolve(self, setup_fixture, target, expected_regions, expected_direction):
        setup_fixture()

        selection = VisualBlockSelection(self.view, self.getVblockDirection())

        self.assertEqual(selection.resolve_target(target), expected_regions)
        self.assertVblockDirection(expected_direction)

    def assertTransform(self, setup_fixture, target, expected, expected_direction):
        setup_fixture()

        selection = VisualBlockSelection(self.view, self.getVblockDirection())
        selection.transform_target(target)

        if 'r_' == expected[:2]:
            self.assertRVblock(expected[2:], direction=expected_direction)
        else:
            self.assertVblock(expected, direction=expected_direction)

    def test_transform_forward_single_line_down(self):
        def f(): self.vblock('fi|zz| b', DIRECTION_DOWN)  # noqa: E704
        self.assertTransform(f, 0, 'r_|fiz|z b', DIRECTION_UP)
        self.assertTransform(f, 1, 'r_f|iz|z b', DIRECTION_UP)
        self.assertTransform(f, 2, 'fi|z|z b', DIRECTION_DOWN)
        self.assertTransform(f, 3, 'fi|zz| b', DIRECTION_DOWN)
        self.assertTransform(f, 4, 'fi|zz |b', DIRECTION_DOWN)
        self.assertTransform(f, 5, 'fi|zz b|', DIRECTION_DOWN)

    def test_transform_forward_single_line_up(self):
        def f(): self.vblock('fi|zz| b', DIRECTION_UP)  # noqa: E704
        self.assertTransform(f, 0, 'r_|fiz|z b', DIRECTION_UP)
        self.assertTransform(f, 1, 'r_f|iz|z b', DIRECTION_UP)
        self.assertTransform(f, 2, 'fi|z|z b', DIRECTION_UP)
        self.assertTransform(f, 3, 'fi|zz| b', DIRECTION_UP)
        self.assertTransform(f, 4, 'fi|zz |b', DIRECTION_DOWN)
        self.assertTransform(f, 5, 'fi|zz b|', DIRECTION_DOWN)

    def test_transform_reverse_single_line_down(self):
        def f(): self.rvblock('fi|zz| b', DIRECTION_DOWN)  # noqa: E704
        self.assertTransform(f, 0, 'r_|fizz| b', DIRECTION_UP)
        self.assertTransform(f, 1, 'r_f|izz| b', DIRECTION_UP)
        self.assertTransform(f, 2, 'r_fi|zz| b', DIRECTION_DOWN)
        self.assertTransform(f, 3, 'fiz|z| b', DIRECTION_DOWN)
        self.assertTransform(f, 4, 'fiz|z |b', DIRECTION_DOWN)
        self.assertTransform(f, 5, 'fiz|z b|', DIRECTION_DOWN)

    def test_transform_reverse_single_line_up(self):
        def f(): self.rvblock('fi|zz| b', DIRECTION_UP)  # noqa: E704
        self.assertTransform(f, 0, 'r_|fizz| b', DIRECTION_UP)
        self.assertTransform(f, 1, 'r_f|izz| b', DIRECTION_UP)
        self.assertTransform(f, 2, 'r_fi|zz| b', DIRECTION_UP)
        self.assertTransform(f, 3, 'fiz|z| b', DIRECTION_UP)
        self.assertTransform(f, 4, 'fiz|z |b', DIRECTION_DOWN)
        self.assertTransform(f, 5, 'fiz|z b|', DIRECTION_DOWN)

    def test_transform_multi_line_down(self):
        for direction in (DIRECTION_DOWN, DIRECTION_UP):
            def f(): self.vblock('fizzbuzz\nfizzbuzz\nfi|zzb|uzz\nfizzbuzz\nfizzbuzz\n', direction)  # noqa: E704
            self.assertTransform(f, 0, 'r_|fiz|zbuzz\n|fiz|zbuzz\n|fiz|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 1, 'r_f|iz|zbuzz\nf|iz|zbuzz\nf|iz|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 2, 'fi|z|zbuzz\nfi|z|zbuzz\nfi|z|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 3, 'fi|zz|buzz\nfi|zz|buzz\nfi|zz|buzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 4, 'fi|zzb|uzz\nfi|zzb|uzz\nfi|zzb|uzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 5, 'fi|zzbu|zz\nfi|zzbu|zz\nfi|zzbu|zz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 6, 'fi|zzbuz|z\nfi|zzbuz|z\nfi|zzbuz|z\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 7, 'fi|zzbuzz|\nfi|zzbuzz|\nfi|zzbuzz|\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 8, 'fi|zzbuzz\n|fi|zzbuzz\n|fi|zzbuzz\n|fizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 9, 'r_fizzbuzz\n|fiz|zbuzz\n|fiz|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 10, 'r_fizzbuzz\nf|iz|zbuzz\nf|iz|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 11, 'fizzbuzz\nfi|z|zbuzz\nfi|z|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 12, 'fizzbuzz\nfi|zz|buzz\nfi|zz|buzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 13, 'fizzbuzz\nfi|zzb|uzz\nfi|zzb|uzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 14, 'fizzbuzz\nfi|zzbu|zz\nfi|zzbu|zz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 15, 'fizzbuzz\nfi|zzbuz|z\nfi|zzbuz|z\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 16, 'fizzbuzz\nfi|zzbuzz|\nfi|zzbuzz|\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 17, 'fizzbuzz\nfi|zzbuzz\n|fi|zzbuzz\n|fizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 18, 'r_fizzbuzz\nfizzbuzz\n|fiz|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 19, 'r_fizzbuzz\nfizzbuzz\nf|iz|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            if direction == DIRECTION_DOWN:
                self.assertTransform(f, 20, 'fizzbuzz\nfizzbuzz\nfi|z|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
                self.assertTransform(f, 21, 'fizzbuzz\nfizzbuzz\nfi|zz|buzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
                self.assertTransform(f, 22, 'fizzbuzz\nfizzbuzz\nfi|zzb|uzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            else:
                self.assertTransform(f, 20, 'fizzbuzz\nfizzbuzz\nfi|z|zbuzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
                self.assertTransform(f, 21, 'fizzbuzz\nfizzbuzz\nfi|zz|buzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
                self.assertTransform(f, 22, 'fizzbuzz\nfizzbuzz\nfi|zzb|uzz\nfizzbuzz\nfizzbuzz\n', DIRECTION_UP)
            self.assertTransform(f, 23, 'fizzbuzz\nfizzbuzz\nfi|zzbu|zz\nfizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 24, 'fizzbuzz\nfizzbuzz\nfi|zzbuz|z\nfizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 25, 'fizzbuzz\nfizzbuzz\nfi|zzbuzz|\nfizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 26, 'fizzbuzz\nfizzbuzz\nfi|zzbuzz\n|fizzbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 27, 'r_fizzbuzz\nfizzbuzz\n|fiz|zbuzz\n|fiz|zbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 28, 'r_fizzbuzz\nfizzbuzz\nf|iz|zbuzz\nf|iz|zbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 29, 'fizzbuzz\nfizzbuzz\nfi|z|zbuzz\nfi|z|zbuzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 30, 'fizzbuzz\nfizzbuzz\nfi|zz|buzz\nfi|zz|buzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 31, 'fizzbuzz\nfizzbuzz\nfi|zzb|uzz\nfi|zzb|uzz\nfizzbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 36, 'r_fizzbuzz\nfizzbuzz\n|fiz|zbuzz\n|fiz|zbuzz\n|fiz|zbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 37, 'r_fizzbuzz\nfizzbuzz\nf|iz|zbuzz\nf|iz|zbuzz\nf|iz|zbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 38, 'fizzbuzz\nfizzbuzz\nfi|z|zbuzz\nfi|z|zbuzz\nfi|z|zbuzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 39, 'fizzbuzz\nfizzbuzz\nfi|zz|buzz\nfi|zz|buzz\nfi|zz|buzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 40, 'fizzbuzz\nfizzbuzz\nfi|zzb|uzz\nfi|zzb|uzz\nfi|zzb|uzz\n', DIRECTION_DOWN)
            self.assertTransform(f, 41, 'fizzbuzz\nfizzbuzz\nfi|zzbu|zz\nfi|zzbu|zz\nfi|zzbu|zz\n', DIRECTION_DOWN)
            self.assertTransform(f, 42, 'fizzbuzz\nfizzbuzz\nfi|zzbuz|z\nfi|zzbuz|z\nfi|zzbuz|z\n', DIRECTION_DOWN)
            self.assertTransform(f, 43, 'fizzbuzz\nfizzbuzz\nfi|zzbuzz|\nfi|zzbuzz|\nfi|zzbuzz|\n', DIRECTION_DOWN)
            self.assertTransform(f, 44, 'fizzbuzz\nfizzbuzz\nfi|zzbuzz\n|fi|zzbuzz\n|fi|zzbuzz\n|', DIRECTION_DOWN)

    def test_transform_reverse_low_line(self):
        def f(): self.rvblock('fizzbuzz\nfizz\nfizzbu|zz|\n', DIRECTION_DOWN)  # noqa: E704
        self.assertTransform(f, 4, 'r_fizz|buzz|\nfizz|\n|fizz|buzz|\n', DIRECTION_UP)
        self.assertTransform(f, 6, 'r_fizzbu|zz|\nfizz\nfizzbu|zz|\n', DIRECTION_UP)
        self.assertTransform(f, 7, 'fizzbuz|z|\nfizz\nfizzbuz|z|\n', DIRECTION_UP)

    def test_transform_forward_low_line(self):
        def f(): self.vblock('fizzbu|zz|\nx\nfizzbuzz\n', DIRECTION_DOWN)  # noqa: E704
        self.assertTransform(f, 9, 'r_|fizzbuz|z\n|x\n|fizzbuzz\n', DIRECTION_DOWN)
        self.assertTransform(f, 17, 'fizzbu|z|z\nx\nfizzbu|z|z\n', DIRECTION_DOWN)

    def test_transform_forward_skip_line(self):
        def f(): self.vblock('fizzbu|zz|\nx\nfizz\n', DIRECTION_DOWN)  # noqa: E704
        self.assertTransform(f, 9, 'r_|fizzbuz|z\n|x\n|fizz\n', DIRECTION_DOWN)
        self.assertTransform(f, 12, 'r_f|izzbuz|z\nx|\n|f|izz\n|', DIRECTION_DOWN)
        self.assertTransform(f, 14, 'r_fiz|zbuz|z\nx\nfiz|z\n|', DIRECTION_DOWN)


class TestSelectionObserver(unittest.ViewTestCase):

    def test_has_sel_changed(self):
        self.normal('fi|zz buzz')
        with sel_observer(self.view) as observer:
            self.assertFalse(observer.has_sel_changed())
            self.select(3)
            self.assertTrue(observer.has_sel_changed())
            self.select(1)
            self.assertTrue(observer.has_sel_changed())
            self.select(2)
            self.assertFalse(observer.has_sel_changed())
            self.select([2, 3])
            self.assertTrue(observer.has_sel_changed())

        self.visual('fi|zz b|uzz')
        with sel_observer(self.view) as observer:
            self.assertFalse(observer.has_sel_changed())
            self.select((3, 6))
            self.assertTrue(observer.has_sel_changed())
            self.select((2, 5))
            self.assertTrue(observer.has_sel_changed())
            self.select((2, 6))
            self.assertFalse(observer.has_sel_changed())
            self.select(2)
            self.assertTrue(observer.has_sel_changed())
            self.select(5)
            self.assertTrue(observer.has_sel_changed())

    def test_restore_sel(self):
        self.normal('fi|zz buzz')
        with sel_observer(self.view) as observer:
            observer.restore_sel()
            self.assertNormal('fi|zz buzz')
            self.select(0)
            observer.restore_sel()
            self.assertNormal('fi|zz buzz')
            self.select(4)
            observer.restore_sel()
            self.assertNormal('fi|zz buzz')
            self.select((2, 3))
            observer.restore_sel()
            self.assertNormal('fi|zz buzz')

        self.visual('fi|zz bu|zz')
        with sel_observer(self.view) as observer:
            self.select((0, 4))
            observer.restore_sel()
            self.assertVisual('fi|zz bu|zz')
