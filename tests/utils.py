import unittest

import sublime

from NeoVintageous.lib.state import State


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

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.view.set_scratch(True)

    def select(self, point_or_region):
        self.view.sel().clear()
        self.view.sel().add(point_or_region)

    @property
    def state(self):
        return State(self.view)

    def clear_sel(self):
        self.view.sel().clear()

    def create(self, text=''):
        if text:
            self.view.run_command('__vi_tests_write_buffer', {'text': text})

    def write(self, text):
        if not self.view:
            raise TypeError('no view available yet')
        self.view.run_command('__vi_tests_write_buffer', {'text': text})

    def R(self, a, b=None):
        return _make_region(self.view, a, b)

    def get_all_text(self):
        return self.view.substr(self.R(0, self.view.size()))

    def add_sel(self, a=0, b=0):
        if not self.view:
            raise TypeError('no view available yet')

        if isinstance(a, sublime.Region):
            self.view.sel().add(a)
            return

        self.view.sel().add(sublime.Region(a, b))

    def num_sels(self):
        return len(self.view.sel())

    def first_sel(self):
        return self.view.sel()[0]

    def second_sel(self):
        return self.view.sel()[1]

    def region2rowcols(self, reg):
        """Return row-col pair of tuples corresponding to region start and end points."""
        points = (reg.begin(), reg.end())
        return list(map(self.view.rowcol, points))

    def tearDown(self):
        if self.view:
            self.view.close()

    def assertRegionsEqual(self, expected_region, actual_region, msg=''):
        """Test that regions covers the exact same region. Does not take region orientation into account."""
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(self.view, expected_region.begin(), expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(), actual_region.end())
        self.assertEqual(expected_region, actual_region, msg)

    def assertContentIsEqualTo(self, expected):
        self.assertEqual(self.view.substr(sublime.Region(0, self.view.size())), expected)
