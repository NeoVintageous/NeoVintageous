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

from NeoVintageous.nv.vi.text_objects import find_next_lone_bracket


test = namedtuple('simple_test', 'content start brackets expected msg')

TESTS_NEXT_BRACKET = (
    test(content='a\\}bc', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket at caret position'),  # noqa: E501
    test(content='a\\}bc', start=0, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket'),
    test(content='foo {bar foo bar}', start=16, brackets=('\\{', '\\}'), expected=unittest.Region(16, 17), msg='should find next bracket at caret position'),  # noqa: E501
)


class Test_find_next_lone_bracket(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS_NEXT_BRACKET):
            self.write(data.content)
            self.view.sel().clear()

            actual = find_next_lone_bracket(self.view, data.start, data.brackets)

            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))
