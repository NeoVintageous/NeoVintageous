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


class Test_gh(unittest.FunctionalTestCase):

    def test_gh(self):
        self.eq('x fi|zz x', 'gh', 's_x |fizz| x')
        self.eq('x fizz fi|zz fizz x', 'gh', 's_x fizz |fizz| fizz x')
        self.eq('x fizz |fizz| fizz x', 'gh', 's_x fizz |fizz| fizz x')
        self.eq('x fizz f|iz|z fizz x', 'gh', 's_x fizz |fizz| fizz x')
        self.assertStatusLineIsSelect()

    def test_gh_j(self):
        self.eq('x fizz fi|zz fizz x', 'gh', 's_x fizz |fizz| fizz x')
        self.feed('s_j')
        self.assertVSelect('x fizz |fizz| |fizz| x')
        self.feed('s_j')
        self.assertVSelect('x |fizz| |fizz| |fizz| x')
        self.feed('s_j')
        self.assertVSelect('x |fizz| |fizz| |fizz| x')
        self.assertStatusLineIsSelect()

    def test_gh_j_count(self):
        self.eq('fi|zz fizz fizz fizz', 'gh', 's_|fizz| fizz fizz fizz')
        self.feed('s_2j')
        self.assertVSelect('|fizz| |fizz| |fizz| fizz')
        self.feed('s_2j')
        self.assertVSelect('|fizz| |fizz| |fizz| |fizz|')
        self.assertStatusLineIsSelect()

    def test_gh_k(self):
        self.eq('fizz fi|zz fizz fizz fizz', 'gh', 's_fizz |fizz| fizz fizz fizz')
        self.feed('s_j')
        self.feed('s_j')
        self.assertVSelect('fizz |fizz| |fizz| |fizz| fizz')
        self.feed('s_k')
        self.assertVSelect('fizz |fizz| |fizz| fizz fizz')
        self.feed('s_k')
        self.assertVSelect('fizz |fizz| fizz fizz fizz')
        self.assertStatusLineIsSelect()
        self.feed('s_k')
        self.assertNormal('fizz |fizz fizz fizz fizz')
        self.assertStatusLineIsBlank()

    def test_gh_k_count(self):
        self.eq('fizz fi|zz fizz fizz fizz', 'gh', 's_fizz |fizz| fizz fizz fizz')
        self.feed('s_j')
        self.feed('s_j')
        self.assertVSelect('fizz |fizz| |fizz| |fizz| fizz')
        self.feed('s_2k')
        self.assertVSelect('fizz |fizz| fizz fizz fizz')
        self.assertStatusLineIsSelect()
        self.feed('s_j')
        self.feed('s_j')
        self.assertVSelect('fizz |fizz| |fizz| |fizz| fizz')
        self.assertStatusLineIsSelect()
        self.feed('s_6k')
        self.assertNormal('fizz |fizz fizz fizz fizz')
        self.assertStatusLineIsBlank()

    def test_gh_J(self):
        self.eq('fizz fi|zz fizz fizz fizz', 'gh', 's_fizz |fizz| fizz fizz fizz')
        self.feed('s_j')
        self.feed('s_j')
        self.assertVSelect('fizz |fizz| |fizz| |fizz| fizz')
        self.feed('s_J')
        self.assertNormal('fizz |fizz fizz fizz fizz')
        self.assertStatusLineIsBlank()
