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


test_data = namedtuple('test_data', 'cmd initial_text regions cmd_params expected actual_func msg')
region_data = namedtuple('region_data', 'regions')


TESTS_MODES = (
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[1, 1]], cmd_params={'mode': unittest.NORMAL, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(1, 1), (1, 1)]), actual_func=first_sel, msg='move one line down'),
    test_data(cmd='nv_vi_j', initial_text=(''.join('abc\n' * 60)), regions=[[1, 1]], cmd_params={'mode': unittest.NORMAL, 'count': 50, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(50, 1), (50, 1)]), actual_func=first_sel, msg='move many lines down'),
    test_data(cmd='nv_vi_j', initial_text=(''.join('abc\n' * 60)), regions=[[1, 1]], cmd_params={'mode': unittest.NORMAL, 'count': 50, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(50, 1), (50, 1)]), actual_func=first_sel, msg='move many lines down'),
    test_data(cmd='nv_vi_j', initial_text='foo\nfoo bar\nfoo bar', regions=[[1, 1]], cmd_params={'mode': unittest.NORMAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(1, 1), (1, 1)]), actual_func=first_sel, msg='move onto longer line'),
    test_data(cmd='nv_vi_j', initial_text='foo bar\nfoo\nbar', regions=[[5, 5]], cmd_params={'mode': unittest.NORMAL, 'count': 1, 'xpos': 5},  # noqa: E241,E501
              expected=region_data([(1, 2), (1, 2)]), actual_func=first_sel, msg='move onto shorter line'),
    test_data(cmd='nv_vi_j', initial_text='\nfoo\nbar', regions=[[0, 0]], cmd_params={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(1, 0), (1, 0)]), actual_func=first_sel, msg='move from empty line'),

    test_data(cmd='nv_vi_j', initial_text='\n\nbar', regions=[[0, 0]], cmd_params={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(1, 0), (1, 0)]), actual_func=first_sel, msg='move from empty line'),
    test_data(cmd='nv_vi_j', initial_text='foo\nbar\nbaz', regions=[[0, 0]], cmd_params={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(1, 0), (1, 0)]), actual_func=first_sel, msg='move from empty line'),

    test_data(cmd='nv_vi_j', initial_text='abc\nabc', regions=[[1, 2]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (1, 2)]), actual_func=first_sel, msg='move onto next line (VISUAL)'),
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[10, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 10), (1, 1)]), actual_func=first_sel, msg='move from empty line'),
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[6, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 2, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 5), (2, 2)]), actual_func=first_sel, msg='move from empty line'),
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[6, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 100, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 5), (2, 2)]), actual_func=first_sel, msg='xxxx'),
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[6, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(1, 2), (1, 1)]), actual_func=first_sel, msg='move from different line to home position'),  # noqa: E241,E501
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[6, 5]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 5), (2, 2)]), actual_func=first_sel, msg='move from empty line'),
    test_data(cmd='nv_vi_j', initial_text=('abc\n' * 60), regions=[[1, 2]], cmd_params={'mode': unittest.VISUAL, 'count': 50, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (50, 2)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo\nfoo bar\nfoo bar', regions=[[1, 2]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (1, 2)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo bar\nfoo\nbar', regions=[[5, 6]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 5},  # noqa: E241,E501
              expected=region_data([(0, 5), (1, 4)]), actual_func=first_sel, msg='move from longer to shorter'),
    test_data(cmd='nv_vi_j', initial_text='\nfoo\nbar', regions=[[0, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 1)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='\n\nbar', regions=[[0, 1]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 1)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo\nbar\nbaz', regions=[[1, 2]], cmd_params={'mode': unittest.VISUAL, 'count': 10000, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (2, 2)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[1, 1]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text=('abc\n' * 60), regions=[[1, 1]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 50, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (50, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo\nfoo bar\nfoo bar', regions=[[1, 1]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 8)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo bar\nfoo\nbar', regions=[[5, 5]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 1, 'xpos': 5},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='\nfoo\nbar', regions=[[0, 0]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='\n\nbar', regions=[[0, 0]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 1)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo\nbar\nbaz', regions=[[1, 1]], cmd_params={'mode': unittest.INTERNAL_NORMAL, 'count': 10000, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (2, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='abc\nabc\nabc', regions=[[0, 4]], cmd_params={'mode': unittest.VISUAL_LINE, 'count': 1, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text=('abc\n' * 60), regions=[[0, 4]], cmd_params={'mode': unittest.VISUAL_LINE, 'count': 50, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (50, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='\nfoo\nbar', regions=[[0, 1]], cmd_params={'mode': unittest.VISUAL_LINE, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 4)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='\n\nbar', regions=[[1, 0]], cmd_params={'mode': unittest.VISUAL_LINE, 'count': 1, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (1, 1)]), actual_func=first_sel, msg='move many lines'),
    test_data(cmd='nv_vi_j', initial_text='foo\nbar\nbaz', regions=[[0, 4]], cmd_params={'mode': unittest.VISUAL_LINE, 'count': 10000, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 0), (2, 4)]), actual_func=first_sel, msg='move many lines'),
)


TESTS = TESTS_MODES

test = namedtuple('simple_test', 'content regions kwargs expected msg')

MORE_TESTS = (
    test(content='''aaa
bbb
''', regions=((1,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 1}, expected=((1, 1), (1, 1)), msg='from same length'),  # noqa: E241,E501

    test(content='''

''', regions=((0,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0}, expected=((1, 0), (1, 0)), msg='from empty to empty'),  # noqa: E241,E501

    test(content='''aaa

''', regions=((2,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 2}, expected=((1, 0), (1, 0)), msg='from longer to empty'),  # noqa: E241,E501

    test(content='''
aaa
''', regions=((0,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0}, expected=((1, 0), (1, 0)), msg='from empty to longer'),  # noqa: E241,E501

    test(content='''aaa
aaa bbb
''', regions=((2,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 2}, expected=((1, 2), (1, 2)), msg='from shorter to longer'),  # noqa: E241,E501

    test(content='''aaa bbb
aaa
''', regions=((6,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 6}, expected=((1, 2), (1, 2)), msg='from longer to shorter'),  # noqa: E241,E501

    #     test(content='''aaa bbb ccc
    # \t\taaa
    # ''',
    #     regions=((8,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 8}, expected=((1, 2), (1, 2)), msg='xpos with tabs'),  # noqa: E241,E501

    test(content='''aaa bbb ccc
aaa
''', regions=((8,),), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 1000}, expected=((1, 2), (1, 2)), msg='xpos stops at eol'),  # noqa: E241,E501

    # VISUAL MODE
    test(content='''
aaa
''', regions=((0, 1),), kwargs={'mode': unittest.VISUAL, 'count': 1, 'xpos': 0}, expected=((0, 0), (1, 1)), msg='from empty to non-empty (visual)'),  # noqa: E241,E501
)


class Test__nv_vi_j(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command(data.cmd, data.cmd_params)

            msg = "failed at test index {0} {1}".format(i, data.msg)
            actual = data.actual_func(self)

            if isinstance(data.expected, region_data):
                self.assertEqual(self._R(*data.expected.regions), actual, msg)
            else:
                self.assertEqual(data.expected, actual, msg)


class Test__nv_vi_j_new(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(MORE_TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.content)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('nv_vi_j', data.kwargs)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            actual = self.view.sel()[0]
            self.assertEqual(self._R(*data.expected), actual, msg)
