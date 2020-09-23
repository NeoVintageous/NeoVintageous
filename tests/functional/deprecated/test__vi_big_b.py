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


def first_sel(self):
    return self.view.sel()[0]


test_data = namedtuple('test_data', 'content sel params expected actual_func msg')

TESTS = (
    test_data(content='abc', sel=[[(0, 2), (0, 2)]],
              params={'mode': unittest.NORMAL}, expected=[(0, 0), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from single word in file (normal mode)'),
    test_data(content='abc abc', sel=[[(0, 4), (0, 4)]],
              params={'mode': unittest.NORMAL}, expected=[(0, 0), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from second word start (normal mode)'),
    test_data(content='abc a', sel=[[(0, 4), (0, 4)]],
              params={'mode': unittest.NORMAL}, expected=[(0, 0), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from second word start (1-char long) (normal mode)'),

    test_data(content='abc abc', sel=[[(0, 5), (0, 5)]],
              params={'mode': unittest.NORMAL, 'count': 2}, expected=[(0, 0), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from second word (count 2) (normal mode)'),

    test_data(content='abc abc', sel=[[(0, 5), (0, 5)]],
              params={'mode': unittest.NORMAL, 'count': 10}, expected=[(0, 0), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from second word (excessive count) (normal mode)'),

    test_data(content='abc', sel=[[(0, 2), (0, 3)]],
              params={'mode': unittest.VISUAL}, expected=[(0, 3), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from single word in file (visual mode)'),
    test_data(content='abc abc', sel=[[(0, 4), (0, 5)]],
              params={'mode': unittest.VISUAL}, expected=[(0, 5), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from second word start (visual mode)'),
    test_data(content='abc a', sel=[[(0, 4), (0, 5)]],
              params={'mode': unittest.VISUAL}, expected=[(0, 5), (0, 0)],
              actual_func=first_sel, msg='moves to BOF from second word start (1-char long) (visual mode)'),

    test_data(content='abc abc', sel=[[(0, 4), (0, 7)]],
              params={'mode': unittest.VISUAL}, expected=[(0, 4), (0, 5)],
              actual_func=first_sel, msg='moves to word start from 1-word selection (visual mode)'),
    test_data(content='abc abc', sel=[[(0, 0), (0, 8)]],
              params={'mode': unittest.VISUAL}, expected=[(0, 0), (0, 5)],
              actual_func=first_sel, msg='moves to previous word start from multiword selection (visual mode)'),
)


class Test__nv_vi_b(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.content)
            self.select([self._R(*region) for region in data.sel])

            self.view.run_command('nv_vi_big_b', data.params)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            actual = data.actual_func(self)
            self.assertEqual(self._R(*data.expected), actual, msg)
