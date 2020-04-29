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

from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.nodes import TokenDigits
from NeoVintageous.nv.ex.nodes import TokenDollar
from NeoVintageous.nv.ex.nodes import TokenDot
from NeoVintageous.nv.ex.nodes import TokenMark
from NeoVintageous.nv.ex.nodes import TokenOffset
from NeoVintageous.nv.ex.nodes import TokenPercent
from NeoVintageous.nv.ex.nodes import TokenSearchBackward
from NeoVintageous.nv.ex.nodes import TokenSearchForward
from NeoVintageous.nv.ex.nodes import _resolve_line_number


class TestRangeNode(unittest.TestCase):

    def test_can_instantiate(self):
        node = RangeNode(['foo'], ['bar'], ';')
        self.assertEqual(node.start, ['foo'])
        self.assertEqual(node.end, ['bar'])
        self.assertEqual(node.separator, ';')

    def test_can_detect_if_its_empty(self):
        self.assertTrue(RangeNode().is_empty)

    def test__eq__(self):
        self.assertEqual(True, RangeNode().__eq__(RangeNode()))
        self.assertEqual(True, RangeNode().__eq__(unittest.mock.Mock(spec=RangeNode, start=[], end=[], separator=None)))
        self.assertEqual(True, RangeNode().__eq__(unittest.mock.Mock(spec=RangeNode, start=[], end=[], separator=None)))
        self.assertEqual(False, RangeNode().__eq__(unittest.mock.Mock()))
        self.assertEqual(False, RangeNode().__eq__(unittest.mock.Mock(spec=RangeNode, start=[], end=[], separator=';')))
        self.assertEqual(False, RangeNode([2]).__eq__(unittest.mock.Mock(
            spec=RangeNode, start=[], end=[], separator=None)))

    def test_to_str(self):
        self.assertEqual(str(RangeNode(['s'], ['e'], ';')), 's;e')


