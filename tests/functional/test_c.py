# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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
from NeoVintageous.tests.text_object_targets import all_one_line_targets


class Test_c(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)

    def test_c0(self):
        self.eq('1\nfi|zz\n2', 'c0', 'i_1\n|zz\n2')
        self.assertRegisters('"-', 'fi')
        self.assertRegistersEmpty('01')

    def test_ce(self):
        self.eq('one |two three', 'ce', 'i_one | three')
        self.eq('one t|wo three', 'ce', 'i_one t| three')
        self.assertRegister('"wo')
        self.assertRegister('-wo')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_ce_to_register(self):
        self.normal('one t|wo three')
        self.feed('"a')
        self.feed('ce')
        self.assertRegister('"wo')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_v(self):
        self.eq('fi|zz bu|zz', 'v_c', 'i_fi|zz')
        self.eq('r_fi|zz bu|zz', 'v_c', 'i_fi|zz')
        self.eq('r_fi|   |zz', 'v_c', 'i_fi|zz')

    def test_s(self):
        self.eq('fi|zz bu|zz', 's_c', 'i_fi|zz')

    def test_cb(self):
        self.eq('x fizz|buzz x', 'cb', 'i_x |buzz x')
        self.assertRegister('"fizz')
        self.assertRegister('-fizz')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_cw(self):
        self.eq('one |two three', 'cw', 'i_one | three')
        self.eq('one t|wo three', 'cw', 'i_one t| three')
        self.assertRegister('"wo')
        self.assertRegister('-wo')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')
        self.eq('one t|wo\nthree four', '2cw', 'i_one t| four')
        self.eq('one |two\nthree four', '2cw', 'i_one | four')
        self.eq('one |two\nthree\nfour', '2cw', 'i_one |\nfour')

    def test_cw_to_default_register(self):
        self.normal('f|izz buzz')
        self.feed('cw')
        self.assertInsert('f| buzz')
        self.assertRegister('"izz')
        self.assertRegister('-izz')

    def test_cw_to_register(self):
        self.normal('f|izz buzz')
        self.feed('"')
        self.feed('a')
        self.feed('cw')
        self.assertInsert('f| buzz')
        self.assertRegister('"izz')
        self.assertRegister('aizz')

    def test_ciw(self):
        self.eq('a |fizz b', 'ciw', 'i_a | b')
        self.eq('a fi|zz b', 'ciw', 'i_a | b')
        self.eq('a fiz|z b', 'ciw', 'i_a | b')
        self.eq('a| b', 'ciw', 'i_a|b')
        self.eq('a|    b', 'ciw', 'i_a|b')
        self.eq('a .|.. b', 'ciw', 'i_a | b')
        self.eq('a.|..b', 'ciw', 'i_a|b')

    @unittest.expectedFailure
    def test_ciw_issue_748_01(self):
        self.eq('x\n\n|\n\nx', 'ciw', 'i_x\n\n|\n\nx')

    @unittest.expectedFailure
    def test_ciw_issue_748_02(self):
        self.eq('\n|\nx\nx\n', 'ciw', 'i_\n|\nx\nx\n')

    def test_caw(self):
        self.eq('a fi|zz...', 'caw', 'i_a|...')
        self.eq('a    fi|zz...', 'caw', 'i_a|...')
        self.eq('one t|wo\nthree\nfour', '2caw', 'i_one|\nfour')
        self.eq('one |two\nthree\nfour', '2caw', 'i_one|\nfour')
        self.eq('x\n\n|\n\nx', 'caw', 'i_x\n\n|\nx')

    @unittest.expectedFailure
    def test_caw_issue_748_01(self):
        self.eq('a fi|zz b', 'caw', 'i_a |b')

    @unittest.expectedFailure
    def test_caw_issue_748_02(self):
        self.eq('a fi|zz    b', 'caw', 'i_a |b')

    @unittest.expectedFailure
    def test_caw_issue_748_03(self):
        self.eq('\n|\nfoo\nx\n', 'caw', 'i_x\n|\nx\n')

    @unittest.expectedFailure
    def test_caw_issue_748_04(self):
        self.eq('1\na fi|zz b\n3', 'caw', 'i_1\na |b\n3')

    @unittest.expectedFailure
    def test_caw_issue_748_05(self):
        self.eq('one t|wo\nthree four', '2caw', 'i_one |four')

    @unittest.expectedFailure
    def test_caw_issue_748_06(self):
        self.eq('one |two\nthree four', '2caw', 'i_one |four')

    def test_c__dollar(self):
        self.eq('one |two three', 'c$', 'i_one |')
        self.eq('one t|wo three', 'c$', 'i_one t|')
        self.assertRegister('"wo three')
        self.assertRegister('-wo three')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_cc(self):
        self.eq('\n\n|\n\n', 'cc', 'i_\n\n|\n\n')
        self.eq('|aaa\nbbb\nccc', 'cc', 'i_|\nbbb\nccc')
        self.eq('aaa\nbb|b\nccc', 'cc', 'i_aaa\n|\nccc')
        self.eq('aaa\nbbb\n|ccc', 'cc', 'i_aaa\nbbb\n|')
        self.assertLinewiseRegister('"ccc\n')
        self.assertLinewiseRegister('1ccc\n')
        self.assertLinewiseRegister('2bbb\n')
        self.assertLinewiseRegister('3aaa\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.eq('x\n    fi|zz\ny', 'cc', 'i_x\n    |\ny')
        self.assertXpos(4)

    def test_cc_should_not_strip_preceding_whitespace(self):
        self.eq('    |one', 'cc', 'i_    |')
        self.eq('one\n  tw|o\nthree\n', 'cc', 'i_one\n  |\nthree\n')

    def test_cc_last_line(self):
        self.eq('1\ntw|o', 'cc', 'i_1\n|')
        self.eq('1\ntw|o\n', 'cc', 'i_1\n|\n')

    def test_ci__quote(self):
        self.eq('"|"', 'ci"', 'i_"|"')
        self.eq('"1|23"', 'ci"', 'i_"|"')
        self.assertRegister('"123')
        self.assertRegister('-123')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')
        self.eq('"1|23  "', 'ci"', 'i_"|"')
        self.assertRegister('"123  ')

    def test_ci__one_line_targets(self):
        for t in all_one_line_targets:
            self.eq('{0}|{0}'.format(t), 'ci' + t, 'i_{0}|{0}'.format(t))
            self.eq('{0}1|23{0}'.format(t), 'ci' + t, 'i_{0}|{0}'.format(t))
            self.assertRegister('"123')
            self.assertRegister('-123')
            self.assertRegisterEmpty('0')
            self.assertRegisterEmpty('1')
            self.eq('{0}1|23  {0}'.format(t), 'ci' + t, 'i_{0}|{0}'.format(t))

    def test_ca__one_line_targets(self):
        for t in all_one_line_targets:
            self.eq('{0}|{0}'.format(t), 'ca' + t, 'i_|')
            self.eq('x{0}fi|zz{0}x'.format(t), 'ca' + t, 'i_x|x')
            self.assertRegister('"{0}fizz{0}'.format(t))
            self.assertRegister('-{0}fizz{0}'.format(t))
            self.assertRegisterEmpty('0')
            self.assertRegisterEmpty('1')

    def test_ci__quote_multi_sel(self):
        self.eq('x"1|23"y\ni"ab|c"j\n', 'ci"', 'i_x"|"y\ni"|"j\n')
        self.assertRegister('"', ['123', 'abc'])
        self.assertRegister('-', ['123', 'abc'])
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_ci__quote__empty_should_not_fill_registers(self):
        self.eq('"|"', 'ci"', 'i_"|"')
        self.assertRegisterEmpty('"')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_ci__quote__multi_sels_empty_should_not_fill_registers(self):
        self.eq('"|"\n"|"', 'ci"', 'i_"|"\n"|"')
        self.assertRegisterEmpty('"')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.assertRegisterEmpty('1')

    def test_c_visual_line_sets_linewise_register(self):
        self.eq('x\n|abc\n|y', 'V_c', 'i_x\n|y')
        self.assertLinewiseRegister('"abc\n')
        self.assertLinewiseRegister('1abc\n')
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_c_(self):
        self.eq('1\nfi|zz\n2\n3', 'c_', 'i_1\n|\n2\n3')
        self.eq('1\n    fi|zz\n2\n3', 'c_', 'i_1\n|\n2\n3')

    def test_cit(self):
        self.eq('<div><h1>fi|zz</h1></div>', 'cit', 'i_<div><h1>|</h1></div>')
        self.eq('<div><h|1>fizz</h1></div>', 'cit', 'i_<div><h1>|</h1></div>')
        self.eq('<div>  |  <h1>fizz</h1></div>', 'cit', 'i_<div>|</div>')
        self.eq('<div>\n  |  <h1>fizz</h1>\n</div>', 'cit', 'i_<div>\n    <h1>|</h1>\n</div>')
        self.eq('<div>\n  |  <h1>fizz</h1>\n</div>', 'cit', 'i_<div>\n    <h1>|</h1>\n</div>')
        self.eq('<div>\n|\n  <h1>fizz</h1>\n</div>', 'cit', 'i_<div>|</div>')

    def test_cat(self):
        self.eq('<div><h1>fi|zz</h1></div>', 'cat', 'i_<div>|</div>')
        self.eq('<div><h|1>fizz</h1></div>', 'cat', 'i_<div>|</div>')
        self.eq('<div>  |  <h1>fizz</h1></div>', 'cat', 'i_|')
        self.eq('<div>\n  |  <h1>fizz</h1>\n</div>', 'cat', 'i_<div>\n    |\n</div>')

    def test_issue_654(self):
        self.eq('<header>\n |   <h1>fizz</h1>\n<header>', 'cit', 'i_<header>\n    <h1>|</h1>\n<header>')

    def test_issue_740(self):
        self.eq('fizz |(inner) buzz', 'ci(', 'i_fizz (|) buzz')
        self.eq('fizz |(inner) buzz', 'ca(', 'i_fizz | buzz')

    def test_issue_734_empty_tag(self):
        self.eq('<div>|</div>', 'cit', 'i_<div>|</div>')
        self.eq('x<div>|</div>x', 'cit', 'i_x<div>|</div>x')
        self.eq('<fi|zz></fizz>', 'cit', 'i_<fizz>|</fizz>')
