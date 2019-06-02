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


class TestIndentObject(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('tab_size', 2)

    def test_vii(self):
        self.eq('a\n\nfi|zz\n\nb', 'v_ii', 'a\n\n|fizz|\n\nb')
        self.eq('a\n\nfi|zz\nbuzz\n\nb', 'v_ii', 'a\n\n|fizz\nbuzz|\n\nb')
        self.eq('a\n\n  fi|zz\n\nb', 'v_ii', 'a\n\n|  fizz|\n\nb')
        self.eq('a\n\n  fi|zz\n  buzz\n\nb', 'v_ii', 'a\n\n|  fizz\n  buzz|\n\nb')
