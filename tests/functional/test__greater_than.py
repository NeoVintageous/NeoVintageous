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


class Test_greater_than(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('translate_tabs_to_spaces', True)
        self.settings().set('tab_size', 4)

    def test_G(self):
        self.eq('1\n|2\n3\n4\n', '>G', '1\n    |2\n    3\n    4\n')
        self.eq('1\n|    2\n3\n4\n', '>G', '1\n        |2\n    3\n    4\n')

    def test_ip(self):
        self.eq('x\n\nf|iz|z\nb|uz|z\n\nx', '>ip', 'x\n\n    |fizz\n    buzz\n\nx')

    def test_v(self):
        self.eq('|abc\ndef\n', 'v_>', 'n_    |abc\ndef\n')
        self.eq('|    abc\ndef\n', 'v_>', 'n_        |abc\ndef\n')
        self.eq('x\nfi|zz\nbu|zz\nx', 'v_>', 'n_x\n    |fizz\n    buzz\nx')
        self.eq('x\nfi|zz\n    bu|zz\nx', 'v_>', 'n_x\n    |fizz\n        buzz\nx')

    def test_l(self):
        self.eq('x\n|fizz\nbuzz\n|x', 'V_>', 'n_x\n    |fizz\n    buzz\nx')

    def test_b(self):
        self.eq('x\nf|iz|z\nb|uz|z\nx', 'b_>', 'n_x\nf|    izz\nb    uzz\nx')
        self.eq('x\nf|iz|z\nb|uz|z\nx', 'b_2>', 'n_x\nf|        izz\nb        uzz\nx')
