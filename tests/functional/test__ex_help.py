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
# along with NeoVintageous.  If not, see <https://www.gnu.org/licensesubstitute/>.

from sublime import CLASS_WORD_END
from sublime import CLASS_WORD_START
from sublime import platform

from NeoVintageous.nv.utils import is_help_view
from NeoVintageous.tests import unittest


class Test_ex_help(unittest.FunctionalTestCase):

    def get_active_help_view(self):
        av = self.view.window().active_view()
        if is_help_view(av):
            return av

    def close_active_help_views(self):
        for view in self.view.window().views():
            if is_help_view(view):
                view.close()

    def tearDown(self):
        self.close_active_help_views()
        super().tearDown()

    def assertHelpView(self, expected_name: str, expected_tag: str) -> None:
        av = self.get_active_help_view()
        self.assertIsNotNone(av, 'expected help view: %s -> %s' % (expected_name, expected_tag))
        self.assertIn(expected_name + ' [vim help]', av.name())
        tag = av.substr(av.expand_by_class(av.sel()[0].b, CLASS_WORD_START | CLASS_WORD_END, ' '))
        self.assertEqual(tag, expected_tag)

    @unittest.mock_status_message()
    def test_dont_panic(self):
        self.normal('fi|zz')
        self.feed(':help!')
        self.assertStatusMessage('E478: Don\'t panic!')

    @unittest.mock_status_message()
    def test_help_not_found(self):
        self.normal('fi|zz')
        self.feed(':help foobar')
        self.assertStatusMessage('E149: Sorry, no help for foobar')

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_help(self):
        self.normal('fi|zz')
        self.feed(':help')
        self.assertHelpView('help.txt', '*help.txt*')

        self.feed(':help w')
        self.assertHelpView('motion.txt', '*w*')
        self.feed(':help W')
        self.assertHelpView('motion.txt', '*W*')
        self.feed(':help |')
        self.assertHelpView('motion.txt', '*bar*')

        self.feed(':help i_<Esc>')
        self.assertHelpView('insert.txt', '*i_<Esc>*')

        self.feed(':help "')
        self.assertHelpView('change.txt', '*quote*')
        self.feed(':help v_x')
        self.assertHelpView('change.txt', '*v_x*')
        self.feed(':help COPY')
        self.assertHelpView('change.txt', '*:copy*')
        self.feed(':help :s')
        self.assertHelpView('change.txt', '*:s*')

        self.feed(':help *')
        self.assertHelpView('pattern.txt', '*star*')
        self.feed(':help /*')
        self.assertHelpView('pattern.txt', '*/star*')
        self.feed(':help /\\*')
        self.assertHelpView('pattern.txt', '*/\\star*')
        self.feed(':help /|')
        self.assertHelpView('pattern.txt', '*/bar*')
        self.feed(':help /\\|')
        self.assertHelpView('pattern.txt', '*/\\bar*')

        self.feed(':help :w')
        self.assertHelpView('editing.txt', '*:w*')

        self.feed(':help \'ignorecase\'')
        self.assertHelpView('options.txt', '*\'ignorecase\'*')

        self.feed(':help ctrl-d')
        self.assertHelpView('scroll.txt', '*CTRL-D*')

        self.feed(':help c_CTRL-W')
        self.assertHelpView('cmdline.txt', '*c_CTRL-W*')
        self.feed(':help c_ctrl-u')
        self.assertHelpView('cmdline.txt', '*c_CTRL-U*')

        self.feed(':help CTRL-W')
        self.assertHelpView('index.txt', '*CTRL-W*')
