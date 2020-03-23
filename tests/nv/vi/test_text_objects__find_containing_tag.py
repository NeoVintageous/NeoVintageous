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

from NeoVintageous.nv.vi.text_objects import find_containing_tag


test_data = namedtuple('test_data', 'content args expected msg')


TESTS_CONTAINING_TAG = (
    test_data(content='<a>foo</a>', args={'start': 4}, expected=(unittest.Region(0, 3), unittest.Region(6, 10), 'a'), msg='find tag'),  # noqa: E501
    test_data(content='<div>foo</div>', args={'start': 5}, expected=(unittest.Region(0, 5), unittest.Region(8, 14), 'div'), msg='find long tag'),  # noqa: E501
    test_data(content='<div class="foo">foo</div>', args={'start': 17}, expected=(unittest.Region(0, 17), unittest.Region(20, 26), 'div'), msg='find tag with attributes'),  # noqa: E501
    test_data(content='<div>foo</div>', args={'start': 2}, expected=(unittest.Region(0, 5), unittest.Region(8, 14), 'div'), msg='find tag from within start tag'),  # noqa: E501
    test_data(content='<div>foo</div>', args={'start': 13}, expected=(unittest.Region(0, 5), unittest.Region(8, 14), 'div'), msg='find tag from within end tag'),  # noqa: E501
    test_data(content='<div>foo <p>bar</p></div>', args={'start': 12}, expected=(unittest.Region(9, 12), unittest.Region(15, 19), 'p'), msg='find nested tag from inside'),  # noqa: E501
    test_data(content='<head><link rel="shortcut icon" href="favicon.png"></head>', args={'start': 16}, expected=(unittest.Region(0, 6), unittest.Region(51, 58), 'head'), msg='find head'),  # noqa: E501
)


class Test_find_containing_tag(unittest.ViewTestCase):

    def test_find_containing_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_CONTAINING_TAG):
            self.write(data.content)
            actual = find_containing_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)
