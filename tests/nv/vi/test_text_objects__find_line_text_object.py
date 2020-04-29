# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from collections import namedtuple

from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.text_objects import find_line_text_object


test = namedtuple('simple_test', 'start expected msg content')

# cursor is at "|"
TESTS_INDENT = (
    test(start=unittest.Region(2, 5), expected=unittest.Region(0, 16), msg='should work', content='asf  whitespaced'),
    test(start=unittest.Region(0, 0), expected=unittest.Region(2, 13), msg='should work with whitepsace', content='  whitespaced'),  # noqa: E501
)


class Test_find_line_text_object(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS_INDENT):
            self.write(data.content)
            self.view.sel().clear()

            start, end = find_line_text_object(self.view, data.start)
            actual = self.Region(start, end)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))
