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

from NeoVintageous.nv.vi.text_objects import big_word_start
from NeoVintageous.nv.vi.text_objects import big_word_end


class TestIssue280(unittest.ViewTestCase):

    def test_big_word_guards_against_runaway_loops(self):
        self.write("a bc_ x")
        self.settings().set('word_separators', "_./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?")
        self.assertEqual(big_word_start(self.view, 2), 2)
        self.assertEqual(big_word_end(self.view, 2), 4)

    def _run_caW(self):
        self.view.run_command(
            'nv_vi_c',
            {
                'motion': {
                    'motion_args': {
                        'text_object': 'W',
                        'mode': unittest.INTERNAL_NORMAL,
                        'count': 1,
                        'inclusive': True
                    },
                    'motion': 'nv_vi_select_text_object'
                },
                'mode': unittest.INTERNAL_NORMAL,
                'count': 1,
                'register': '"'
            }
        )

    def test_should_not_cause_recursion_resulting_in_hang_1(self):
        self.write("$$\n\\E\\left[ \\langle \\partial_i k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.select(21)
        self._run_caW()
        self.assertContent("$$\n\\E\\left[ \\langle  k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.assertSelection(20)

    def test_should_not_cause_recursion_resulting_in_hang_2(self):
        self.settings().set('word_separators', "_./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?")
        self.write("$$\n\\E\\left[ \\langle \\partial_i k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.select(21)
        self._run_caW()
        self.assertContent("$$\n\\E\\left[ \\langle _i k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.assertSelection(20)

    def test_should_not_cause_recursion_resulting_in_hang_3(self):
        self.write("$$\n\\E\\left[ \\langle \\partial_i k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.settings().set('syntax', 'Packages/LaTeX/LaTeX.sublime-syntax')
        self.select(21)
        self._run_caW()
        self.assertContent("$$\n\\E\\left[ \\langle  k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.assertSelection(20)

    def _run_daW(self):
        self.view.run_command(
            'nv_vi_d',
            {
                'motion': {
                    'motion': 'nv_vi_select_text_object',
                    'motion_args': {
                        'inclusive': True,
                        'count': 1,
                        'mode': unittest.INTERNAL_NORMAL,
                        'text_object': 'W'
                    }
                },
                'register': '"',
                'count': 1,
                'mode': unittest.INTERNAL_NORMAL
            }
        )

    def test_should_not_cause_recursion_resulting_in_hang_4(self):
        self.write("$$\n\\E\\left[ \\langle \\partial_i k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.settings().set('syntax', 'Packages/LaTeX/LaTeX.sublime-syntax')
        self.settings().set('word_separators', "_./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?")
        self.select(21)
        self._run_daW()
        self.assertContent("$$\n\\E\\left[ \\langle _i k(x, \\cdot), \\nu_i \\rangle_\\h^2 \\right]\n$$")
        self.assertSelection(20)
