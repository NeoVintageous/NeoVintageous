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

from NeoVintageous.nv.plugin_sneak import _set_last_sneak_search


class Test_s(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('enable_sneak', True)

    @unittest.mock_status_message()
    def test_n(self):
        self.eq('|fizz', 'n_siz', 'f|izz')
        self.assertSearch('f|iz|z')
        self.assertSearchCurrent('f|iz|z')
        self.eq('fizz| fizz fizz', 'n_siz', 'fizz f|izz fizz')
        self.assertSearch('fizz f|iz|z f|iz|z')
        self.assertSearchCurrent('fizz f|iz|z fizz')
        self.eq('f|izz fizz fizz fizz', 'n_siz', 'fizz f|izz fizz fizz')
        self.assertSearch('fizz f|iz|z f|iz|z f|iz|z')
        self.assertSearchCurrent('fizz f|iz|z fizz fizz')
        self.feed('s<CR>')
        self.assertNormal('fizz fizz f|izz fizz')
        self.assertSearch('fizz fizz f|iz|z f|iz|z')
        self.assertSearchCurrent('fizz fizz f|iz|z fizz')
        self.feed('s<CR>')
        self.assertNormal('fizz fizz fizz f|izz')
        self.assertSearch('fizz fizz fizz f|iz|z')
        self.assertSearchCurrent('fizz fizz fizz f|iz|z')
        self.assertNoStatusMessage()
        self.feed('s<CR>')
        self.assertNormal('fizz fizz fizz f|izz')
        self.assertNoSearch()
        self.assertStatusMessage('not found: iz')

    @unittest.mock_status_message()
    def test_n_not_found(self):
        self.eq('|buzz', 'n_sab', '|buzz')
        self.assertNoSearch()
        self.assertStatusMessage('not found: ab')

    @unittest.mock_status_message()
    def test_n_no_last_search(self):
        self.normal('|fizz')
        _set_last_sneak_search(self.view, '')
        self.feed('s<CR>')
        self.assertNormal('|fizz')
        self.assertStatusMessage('no previous sneak search')

    @unittest.mock_status_message()
    def test_n_single_character_and_repeat(self):
        self.eq('x x _|_ x x x', 'n_sx<CR>', 'x x __ |x x x')
        self.assertSearch('x x __ |x| |x| |x|')
        self.assertSearchCurrent('x x __ |x| x x')
        self.feed('s<CR>')
        self.assertNormal('x x __ x |x x')
        self.assertSearch('x x __ x |x| |x|')
        self.assertSearchCurrent('x x __ x |x| x')
        self.feed('s<CR>')
        self.assertNormal('x x __ x x |x')
        self.assertSearch('x x __ x x |x|')
        self.assertSearchCurrent('x x __ x x |x|')
        self.assertNoStatusMessage()
        self.feed('s<CR>')
        self.assertNormal('x x __ x x |x')
        self.assertNoSearch()
        self.assertStatusMessage('not found: x')

    @unittest.mock_status_message()
    def test_n_use_ic_scs(self):
        def _case_sensitive_assertions():
            self.eq('| iz IZ iz IZ', 'n_sIZ', ' iz |IZ iz IZ')
            self.assertSearch(' iz |IZ| iz |IZ|')
            self.assertSearchCurrent(' iz |IZ| iz IZ')

        self.set_setting('sneak_use_ic_scs', 0)
        self.set_option('ignorecase', False)
        self.set_option('smartcase', False)
        _case_sensitive_assertions()
        self.set_option('ignorecase', True)
        self.set_option('smartcase', False)
        _case_sensitive_assertions()
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        _case_sensitive_assertions()

        self.set_setting('sneak_use_ic_scs', 1)
        self.set_option('ignorecase', False)
        self.set_option('smartcase', False)
        _case_sensitive_assertions()

        self.set_option('ignorecase', True)
        self.set_option('smartcase', False)
        self.eq('| iz IZ iz IZ', 'n_sIZ', ' |iz IZ iz IZ')
        self.assertSearch(' |iz| |IZ| |iz| |IZ|')
        self.assertSearchCurrent(' |iz| IZ iz IZ')

        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.eq('| iz IZ iz IZ', 'n_sIZ', ' iz |IZ iz IZ')
        self.assertSearch(' iz |IZ| iz |IZ|')
        self.assertSearchCurrent(' iz |IZ| iz IZ')

    def test_v(self):
        self.eq('x|xx|x fizz', 'v_siz', 'x|xxx fi|zz')
        self.eq('iz iz x|xx|x iz iz iz', 'v_siz', 'iz iz x|xxx i|z iz iz')
        self.assertSearch('iz iz xxxx |iz| |iz| |iz|')
        self.eq('|iz iz', 'v_siz', '|iz i|z')
        self.eq('r_iz |iz xx|xx iz iz', 'v_siz', 'iz iz x|xxx i|z iz')
        self.eq('r_iz| iz xx|xx iz iz', 'v_siz', 'r_iz |iz xx|xx iz iz')

    def test_V(self):
        self.eq('iz\n|x\n|x\niz\niz\nx', 'V_siz', 'iz\n|x\nx\niz\n|iz\nx')
        self.eq('|iz\n|iz\nx', 'V_siz', '|iz\niz\n|x')

    @unittest.mock_bell()
    def test_n_does_not_support_multiple_cursors(self):
        self.eq('|fizz |buzz', 'n_siz', '|fizz |buzz')
        self.assertBell('sneak does not support multiple cursors')

    @unittest.mock_status_message()
    def test_issue_772(self):
        self.eq('|  $this $this $this', 'n_s$t', '  |$this $this $this')
        self.assertSearch('  |$t|his |$t|his |$t|his')
        self.assertSearchCurrent('  |$t|his $this $this')


class Test_S(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('enable_sneak', True)

    @unittest.mock_status_message()
    def test_n(self):
        self.eq('fizz fizz fiz|z', 'n_Siz', 'fizz fizz f|izz')
        self.assertSearch('f|iz|z f|iz|z f|iz|z')
        self.assertSearchCurrent('fizz fizz f|iz|z')
        self.feed('S<CR>')
        self.assertNormal('fizz f|izz fizz')
        self.assertSearch('f|iz|z f|iz|z fizz')
        self.assertSearchCurrent('fizz f|iz|z fizz')
        self.feed('S<CR>')
        self.assertNormal('f|izz fizz fizz')
        self.assertSearch('f|iz|z fizz fizz')
        self.assertSearchCurrent('f|iz|z fizz fizz')
        self.feed('S<CR>')
        self.assertNormal('f|izz fizz fizz')
        self.assertNoSearch()
        self.assertStatusMessage('not found: iz')

    @unittest.mock_status_message()
    def test_n_not_found(self):
        self.eq('buz|z', 'n_Sab', 'buz|z')
        self.assertNoSearch()
        self.assertStatusMessage('not found: ab')

    @unittest.mock_status_message()
    def test_n_single_character_and_repeat(self):
        self.eq(' x x x| x', 'n_Sx<CR>', ' x x |x x')
        self.assertSearch(' |x| |x| |x| x')
        self.assertSearchCurrent(' x x |x| x')
        self.feed('S<CR>')
        self.assertNormal(' x |x x x')
        self.assertSearch(' |x| |x| x x')
        self.assertSearchCurrent(' x |x| x x')
        self.feed('S<CR>')
        self.assertNormal(' |x x x x')
        self.assertSearch(' |x| x x x')
        self.assertSearchCurrent(' |x| x x x')
        self.feed('S<CR>')
        self.assertNormal(' |x x x x')
        self.assertNoSearch()
        self.assertStatusMessage('not found: x')

    @unittest.mock_status_message()
    def test_issue_772(self):
        self.eq('$this $this $thi|s', 'n_S$t', '$this $this |$this')
        self.assertSearch('|$t|his |$t|his |$t|his')
        self.assertSearchCurrent('$this $this |$t|his')


class Test_Z(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('enable_sneak', True)

    def test_v(self):
        self.eq('x x iz iz iz x|xxx| iz', 'v_Ziz', 'r_x x iz iz |iz xx|xx iz')
        self.assertSearch('x x |iz| |iz| |iz| xxxx iz')
        self.feed('Z<CR>')
        self.assertRVisual('x x iz |iz iz xx|xx iz')
        self.assertSearch('x x |iz| |iz| iz xxxx iz')
        self.feed('Zx<CR>')
        self.assertRVisual('x |x iz iz iz xx|xx iz')
        self.assertSearch('|x| |x| iz iz iz xxxx iz')

    def test_V(self):
        self.eq('iz\niz\nxx\n|xxxx\n|iz\niz\n', 'V_Ziz', 'r_iz\n|iz\nxx\nxxxx\n|iz\niz\n')


class Test_z(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('enable_sneak', True)

    @unittest.mock_bell()
    def test_dz(self):
        self.eq('f|xxxizz', 'dziz', 'f|izz')
        self.eq('f|xxxizz', 'cziz', 'i_f|izz')
        self.eq('f|xxxizzxxfizz', '2dziz', 'f|izz')
        self.eq('f|xxxizzxxfizz', '2cziz', 'i_f|izz')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_dZ(self):
        self.eq('fiizzxxx|zz', 'dZiz', 'fi|zz')
        self.eq('fiizzxxx|zz', 'cZiz', 'i_fi|zz')
        self.eq('fiizxxizzxxx|zz', '2dZiz', 'fi|zz')
        self.eq('fiizxxizzxxx|zz', '2cZiz', 'i_fi|zz')


class Test_goto_next_and_goto_previous(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('enable_sneak', True)

    @unittest.mock_bell()
    def test_n(self):
        self.normal('|x iz iz iz iz iz iz')
        self.feed('siz')
        self.feed(';')
        self.assertNormal('x iz |iz iz iz iz iz')
        self.assertSearch('x iz |iz| |iz| |iz| |iz| |iz|')
        self.feed(';')
        self.assertNormal('x iz iz |iz iz iz iz')
        self.assertSearch('x iz iz |iz| |iz| |iz| |iz|')
        self.feed('3;')
        self.assertNormal('x iz iz iz iz iz |iz')
        self.assertSearch('x iz iz iz iz iz |iz|')
        self.assertNoBell()
        self.feed(';')
        self.assertNormal('x iz iz iz iz iz |iz')
        self.assertNoSearch()
        self.assertBell('not found: iz')
        self.feed(',')
        self.assertNormal('x iz iz iz iz |iz iz')
        self.assertSearch('x |iz| |iz| |iz| |iz| |iz| iz')
        self.feed('3,')
        self.assertNormal('x iz |iz iz iz iz iz')
        self.assertSearch('x |iz| |iz| iz iz iz iz')
        self.feed('Siz')
        self.assertNormal('x |iz iz iz iz iz iz')
        self.assertSearch('x |iz| iz iz iz iz iz')
        self.feed(',')
        self.assertNormal('x iz |iz iz iz iz iz')
        self.assertSearch('x iz |iz| |iz| |iz| |iz| |iz|')
        self.feed(';')
        self.assertNormal('x |iz iz iz iz iz iz')
        self.assertSearch('x |iz| iz iz iz iz iz')
        self.feed(';')
        self.assertNoSearch()
        self.assertBell('not found: iz')
        self.feed('4,')
        self.assertNormal('x iz iz iz iz |iz iz')
        self.assertSearch('x iz iz iz iz |iz| |iz|')
