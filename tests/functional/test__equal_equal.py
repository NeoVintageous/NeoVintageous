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


class Test_equal_equal(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.syntax('Packages/Python/Python.sublime-syntax')
        self.settings().set('translate_tabs_to_spaces', True)
        self.settings().set('tab_size', 2)

    def test_N(self):
        self.eq('|', '==', '|')
        self.eq('def x():\n|x = 1', '==', 'def x():\n  |x = 1')
        self.eq('def x():\n|x = 1\nx = 2\nx = 3\nx = 4\n', '3==', 'def x():\n  |x = 1\n  x = 2\n  x = 3\nx = 4\n')
        self.eq('def x():\nx |= 1\nx = 2\nx = 3\nx = 4\n', '3==', 'def x():\n  |x = 1\n  x = 2\n  x = 3\nx = 4\n')
        self.eq('def a():\n|a1=1\na2=2\na3=3\ndef b():\n|b1=1\nb2=2\nb3=3\n', '==', 'def a():\n  |a1=1\na2=2\na3=3\ndef b():\n  |b1=1\nb2=2\nb3=3\n')  # noqa: E501
        self.eq('def a():\n|a1=1\na2=2\na3=3\ndef b():\n|b1=1\nb2=2\nb3=3\n', '2==', 'def a():\n  |a1=1\n  a2=2\na3=3\ndef b():\n  |b1=1\n  b2=2\nb3=3\n')  # noqa: E501
        self.eq('def a():\na1|=1\na2=2\na3=3\ndef b():\nb1|=1\nb2=2\nb3=3\n', '2==', 'def a():\n  |a1=1\n  a2=2\na3=3\ndef b():\n  |b1=1\n  b2=2\nb3=3\n')  # noqa: E501
