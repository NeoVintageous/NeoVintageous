from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi.text_objects import big_word_start
from NeoVintageous.lib.vi.text_objects import big_word_end


class TestIssue280(unittest.ViewTestCase):

    def test_big_word_guards_against_runaway_loops(self):
        self.write("a bc_ x")
        self.settings().set('word_separators', "_./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?")
        self.assertEqual(big_word_start(self.view, 2), 2)
        self.assertEqual(big_word_end(self.view, 2), 4)

    def _run_caW(self):
        self.view.run_command(
            '_vi_c',
            {
                'motion': {
                    'motion_args': {
                        'text_object': 'W',
                        'mode': 'mode_internal_normal',
                        'count': 1,
                        'inclusive': True
                    },
                    'motion': '_vi_select_text_object'
                },
                'mode': 'mode_internal_normal',
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
            '_vi_d',
            {
                'motion': {
                    'motion': '_vi_select_text_object',
                    'motion_args': {
                        'inclusive': True,
                        'count': 1,
                        'mode': 'mode_internal_normal',
                        'text_object': 'W'
                    }
                },
                'register': '"',
                'count': 1,
                'mode': 'mode_internal_normal'
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
