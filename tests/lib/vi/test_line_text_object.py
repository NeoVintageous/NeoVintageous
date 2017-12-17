from collections import namedtuple

from sublime import Region

from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi.text_objects import find_line_text_object


test = namedtuple('simple_test', 'start expected msg content')

# cursor is at "|"
TESTS_INDENT = (
    test(start=Region(2, 5), expected=Region(0, 16), msg='should work', content='asf  whitespaced'),
    test(start=Region(0, 0), expected=Region(2, 13), msg='should work with whitepsace', content='  whitespaced'),
)


class Test_line(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS_INDENT):
            self.write(data.content)
            self.view.sel().clear()

            start, end = find_line_text_object(self.view, data.start)
            actual = Region(start, end)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))
