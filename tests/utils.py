import unittest

from sublime import Region
from sublime import active_window

from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi.utils import modes


def _make_region(view, a, b=None):
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)

        return Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if isinstance(a, int) and b is None:
        pass
    elif not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError("a and b parameters must be either ints or (row, col)")

    if b is not None:
        return Region(a, b)
    else:
        return Region(a)


class ViewTestCase(unittest.TestCase):

    modes = modes

    def setUp(self):
        self.view = active_window().new_file()
        self.view.set_scratch(True)

    def tearDown(self):
        if self.view:
            self.view.close()

    @property
    def state(self):
        return State(self.view)

    def settings(self):
        return self.view.settings()

    def content(self):
        return self.view.substr(Region(0, self.view.size()))

    def write(self, text):
        self.view.run_command('__neovintageous_test_write', {'text': text})

    def select(self, selections):
        # Create selections in the test view.
        #
        # selections -- point|tuple|Region|list<point|tuple|Region>
        #
        # Points and tuples are converted to regions.
        #
        # # Examples
        #
        #     self.select(3)
        #     self.select((3, 5))
        #     self.select([3, 5, 7])
        #     self.select([(3, 5), (7, 11))
        #     self.select([3, (7, 11), 17, (19, 23))
        #
        #     # The above is shorthand for:
        #
        #     self.select(sublime.Region(3))
        #     self.select(sublime.Region(3, 5))
        #     self.select([sublime.Region(3), sublime.Region(5), sublime.Region(7)])
        #     self.select([sublime.Region(3, 5), sublime.Region(7, 11))
        #     self.select([sublime.Region(3), sublime.Region(7, 11), sublime.Region(17), sublime.Region(19, 23)])
        self.view.sel().clear()

        if not isinstance(selections, list):
            selections = [selections]

        for selection in selections:
            if isinstance(selection, tuple):
                self.view.sel().add(Region(selection[0], selection[1]))
            else:
                self.view.sel().add(selection)

    # DEPRECATED??? in favour of self.select() or self.select(self.region(...))
    def selectRegion(self, a, b, xpos=-1):
        self.select(Region(a, b, xpos))

    # DEPRECATED??? in favour of self.select() instead
    def selectMultiple(self, points_and_or_regions):
        self.select(points_and_or_regions)

    def region(self, a, b=None, xpos=-1):
        return Region(a, b, xpos)

    # DEPRECATED??? in favour of self.select() or self.select(self.region(...))
    def R(self, a, b=None):
        return _make_region(self.view, a, b)

    # DEPRECATED???
    def assertRegionsEqual(self, expected_region, actual_region, msg=None):
        """Test that regions covers the exact same region. Does not take region orientation into account."""
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(self.view, expected_region.begin(), expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(), actual_region.end())
        self.assertEqual(expected_region, actual_region, msg)

    def assertContent(self, expected, msg=None):
        self.assertEqual(self.view.substr(Region(0, self.view.size())), expected, msg)

    def assertSelection(self, expected):
        # Test the expected selection is the same as the selection in the test view.
        #
        # expected -- point|tuple|Region|list<Region>
        #
        # Points and tuples are converted to regions.
        #
        # # Examples
        #
        #     self.assertSelection(3)
        #     self.assertSelection((3, 5))
        #     self.assertSelection([self.region(3, 5), self.region(7)])
        #
        #     # The above is shorthand for:
        #
        #     self.assertEqual([sublime.Region(3)], list(self.view.sel()))
        #     self.assertEqual([sublime.Region(3, 5)], list(self.view.sel()))
        #     self.assertEqual([sublime.Region(3, 5), sublime.Region(7)], list(self.view.sel()))
        if isinstance(expected, int):
            self.assertEqual([Region(expected)], list(self.view.sel()))
        elif isinstance(expected, tuple):
            self.assertEqual([Region(expected[0], expected[1])], list(self.view.sel()))
        elif isinstance(expected, Region):
            self.assertEqual([expected], list(self.view.sel()))
        else:  # Defaults to expect a list of regions.
            self.assertEqual(expected, list(self.view.sel()))

    def assertFirstSelection(self, expected):
        # Works similar to assertSelection() except the etst is only against the
        # first selection.
        if isinstance(expected, int):
            self.assertEqual(Region(expected), self.view.sel()[0])
        elif isinstance(expected, tuple):
            self.assertEqual(Region(expected[0], expected[1]), self.view.sel()[0])
        else:  # Defaults to expect a region.
            self.assertEqual(expected, self.view.sel()[0])

    def assertSecondSelection(self, expected):
        # Works similar to assertSelection() except the etst is only against the
        # first selection.
        if isinstance(expected, int):
            self.assertEqual(Region(expected), self.view.sel()[1])
        elif isinstance(expected, tuple):
            self.assertEqual(Region(expected[0], expected[1]), self.view.sel()[1])
        else:  # Defaults to expect a region.
            self.assertEqual(expected, self.view.sel()[1])

    def assertSelectionCount(self, expected):
        self.assertEqual(expected, len(self.view.sel()))
