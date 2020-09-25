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


class TestSurround_ys(unittest.FunctionalTestCase):

    def test_yse(self):
        self.eq('one |two three', 'yse\'', 'one |\'two\' three')
        self.eq('one |two three', 'yse"', 'one |"two" three')
        self.eq('one |two three', 'yse2', 'one |2two2 three')
        self.eq('one |two three', 'yse(', 'one |( two ) three')
        self.eq('one |two three', 'yse)', 'one |(two) three')
        self.eq('one |two three', 'yse[', 'one |[ two ] three')
        self.eq('one |two three', 'yse]', 'one |[two] three')
        self.eq('one |two three', 'yse{', 'one |{ two } three')
        self.eq('one |two three', 'yse}', 'one |{two} three')
        self.eq('one |two three', 'yse<foo>', 'one |<foo>two</foo> three')

    def test_ysiw(self):
        self.eq('one |two three', 'ysiw\'', 'one |\'two\' three')
        self.eq('one |two three', 'ysiw"', 'one |"two" three')
        self.eq('one |two three', 'ysiw2', 'one |2two2 three')
        self.eq('one |two three', 'ysiw(', 'one |( two ) three')
        self.eq('one |two three', 'ysiw)', 'one |(two) three')
        self.eq('one |two three', 'ysiwb', 'one |(two) three')
        self.eq('one |two three', 'ysiw[', 'one |[ two ] three')
        self.eq('one |two three', 'ysiw]', 'one |[two] three')
        self.eq('one |two three', 'ysiwr', 'one |[two] three')
        self.eq('one |two three', 'ysiw{', 'one |{ two } three')
        self.eq('one |two three', 'ysiw}', 'one |{two} three')
        self.eq('one |two three', 'ysiwB', 'one |{two} three')
        self.eq('one |two three', 'ysiw<foo>', 'one |<foo>two</foo> three')

    @unittest.expectedFailure
    def test_ysiw_bug_01(self):
        self.eq('one |two three', 'ysiwafoo>', 'one |<foo>two</foo> three')

    def test_yss(self):
        self.eq('abc', 'yss)', '|(abc)')
        self.eq('x\nfi|zz\nx', 'yss)', 'x\n|(fizz)\nx')
        self.eq('x\n    ab  fi|zz  x y  \nx', 'yss)', 'x\n    |(ab  fizz  x y  )\nx')

    def test_multiple_cursors(self):
        self.eq('x a|c\nd|c y', 'ysiw"', 'x |"ac"\n|"dc" y')

    def test_issue_305_multiple_selection_leaves_cursors_in_the_wrong_place(self):
        self.eq("eats fi|sh\neats fi|sh\neats fi|sh", "ysiw'", "eats |'fish'\neats |'fish'\neats |'fish'")

    def test_tags(self):
        self.eq('"fi|zz"', 'ysiw<i x="y">', '"|<i x="y">fizz</i>"')

    @unittest.expectedFailure
    def test_tags_bug_01(self):
        self.eq('"fi|zz"', 'ysiwti x="y">', '"|<i x="y">fizz</i>"')
