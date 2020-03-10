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
        self.eq('1|{ab}2|{cd}3|{ef}x', 'n_%', '1{ab|}2{cd|}3{ef|}x')
        self.eq('1|{ab}2{cd}3|{ef}x', 'n_%', '1{ab|}2{cd}3{ef|}x')
        self.eq('|1\n2\n3\n4\n5\n6\n7\n8\n9\n0', 'n_30%', '1\n2\n|3\n4\n5\n6\n7\n8\n9\n0')
        self.eq('|1\n2\n3\n4\n5\n6', 'n_80%', '1\n2\n3\n4\n|5\n6')
        self.eq('|fi(zzbu)zz', 'n_%', 'fi(zzbu|)zz')
        self.eq('f|i(zzbu)zz', 'n_%', 'fi(zzbu|)zz')
        self.eq('fi|(zzbu)zz', 'n_%', 'fi(zzbu|)zz')
        self.eq('fi(|zzbu)zz', 'n_%', 'fi|(zzbu)zz')
        self.eq('fi(z|zbu)zz', 'n_%', 'fi|(zzbu)zz')
        self.eq('fi(zz|bu)zz', 'n_%', 'fi|(zzbu)zz')
        self.eq('fi(zzb|u)zz', 'n_%', 'fi|(zzbu)zz')
        self.eq('fi(zzbu|)zz', 'n_%', 'fi|(zzbu)zz')
        self.eq('fi(zzbu)|zz', 'n_%', 'fi(zzbu)|zz')
        self.eq('fi(zzbu)z|z', 'n_%', 'fi(zzbu)z|z')
        self.eq('fi|(zzbuzz', 'n_%', 'fi|(zzbuzz')
        self.eq('fi(zz|buzz', 'n_%', 'fi(zz|buzz')
        self.eq('fizzbu|)zz', 'n_%', 'fizzbu|)zz')
        self.eq('fizz|bu)zz', 'n_%', 'fizz|bu)zz')
        self.eq('fi|(zz(buzz)fi)zz', 'n_%', 'fi(zz(buzz)fi|)zz')
        self.eq('fi(zz|(buzz)fi)zz', 'n_%', 'fi(zz(buzz|)fi)zz')
        self.eq('fi(zz(buzz)fi|)zz', 'n_%', 'fi|(zz(buzz)fi)zz')
        self.eq('fi(zz(buzz|)fi)zz', 'n_%', 'fi(zz|(buzz)fi)zz')
        self.eq('f|(i(zz(buzz)fi)z)z', 'n_%', 'f(i(zz(buzz)fi)z|)z')
        self.eq('f(i(zz(buzz)fi)z|)z', 'n_%', 'f|(i(zz(buzz)fi)z)z')
        self.eq('()\nfi|zz\n()\n', 'n_%', '()\nfi|zz\n()\n')
        self.eq('{}\nfi|zz\n{}\n', 'n_%', '{}\nfi|zz\n{}\n')
        self.eq('<fi|zz> <bu>zz', 'n_%', '|<fizz> <bu>zz')
        self.eq('<fi|zz <bu>zz', 'n_%', '<fizz <bu|>zz')

    def test_v(self):
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
        self.eq('f|iz|z', 'v_%', 'f|iz|z')

    def test_V(self):
        self.eq('|\n|', 'V_%', '|\n|')
        self.eq('|ab\n|', 'V_%', '|ab\n|')
        self.eq('1| \n|2', 'V_%', '1| \n|2')
        self.eq('\n|\n\n|\n', 'V_%', '\n|\n\n|\n')

    def test_d(self):
        self.eq('abc (a|bc) abc', 'd%', 'abc |c) abc')
        self.eq('abc (abc|) abc', 'd%', 'abc  |abc')
        self.eq('abc |(abc) abc', 'd%', 'abc  |abc')
        self.eq('|abc (abc) abc', 'd%', ' |abc')
        self.eq('f|izz', 'd%', 'f|izz')


