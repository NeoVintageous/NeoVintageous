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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.modeline import _gen_modelines
from NeoVintageous.nv.modeline import do_modeline


class Test_gen_modelines(unittest.ViewTestCase):

    def test_basic(self):
        self.write('# sublime: translate_tab_to_spaces false\n'
                   '# sublime: gutter true\n'
                   '# sublime: wrap_width 55\n'
                   '# sublime: tab_size 4\n'
                   '# sublime: rulers [80,120]\n')

        expected = [
            '# sublime: translate_tab_to_spaces false',
            '# sublime: gutter true',
            '# sublime: wrap_width 55',
            '# sublime: tab_size 4',
            '# sublime: rulers [80,120]'
        ]

        self.assertEqual(expected, list(_gen_modelines(self.view, 5)))

    def test_empty(self):
        self.write('')
        self.assertEqual([], list(_gen_modelines(self.view, 5)))

    def test_invalid(self):
        self.write('# foo: bar\n'
                   'sublime: foo\n'
                   'sublime: gutter true\n'
                   '# : wrap_width 55\n'
                   '# x: tab_size 4\n')
        self.assertEqual([], list(_gen_modelines(self.view, 10)))

    def test_bottom_of_file(self):
        self.write('# 1\n'
                   '# 2\n'
                   '# 3\n'
                   '# 4\n'
                   '# 5\n'
                   '# 6\n'
                   '# 7\n'
                   '# sublime: translate_tab_to_spaces false\n'
                   '# sublime: gutter true\n'
                   '# sublime: wrap_width 55\n'
                   '# sublime: tab_size 4\n'
                   '# sublime: rulers [80,120]\n')

        expected = [
            '# sublime: translate_tab_to_spaces false',
            '# sublime: gutter true',
            '# sublime: wrap_width 55',
            '# sublime: tab_size 4',
            '# sublime: rulers [80,120]'
        ]

        self.assertEqual(expected, list(_gen_modelines(self.view, 5)))

    def test_only_checks_number_of_modelines(self):
        self.write('# 1\n'
                   '# 2\n'
                   '# 3\n'
                   '# 4\n'
                   '# 5\n'
                   '# sublime: translate_tab_to_spaces false\n'
                   '# sublime: gutter true\n'
                   '# sublime: wrap_width 55\n'
                   '# sublime: tab_size 4\n'
                   '# sublime: rulers [80,120]\n'
                   '# 11\n'
                   '# 12\n'
                   '# 13\n'
                   '# 14\n'
                   '# 15\n')

        self.assertEqual([], list(_gen_modelines(self.view, 5)))

    def test_checks_max_size_area_bof(self):
        self.write(
            '# 1.......__________..........__________..........__________.........._________|'
            '# 2.......__________..........__________..........__________.........._________|'
            '# 3.......__________..........__________..........__________.........._________|'
            '# 4.......__________..........__________..........__________.........._________|'
            '# 5.......__________..........__________..........__________.........._________|\n'
            '# sublime: translate_tab_to_spaces false\n'
            '# sublime: gutter true\n'
            '# sublime: wrap_width 55\n'
            '# sublime: tab_size 4\n'
            '# sublime: rulers [80,120]\n'
            '# 11\n'
            '# 12\n'
            '# 13\n'
            '# 14\n'
            '# 15\n')
        self.assertEqual([], list(_gen_modelines(self.view, 5)))

    def test_checks_max_size_area_eof(self):
        self.write(
            '# 1\n'
            '# 2\n'
            '# 3\n'
            '# 4\n'
            '# 5\n'
            '# sublime: translate_tab_to_spaces false\n'
            '# sublime: gutter true\n'
            '# sublime: wrap_width 55\n'
            '# sublime: tab_size 4\n'
            '# sublime: rulers [80,120]\n'
            '# 11......__________..........__________..........__________.........._________|'
            '# 12......__________..........__________..........__________.........._________|'
            '# 13......__________..........__________..........__________.........._________|'
            '# 14......__________..........__________..........__________.........._________|'
            '# 15......__________..........__________..........__________.........._________|'
        )
        self.assertEqual([], list(_gen_modelines(self.view, 5)))


class Test_do_modeline(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('vintageous_modeline', True)
        self.settings().set('translate_tab_to_spaces', True)
        self.settings().set('gutter', False)
        self.settings().set('wrap_width', 100)
        self.settings().set('rulers', [])
        self.settings().set('tab_size', 2)

    def test_basic(self):
        self.write('# sublime: translate_tab_to_spaces false\n'
                   '# sublime: gutter true\n'
                   '# sublime: wrap_width 55\n'
                   '# sublime: tab_size 4\n'
                   '# sublime: rulers [80,120]\n')

        do_modeline(self.view)

        self.assertEqual([False, True, 55, [80, 120], 4], [
            self.settings().get('translate_tab_to_spaces'),
            self.settings().get('gutter'),
            self.settings().get('wrap_width'),
            self.settings().get('rulers'),
            self.settings().get('tab_size')
        ])

    def test_none(self):
        self.write('')

        do_modeline(self.view)

        self.assertEqual([True, True, False, 100, [], 2], [
            self.settings().get('vintageous_modeline'),
            self.settings().get('translate_tab_to_spaces'),
            self.settings().get('gutter'),
            self.settings().get('wrap_width'),
            self.settings().get('rulers'),
            self.settings().get('tab_size')
        ])

    def test_invalid(self):
        self.write('# foo: bar')

        do_modeline(self.view)

        self.assertEqual([True, True, False, 100, [], 2], [
            self.settings().get('vintageous_modeline'),
            self.settings().get('translate_tab_to_spaces'),
            self.settings().get('gutter'),
            self.settings().get('wrap_width'),
            self.settings().get('rulers'),
            self.settings().get('tab_size')
        ])
