from collections import namedtuple

from sublime import Region as R

from NeoVintageous.tests import set_text
from NeoVintageous.tests import add_sel
from NeoVintageous.tests import ViewTest

from NeoVintageous.vi.text_objects import find_line_text_object

test = namedtuple('simple_test', 'start expected msg content')

# cursor is at "|"

TESTS_INDENT = (
    test(start=R(2, 5), expected=R(0, 16),
         msg='should work', content='asf  whitespaced'),
    test(start=R(0, 0), expected=R(2, 13),
         msg='should work with whitepsace', content='  whitespaced'),
)

class Test_line(ViewTest):
    def clear_selected_regions(self):
        self.view.sel().clear()

    def testAll(self):
        for (i, data) in enumerate(TESTS_INDENT):
            self.clear_selected_regions()
            self.write(data.content)

            start, end = find_line_text_object(self.view, data.start)
            actual = R(start, end)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)

