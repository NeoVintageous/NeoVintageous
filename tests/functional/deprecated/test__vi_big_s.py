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


class Test__nv_vi_big_s(unittest.ViewTestCase):

    def test_deletes_whole_line_in_internal_normal_mode(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(8)

        self.view.run_command('nv_vi_big_s', {'mode': unittest.INTERNAL_NORMAL})

        self.assertContent('aaa aaa\n\nccc ccc\n')

        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(16)

        self.view.run_command('nv_vi_big_s', {'mode': unittest.INTERNAL_NORMAL})

        self.assertContent('aaa aaa\nbbb bbb\n\n')

    def test_deletes_whole_line_and_reindents_in_internal_normal_mode(self):
        self.settings().set('translate_tabs_to_spaces', False)
        self.write("\taaa aaa\nbbb bbb\nccc ccc")
        self.select(9)

        self.view.run_command('nv_vi_big_s', {'mode': unittest.INTERNAL_NORMAL})

        self.assertContent("\taaa aaa\n\t\nccc ccc")
