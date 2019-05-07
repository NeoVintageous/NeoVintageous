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


class Test_at(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.resetMacros()

    @unittest.mock_bell()
    def test_invalid_register_name(self):
        self.normal('fi|zz')
        self.feed('n_@-')
        self.assertBell("E354: Invalid register name: '-'")
        self.assertStatusLineIsNormal()

    @unittest.mock_bell()
    def test_invalid_register_name__percent__(self):
        self.normal('fi|zz')
        self.feed('n_@%')
        self.assertBell("E354: Invalid register name: '%'")
        self.assertStatusLineIsNormal()

    @unittest.mock_bell()
    def test_invalid_register_name__hash__(self):
        self.normal('fi|zz')
        self.feed('n_@#')
        self.assertBell("E354: Invalid register name: '#'")
        self.assertStatusLineIsNormal()

    @unittest.mock_bell()
    def test_no_previously_used_register(self):
        self.normal('fi|zz')
        self.feed('n_@@')
        self.assertBell('E748: No previously used register')
        self.assertStatusLineIsNormal()

    @unittest.mock_bell()
    def test_no_such_macro(self):
        self.normal('fi|zz')
        self.feed('n_@a')
        self.assertStatusLineIsNormal()

    @unittest.mock_bell()
    def test_empty_macro_should_do_nothing(self):
        self.normal('fi|zz')
        self.feed('n_qa')
        self.feed('n_q')
        self.feed('n_@a')
        self.assertNormal('fi|zz')
        self.assertStatusLineIsNormal()
