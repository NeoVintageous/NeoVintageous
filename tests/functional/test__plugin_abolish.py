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


class TestAbolish(unittest.FunctionalTestCase):

    def test_coercion(self):
        self.eq('a b snake_ca|seCamelCaseTitleUPPER c', 'crm', 'a b |SnakeCaseCamelCaseTitleUpper c')
        self.eq('a b sn|ake_caseCamelCaseTitleUPPER c', 'crc', 'a b |snakeCaseCamelCaseTitleUpper c')
        self.eq('a b snake_caseCamelCaseTitleUPP|ER c', 'cr ', 'a b |snake case camel case title upper c')
        self.eq('a b s|nake_caseCamelCaseTitleUPPER c', 'cr.', 'a b |snake.case.camel.case.title.upper c')
        self.eq('a b snake_caseCamelCase|TitleUPPER c', 'crt', 'a b |Snake Case Camel Case Title Upper c')
        self.eq('a b snake_c|aseCamelCaseTitleUPPER c', 'crs', 'a b |snake_case_camel_case_title_upper c')
        self.eq('a b snake_c|aseCamelCaseTitleUPPER c', 'cr_', 'a b |snake_case_camel_case_title_upper c')
        self.eq('a b snake_caseCamelCaseT|itleUPPER c', 'cru', 'a b |SNAKE_CASE_CAMEL_CASE_TITLE_UPPER c')
        self.eq('a b snake_caseCamelCaseT|itleUPPER c', 'crU', 'a b |SNAKE_CASE_CAMEL_CASE_TITLE_UPPER c')
        self.eq('a b snake|_caseCamelCaseTitleUPPER c', 'cr-', 'a b |snake-case-camel-case-title-upper c')
        self.eq('a b snake|_caseCamelCaseTitleUPPER c', 'crk', 'a b |snake-case-camel-case-title-upper c')

    def test_unknown_coercion_should_be_noop(self):
        self.eq('a b snake_ca|seCamelCaseTitleUPPER c', 'cre', 'a b snake_ca|seCamelCaseTitleUPPER c')

    def test_crc(self):
        self.eq('|X', 'n_crc', '|x')
        self.eq('|x', 'n_crc', '|x')
