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

from NeoVintageous.nv.vi.text_objects import find_prev_lone_bracket


test = namedtuple('simple_test', 'content start brackets expected msg')

TESTS = (
    test(content='aaa', start=1, brackets=('\\{', '\\}'), expected=None, msg='should return none'),
    test(content='a{a}a', start=1, brackets=('\\{', '\\}'), expected=unittest.Region(1, 2), msg='should find bracket at caret position'),  # noqa: E501
    test(content='{aa}a', start=1, brackets=('\\{', '\\}'), expected=unittest.Region(0, 1), msg='should find bracket at BOF'),  # noqa: E501
    test(content='bbb{aa}a', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find brackets after caret'),  # noqa: E501
    test(content='a{bc', start=3, brackets=('\\{', '\\}'), expected=unittest.Region(1, 2), msg='should find unbalanced bracket before caret'),  # noqa: E501

    test(content='foo {bar {foo} bar}', start=16, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find outer bracket from RHS'),  # noqa: E501
    test(content='foo {bar {foo} bar}', start=7, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find outer bracket from LHS'),  # noqa: E501
    test(content='foo {bar {foo} bar}', start=13, brackets=('\\{', '\\}'), expected=unittest.Region(9, 10), msg='should find inner bracket'),  # noqa: E501

    test(content='foo {bar {foo} bar', start=16, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find outer if unbalanced outer'),  # noqa: E501
    test(content='foo {bar {foo} bar', start=12, brackets=('\\{', '\\}'), expected=unittest.Region(9, 10), msg='should find inner if unbalanced outer'),  # noqa: E501
    test(content='foo {bar {foo} bar', start=4, brackets=('\\{', '\\}'), expected=unittest.Region(4, 5), msg='should find bracket at caret position'),  # noqa: E501

    test(content='foo <bar <foo> bar>', start=16, brackets=('<', '>'), expected=unittest.Region(4, 5), msg='should find outer angle bracket from RHS'),  # noqa: E501
    test(content='foo <bar <foo> bar>', start=7, brackets=('<', '>'), expected=unittest.Region(4, 5), msg='should find outer angle bracket from LHS'),  # noqa: E501
    test(content='foo <bar <foo> bar>', start=13, brackets=('<', '>'), expected=unittest.Region(9, 10), msg='should find inner angle bracket'),  # noqa: E501

    test(content='a\\{bc', start=2, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket at caret position'),  # noqa: E501
    test(content='a\\{bc', start=3, brackets=('\\{', '\\}'), expected=None, msg='should not find escaped bracket'),
)


class Test_find_previous_lone_bracket(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.content)
            self.view.sel().clear()
            actual = find_prev_lone_bracket(self.view, data.start, data.brackets)
            self.assertEqual(data.expected, actual, "failed at test index {0}: {1}".format(i, data.msg))
