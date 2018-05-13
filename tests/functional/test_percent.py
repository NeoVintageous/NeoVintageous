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


class Test_percent(unittest.FunctionalTestCase):

    def test_percent(self):
        self.eq('|', '%', '|')
        self.eq('fi|zz', '%', 'fi|zz')
        self.eq('|{ab}', '%', '{ab|}')
        self.eq('{ab|}', '%', '|{ab}')
        self.eq('a |{\nb\n}\nc', '%', 'a {\nb\n|}\nc')
        self.eq('a {\nb\n|}\nc', '%', 'a |{\nb\n}\nc')
        self.eq('|12{}', '%', '12{|}', 'should jump to the *match* of the next item in the line')
        self.eq('{}12|', '%', '{}12|', 'should NOT jump backwards')
        self.eq('12{}3|4{}', '%', '12{}34{|}', 'should jump forward')

    def test_percent_mutiple_selection(self):
        self.eq('1|{ab}2|{cd}3|{ef}x', '%', '1{ab|}2{cd|}3{ef|}x')
        self.eq('1|{ab}2{cd}3|{ef}x', '%', '1{ab|}2{cd}3{ef|}x')

    def test_v_percent(self):
        self.eq('|{ab}', 'v_%', '|{ab}|')
        self.eq('{ab|}', 'v_%', '|{ab}|')
        self.eq('a |{\nb\n}\nc', 'v_%', 'a |{\nb\n}|\nc')
        self.eq('a {\nb\n|}\nc', 'v_%', 'a |{\nb\n}|\nc')
        self.eq('a|123{|\nb\n}\nc', 'v_%', 'a|123{\nb\n}|\nc')

    def test_l_percent(self):
        self.eq('|\n|', 'l_%', '|\n|')
        self.eq('|ab\n|', 'l_%', '|ab\n|')
        self.eq('1| \n|2', 'l_%', '1| \n|2', 'single space lines should be noop')
        self.eq('\n|\n\n|\n', 'l_%', '\n|\n\n|\n', 'empty lines should be noop')


class Test_percent_in_php_syntax(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.view.assign_syntax('Packages/PHP/PHP.sublime-syntax')

    def test_percent(self):
        self.eq('<?php\nfunct|ion x() {\n//...\n}\n', '%', '<?php\nfunction x(|) {\n//...\n}\n')
