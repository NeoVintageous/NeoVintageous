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


class Test_gf(unittest.FunctionalTestCase):

    def assertOpened(self, opener, file: str) -> None:
        opener.assert_called_with(self.view.window(), file)
        # Reset to avoid false-positives in subsequent calls.
        opener.reset_mock()

    @unittest.mock.patch.dict(unittest.os.environ, {"HOME": "/home"})
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_gf(self, opener):
        # (before, after, expected file name)
        tests = [
            ('x path/to/READ|ME.md y', 'x path/to/READ|ME.md y', 'path/to/README.md'),
            ('|/tmp/fizz.txt', '|/tmp/fizz.txt', '/tmp/fizz.txt'),
            ('/|tmp/fizz.txt', '/|tmp/fizz.txt', '/tmp/fizz.txt'),
            ('|stop.txt.', '|stop.txt.', 'stop.txt'),
            ('|comma.txt,', '|comma.txt,', 'comma.txt'),
            ('|semicolon.txt;', '|semicolon.txt;', 'semicolon.txt'),
            ('|colon.txt:', '|colon.txt:', 'colon.txt'),
            ('|bang.txt!', '|bang.txt!', 'bang.txt'),
            ('|xxx:/tmp/fizz1.txt', '|xxx:/tmp/fizz1.txt', '/tmp/fizz1.txt'),
            ('|xxx:/tmp/fizz2.txt', '|xxx:/tmp/fizz2.txt', '/tmp/fizz2.txt'),
            ('|$HOME/fizz3.txt', '|$HOME/fizz3.txt', '/home/fizz3.txt'),
            ('REA|DME.md', 'REA|DME.md', 'README.md'),
            (' REA|DME.md ', ' REA|DME.md ', 'README.md'),
            ('\nREA|DME.md\n', '\nREA|DME.md\n', 'README.md'),
            ('path/to/REA|DME.md', 'path/to/REA|DME.md', 'path/to/README.md'),
            (' pat|h/to/README.md ', ' pat|h/to/README.md ', 'path/to/README.md'),
            ('\npath|/to/README.md\n', '\npath|/to/README.md\n', 'path/to/README.md'),
            ('|./fizz.txt', '|./fizz.txt', './fizz.txt'),
            ('|../fizz.txt', '|../fizz.txt', '../fizz.txt'),
            ('|../../fizz.txt', '|../../fizz.txt', '../../fizz.txt'),
            ('|  /fizz.txt', '|  /fizz.txt', '/fizz.txt'),
            ('|/fizz.txt /buzz.txt', '|/fizz.txt /buzz.txt', '/fizz.txt'),
            ('/fi|zz.txt /buzz.txt', '/fi|zz.txt /buzz.txt', '/fizz.txt'),
            ('/fizz.txt |/buzz.txt', '/fizz.txt |/buzz.txt', '/buzz.txt'),
            ('/fizz.txt /bu|zz.txt', '/fizz.txt /bu|zz.txt', '/buzz.txt'),
            ('x   /fizz.txt   /buzz|.txt   x', 'x   /fizz.txt   /buzz|.txt   x', '/buzz.txt'),
            ('|parans.txt(1).', '|parans.txt(1).', 'parans.txt'),
        ]

        for test in tests:
            self.eq(test[0], 'n_gf', test[1])
            self.assertOpened(opener, test[2])

    @unittest.mock_status_message()
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_gf_no_file_name_under_cursor(self, opener):
        self.eq('|', 'n_gf', '|')
        self.eq('$|$$', 'n_gf', '$|$$')
        self.assertMockNotCalled(opener)
        self.assertStatusMessage('E446: No file name under cursor', count=2)

    @unittest.mock.patch.dict(unittest.os.environ, {"HOME": "/home"})
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_v(self, opener):
        self.eq('/tmp|/fizz/buzz1.log| x', 'v_gf', '/tmp|/fizz/buzz1.log| x')
        self.assertOpened(opener, '/fizz/buzz1.log')
        self.eq('r_/tmp|/fizz/buzz2.log| x', 'v_gf', 'r_/tmp|/fizz/buzz2.log| x')
        self.assertOpened(opener, '/fizz/buzz2.log')

    @unittest.mock.patch.dict(unittest.os.environ, {"HOME": "/home"})
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_V(self, opener):
        self.eq('x\n|/tmp/fizz.log\n|x', 'V_gf', 'x\n|/tmp/fizz.log\n|x')
        self.assertOpened(opener, '/tmp/fizz.log')

    @unittest.mock.patch.dict(unittest.os.environ, {"HOME": "/home"})
    @unittest.mock.patch('NeoVintageous.nv.commands.window_open_file')
    def test_b(self, opener):
        self.eq('x\n|/tmp/fizz.log|\nx', 'b_gf', 'x\n|/tmp/fizz.log|\nx')
        self.assertOpened(opener, '/tmp/fizz.log')
