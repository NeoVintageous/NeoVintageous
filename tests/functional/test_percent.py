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

    def test_find_next_item_in_this_line_after_the_cursor(self):
        start = '<?php\nfunct|ion x() {\n    //...\n}\n'
        self.normal(start)
        self.feed('%')
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
        self.assertVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('l_%')
        self.assertVline(start)
        # TODO Addding a "reverse" param for assertVline() would make this call to assertSelection() obsolete.
        self.assertSelection((14, 12), 'selection should be reversed')

    def test_if_forward_vlines_within_targets_and_target_is_before_selection_it_should_flip_and_reverse_selection(self):
        start = 'x\nf {\na\n|b\nc\n}\n|x\n'
        self.vline(start)
        # TODO Addding a "reverse" param for vline() above would make this calls to assertSelection() and select() obsolete.  # noqa: E501
        self.feed('l_%')
        self.assertVline('x\n|f {\na\nb\n|c\n}\nx\n')
        self.assertSelection((10, 2))
        self.feed('l_%')
        self.assertVline(start)
        self.assertSelection((8, 14))

    def test_if_backward_vline_and_target_is_before_selection_it_should_extend_selection(self):
        start = 'x\nf {\na\nb\nc\n|}\n|x\n'
        self.vline(start)
        # TODO Addding a "reverse" param for vline() and assertVline() would make the calls to assertSelection() and select() below obsolete.  # noqa: E501
        self.assertSelection((12, 14))
        self.select((14, 12))
        self.feed('l_%')
        self.assertVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.assertSelection((14, 2))
        self.feed('l_%')
        self.assertVline(start)
        self.assertSelection((14, 12))

    def test_if_backward_vlines_and_target_is_before_selection_it_should_extend_selection(self):
        start = 'x\nf {\na\nb\nc\n|}\nx\ny\n|z\n'
        self.vline(start)
        # TODO Addding a "reverse" param for vline() and assertVline() would make the calls to assertSelection() and select() below obsolete.  # noqa: E501
        self.assertSelection((12, 18))
        self.select((18, 12))
        self.feed('l_%')
        self.assertVline('x\n|f {\na\nb\nc\n}\nx\ny\n|z\n')
        self.assertSelection((18, 2))
        self.feed('l_%')
        self.assertVline(start)
        self.assertSelection((18, 12))

    def test_if_reverse_vlines_within_targets_and_target_is_before_selection_it_should_flip_and_reverse_selection(self):
        start = 'x\n|f {\na\nb\n|c\n}\nx\n'
        self.vline(start)
        # TODO Addding a "reverse" param for vline() above would make this calls to assertSelection() and select() obsolete.  # noqa: E501
        self.assertSelection((2, 10))
        self.select((10, 2))
        self.feed('l_%')
        self.assertVline('x\nf {\na\n|b\nc\n}\n|x\n')
        self.assertSelection((8, 14))
        self.feed('l_%')
        self.assertVline(start)
        self.assertSelection((10, 2))
