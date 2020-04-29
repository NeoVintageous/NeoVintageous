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


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {}, clear=True)
class TestExRead(unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_read_cmd(self):
        self.normal('f|izz\nxxx\n')
        self.feed(':read !echo buzz')
        self.assertNormal('fizz\n|buzz\nxxx\n')

    def test_read_cmd_error(self):
        self.normal('f|izz\nxxx\n')
        self.feed(':read !ls foo_test_read_cmd_error')
        if self.platform() == 'osx':
            self.assertNormal('fizz\n|ls: foo_test_read_cmd_error: No such file or directory\nxxx\n')
        else:
            self.assertEqual(self.content().replace('\'', ''), 'fizz\nls: cannot access foo_test_read_cmd_error: No such file or directory\nxxx\n')  # noqa: E501
            self.assertSelection(5)
