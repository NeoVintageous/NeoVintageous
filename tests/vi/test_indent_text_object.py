from collections import namedtuple

from sublime import Region as R

from NeoVintageous.tests import set_text
from NeoVintageous.tests import add_sel
from NeoVintageous.tests import ViewTest

from NeoVintageous.vi.text_objects import find_indent_text_object

test = namedtuple('simple_test', 'content start expected expected_inclusive msg')

# cursor is at "|"

TESTS_INDENT = (
    test(start=R(37, 37), expected=R(29, 62), expected_inclusive=R(29, 62), msg='should find indent', content='''
# a comment
def a_ruby_block
  some_c|all
  another_one
  yerp
end'''.lstrip()),

    test(start=R(37, 37), expected=R(29, 41), expected_inclusive=R(29, 80), msg='should find indent when there\'s a blank line', content='''
# a comment
def a_ruby_block
  some_c|all

  another_one_with(blank_line)
  yerp
end'''.lstrip()),

    test(start=R(42, 42), expected=R(34, 57), expected_inclusive=R(34, 58), msg='should work with pyhton-ey functions', content='''
# a python thing
def a_python_fn:
  some_c|all()
  what()

a_python_fn'''.lstrip()),

    test(start=R(57, 57), expected=R(57, 57), expected_inclusive=R(57, 57), msg='should ignore when triggered on a whitespace-only line', content='''
# a python thing
def a_python_fn:
  some_call()
  what()

a_python_fn'''.lstrip()),
)

class Test_indent(ViewTest):
    def clear_selected_regions(self):
        self.view.sel().clear()

    def testAll(self):
        for (i, data) in enumerate(TESTS_INDENT):
            self.clear_selected_regions()
            self.write(data.content)

            for inclusive in [True, False]:
                start, end = find_indent_text_object(self.view, data.start, inclusive)
                actual = R(start, end)

                msg = "failed at test index {0}: {1}".format(i, data.msg)
                expected = data.expected_inclusive if inclusive else data.expected
                self.assertEqual(expected, actual, msg)

