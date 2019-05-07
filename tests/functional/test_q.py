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


class Test_q(unittest.FunctionalTestCase):

    def tearDown(self):
        super().tearDown()
        self.resetMacros()

    @unittest.mock_bell()
    def test_invalid_register_name__dash(self):
        self.normal('fi|zz')
        self.feed('n_q-')
        self.assertBell("E354: Invalid register name: '-'")
        self.assertStatusLineIsNormal()

    @unittest.mock_bell()
    def test_invalid_register_name__at(self):
        self.normal('fi|zz')
        self.feed('n_q@')
        self.assertBell("E354: Invalid register name: '@'")
        self.assertStatusLineIsNormal()

    def test_recording_status_line(self):
        self.normal('fi|zz')
        self.feed('n_qa')
        self.assertStatusLineEqual('recording @a')
        self.feed('n_q')
        self.assertStatusLineEqual('')
        self.feed('n_qA')
        self.assertStatusLineEqual('recording @A')
        self.feed('n_q')
        self.assertStatusLineEqual('')
        self.feed('n_qx')
        self.assertStatusLineEqual('recording @x')
        self.feed('n_q')
        self.assertStatusLineEqual('')
