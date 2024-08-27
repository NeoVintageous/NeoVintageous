# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from NeoVintageous.nv.modeline import _parse_line
from NeoVintageous.nv.modeline import do_modeline


class TestParseLine(unittest.ViewTestCase):

    def test_vim(self):
        self.assertEqual(['list'], _parse_line('vi: list'))
        self.assertEqual(['list'], _parse_line('vim: list'))
        self.assertEqual(['list'], _parse_line(' vi: list'))
        self.assertEqual(['list'], _parse_line(' vim: list'))
        self.assertEqual(['list'], _parse_line(' Vim: list'))
        self.assertEqual(['list'], _parse_line(' ex: list'))

        self.assertEqual(['list'], _parse_line('vi:list'))
        self.assertEqual(['list'], _parse_line('xxx vi: list'))
        self.assertEqual(['list'], _parse_line('xxx vi:list'))

        self.assertEqual(['noai', 'ic'], _parse_line('vi: noai:ic'))
        self.assertEqual(['noai', 'ic'], _parse_line('vi: noai ic'))
        self.assertEqual(['noai', 'ic', 'hls', 'list'], _parse_line('vi: noai:ic hls:list'))

        self.assertEqual(['noai', 'ic', 'hls'], _parse_line('vi: set noai ic hls:'))
        self.assertEqual(['noai', 'ic', 'hls'], _parse_line('/* vi: set noai ic hls: */'))
        self.assertEqual(['noai', 'ic', 'hls'], _parse_line('xxx vi: set noai ic hls:'))

        self.assertEqual(['sw=4', 'sts=4', 'et', 'tw=80'], _parse_line(' vim: set sw=4 sts=4 et tw=80 :'))
        self.assertEqual(['tw=78', 'sw=4'], _parse_line('vi:tw=78:sw=4:'))

    def test_invalid(self):
        self.assertEqual(None, _parse_line(''))
        self.assertEqual(None, _parse_line(' '))
        self.assertEqual(None, _parse_line('foobar'))
        self.assertEqual(None, _parse_line('Vim: list'))
        self.assertEqual(None, _parse_line('ex: list'))
        self.assertEqual(None, _parse_line('lex: list'))
        self.assertEqual(None, _parse_line('xvi: list'))
        self.assertEqual(None, _parse_line('xvim: list'))
        self.assertEqual(None, _parse_line('xVim: list'))
        self.assertEqual(None, _parse_line('xex: list'))


class TestDoModeline(unittest.ViewTestCase):

    def test_modeline(self):
        self.set_option('wrap', True)
        self.set_option('number', False)
        self.write('# vim: nowrap nu\n')
        do_modeline(self.view)
        self.assertOption('wrap', False)
        self.assertOption('number', True)

    def test_multiline(self):
        self.set_option('wrap', False)
        self.set_option('number', True)
        self.set_option('autoindent', True)
        self.write('1\n'
                   'vim: wrap\n'
                   'vim: nonu\n'
                   'vim: noai\n'
                   'EOF\n')
        do_modeline(self.view)
        self.assertOption('wrap', True)
        self.assertOption('number', False)
        self.assertOption('autoindent', False)

    def test_bottom_of_file_modelines(self):
        self.set_option('wrap', False)
        self.set_option('number', False)
        self.set_option('textwidth', 80)
        self.set_option('tabstop', 4)
        self.write('# 1\n'
                   '# 2\n'
                   '# 3\n'
                   '# 4\n'
                   '# 5\n'
                   '# 6\n'
                   '# 7\n'
                   '# vim: wrap\n'
                   '# vim: number\n'
                   '# vim: tw=50\n'
                   '# vim: ts=2\n')
        do_modeline(self.view)
        self.assertOption('wrap', True)
        self.assertOption('number', True)
        self.assertOption('textwidth', 50)
        self.assertOption('tabstop', 2)

    def test_only_checks_number_of_modelines_5(self):
        self.set_option('modelines', 5)
        self.set_option('wrap', False)
        self.set_option('number', False)
        self.set_option('textwidth', 80)
        self.set_option('tabstop', 4)
        self.write('# 1\n'
                   '# 2\n'
                   '# 3\n'
                   '# 4\n'
                   '# 5\n'
                   '# vim: wrap\n'
                   '# vim: number\n'
                   '# vim: tw=50\n'
                   '# vim: ts=2\n'
                   '# 11\n'
                   '# 12\n'
                   '# 13\n'
                   '# 14\n'
                   '# 15\n')
        do_modeline(self.view)
        self.assertOption('wrap', False)
        self.assertOption('number', False)
        self.assertOption('textwidth', 80)
        self.assertOption('tabstop', 4)

    def test_only_checks_number_of_modelines_2(self):
        self.set_option('modelines', 2)
        self.set_option('wrap', False)
        self.set_option('number', False)
        self.set_option('textwidth', 80)
        self.set_option('tabstop', 4)
        self.write('# 1\n'
                   '# 2\n'
                   '# vim: wrap\n'
                   '# vim: number\n'
                   '# vim: tw=50\n'
                   '# vim: ts=2\n'
                   '# 14\n'
                   '# 15\n')
        do_modeline(self.view)
        self.assertOption('wrap', False)
        self.assertOption('number', False)
        self.assertOption('textwidth', 80)
        self.assertOption('tabstop', 4)

    @unittest.mock.patch('NeoVintageous.nv.modeline.do_ex_cmdline')
    @unittest.mock.patch('NeoVintageous.nv.modeline.message')
    def test_shell_dissallowed(self, message, ex_cmd):
        option = self.get_option('shell')
        self.write('1\nvim: shell=sh\n\n')
        do_modeline(self.view)
        self.assertOption('shell', option)
        message.assert_called_with('E520: Not allowed in a modeline: %s', 'shell=sh')
        self.assertMockNotCalled(ex_cmd)

    def test_top_lines_are_processed_top_down(self):
        self.set_option('number', False)
        self.write('# 1\n'
                   '# vim: nonumber\n'
                   '# vim: number\n')
        do_modeline(self.view)
        self.assertOption('number', True)
        self.write('# 1\n'
                   '# vim: number\n'
                   '# vim: nonumber\n')
        do_modeline(self.view)
        self.assertOption('number', False)

    def test_bottom_lines_are_processed_bottom_up(self):
        self.set_option('number', False)
        self.write('#1\n#2\n#3\n#4\n#5\n#6\n'
                   '# vim: number\n'
                   '# vim: nonumber\n')
        do_modeline(self.view)
        self.assertOption('number', True)
        self.write('#1\n#2\n#3\n#4\n#5\n#6\n'
                   '# vim: nonumber\n'
                   '# vim: number\n')
        do_modeline(self.view)
        self.assertOption('number', False)
