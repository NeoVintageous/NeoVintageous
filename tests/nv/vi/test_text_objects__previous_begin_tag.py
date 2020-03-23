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

from NeoVintageous.nv.vi.text_objects import previous_begin_tag


test_data = namedtuple('test_data', 'content args expected msg')


TESTS_SEARCH_TAG_BACKWARD = (
    test_data(content='<a>foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 6}, expected=(unittest.Region(0, 3), 'a', True), msg='find tag'),  # noqa: E501
    test_data(content='<a>foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 0}, expected=(None, None, None), msg="don't find tag"),  # noqa: E501
    test_data(content='</a>foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 6}, expected=(unittest.Region(0, 4), 'a', False), msg='find a closing tag'),  # noqa: E501
    test_data(content='<a>foo</a>', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 5}, expected=(unittest.Region(0, 3), 'a', True), msg='find other tag'),  # noqa: E501
    test_data(content='<a hey="ho">foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 14}, expected=(unittest.Region(0, 12), 'a', True), msg='find tag with attributes'),  # noqa: E501
)


class Test_previous_begin_tag(unittest.ViewTestCase):

    def test_previous_begin_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_SEARCH_TAG_BACKWARD):
            self.write(data.content)
            actual = previous_begin_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)
