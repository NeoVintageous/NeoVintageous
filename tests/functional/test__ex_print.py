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


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
class Test_ex_print(unittest.FunctionalTestCase):

    def tearDown(self) -> None:
        self.closeExPrintOutputViews()
        super().tearDown()

    @unittest.mock_status_message()
    def test_empty_buffer(self):
        self.eq('|', ':1,3print', '|')
        self.assertStatusMessage('E749: empty buffer')

    @unittest.mock_status_message()
    def test_print_range(self):
        self.eq('|1\n2\n3\n4\n5\n6\n7', ':3,5print', '|1\n2\n3\n4\n5\n6\n7')
        self.assertNoStatusMessage()
        self.assertExPrintOutput('3\n4\n5')

    def test_print_range_with_l_flag(self):
        self.eq('|1\n2\n3\n4\n5\n6\n7', ':3,5print l', '|1\n2\n3\n4\n5\n6\n7')
        self.assertTrue(self.get_option('list', self.exPrintOutputView()))

    def test_print_range_without_l_flag(self):
        self.eq('|1\n2\n3\n4\n5\n6\n7', ':3,5print', '|1\n2\n3\n4\n5\n6\n7')
        self.assertNotEqual(True, self.get_option('list', self.exPrintOutputView()))

    def test_print_range_with_hash_flag(self):
        self.eq('|a\nb\nc\nd\ne\nf\ng', ':3,5print #', '|a\nb\nc\nd\ne\nf\ng')
        self.assertExPrintOutput('3 c\n4 d\n5 e')
