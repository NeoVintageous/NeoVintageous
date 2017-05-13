import unittest

import sublime

from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi.utils import modes


def _make_region(view, a, b=None):
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)

        return sublime.Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if isinstance(a, int) and b is None:
        pass
    elif not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError("a and b parameters must be either ints or (row, col)")

    if b is not None:
        return sublime.Region(a, b)
    else:
        return sublime.Region(a)


class ViewTestCase(unittest.TestCase):

    modes = modes

    def setUp(self):
        self.view = sublime.active_window().new_file()
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
        return self.view.substr(sublime.Region(0, self.view.size()))

    def write(self, text):
        self.view.run_command('__vi_tests_write_buffer', {'text': text})

    def select(self, point_or_region):
        self.view.sel().clear()
        self.view.sel().add(point_or_region)

    def selectRegion(self, a, b):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(a, b))

    def selectMultiple(self, points_and_or_regions):
        self.view.sel().clear()
        for point_or_region in points_and_or_regions:
            self.view.sel().add(point_or_region)

    def R(self, a, b=None):
        return _make_region(self.view, a, b)

    def assertRegionsEqual(self, expected_region, actual_region, msg=None):
        """Test that regions covers the exact same region. Does not take region orientation into account."""
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(self.view, expected_region.begin(), expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(), actual_region.end())
        self.assertEqual(expected_region, actual_region, msg)

    def assertContent(self, expected, msg=None):
        self.assertEqual(self.view.substr(sublime.Region(0, self.view.size())), expected, msg)

    def assertSelectionCount(self, expected):
        self.assertEqual(expected, len(self.view.sel()))

    def assertFirstSelection(self, expected):
        self.assertEqual(expected, self.view.sel()[0])

    def assertSecondSelection(self, expected):
        self.assertEqual(expected, self.view.sel()[1])
