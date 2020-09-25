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

from NeoVintageous.nv.vi.text_objects import _a_word


class Test_a_word(unittest.ViewTestCase):

    def test_returns_full_word__count_one(self):
        self.write('foo bar baz\n')
        self.select(5)

        self.assertEqual('bar ', self.view.substr(_a_word(self.view, 5)))

    def test_returns_word_and_preceding_white_space__count_one(self):
        self.write('(foo bar) baz\n')
        self.select(5)

        self.assertEqual(' bar', self.view.substr(_a_word(self.view, 5)))

    def test_returns_word_and_all_preceding_white_space__count_one(self):
        self.write('(foo   bar) baz\n')
        self.select(8)

        self.assertEqual('   bar', self.view.substr(_a_word(self.view, 8)))

    def test_returns_full_word(self):
        self.write('foo bar baz\n')
        self.assertRegion(_a_word(self.view, 5), 'bar ')

    def test_returns_word_and_preceding_white_space(self):
        self.write('(foo bar) baz\n')
        self.assertRegion(_a_word(self.view, 5), ' bar')

    def test_returns_word_and_all_preceding_white_space(self):
        self.write('(foo   bar) baz\n')
        self.assertRegion(_a_word(self.view, 8), '   bar')

    # XXX when the cursor starts at space character
    # it should probably include the following
    # word too to match Vim behaviour e.g
    # `a| b c` -> daw should delete ` b`
    def test_letters_digits_and_underscores(self):
        self.write('a ab _a _a1 x')
        self.assertRegion(_a_word(self.view, 0), 'a ')
        self.assertRegion(_a_word(self.view, 1), ' ')
        self.assertRegion(_a_word(self.view, 2), 'ab ')
        self.assertRegion(_a_word(self.view, 3), 'ab ')
        self.assertRegion(_a_word(self.view, 4), ' ')
        self.assertRegion(_a_word(self.view, 5), '_a ')
        self.assertRegion(_a_word(self.view, 6), '_a ')
        self.assertRegion(_a_word(self.view, 7), ' ')
        self.assertRegion(_a_word(self.view, 8), '_a1 ')
        self.assertRegion(_a_word(self.view, 9), '_a1 ')
        self.assertRegion(_a_word(self.view, 10), '_a1 ')
        self.assertRegion(_a_word(self.view, 11), ' ')
        self.assertRegion(_a_word(self.view, 12), ' x')

    def test_letters_digits_and_underscores_eol_includes_preceding_space(self):
        self.write('x   e12_x')
        self.assertRegion(_a_word(self.view, 4), '   e12_x')

    # XXX when the cursor starts at space character
    # it should probably include the following
    # word too to match Vim behaviour e.g
    # `a| b c` -> daw should delete ` b`
    def test_non_blank_characters(self):
        self.write('.. .,-= .%.$ .')
        self.assertRegion(_a_word(self.view, 0), '.. ')
        self.assertRegion(_a_word(self.view, 1), '.. ')
        self.assertRegion(_a_word(self.view, 2), ' ')
        self.assertRegion(_a_word(self.view, 3), '.,-= ')
        self.assertRegion(_a_word(self.view, 4), '.,-= ')
        self.assertRegion(_a_word(self.view, 5), '.,-= ')
        self.assertRegion(_a_word(self.view, 6), '.,-= ')
        self.assertRegion(_a_word(self.view, 7), ' ')
        self.assertRegion(_a_word(self.view, 8), '.%.$ ')
        self.assertRegion(_a_word(self.view, 9), '.%.$ ')
        self.assertRegion(_a_word(self.view, 10), '.%.$ ')
        self.assertRegion(_a_word(self.view, 11), '.%.$ ')
        self.assertRegion(_a_word(self.view, 12), ' ')
        self.assertRegion(_a_word(self.view, 13), ' .')

    def test_non_blank_characters_eol_includes_preceding_space(self):
        self.write('x    .=-,')
        self.assertRegion(_a_word(self.view, 5), '    .=-,')

    # XXX when the cursor starts at space character
    # it should probably include the following
    # word too to match Vim behaviour e.g
    # `a| b c` -> daw should delete ` b`
    def test_letters_digits_underscores_and_non_blank_characters(self):
        self.write('ab.. _a_,=-12.34 .')
        self.assertRegion(_a_word(self.view, 0), 'ab')
        self.assertRegion(_a_word(self.view, 1), 'ab')
        self.assertRegion(_a_word(self.view, 2), '.. ')
        self.assertRegion(_a_word(self.view, 3), '.. ')
        self.assertRegion(_a_word(self.view, 4), ' ')
        self.assertRegion(_a_word(self.view, 5), ' _a_')
        self.assertRegion(_a_word(self.view, 8), ',=-')
        self.assertRegion(_a_word(self.view, 11), '12')
        self.assertRegion(_a_word(self.view, 13), '.')
        self.assertRegion(_a_word(self.view, 14), '34 ')
