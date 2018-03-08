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


class Test__vi_cc(unittest.ViewTestCase):

    def test_cc(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.select([self._R(*region) for region in [[(0, 0), (1, 0)]]])

        self.view.run_command('_vi_cc', {'mode': unittest.INTERNAL_NORMAL})

        self.assertContent('foo bar\n\nfoo bar\n')
