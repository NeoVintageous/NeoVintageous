from NeoVintageous.tests import unittest

from NeoVintageous.nv.ex.cmd_substitute import TokenCommandSubstitute
from NeoVintageous.nv.ex.nodes import CommandLineNode
from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.nodes import TokenDigits
from NeoVintageous.nv.ex.nodes import TokenDollar
from NeoVintageous.nv.ex.nodes import TokenDot
from NeoVintageous.nv.ex.nodes import TokenMark
from NeoVintageous.nv.ex.nodes import TokenOffset
from NeoVintageous.nv.ex.nodes import TokenPercent
from NeoVintageous.nv.ex.nodes import TokenSearchBackward
from NeoVintageous.nv.ex.nodes import TokenSearchForward


class TestRangeNode(unittest.TestCase):

    def test_can_instantiate(self):
        node = RangeNode('foo', 'bar', ';')
        self.assertEqual(node.start, 'foo')
        self.assertEqual(node.end, 'bar')
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


class TestRangeNodeResolve(unittest.ViewTestCase):

    def test_resolve_returns_current_line_if_range_is_empty(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(8)
        self.assertRegion((8, 16), RangeNode().resolve(self.view))

    def test_resolve_returns_current_line_if_range_is_empty2(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(0)
        self.assertRegion((0, 8), RangeNode().resolve(self.view))

    def test_resolve_returns_current_line_if_range_is_empty_and_adds_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion((16, 24), RangeNode(start=[TokenOffset([1, 1])]).resolve(self.view))

    def test_resolve_returns_current_line_if_range_is_empty_and_adds_offsets(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion((16, 24), RangeNode(start=[TokenOffset([2])]).resolve(self.view))

    def test_resolve_returns_requested_start_line_number(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion((8, 16), RangeNode(start=[TokenDigits('2')]).resolve(self.view))

    def test_resolve_returns_requested_start_line_number_and_adds_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion((24, 32), RangeNode(start=[TokenDigits('2'), TokenOffset([2])]).resolve(self.view))

    def test_resolve_returns_requested_start_line_number_and_adds_offset2(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion((16, 24), RangeNode(start=[TokenDigits('2'), TokenOffset([1])]).resolve(self.view))

    def test_resolve_returns_whole_buffer_if_percent_requested(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\nddd ddd\n')
        self.select(0)
        self.assertRegion((0, 32), RangeNode(start=[TokenPercent()]).resolve(self.view))

    def test_resolve__dollar__(self):
        self.write('a\nb\nc\n')
        self.select(0)
        self.assertRegion(6, RangeNode([TokenDollar()]).resolve(self.view))

        self.write('a\nb\nc\nd\n')
        self.select(5)
        self.assertRegion(8, RangeNode([TokenDollar()]).resolve(self.view))

    def test_resolve__dot__(self):
        self.write('a\nbcd\ne\n')
        self.select(2)
        self.assertRegion((2, 6), RangeNode([TokenDot()]).resolve(self.view))

    def test_resolve__dot__dollar__(self):
        self.write('a\nbcd\nef\n')
        self.select(4)
        self.assertRegion((2, 9), RangeNode([TokenDot()], [TokenDollar()], ',').resolve(self.view))

    def test_resolve__dot__4(self):
        self.write('a\nbcd\nef\ng\nhi\n')
        self.select(3)
        self.assertRegion((2, 11), RangeNode([TokenDot()], [TokenDigits(4)], ',').resolve(self.view))

    def test_resolve__1__comma__dollar__(self):
        self.write('a\nb\n')
        self.select(0)
        self.assertRegion((0, 4), RangeNode([TokenDigits(1)], [TokenDollar()], ',').resolve(self.view))

        self.write('a\nb\nc\nde\n')
        self.select(4)
        self.assertRegion((0, 9), RangeNode([TokenDigits(1)], [TokenDollar()], ',').resolve(self.view))

    def test_resolve__3__comma__dollar__(self):
        self.write('a\nb\nc\nde\n')
        self.select(1)
        self.assertRegion((4, 9), RangeNode([TokenDigits(3)], [TokenDollar()], ',').resolve(self.view))


class TestRangeNodeResolve_SearchForward(unittest.ViewTestCase):

    def test_resolve_can_search_forward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\n')
        self.select(0)
        self.assertRegion((16, 24), RangeNode(start=[TokenSearchForward('cat')]).resolve(self.view))

    def test_resolve_can_search_forward_with_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\n')
        self.select(0)
        self.assertRegion((24, 32), RangeNode(start=[TokenSearchForward('cat'), TokenOffset([1])]).resolve(self.view))

    def test_resolve_failed_search_throws(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\n')
        self.select(0)
        self.assertRaises(ValueError, RangeNode(start=[TokenSearchForward('dog')]).resolve, self.view)

    def test_resolve_can_search_multiple_times_forward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\neee eee\nfff cat\n')
        self.select(0)
        self.assertRegion(
            (40, 48),
            RangeNode(start=[TokenSearchForward('cat'), TokenSearchForward('cat')]).resolve(self.view))


class TestRangeNodeResolve_SearchBackward(unittest.ViewTestCase):

    def test_resolve_can_search_backward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\nxxx xxx\n')
        self.select(self.view.size())
        self.assertRegion((16, 24), RangeNode(start=[TokenSearchBackward('cat')]).resolve(self.view))

    def test_resolve_can_search_backward_with_offset(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd ddd\nxxx xxx\n')
        self.select(self.view.size())
        self.assertRegion((24, 32), RangeNode(start=[TokenSearchBackward('cat'), TokenOffset([1])]).resolve(self.view))

    def test_resolve_failed_search_throws(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\n')
        self.select(self.view.size())
        self.assertRaises(ValueError, RangeNode(start=[TokenSearchBackward('dog')]).resolve, self.view)

    def test_resolve_can_search_multiple_times_backward(self):
        self.write('aaa aaa\nbbb bbb\nccc cat\nddd cat\neee eee\nfff fff\n')
        self.select(self.view.size())
        self.assertRegion(
            (16, 24),
            RangeNode(start=[TokenSearchBackward('cat'), TokenSearchBackward('cat')]).resolve(self.view))


class TestRangeNodeResolve_Line0(unittest.ViewTestCase):

    def test_resolve_can_calculate_visual_start(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\n')
        self.select((8, 10))
        self.assertRegion((-1, -1), RangeNode(start=[TokenDigits('0')]).resolve(self.view))


class TestRangeNodeResolve_Marks(unittest.ViewTestCase):

    def test_resolve_can_calculate_visual_start(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\n')
        self.select((8, 10))
        self.assertRegion((8, 16), RangeNode(start=[TokenMark("<")]).resolve(self.view))

    def test_resolve_can_calculate_visual_start_with_multiple_sels(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\nxxx xxx\nccc ccc\n')
        self.select([(8, 10), (24, 27)])
        self.assertRegion((8, 16), RangeNode(start=[TokenMark("<")]).resolve(self.view))

    def test_resolve_can_calculate_visual_end(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\n')
        self.select((8, 10))
        self.assertRegion((8, 16), RangeNode(start=[TokenMark(">")]).resolve(self.view))

    def test_resolve_can_calculate_visual_end_with_multiple_sels(self):
        self.write('xxx xxx\naaa aaa\nxxx xxx\nbbb bbb\nxxx xxx\nccc ccc\n')
        self.select((8, 10))
        self.assertRegion((8, 16), RangeNode(start=[TokenMark("<"), TokenMark(">")]).resolve(self.view))


class TestCommandLineNode(unittest.TestCase):

    def test_can_instantiate(self):
        range_node = RangeNode("foo", "bar", False)
        command = TokenCommandSubstitute({})
        command_line_node = CommandLineNode(range_node, command)

        self.assertEqual(range_node, command_line_node.line_range)
        self.assertEqual(command, command_line_node.command)