class TestRangeNode_resolve_line_number(unittest.ViewTestCase):

    def test_raises_exception_for_unknown_tokens(self):
        class Unknown:
            content = ''

        with self.assertRaises(NotImplementedError):
            _resolve_line_number(self.view, Unknown(), 0)

    def test_digits(self):
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('11'), 0), 10)
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('3'), 0), 2)
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('2'), 0), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('1'), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('0'), 0), -1)
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('-1'), 0), -1)
        self.assertEqual(_resolve_line_number(self.view, TokenDigits('-2'), 0), -1)

    def test_dollar(self):
        self.write('')
        self.assertEqual(_resolve_line_number(self.view, TokenDollar(), 0), 0)

        self.write('1')
        self.assertEqual(_resolve_line_number(self.view, TokenDollar(), 0), 0)

        self.write('1\n')
        self.assertEqual(_resolve_line_number(self.view, TokenDollar(), 0), 1)

        self.write('1\n2')
        self.assertEqual(_resolve_line_number(self.view, TokenDollar(), 0), 1)

        self.write('1\n2\n')
        self.assertEqual(_resolve_line_number(self.view, TokenDollar(), 0), 2)

        self.write('1\n2\n3\n')
        self.assertEqual(_resolve_line_number(self.view, TokenDollar(), 0), 3)

    def test_dot(self):
        self.write('111\n222\n333\n')

        self.assertEqual(_resolve_line_number(self.view, TokenDot(), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenDot(), 1), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenDot(), 2), 2)
        self.assertEqual(_resolve_line_number(self.view, TokenDot(), 10), 3, 'should not exceed max line of view')

    def test_mark(self):
        self.write('11\n222\n3\n44\n55\n')

        with self.assertRaises(NotImplementedError):
            _resolve_line_number(self.view, TokenMark(''), 0)

        with self.assertRaises(NotImplementedError):
            _resolve_line_number(self.view, TokenMark('foobar'), 0)

        self.select(0)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 0)

        self.select(1)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 0)

        self.select(4)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 1)

        self.select(10)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 3)

        self.select(100)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 4)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 5)

        self.select((0, 1))
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 0)

        self.select((4, 5))
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 1)

        self.select((10, 11))
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 3)

        self.select((0, self.view.size()))
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 4)

        self.select((5, 11))
        self.assertEqual(_resolve_line_number(self.view, TokenMark('<'), 0), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenMark('>'), 0), 3)

    def test_offset(self):
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([0]), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([0]), 5), 5)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([1]), 0), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([1]), 1), 2)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([1]), 9), 10)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([1, 2]), 0), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([1, 2]), 7), 10)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([-1]), 0), -1)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([-1]), 1), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([-1]), 6), 5)
        self.assertEqual(_resolve_line_number(self.view, TokenOffset([-1, -4]), 15), 10)

    def test_percent(self):
        self.write('')
        self.assertEqual(_resolve_line_number(self.view, TokenPercent(), 0), 0)

        self.write('1')
        self.assertEqual(_resolve_line_number(self.view, TokenPercent(), 0), 0)

        self.write('1\n')
        self.assertEqual(_resolve_line_number(self.view, TokenPercent(), 0), 1)

        self.write('1\n2')
        self.assertEqual(_resolve_line_number(self.view, TokenPercent(), 0), 1)

        self.write('1\n2\n')
        self.assertEqual(_resolve_line_number(self.view, TokenPercent(), 0), 2)

        self.write('1\n2\n3\n')
        self.assertEqual(_resolve_line_number(self.view, TokenPercent(), 0), 3)

    def test_search_backward(self):
        self.write('ab\ncd\nx\nabcd\ny\nz\n')

        with self.assertRaisesRegex(ValueError, 'E384: Search hit TOP without match for: foo'):
            _resolve_line_number(self.view, TokenSearchBackward('foo'), 0)

        with self.assertRaisesRegex(ValueError, 'E384: Search hit TOP without match for: bar'):
            _resolve_line_number(self.view, TokenSearchBackward('bar'), 100)

        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('a'), 100), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('a'), 5), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('a'), 4), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('a'), 3), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('a'), 2), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('a'), 1), 0)
        with self.assertRaisesRegex(ValueError, 'E384: Search hit TOP without match for: a'):
            _resolve_line_number(self.view, TokenSearchBackward('a'), 0)

        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('bc'), 5), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchBackward('bc'), 4), 3)
        with self.assertRaisesRegex(ValueError, 'E384: Search hit TOP without match for: bc'):
            _resolve_line_number(self.view, TokenSearchBackward('bc'), 3)

    def test_search_forward(self):
        self.write('ab\ncd\nx\nabcd\ny\nz\n')

        with self.assertRaisesRegex(ValueError, 'E385: Search hit BOTTOM without match for: foo'):
            _resolve_line_number(self.view, TokenSearchForward('foo'), 0)

        with self.assertRaisesRegex(ValueError, 'E385: Search hit BOTTOM without match for: bar'):
            _resolve_line_number(self.view, TokenSearchForward('bar'), 100)

        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('a'), 0), 0)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('a'), 1), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('a'), 2), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('a'), 3), 3)
        with self.assertRaisesRegex(ValueError, 'E385: Search hit BOTTOM without match for: a'):
            _resolve_line_number(self.view, TokenSearchForward('a'), 4)

        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('cd'), 0), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('cd'), 1), 1)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('cd'), 2), 3)
        self.assertEqual(_resolve_line_number(self.view, TokenSearchForward('cd'), 3), 3)
        with self.assertRaisesRegex(ValueError, 'E385: Search hit BOTTOM without match for: cd'):
            _resolve_line_number(self.view, TokenSearchForward('cd'), 4)


class TestRangeNodeResolve(unittest.ViewTestCase):

    def test_resolve_returns_current_line_if_range_is_empty(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(8)
        self.assertRegion(RangeNode().resolve(self.view), (8, 16))

    def test_resolve_returns_current_line_if_range_is_empty2(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(0)
        self.assertRegion(RangeNode().resolve(self.view), (0, 8))

    def test_resolve_returns_current_line_if_range_is_empty_and_adds_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenOffset([1, 1])]).resolve(self.view), (16, 24))

    def test_resolve_returns_current_line_if_range_is_empty_and_adds_offsets(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenOffset([2])]).resolve(self.view), (16, 24))

    def test_resolve_returns_requested_start_line_number(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenDigits('2')]).resolve(self.view), (8, 16))

    def test_resolve_returns_requested_start_line_number_and_adds_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenDigits('2'), TokenOffset([2])]).resolve(self.view), (24, 32))

    def test_resolve_returns_requested_start_line_number_and_adds_offset2(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenDigits('2'), TokenOffset([1])]).resolve(self.view), (16, 24))

    def test_resolve_returns_whole_buffer_if_percent_requested(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenPercent()]).resolve(self.view), (0, 32))

    def test_resolve__dollar__(self):
        self.write('a\nb\nc\n')
        self.select(0)
        self.assertRegion(RangeNode([TokenDollar()]).resolve(self.view), 6)

        self.write('a\nb\nc\nd\n')
        self.select(5)
        self.assertRegion(RangeNode([TokenDollar()]).resolve(self.view), 8)

    def test_resolve__dot__(self):
        self.write('a\nbcd\ne\n')
        self.select(2)
        self.assertRegion(RangeNode([TokenDot()]).resolve(self.view), (2, 6))

    def test_resolve__dot__dollar__(self):
        self.write('a\nbcd\nef\n')
        self.select(4)
        self.assertRegion(RangeNode([TokenDot()], [TokenDollar()], ',').resolve(self.view), (2, 9))

    def test_resolve__dot__4(self):
        self.write('a\nbcd\nef\ng\nhi\n')
        self.select(3)
        self.assertRegion(RangeNode([TokenDot()], [TokenDigits(4)], ',').resolve(self.view), (2, 11))

    def test_resolve__1__comma__dollar__(self):
        self.write('a\nb\n')
        self.select(0)
        self.assertRegion(RangeNode([TokenDigits(1)], [TokenDollar()], ',').resolve(self.view), (0, 4))

        self.write('a\nb\nc\nde\n')
        self.select(4)
        self.assertRegion(RangeNode([TokenDigits(1)], [TokenDollar()], ',').resolve(self.view), (0, 9))

    def test_resolve__3__comma__dollar__(self):
        self.write('a\nb\nc\nde\n')
        self.select(1)
        self.assertRegion(RangeNode([TokenDigits(3)], [TokenDollar()], ',').resolve(self.view), (4, 9))


