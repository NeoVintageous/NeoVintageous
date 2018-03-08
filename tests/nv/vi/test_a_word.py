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

# DEPRECATED This can be removed when the functional test suite is merged.
from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.text_objects import a_word


class Test_a_word_InInternalNormalMode_Inclusive(unittest.ViewTestCase):

    def test_returns_full_word__count_one(self):
        self.write('foo bar baz\n')
        self.select(5)

        self.assertEqual('bar ', self.view.substr(a_word(self.view, 5)))

    def test_returns_word_and_preceding_white_space__count_one(self):
        self.write('(foo bar) baz\n')
        self.select(5)

        self.assertEqual(' bar', self.view.substr(a_word(self.view, 5)))

    def test_returns_word_and_all_preceding_white_space__count_one(self):
        self.write('(foo   bar) baz\n')
        self.select(8)

        self.assertEqual('   bar', self.view.substr(a_word(self.view, 8)))
