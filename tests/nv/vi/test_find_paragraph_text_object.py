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

from NeoVintageous.nv.vi.text_objects import find_paragraph_text_object


# Note: trailing spaces are encoded in unicode to prevent automatic traling
# white space removal.
TEXT = '''
0  ip0.1
1  ip0.2
2  ip0.3

\u0020\u0020\u0020
5  ip2.1
6  ip2.2
7  ip2.3

9  ip4.1
10 ip4.2
11 ip4.3

\u0020\u0020\u0020\u0020

15 ip6.1
16 ip6.2
17 ip6.3
'''.lstrip()


test_data = namedtuple('test_data', 'start_region motion expected_region msg')


ALL_CASES = (
    #          start_region      motion   expected_region  msg
    test_data([(6, 2), (6, 2)], '1ip', [(5, 0), (8, 0)], 'basic'),
    test_data([(6, 2), (6, 2)], '1ap', [(5, 0), (9, 0)], 'basic'),

    test_data([(6, 2), (6, 2)], '3ip', [(5, 0), (12, 0)], 'counts'),
    test_data([(6, 2), (6, 2)], '2ap', [(5, 0), (15, 0)], 'counts'),

    test_data([(0, 0), (0, 0)], '1ip', [(0, 0), (3, 0)], 'start of view'),
    test_data([(0, 0), (0, 0)], '2ap', [(0, 0), (9, 0)], 'start of view'),

    test_data([(9, 0), (9, 0)], '3ip', [(9, 0), (18, 0)], 'end of view'),
    test_data([(8, 0), (8, 0)], '2ap', [(8, 0), (18, 0)], 'end of view'),
)


class Test_find_paragraph_text_object(unittest.ViewTestCase):

    def runTests(self, data):

        def region2rowcols(reg):
            """Return row-col pair of tuples corresponding to region start and end points."""
            points = (reg.begin(), reg.end())
            return list(map(self.view.rowcol, points))

        for (i, td) in enumerate(data):
            # Get method params from the Vim motion.
            count = int(td.motion[0:-2])
            inclusive = td.motion[-2] == 'a'

            # Set up the view.
            self.write(TEXT)

            r = self._R(*td.start_region)

            self.select(r)

            # Expected vs actual region returned by find_paragraph_text_object().
            exp = self._R(*td.expected_region)
            got = find_paragraph_text_object(self.view, r, inclusive=inclusive, count=count)

            rcs = [region2rowcols(r) for r in (exp, got)]
            msg = 'find_paragraph_text_object(msg={!r}, motion={}, exp_rc={}, got_rc={})'.format(
                  td.msg, td.motion, *rcs)

            self._assertRegionsEqual(exp, got, msg)

    def test_all_cases(self):
        self.runTests(ALL_CASES)