class TestRangeNodeResolve_SearchForward(unittest.ViewTestCase):

    def test_resolve_can_search_forward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenSearchForward('cat')]).resolve(self.view), (16, 24))

    def test_resolve_can_search_forward_with_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\n')
        self.select(0)
        self.assertRegion(RangeNode(start=[TokenSearchForward('cat'), TokenOffset([1])]).resolve(self.view), (24, 32))

    def test_resolve_failed_search_throws(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\n')
        self.select(0)
        self.assertRaises(ValueError, RangeNode(start=[TokenSearchForward('dog')]).resolve, self.view)

    def test_resolve_can_search_multiple_times_forward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\neee eee\nfff cat\n')
        self.select(0)
        self.assertRegion(
            RangeNode(start=[TokenSearchForward('cat'), TokenSearchForward('cat')]).resolve(self.view),
            (40, 48)
        )


class TestRangeNodeResolve_SearchBackward(unittest.ViewTestCase):

    def test_resolve_can_search_backward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\nxxx xxx\n')
        self.select(self.view.size())
        self.assertRegion(RangeNode(start=[TokenSearchBackward('cat')]).resolve(self.view), (16, 24))

    def test_resolve_can_search_backward_with_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\nxxx xxx\n')
        self.select(self.view.size())
        self.assertRegion(RangeNode(start=[TokenSearchBackward('cat'), TokenOffset([1])]).resolve(self.view), (24, 32))

    def test_resolve_failed_search_throws(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\n')
        self.select(self.view.size())
        self.assertRaises(ValueError, RangeNode(start=[TokenSearchBackward('dog')]).resolve, self.view)

    def test_resolve_can_search_multiple_times_backward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\neee eee\nfff fff\n')
        self.select(self.view.size())
        self.assertRegion(
            RangeNode(start=[TokenSearchBackward('cat'), TokenSearchBackward('cat')]).resolve(self.view),
            (16, 24)
        )


class TestRangeNodeResolve_Line0(unittest.ViewTestCase):

    def test_resolve_can_calculate_visual_start(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\n')
        self.select((8, 10))
        self.assertRegion(RangeNode(start=[TokenDigits('0')]).resolve(self.view), (-1, -1))


class TestRangeNodeResolve_Marks(unittest.ViewTestCase):

    def test_resolve_can_calculate_visual_start(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\n')
        self.select((8, 10))
        self.assertRegion(RangeNode(start=[TokenMark("<")]).resolve(self.view), (8, 16))

    def test_resolve_can_calculate_visual_start_with_multiple_sels(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\nxxx xxx\nccc ccc\n')
        self.select([(8, 10), (24, 27)])
        self.assertRegion(RangeNode(start=[TokenMark("<")]).resolve(self.view), (8, 16))

    def test_resolve_can_calculate_visual_end(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\n')
        self.select((8, 10))
        self.assertRegion(RangeNode(start=[TokenMark(">")]).resolve(self.view), (8, 16))

    def test_resolve_can_calculate_visual_end_with_multiple_sels(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\nxxx xxx\nccc ccc\n')
        self.select((8, 10))
        self.assertRegion(RangeNode(start=[TokenMark("<"), TokenMark(">")]).resolve(self.view), (8, 16))
