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

from NeoVintageous.nv.vi.text_objects import get_region_end
from NeoVintageous.nv.vi.text_objects import next_end_tag
from NeoVintageous.nv.vi.text_objects import next_unbalanced_tag


test_data = namedtuple('test_data', 'content args expected msg')


TESTS_NEXT_UNBALANCED_END_TAG = (
    test_data(content='<p>foo <p>bar</p> baz</p>', args={'search': next_end_tag, 'search_args': {'start': 3}, 'restart_at': get_region_end}, expected=(unittest.Region(21, 25), 'p'), msg='find end tag skipping nested'),  # noqa: E501
)


class Test_next_unbalanced_tag(unittest.ViewTestCase):

    def test_next_unbalanced_end_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_NEXT_UNBALANCED_END_TAG):
            self.write(data.content)
            actual = next_unbalanced_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)
