from collections import namedtuple

from sublime import Region

from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi.text_objects import find_indent_text_object


test = namedtuple('simple_test', 'content start expected expected_inclusive msg')

# cursor is at "|"

TESTS_INDENT = (
    test(start=Region(37, 37), expected=Region(29, 62), expected_inclusive=Region(29, 62), msg='should find indent', content='''
# a comment
def a_ruby_block
  some_c|all
  another_one
  yerp
end'''.lstrip()),

    test(start=Region(37, 37), expected=Region(29, 41), expected_inclusive=Region(29, 80), msg='should find indent when there\'s a blank line', content='''
# a comment
def a_ruby_block
  some_c|all

  another_one_with(blank_line)
  yerp
end'''.lstrip()),

    test(start=Region(42, 42), expected=Region(34, 57), expected_inclusive=Region(34, 58), msg='should work with pyhton-ey functions', content='''
# a python thing
def a_python_fn:
  some_c|all()
  what()

a_python_fn'''.lstrip()),

    test(start=Region(57, 57), expected=Region(57, 57), expected_inclusive=Region(57, 57), msg='should ignore when triggered on a whitespace-only line', content='''
# a python thing
def a_python_fn:
  some_call()
  what()

a_python_fn'''.lstrip()),
)


class Test_indent(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS_INDENT):
            self.write(data.content)
            self.view.sel().clear()

            for inclusive in [True, False]:
                start, end = find_indent_text_object(self.view, data.start, inclusive)
                actual = Region(start, end)

                msg = "failed at test index {0}: {1}".format(i, data.msg)
                expected = data.expected_inclusive if inclusive else data.expected
                self.assertEqual(expected, actual, msg)
