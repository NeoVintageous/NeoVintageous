from unittest import mock  # noqa: F401
from unittest import skipIf  # noqa: F401
from unittest import TestCase  # noqa: F401
import unittest

# Use aliases to indicate that they are not public testing APIs.
from sublime import active_window as _active_window
from sublime import Region

# Use aliases to indicate that they are not public testing APIs.
from NeoVintageous.nv.state import State as _State

from NeoVintageous.nv.vi.utils import COMMAND_LINE  # noqa: F401
from NeoVintageous.nv.vi.utils import CTRL_X  # noqa: F401
from NeoVintageous.nv.vi.utils import INSERT  # noqa: F401
from NeoVintageous.nv.vi.utils import INTERNAL_NORMAL  # noqa: F401
from NeoVintageous.nv.vi.utils import NORMAL  # noqa: F401
from NeoVintageous.nv.vi.utils import NORMAL_INSERT  # noqa: F401
from NeoVintageous.nv.vi.utils import OPERATOR_PENDING  # noqa: F401
from NeoVintageous.nv.vi.utils import REPLACE  # noqa: F401
from NeoVintageous.nv.vi.utils import SELECT  # noqa: F401
from NeoVintageous.nv.vi.utils import UNKNOWN  # noqa: F401
from NeoVintageous.nv.vi.utils import VISUAL  # noqa: F401
from NeoVintageous.nv.vi.utils import VISUAL_BLOCK  # noqa: F401
from NeoVintageous.nv.vi.utils import VISUAL_LINE  # noqa: F401


