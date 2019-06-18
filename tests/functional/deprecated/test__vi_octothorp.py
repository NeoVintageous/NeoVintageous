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


class Test__vi_octothorp_InNormalMode(unittest.ViewTestCase):

    def test_select_match(self):
        self.write('abc\nabc')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(0)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_match_middle(self):
        self.write('abc\nabc')
        self.select(5)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(0)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_match_end(self):
        self.write('abc\nabc')
        self.select(6)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(0)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(0, 3), self.Region(4, 7)])

    def test_select_repeat_match(self):
        self.write('abc\nabc\nfoo\nabc\nbar')
        self.select(12)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})
        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(0)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [
            self.Region(0, 3), self.Region(4, 7), self.Region(12, 15)])

    def test_select_wrap_match(self):
        self.write('boo\nabc\nfoo\nabc\nbar')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(4, 7), self.Region(12, 15)])

    def test_select_no_partial_match(self):
        self.write('boo\nabc\nabcxabc\nabc\nbar')
        self.select(16)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(4, 7), self.Region(16, 19)])

    def test_select_no_match(self):
        self.write('boo\nabc\nfoo\nabc\nbar')
        self.select(9)

        self.view.run_command('_vi_octothorp', {'mode': unittest.NORMAL})

        self.assertSelection(8)
        self.assertEqual(self.view.get_regions('_nv_search_occ'), [self.Region(8, 11)])
