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


class Test_l(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|abc', 'n_l', 'a|bc')
        self.eq('|foo bar baz', 'n_9l', 'foo bar b|az')
        self.eq('|ping', 'n_9l', 'pin|g')
        self.eq('|ping\n', 'n_9l', 'pin|g\n')
        self.eq('|', 'n_l', '|')
        self.eq('\n\n|\n\n', 'n_l', '\n\n|\n\n')

    def test_v(self):
        self.eq('|abc', 'v_l', '|ab|c')
        self.eq('|abc', 'v_1l', '|ab|c')
        self.eq('f|oo bar baz', 'v_5l', 'f|oo bar| baz')
        self.eq('|ping', 'v_9l', '|ping|')
        self.eq('p|ing\n', 'v_9l', 'p|ing\n|')
        self.eq('a|bc\nx', 'v_5l', 'a|bc\n|x')
        self.eq('a|bc\nd|ef\nx', 'v_9l', 'a|bc\ndef\n|x')
        self.eq('|', 'v_l', '|')
        self.eq('\n\n|\n|\n', 'v_l', '\n\n|\n|\n')
        self.eq('r_h|el|lo world', 'v_5l', 'he|llo w|orld')
        self.eq('r_h|el|lo\n', 'v_5l', 'he|llo\n|')
        self.eq('r_a|\n|', 'v_5l', 'r_a|\n|')
        self.eq('r_|ab|\n', 'v_9l', 'a|b\n|')
        self.eq('r_|ab\n|', 'v_9l', 'r_ab|\n|')

    def test_V(self):
        self.eq('ab\n|cd\n|ef\n', 'V_l', 'ab\n|cd\n|ef\n')

    @unittest.mock_bell()
    def test_c(self):
        self.eq('12|34', 'cl', 'i_12|4')
        self.eq('12| 4', 'cl', 'i_12|4')
        self.eq('12|  ', 'cl', 'i_12| ')
        self.eq('1|234567890', '4cl', 'i_1|67890')
        self.eq('1|23     90', '4cl', 'i_1|   90')
        self.eq('|', 'cl', 'i_|')
        self.eq('\n\n|\n\n', 'cl', 'i_\n\n|\n\n')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('1|234', 'dl', '1|34')
        self.eq('|abc', 'dl', '|bc')
        self.eq('1|234567890', '4dl', '1|67890')
        self.eq('1|23     90', '4dl', '1|   90')
        self.eq('ab|c', 'dl', 'a|b')
        self.eq('|a', 'dl', '|')
        self.eq('\n\n|a\n\n', 'dl', '\n\n|\n\n')
        self.eq('12|34', '9dl', '1|2')
        self.eq('12|34\n', '9dl', '1|2\n')
        self.eq('12|34\nx', '9dl', '1|2\nx')
        self.assertNoBell()
        self.eq('\n\n|\n\n', 'dl', '\n\n|\n\n')
        self.eq('|', 'dl', '|')
        self.assertBellCount(2)