# DEPRECATED Use newer APIs.
def _make_region(view, a, b=None):
    # type: (...) -> Region
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)

        return Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if isinstance(a, int) and b is None:
        pass
    elif not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError('a and b arguments must be integers or a tuple (row, col)')

    if b is not None:
        return Region(a, b)
    else:
        return Region(a)


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.view = _active_window().new_file()
        self.view.set_scratch(True)

    def tearDown(self):
        if self.view:
            self.view.close()

    def content(self):
        # type: () -> str
        return self.view.substr(Region(0, self.view.size()))

    def Region(self, a, b=None):
        # Return a Region with initial values a and b.
        #
        # This method can save having to import `sublime.Region` into test
        # modules.
        #
        # Args:
        #   a (int): The first end of the region.
        #   b (int, optional): The second end of the region. Defaults to the
        #       same as the a end of the region. May be less that a, in
        #       which case the region is a reversed one.
        return Region(a, b)

    def select(self, selections):
        # Create selection in the view.
        #
        # Existing selections are cleared. Integers are converted to Regions
        # e.g. `3 -> sublime.Region(3)`, tuples are converted to Regions e.g.
        # `(3, 5) -> sublime.Region(3, 5)`, and integers and tuples in a list
        # are also converted to Regions.
        #
        # Args:
        #   selections (int|tuple|Region|list<int|tuple|Region>):
        #
        # Usage:
        #
        #   Select a single point:
        #   >>> self.select(3)
        #
        #   Select a region of text e.g. from point 3 to 5:
        #   >>> self.select((3, 5))
        #
        #   To make multiple single point selections pass a list of integers:
        #   >>> self.select([3, 5, 7])
        #
        #   To make multiple regions of text:
        #   >>> self.select([(3, 5), (7, 11)])
        #
        #   You can also mix points and regions in a list:
        #   >>> self.select([3, 5, (7, 11), 17, (19, 23)])
        self.view.sel().clear()

        if not isinstance(selections, list):
            selections = [selections]

        for selection in selections:
            if isinstance(selection, tuple):
                self.view.sel().add(Region(selection[0], selection[1]))
            else:
                self.view.sel().add(selection)

    def settings(self):
        return self.view.settings()

    def write(self, text):
        # type: (str) -> None
        self.view.run_command('_neovintageous_test_write', {'text': text})

    def assertContent(self, expected, msg=None):
        # Test that view contents and *expected* are equal.
        #
        # Args:
        #   expected (str): Expected view contents.
        #   msg (str, optional): If specified, is used as the error message on
        #       failure.
        self.assertEqual(self.content(), expected, msg)

    def assertContentRegex(self, expected, msg=None):
        # Test that view contents matches (or does not match) *expected*.
        #
        # Args:
        #   expected (str): Expected regular expression that should match view
        #       contents.
        #   msg (str, optional): If specified, is used as the error message on
        #       failure.
        self.assertRegex(self.content(), expected, msg)

    def assertNormalMode(self):
        self.assertEquals(self.state.mode, NORMAL)

    def assertRegion(self, expected, actual):
        # Test that *actual* and *expected* are equal.
        #
        # Args:
        #   expected (str|int|tuple|Region): Expected region. *int* and *tuple*
        #       are converted to *Region*. If *str*, then *actual* is converted
        #       to a *str* before testing if both are equal.
        #   actual (Region): Actual region.
        if isinstance(expected, str):
            self.assertEqual(expected, self.view.substr(actual))
        elif isinstance(expected, int):
            self.assertEqual(Region(expected), actual)
        elif isinstance(expected, tuple):
            self.assertEqual(Region(expected[0], expected[1]), actual)
        else:
            self.assertEqual(expected, actual)

    def assertSelection(self, expected):
        # Test that view selection and *expected* are equal.
        #
        # Integers are converted to Regions e.g. `3 -> sublime.Region(3)`,
        # tuples are converted to Regions e.g. `(3, 5) -> sublime.Region(3, 5)`,
        # and integers and tuples in a list are also converted to Regions.
        #
        # Args:
        #   expected (int|tuple|Region|list<Region>):
        #
        # Usage:
        #
        #   Assert single point selection:
        #   >>> self.assertSelection(0)
        #   # Asserts that the current view has one cursor at point zero.
        #   >>> self.assertSelection(3)
        #   # Asserts that the current view has one cursor at point three.
        #
        #   Assert multiple single point selections:
        #   >>> self.assertSelection([3, 5, 7])
        #   # Asserts that the current view has three cursors at points three,
        #   # five, and seven.
        #
        #   Assert a text area selection:
        #   >>> self.assertSelection((3, 5))
        #   # Asserts that the current view has one cursor selection text from
        #   # point three to five.
        #
        #   Assert multiple text are selections:
        #   >>> self.assertSelection([(3, 5), (7, 9))
        #   # Asserts that the current view has two cursors selecting text from
        #   # point three to five, and point seven to nine.
        #
        #   You can also mix points and regions in a list:
        #   >>> self.assertSelection([3, 5, (7, 11)])
        #   # Asserts that the current view has two single point selections at
        #   # points three, and five, and one region selection from point seven
        #   # to eleven.
        if isinstance(expected, int):
            self.assertEqual([Region(expected)], list(self.view.sel()))
        elif isinstance(expected, tuple):
            self.assertEqual([Region(expected[0], expected[1])], list(self.view.sel()))
        elif isinstance(expected, Region):
            self.assertEqual([expected], list(self.view.sel()))
        else:
            # Defaults to expect a list of Regions.
            self.assertEqual(expected, list(self.view.sel()))

    def assertSelectionCount(self, expected):
        # Test that view selection count and *expected* are equal.
        #
        # Args:
        #   expected (int): Expected number of selections in view.
        self.assertEqual(expected, len(self.view.sel()))

    def assertSize(self, expected):
        # Test that number of view characters and *expected* are equal.
        #
        # Args:
        #   expected (int): Expected number of characters in view.
        self.assertEqual(expected, self.view.size())

    # DEPRECATED Try to avoid using this, it will eventually be removed in favour of something better.
    @property
    def state(self):
        return _State(self.view)

    # DEPRECATED Use newer APIs e.g. self.Region(), unittest.Region.
    def _R(self, a, b=None):
        return _make_region(self.view, a, b)

    # DEPRECATED Use newer APIs e.g. assertRegion(), assertSelection(), and assertContent().
    def _assertRegionsEqual(self, expected_region, actual_region, msg=None):
        # Test that regions covers the exact same region. Does not take region
        # orientation into account.
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(self.view, expected_region.begin(),
                                           expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(),
                                         actual_region.end())

        self.assertEqual(expected_region, actual_region, msg)