class Test_percent_in_PHP_syntax(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.syntax('Packages/PHP/PHP.sublime-syntax')

    def test_percent(self):
        self.eq('<?php\nfunct|ion x() {\n//...\n}\n', 'n_%', '<?php\nfunction x(|) {\n//...\n}\n')
        self.eq('<fi|zz>buzz</fizz>', 'n_%', '<fizz>buzz|</fizz>')
        self.eq('<?php function x() |{/*{*/}\n', 'n_%', '<?php function x() {/*{*/|}\n')
        self.eq('<?php function x() {/*{*/|}\n', 'n_%', '<?php function x() |{/*{*/}\n')
        self.eq('<?php functi|on x($x="_)_") {}\n', 'n_%', '<?php function x($x="_)_"|) {}\n')
        self.eq('<?php function x($x="_(_"|) {}\n', 'n_%', '<?php function x|($x="_(_") {}\n')
        self.eq('<?php function x() |{\n// {{}}}\n$x=\'{{}}}\';\n}\n', 'n_%', '<?php function x() {\n// {{}}}\n$x=\'{{}}}\';\n|}\n')  # noqa: E501
        self.eq('<?php function x() {\n// {{}}}\n$x=\'{{}}}\';\n|}\n', 'n_%', '<?php function x() |{\n// {{}}}\n$x=\'{{}}}\';\n}\n')  # noqa: E501
        self.eq('<?php function f() {  |{ // 1\n  // {\n  } // 2\n} // 3\n', 'n_%', '<?php function f() {  { // 1\n  // {\n  |} // 2\n} // 3\n')  # noqa: E501
        self.eq('<?php if (true) {\nif (true) |{\n$x = "{";\n}\n}\n', 'n_%', '<?php if (true) {\nif (true) {\n$x = "{";\n|}\n}\n')  # noqa: E501

    def test_find_next_item_in_this_line_after_the_cursor(self):
        start = '<?php\nfunct|ion x() {\n    //...\n}\n'
        self.normal(start)
        self.feed('n_%')
        self.assertNormal('<?php\nfunction x(|) {\n    //...\n}\n')


class Test_percent_in_HTML_syntax(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.syntax('Packages/HTML/HTML.sublime-syntax')

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
        self.eq('fi|zz<div>buzz', 'n_%', 'fizz<div|>buzz')
        self.eq('fi|zz</div>buzz', 'n_%', 'fizz</div|>buzz')
        self.eq('fi<d|iv>zzbuzz', 'n_%', 'fi|<div>zzbuzz')
        self.eq('fizzb</d|iv>uzz', 'n_%', 'fizzb|</div>uzz')
        self.eq('fi<d|iv>zz <i>b</i>uzz', 'n_%', 'fi|<div>zz <i>b</i>uzz')
        self.eq('f<i>i</i>zz b</d|iv>uzz', 'n_%', 'f<i>i</i>zz b|</div>uzz')
        self.eq('|fi<div>zzbu</div>zz', 'n_%', 'fi<div|>zzbu</div>zz')
        self.eq('f|i<div>zzbu</div>zz', 'n_%', 'fi<div|>zzbu</div>zz')
        self.eq('fi|<div>zzbu</div>zz', 'n_%', 'fi<div|>zzbu</div>zz')
        self.eq('fi<|div>zzbu</div>zz', 'n_%', 'fi<div>zzbu|</div>zz')
        self.eq('fi<d|iv>zzbu</div>zz', 'n_%', 'fi<div>zzbu|</div>zz')
        self.eq('fi<di|v>zzbu</div>zz', 'n_%', 'fi<div>zzbu|</div>zz')
        self.eq('fi<div|>zzbu</div>zz', 'n_%', 'fi|<div>zzbu</div>zz')
        self.eq('fi<div>|zzbu</div>zz', 'n_%', 'fi<div>zzbu|</div>zz')
        self.eq('fi<div>z|zbu</div>zz', 'n_%', 'fi<div>zzbu</div|>zz')
        self.eq('fi<div>zz|bu</div>zz', 'n_%', 'fi<div>zzbu</div|>zz')
        self.eq('fi<div>zzb|u</div>zz', 'n_%', 'fi<div>zzbu</div|>zz')
        self.eq('fi<div>zzbu|</div>zz', 'n_%', 'fi<div>zzbu</div|>zz')
        self.eq('fi<div>zzbu<|/div>zz', 'n_%', 'fi|<div>zzbu</div>zz')
        self.eq('fi<div>zzbu</|div>zz', 'n_%', 'fi|<div>zzbu</div>zz')
        self.eq('fi<div>zzbu</d|iv>zz', 'n_%', 'fi|<div>zzbu</div>zz')
        self.eq('fi<div>zzbu</di|v>zz', 'n_%', 'fi|<div>zzbu</div>zz')
        self.eq('fi<div>zzbu</div|>zz', 'n_%', 'fi<div>zzbu|</div>zz')
        self.eq('fi<div>zzbu</div>|zz', 'n_%', 'fi|<div>zzbu</div>zz')
        self.eq('fi<div>zzbu</div>z|z', 'n_%', 'fi<div>zzbu</div>z|z')


class Test_percent_in_XML_syntax(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.syntax('Packages/XML/XML.sublime-syntax')

    def test_percent(self):
        self.eq('<fi|zz>buzz</fizz>', 'n_%', '<fizz>buzz|</fizz>')


class Test_workaround_for_issue_243(unittest.FunctionalTestCase):

    def test_if_forward_vline_and_target_is_after_selection_it_should_extend_forward(self):
        start = 'x\n|f {\n|a\nb\nc\n}\nx\n'
        self.vline(start)
        self.feed('V_%')
        self.assertVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('V_%')
        self.assertVline(start)

    def test_if_forward_vlines_and_target_is_after_selection_it_should_extend_forward(self):
        start = 'x\n|y\nz\nf {\n|a\nb\nc\n}\nx\n'
        self.vline(start)
        self.feed('V_%')
        self.assertVline('x\n|y\nz\nf {\na\nb\nc\n}\n|x\n')
        self.feed('V_%')
        self.assertVline(start)

    def test_if_forward_vline_and_target_is_before_selection_it_should_reverse_selection_and_extend_backward(self):
        start = 'x\nf {\na\nb\nc\n|}\n|x\n'
        self.vline(start)
        self.feed('V_%')
        self.assertRVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('V_%')
        self.assertRVline(start)

    def test_if_forward_vlines_within_targets_and_target_is_before_selection_it_should_flip_and_reverse_selection(self):
        start = 'x\nf {\na\n|b\nc\n}\n|x\n'
        self.vline(start)
        self.feed('V_%')
        self.assertRVline('x\n|f {\na\nb\n|c\n}\nx\n')
        self.feed('V_%')
        self.assertVline(start)

    def test_if_backward_vline_and_target_is_before_selection_it_should_extend_selection(self):
        start = 'x\nf {\na\nb\nc\n|}\n|x\n'
        self.rvline(start)
        self.feed('V_%')
        self.assertRVline('x\n|f {\na\nb\nc\n}\n|x\n')
        self.feed('V_%')
        self.assertRVline(start)

    def test_if_backward_vlines_and_target_is_before_selection_it_should_extend_selection(self):
        start = 'x\nf {\na\nb\nc\n|}\nx\ny\n|z\n'
        self.rvline(start)
        self.feed('V_%')
        self.assertRVline('x\n|f {\na\nb\nc\n}\nx\ny\n|z\n')
        self.feed('V_%')
        self.assertRVline(start)

    def test_if_reverse_vlines_within_targets_and_target_is_before_selection_it_should_flip_and_reverse_selection(self):
        start = 'x\n|f {\na\nb\n|c\n}\nx\n'
        self.rvline(start)
        self.feed('V_%')
        self.assertVline('x\nf {\na\n|b\nc\n}\n|x\n')
        self.feed('V_%')
        self.assertRVline(start)
