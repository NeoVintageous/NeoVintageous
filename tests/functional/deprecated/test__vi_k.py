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


# TODO: Test against folded regions.
# TODO: Ensure that we only create empty selections while testing. Add assert_all_sels_empty()?
# TODO: Test different values for xpos in combination with the starting col.
test_data = namedtuple('test_data', 'cmd initial_text regions cmd_params expected actual_func msg')
region_data = namedtuple('region_data', 'regions')


TESTS_MODES = (
    # NORMAL mode
    test_data(cmd='nv_vi_k', initial_text='abc\nabc', regions=[[(1, 1), (1, 1)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (0, 1)]), actual_func=first_sel, msg='should move up one line (normal mode)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='abc\nabc\nabc', regions=[[(2, 1), (2, 1)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 1, 'count': 2},  # noqa: E241,E501
              expected=region_data([(0, 1), (0, 1)]), actual_func=first_sel, msg='should move up two lines (normal mode)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo bar\nfoo', regions=[[(1, 1), (1, 1)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (0, 1)]), actual_func=first_sel, msg='should move up one line onto longer line (normal mode)'),  # noqa: E241,E501

    test_data(cmd='nv_vi_k', initial_text='foo\nfoo bar', regions=[[(1, 5), (1, 5)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 5},  # noqa: E241,E501
              expected=region_data([(0, 2), (0, 2)]), actual_func=first_sel, msg='should move onto shorter line (mode normal)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo\n\n', regions=[[(1, 0), (1, 0)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (0, 1)]), actual_func=first_sel, msg='should be able to move from empty line (mode normal)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='\n\n\n', regions=[[(1, 0), (1, 0)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(0, 0), (0, 0)]), actual_func=first_sel, msg='should move from empty line to empty line (mode normal)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(2, 1), (2, 1)]], cmd_params={'mode': unittest.NORMAL, 'xpos': 1, 'count': 100},  # noqa: E241,E501
              expected=region_data([(0, 1), (0, 1)]), actual_func=first_sel, msg='should not move too far (mode normal)'),  # noqa: E241,E501

    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(1, 1), (1, 2)]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 2},  # noqa: E241,E501
              expected=region_data([(1, 2), (0, 2)]), actual_func=first_sel, msg='move one line (visual mode)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(2, 1), (2, 2)]], cmd_params={'mode': unittest.VISUAL, 'count': 1, 'xpos': 2},  # noqa: E241,E501
              expected=region_data([(2, 2), (1, 2)]), actual_func=first_sel, msg='move opposite end greater with sel of size 1 (visual mode)'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo\nfoo\nbaz', regions=[[(1, 1), (1, 3)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 3},  # noqa: E241,E501
              expected=region_data([(1, 2), (0, 3)]), actual_func=first_sel, msg='move opposite end smaller with sel of size 2'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foobar\nbarfoo\nbuzzfizz\n', regions=[[(1, 1), (1, 4)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 3},  # noqa: E241,E501
              expected=region_data([(1, 2), (0, 3)]), actual_func=first_sel, msg='move opposite end smaller with sel of size 3'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(0, 1), (2, 1)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 1},  # noqa: E241,E501
              expected=region_data([(0, 1), (1, 2)]), actual_func=first_sel, msg='move opposite end smaller different lines no cross over'),  # noqa: E241,E501

    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(1, 0), (2, 1)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 0},  # noqa: E241,E501
              expected=region_data([(1, 0), (1, 1)]), actual_func=first_sel, msg='move opposite end smaller different lines cross over xpos at 0'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo bar\nfoo bar\nfoo bar\n', regions=[[(1, 4), (2, 4)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 4, 'count': 2},  # noqa: E241,E501
              expected=region_data([(1, 5), (0, 4)]), actual_func=first_sel, msg='move opposite end smaller different lines cross over non 0 xpos'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(0, 1), (1, 1)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 0, 'count': 1},  # noqa: E241,E501
              expected=region_data([(0, 2), (0, 0)]), actual_func=first_sel, msg='move back to same line same xpos'),  # noqa: E241,E501

    test_data(cmd='nv_vi_k', initial_text='foo\nbar\nbaz\n', regions=[[(0, 2), (1, 0)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 0, 'count': 1},  # noqa: E241,E501
              expected=region_data([(0, 3), (0, 0)]), actual_func=first_sel, msg='move back to same line opposite end has greater xpos'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text=(''.join(('foo\n',) * 50)), regions=[[(20, 2), (20, 1)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 1, 'count': 10},  # noqa: E241,E501
              expected=region_data([(20, 2), (10, 1)]), actual_func=first_sel, msg='move many opposite end greater from same line'),  # noqa: E241,E501
    test_data(cmd='nv_vi_k', initial_text=(''.join(('foo\n',) * 50)), regions=[[(21, 2), (20, 1)]], cmd_params={'mode': unittest.VISUAL, 'xpos': 1, 'count': 10},  # noqa: E241,E501
              expected=region_data([(21, 2), (10, 1)]), actual_func=first_sel, msg='move many opposite end greater from same line'),  # noqa: E241,E501
)


TESTS = TESTS_MODES


class Test__nv_vi_h(unittest.ViewTestCase):

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


test = namedtuple('simple_test', 'content regions kwargs expected msg')

MORE_TESTS = (
    test(content='''aaa
bbb
''', regions=((1, 1), (1, 1)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 1}, expected=((0, 1), (0, 1)), msg='from same length'),  # noqa: E241,E501

    test(content='''

''', regions=((1, 0), (1, 0)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0}, expected=((0, 0), (0, 0)), msg='from empty to empty'),  # noqa: E241,E501

    test(content='''
aaa
''', regions=((1, 2), (1, 2)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 2}, expected=((0, 0), (0, 0)), msg='from longer to empty'),  # noqa: E241,E501

    test(content='''aaa

''', regions=((1, 0), (1, 0)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 0}, expected=((0, 0), (0, 0)), msg='from empty to longer'),  # noqa: E241,E501

    test(content='''aaa bbb
aaa
''', regions=((1, 2), (1, 2)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 2}, expected=((0, 2), (0, 2)), msg='from shorter to longer'),  # noqa: E241,E501

    test(content='''aaa
aaa bbb
''', regions=((1, 6), (1, 6)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 6}, expected=((0, 2), (0, 2)), msg='from longer to shorter'),  # noqa: E241,E501

    #     test(content='''\t\taaa
    # aaa bbb ccc
    # ''',
    #     regions=((1, 8), (1, 8)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 8}, expected=((0, 2), (0, 2)), msg='xpos with tabs'),  # noqa: E241,E501

    test(content='''aaa
aaa bbb ccc
''', regions=((1, 8), (1, 8)), kwargs={'mode': unittest.NORMAL, 'count': 1, 'xpos': 1000}, expected=((0, 2), (0, 2)), msg='xpos stops at eol'),  # noqa: E241,E501

    # VISUAL
    test(content='''aaa

ccc
''', regions=(((1, 0), (1, 1)),), kwargs={'mode': unittest.VISUAL, 'count': 1, 'xpos': 0}, expected=((1, 1), (0, 0)), msg='from empty to non-empty (visual)'),  # noqa: E241,E501

    test(content='''aaa bbb ccc ddd
aaa bbb ccc ddd
''', regions=(((0, 6), (1, 2)),), kwargs={'mode': unittest.VISUAL, 'count': 1, 'xpos': 2}, expected=((0, 7), (0, 2)), msg='from empty to non-empty (visual)'),  # noqa: E241,E501
)


class Test__nv_vi_k_new(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(MORE_TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.content)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('nv_vi_k', data.kwargs)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            actual = self.view.sel()[0]
            self.assertEqual(self._R(*data.expected), actual, msg)
