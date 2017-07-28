from unittest import TestCase

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


class ViewTestCase(TestCase):

    COMMAND_LINE_MODE = modes.COMMAND_LINE
    INSERT_MODE = modes.INSERT
    INTERNAL_NORMAL_MODE = modes.INTERNAL_NORMAL
    NORMAL_MODE = modes.NORMAL
    NORMAL_INSERT_MODE = modes.NORMAL_INSERT
    OPERATOR_PENDING_MODE = modes.OPERATOR_PENDING
    SELECT_MODE = modes.SELECT
    UNKNOWN_MODE = modes.UNKNOWN
    VISUAL_BLOCK_MODE = modes.VISUAL_BLOCK
    VISUAL_LINE_MODE = modes.VISUAL_LINE
    VISUAL_MODE = modes.VISUAL

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
        self.view.sel().clear()

        if not isinstance(selections, list):
            selections = [selections]

        for selection in selections:
            if isinstance(selection, tuple):
                self.view.sel().add(Region(selection[0], selection[1]))
            else:
                self.view.sel().add(selection)

    def Region(self, a, b=None, xpos=-1):
        return Region(a, b, xpos)

    def assertRegion(self, expected, actual):
        if isinstance(expected, str):
            self.assertEqual(expected, self.view.substr(actual))
        elif isinstance(expected, int):
            self.assertEqual(Region(expected), actual)
        elif isinstance(expected, tuple):
            self.assertEqual(Region(expected[0], expected[1]), actual)
        else:
            self.assertEqual(expected, actual)

    # DEPRECATED Use newer API methods self.select(), self.Region()
    def _R(self, a, b=None):
        return _make_region(self.view, a, b)

    # DEPRECATED Favour newer API methods like, e.g. assertRegion(), assertSelection(), and assertContent()
    def _assertRegionsEqual(self, expected_region, actual_region, msg=None):
        """Test that regions covers the exact same region. Does not take region orientation into account."""
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(self.view, expected_region.begin(), expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(), actual_region.end())
        self.assertEqual(expected_region, actual_region, msg)

    def assertContent(self, expected, msg=None):
        self.assertEqual(self.view.substr(Region(0, self.view.size())), expected, msg)

    def assertSize(self, expected):
        self.assertEqual(expected, self.view.size())

    def assertSelection(self, expected):
        if isinstance(expected, int):
            self.assertEqual([Region(expected)], list(self.view.sel()))
        elif isinstance(expected, tuple):
            self.assertEqual([Region(expected[0], expected[1])], list(self.view.sel()))
        elif isinstance(expected, Region):
            self.assertEqual([expected], list(self.view.sel()))
        else:  # Defaults to expect a list of Regions.
            # TODO loop through expected and convert points and tuples to regions
            self.assertEqual(expected, list(self.view.sel()))

    def assertSelectionCount(self, expected):
        self.assertEqual(expected, len(self.view.sel()))
