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

from NeoVintageous.nv.variables import get


class Test_ex_let(unittest.FunctionalTestCase):

    def assertVariable(self, name, expected):
        self.assertEqual(get(name), expected)

    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_let_can_set_mapleader_to_a_comma(self):
        self.feed(':let mapleader=,')
        self.assertVariable('<leader>', ',')
        self.feed(':let mapleader=","')
        self.assertVariable('<leader>', ',')
        self.feed(':let mapleader=\',\'')
        self.assertVariable('<leader>', ',')

    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_let_can_set_mapleader_to_a_slash(self):
        self.feed(':let mapleader=/')
        self.assertVariable('<leader>', '/')
        self.feed(':let mapleader="/"')
        self.assertVariable('<leader>', '/')
        self.feed(':let mapleader=\'/\'')
        self.assertVariable('<leader>', '/')

    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_let_can_set_mapleader_to_a_space(self):
        self.feed(':let mapleader=<space>')
        self.assertVariable('<leader>', '<space>')
        self.feed(':let mapleader="<space>"')
        self.assertVariable('<leader>', '<space>')
        self.feed(':let mapleader=\'<space>\'')
        self.assertVariable('<leader>', '<space>')
        self.feed(':let mapleader=<Space>')
        self.assertVariable('<leader>', '<Space>')
        self.feed(':let mapleader=<SPACE>')
        self.assertVariable('<leader>', '<SPACE>')
