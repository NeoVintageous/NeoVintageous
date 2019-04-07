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

    def onRunFeedCommand(self, command, args):
        # TODO Refactor command to use "count" param name.
        if 'count' in args:
            args['percent'] = args['count']
            del args['count']

    def test_n(self):
        self.eq('|', 'n_%', '|')
        self.eq('fi|zz', 'n_%', 'fi|zz')
        self.eq('|{ab}', 'n_%', '{ab|}')
        self.eq('{ab|}', 'n_%', '|{ab}')
        self.eq('a |{\nb\n}\nc', 'n_%', 'a {\nb\n|}\nc')
        self.eq('a {\nb\n|}\nc', 'n_%', 'a |{\nb\n}\nc')
        self.eq('|12{}', 'n_%', '12{|}', 'should jump to the *match* of the next item in the line')
        self.eq('{}12|', 'n_%', '{}12|', 'should NOT jump backwards')
        self.eq('12{}3|4{}', 'n_%', '12{}34{|}', 'should jump forward')
        self.eq('|1\n2\n3\n4\n5\n6\n7\n8\n9\n0', 'n_30%', '1\n2\n|3\n4\n5\n6\n7\n8\n9\n0')
        self.eq('|1\n2\n3\n4\n5\n6', 'n_80%', '1\n2\n3\n4\n|5\n6')

    def test_percent_mutiple_selection(self):
        self.eq('1|{ab}2|{cd}3|{ef}x', 'n_%', '1{ab|}2{cd|}3{ef|}x')
        self.eq('1|{ab}2{cd}3|{ef}x', 'n_%', '1{ab|}2{cd}3{ef|}x')

    def test_v_percent(self):
        self.eq('|{ab}', 'v_%', '|{ab}|')
        self.eq('{ab|}', 'v_%', 'r_|{ab}|')
        self.eq('a |{\nb\n}\nc', 'v_%', 'a |{\nb\n}|\nc')
        self.eq('a {\nb\n|}\nc', 'v_%', 'r_a |{\nb\n}|\nc')
        self.eq('a|123{|\nb\n}\nc', 'v_%', 'a|123{\nb\n}|\nc')
        self.eq('abc (a|bc) abc', 'v_%', 'r_abc |(ab|c) abc'),
        self.eq('abc (a|bc) abc', 'v_%', 'r_abc |(ab|c) abc')
        self.eq('|0(|2)4', 'v_%', '|0(2)|4')
        self.eq('0|(|2)4', 'v_%', '0|(2)|4')
        self.eq('r_0(2|)4|', 'v_%', 'r_0|(2)4|')
        self.eq('r_0(|2)|4', 'v_%', 'r_0|(2)|4')
        self.eq('0(|2)|4', 'v_%', 'r_0|(2|)4')
        self.eq('0(2|)|4', 'v_%', 'r_0|(2)|4')
        self.eq('r_0|(2|)4', 'v_%', '0(|2)|4')
        self.eq('0|(|2)4', 'v_%', '0|(2)|4')
        self.eq('|()', 'v_%', '|()|')
        self.eq('r_(|)|', 'v_%', 'r_|()|')
        self.eq('(|)|', 'v_%', 'r_|()|')
        self.eq('r_|(|)', 'v_%', '|()|')

    def test_l_percent(self):
        self.eq('|\n|', 'l_%', '|\n|')
        self.eq('|ab\n|', 'l_%', '|ab\n|')
        self.eq('1| \n|2', 'l_%', '1| \n|2', 'single space lines should be noop')
        self.eq('\n|\n\n|\n', 'l_%', '\n|\n\n|\n', 'empty lines should be noop')

    def test_N_percent(self):
        self.eq('abc (a|bc) abc', '%', 'r_N_abc |(ab|c) abc')
        self.eq('abc (abc|) abc', '%', 'r_N_abc |(abc)| abc')
        self.eq('abc |(abc) abc', '%', 'N_abc |(abc)| abc')
        self.eq('|abc (abc) abc', '%', 'N_|abc (abc)| abc')


