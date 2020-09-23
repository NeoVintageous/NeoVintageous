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


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected msg')

TESTS = (
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 1}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 1}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 2}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 2}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 3}, 'abc abc abc',         'should join 3 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\n    abc',                   [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 3}, 'abc abc abc',         'should join 3 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc\nabc\nabc',                 [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 5}, 'abc abc abc abc abc', 'should join 5 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\n    abc\n    abc\n    abc', [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 5}, 'abc abc abc abc abc', 'should join 5 lines'),  # noqa: E241,E501
    test_data('abc\n\n',                                 [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 3}, 'abc ',                'should join 3 lines and add one trailing space'),  # noqa: E241,E501
    test_data('\n\nabc',                                 [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 3}, 'abc',                 'should join 3 lines without adding any spaces'),  # noqa: E241,E501
    test_data('abc \n    abc  \n  abc',                  [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 3}, 'abc abc  abc',        'should join 3 lines with leading spaces removed but trailing spaces intact'),  # noqa: E241,E501
    test_data('   abc\nabc   ',                          [[(0, 0), (0, 0)]],                   {'mode': unittest.INTERNAL_NORMAL, 'count': 1}, '   abc abc   ',       'should join 2 lines with leading spaces of first line and trailing spaces of last line intact'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (1, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (1, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(1, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(1, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (2, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc abc',         'should join 3 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (2, 1)]],                   {'mode': unittest.VISUAL},                       'abc abc abc',         'should join 3 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(2, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc abc',         'should join 3 lines'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(2, 1), (0, 0)]],                   {'mode': unittest.VISUAL},                       'abc abc abc',         'should join 3 lines'),  # noqa: E241,E501
    test_data('abc\nabc\nabc',                           [[(0, 0), (1, 1)]],                   {'mode': unittest.VISUAL, 'count': 3},           'abc abc\nabc',        'should join 2 lines - count shouldn\'t matter'),  # noqa: E241,E501
    test_data('abc\n    abc\nabc',                       [[(0, 0), (1, 1)]],                   {'mode': unittest.VISUAL, 'count': 3},           'abc abc\nabc',        'should join 2 lines - count shouldn\'t matter'),  # noqa: E241,E501
    test_data('   abc\nabc   ',                          [[(0, 0), (1, 5)]],                   {'mode': unittest.VISUAL},                       '   abc abc   ',       'should join 2 lines with leading spaces of first line and trailing spaces of last line intact'),  # noqa: E241,E501
    test_data('    abc\n\n\n',                           [[(0, 0), (3, 0)]],                   {'mode': unittest.VISUAL_LINE},                  '    abc \n',          'should join 4 lines'),  # noqa: E241,E501
    test_data('    abc  \n   abc\nabc',                  [[(0, 0), (0, 1)], [(1, 0), (1, 1)]], {'mode': unittest.VISUAL_BLOCK},                 '    abc  abc\nabc',   'should join 2 lines'),  # noqa: E241,E501
)


class Test__nv_vi_big_j(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            regions = [self._R(*region) for region in data.regions]
            self.select(regions)

            self.view.run_command('nv_vi_big_j', data.cmd_params)

            self.assertEqual(data.expected, self.content(), "[{0}] {1}".format(i, data.msg))
