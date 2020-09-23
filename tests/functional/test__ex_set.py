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


class Test_ex_set(unittest.FunctionalTestCase):

    @unittest.mock_status_message()
    def test_set_belloff(self):
        self.feed(':set belloff=')
        self.assertOption('belloff', '')
        self.feed(':set belloff=all')
        self.assertOption('belloff', 'all')
        self.feed(':set belloff=')
        self.assertOption('belloff', '')
        self.feed(':set belloff=all')
        self.assertOption('belloff', 'all')
        self.feed(':set belloff?')
        self.assertStatusMessage('belloff=all')
        self.feed(':set belloff=')
        self.feed(':set belloff?')
        self.assertStatusMessage('belloff=')

    @unittest.mock_status_message()
    def test_set_hlsearch(self):
        self.assertOption('hlsearch', True)
        self.feed(':set nohlsearch')
        self.assertOption('hlsearch', False)
        self.feed(':set hlsearch')
        self.assertOption('hlsearch', True)
        self.feed(':set nohls')
        self.assertOption('hlsearch', False)
        self.feed(':set hls')
        self.assertOption('hlsearch', True)
        self.feed(':set hlsearch!')
        self.assertOption('hlsearch', False)
        self.feed(':set hlsearch!')
        self.assertOption('hlsearch', True)
        self.feed(':set invhlsearch')
        self.assertOption('hlsearch', False)
        self.feed(':set invhlsearch')
        self.assertOption('hlsearch', True)
        self.feed(':set hlsearch?')
        self.assertStatusMessage('hlsearch')

    @unittest.mock_status_message()
    def test_set_list(self):
        self.feed(':set nolist')
        self.assertOption('list', False)
        self.feed(':set list')
        self.assertOption('list', True)
        self.feed(':set nolist')
        self.assertOption('list', False)
        self.feed(':set list!')
        self.assertOption('list', True)
        self.feed(':set list!')
        self.assertOption('list', False)
        self.feed(':set invlist')
        self.assertOption('list', True)
        self.feed(':set invlist')
        self.assertOption('list', False)
        self.feed(':set list?')
        self.assertStatusMessage('nolist')

    @unittest.mock_status_message()
    def test_set_modelines(self):
        self.assertOption('modelines', 5)
        self.feed(':set modelines=8')
        self.assertOption('modelines', 8)
        self.feed(':set modelines=5')
        self.assertOption('modelines', 5)
        self.feed(':set modelines?')
        self.assertStatusMessage('modelines=5')

    @unittest.mock_status_message()
    def test_set_scrolloff(self):
        self.feed(':set scrolloff=8')
        self.assertOption('scrolloff', 8)
        self.feed(':set scrolloff=5')
        self.assertOption('scrolloff', 5)
        self.feed(':set scrolloff?')
        self.assertStatusMessage('scrolloff=5')

    @unittest.mock_status_message()
    def test_set_spell(self):
        self.assertOption('spell', False)
        self.feed(':set spell')
        self.assertOption('spell', True)
        self.feed(':set nospell')
        self.assertOption('spell', False)
        self.feed(':set spell!')
        self.assertOption('spell', True)
        self.feed(':set spell!')
        self.assertOption('spell', False)
        self.feed(':set invspell')
        self.assertOption('spell', True)
        self.feed(':set invspell')
        self.assertOption('spell', False)
        self.feed(':set spell?')
        self.assertStatusMessage('nospell')

    @unittest.mock_status_message()
    def test_set_winaltkeys(self):
        self.feed(':set winaltkeys=no')
        self.assertOption('winaltkeys', 'no')
        self.feed(':set winaltkeys=yes')
        self.assertOption('winaltkeys', 'yes')
        self.feed(':set winaltkeys=menu')
        self.assertOption('winaltkeys', 'menu')
        self.feed(':set winaltkeys?')
        self.assertStatusMessage('winaltkeys=menu')
        self.feed(':set wak=yes')
        self.assertOption('winaltkeys', 'yes')

    @unittest.mock_status_message()
    def test_set_unknown_option(self):
        self.feed(':set foobar')
        self.assertStatusMessage('E518: Unknown option: foobar')

    @unittest.mock_status_message()
    def test_set_unknown_nooption(self):
        self.feed(':set nofoobar')
        self.assertStatusMessage('E518: Unknown option: nofoobar')

    @unittest.mock_status_message()
    def test_set_invalid_option_value(self):
        self.feed(':set modelines=foobar')
        self.assertStatusMessage('invalid literal for int() with base 10: \'foobar\'')