class Test_percent_in_php_syntax(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.view.assign_syntax('Packages/PHP/PHP.sublime-syntax')

    def test_percent(self):
        self.eq('<?php\nfunct|ion x() {\n//...\n}\n', 'n_%', '<?php\nfunction x(|) {\n//...\n}\n')

    def test_find_next_item_in_this_line_after_the_cursor(self):
        start = '<?php\nfunct|ion x() {\n    //...\n}\n'
        self.normal(start)
        self.feed('n_%')
        self.assertNormal('<?php\nfunction x(|) {\n    //...\n}\n')


class Test_workaround_for_issue_243(unittest.FunctionalTestCase):

    def test_if_forward_vline_and_target_is_after_selection_it_should_extend_forward(self):
        start = 'x\n|f {\n|a\nb\nc\n}\nx\n'
        self.vline(start)
        self.feed('l_%')
        self.assertVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('l_%')
        self.assertVline(start)

    def test_if_forward_vlines_and_target_is_after_selection_it_should_extend_forward(self):
        start = 'x\n|y\nz\nf {\n|a\nb\nc\n}\nx\n'
        self.vline(start)
        self.feed('l_%')
        self.assertVline('x\n|y\nz\nf {\na\nb\nc\n}\n|x\n')
        self.feed('l_%')
        self.assertVline(start)

    def test_if_forward_vline_and_target_is_before_selection_it_should_reverse_selection_and_extend_backward(self):
        start = 'x\nf {\na\nb\nc\n|}\n|x\n'
        self.vline(start)
        self.feed('l_%')
        self.assertRVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('l_%')
        self.assertRVline(start)

    def test_if_forward_vlines_within_targets_and_target_is_before_selection_it_should_flip_and_reverse_selection(self):
        start = 'x\nf {\na\n|b\nc\n}\n|x\n'
        self.vline(start)
        self.feed('l_%')
        self.assertRVline('x\n|f {\na\nb\n|c\n}\nx\n')
        self.feed('l_%')
        self.assertVline(start)

    def test_if_backward_vline_and_target_is_before_selection_it_should_extend_selection(self):
        start = 'x\nf {\na\nb\nc\n|}\n|x\n'
        self.rvline(start)
        self.feed('l_%')
        self.assertRVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('l_%')
        self.assertRVline(start)

    def test_if_backward_vlines_and_target_is_before_selection_it_should_extend_selection(self):
        start = 'x\nf {\na\nb\nc\n|}\nx\ny\n|z\n'
        self.rvline(start)
        self.feed('l_%')
        self.assertRVline('x\n|f {\na\nb\nc\n}\nx\ny\n|z\n')
        self.feed('l_%')
        self.assertRVline(start)

    def test_if_reverse_vlines_within_targets_and_target_is_before_selection_it_should_flip_and_reverse_selection(self):
        start = 'x\n|f {\na\nb\n|c\n}\nx\n'
        self.rvline(start)
        self.feed('l_%')
        self.assertVline('x\nf {\na\n|b\nc\n}\n|x\n')
        self.feed('l_%')
        self.assertRVline(start)


class Test_percent_tags(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.view.assign_syntax('Packages/HTML/HTML.sublime-syntax')

    def test_percent(self):
        self.eq('|<div>fizz</div>', 'n_%', '<div|>fizz</div>')
        self.eq('<div|>fizz</div>', 'n_%', '|<div>fizz</div>')
        self.eq('<div>fizz|</div>', 'n_%', '<div>fizz</div|>')
        self.eq('<div>fizz</div|>', 'n_%', '<div>fizz|</div>')
        self.eq('<div>f|izz</div>', 'n_%', '<div>fizz</div|>')
        self.eq('<div>fi|zz</div>', 'n_%', '<div>fizz</div|>')
        self.eq('<div>fiz|z</div>', 'n_%', '<div>fizz</div|>')
        self.eq('<div><div>f|izz</div></div>', 'n_%', '<div><div>fizz</div|></div>')
        self.eq('ab|<div>fizz</div>cd', 'n_%', 'ab<div|>fizz</div>cd')
        self.eq('ab<div|>fizz</div>cd', 'n_%', 'ab|<div>fizz</div>cd')
        self.eq('ab<div>fizz|</div>cd', 'n_%', 'ab<div>fizz</div|>cd')
        self.eq('ab<div>fizz</div|>cd', 'n_%', 'ab<div>fizz|</div>cd')
        self.eq('ab<div>f|izz</div>cd', 'n_%', 'ab<div>fizz</div|>cd')
        self.eq('ab<div>fi|zz</div>cd', 'n_%', 'ab<div>fizz</div|>cd')
        self.eq('ab<div>fiz|z</div>cd', 'n_%', 'ab<div>fizz</div|>cd')
        self.eq('ab<div><div>f|izz</div></div>cd', 'n_%', 'ab<div><div>fizz</div|></div>cd')
