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

from NeoVintageous.nv.plugin_abolish import _coerce_to_camelcase
from NeoVintageous.nv.plugin_abolish import _coerce_to_dashcase
from NeoVintageous.nv.plugin_abolish import _coerce_to_dotcase
from NeoVintageous.nv.plugin_abolish import _coerce_to_mixedcase
from NeoVintageous.nv.plugin_abolish import _coerce_to_snakecase
from NeoVintageous.nv.plugin_abolish import _coerce_to_spacecase
from NeoVintageous.nv.plugin_abolish import _coerce_to_titlecase
from NeoVintageous.nv.plugin_abolish import _coerce_to_uppercase


class TestAbolish(unittest.TestCase):

    def test_coerce_to_mixedcase(self):
        self.assertEqual('', _coerce_to_mixedcase(''))
        self.assertEqual('M', _coerce_to_mixedcase('m'))
        self.assertEqual('Mixed', _coerce_to_mixedcase('Mixed'))
        self.assertEqual('Mixed', _coerce_to_mixedcase('mixed'))
        self.assertEqual('Mixed', _coerce_to_mixedcase('MIXED'))
        self.assertEqual('MixedCase', _coerce_to_mixedcase('MixedCase'))

    def test_coerce_to_camelcase(self):
        self.assertEqual('', _coerce_to_camelcase(''))
        self.assertEqual('c', _coerce_to_camelcase('c'))
        self.assertEqual('c', _coerce_to_camelcase('C'))
        self.assertEqual('camel', _coerce_to_camelcase('camel'))
        self.assertEqual('camel', _coerce_to_camelcase('Camel'))
        self.assertEqual('camel', _coerce_to_camelcase('CAMEL'))
        self.assertEqual('camelCase', _coerce_to_camelcase('camelCase'))
        self.assertEqual('camelCamelCase', _coerce_to_camelcase('CamelCamelCase'))
        self.assertEqual('snakeCase', _coerce_to_camelcase('snake_case'))
        self.assertEqual('snakeSnakeCase', _coerce_to_camelcase('snake_snake_case'))
        self.assertEqual('mixedCase', _coerce_to_camelcase('MixedCase'))
        self.assertEqual('upperSnakeCase', _coerce_to_camelcase('UPPER_SNAKE_CASE'))

    def test_coerce_to_snakecase(self):
        self.assertEqual('', _coerce_to_snakecase(''))
        self.assertEqual('s', _coerce_to_snakecase('S'))
        self.assertEqual('snake', _coerce_to_snakecase('snake'))
        self.assertEqual('snake', _coerce_to_snakecase('SNAKE'))
        self.assertEqual('snake', _coerce_to_snakecase('Snake'))
        self.assertEqual('snake_case', _coerce_to_snakecase('snake_case'))
        self.assertEqual('snake_case', _coerce_to_snakecase('SnakeCase'))
        self.assertEqual('snake_snake_case', _coerce_to_snakecase('SnakeSnakeCase'))
        self.assertEqual('snake2_snake2_case', _coerce_to_snakecase('Snake2Snake2Case'))
        self.assertEqual('get_http_response_code', _coerce_to_snakecase('getHTTPResponseCode'))
        self.assertEqual('get2_http_response_code', _coerce_to_snakecase('get2HTTPResponseCode'))
        self.assertEqual('http_response_code', _coerce_to_snakecase('HTTPResponseCode'))
        self.assertEqual('http_response_code_xyz', _coerce_to_snakecase('HTTPResponseCodeXYZ'))
        self.assertEqual('html_tidy', _coerce_to_snakecase('HTMLTidy'))
        self.assertEqual('html_tidy_generator', _coerce_to_snakecase('HTMLTidyGenerator'))
        self.assertEqual('free_bsd', _coerce_to_snakecase('FreeBSD'))
        self.assertEqual('html', _coerce_to_snakecase('HTML'))

    def test_coerce_to_uppercase(self):
        self.assertEqual('', _coerce_to_uppercase(''))
        self.assertEqual('U', _coerce_to_uppercase('u'))
        self.assertEqual('UPPERCASE', _coerce_to_uppercase('UPPERCASE'))
        self.assertEqual('UPPERCASE', _coerce_to_uppercase('uppercase'))
        self.assertEqual('SNAKE_CASE', _coerce_to_uppercase('snake_case'))
        self.assertEqual('CAMEL_CASE', _coerce_to_uppercase('camelCase'))
        self.assertEqual('TITLE_CASE', _coerce_to_uppercase('titleCase'))
        self.assertEqual('UPPER_UPPER_CASE', _coerce_to_uppercase('UpperUpperCase'))
        self.assertEqual('UPPER_UPPER_CASE', _coerce_to_uppercase('upper_upperCase'))
        self.assertEqual('UPPER_UPPER_CASE', _coerce_to_uppercase('UPPER_upperCase'))

    def test_coerce_to_dashcase(self):
        self.assertEqual('', _coerce_to_dashcase(''))
        self.assertEqual('dash', _coerce_to_dashcase('dash'))
        self.assertEqual('dash-case', _coerce_to_dashcase('dash-case'))
        self.assertEqual('snake-case', _coerce_to_dashcase('snake_case'))
        self.assertEqual('camel-case', _coerce_to_dashcase('camelCase'))
        self.assertEqual('title-case', _coerce_to_dashcase('TitleCase'))

    def test_coerce_to_spacecase(self):
        self.assertEqual('', _coerce_to_spacecase(''))
        self.assertEqual('space', _coerce_to_spacecase('space'))
        self.assertEqual('space case', _coerce_to_spacecase('space case'))
        self.assertEqual('snake case', _coerce_to_spacecase('snake_case'))
        self.assertEqual('camel case', _coerce_to_spacecase('camelCase'))
        self.assertEqual('title case', _coerce_to_spacecase('TitleCase'))

    def test_coerce_to_dotcase(self):
        self.assertEqual('', _coerce_to_dotcase(''))
        self.assertEqual('dot', _coerce_to_dotcase('dot'))
        self.assertEqual('dot.case', _coerce_to_dotcase('dot.case'))
        self.assertEqual('snake.case', _coerce_to_dotcase('snake_case'))
        self.assertEqual('camel.case', _coerce_to_dotcase('camelCase'))
        self.assertEqual('title.case', _coerce_to_dotcase('TitleCase'))

    def test_coerce_to_titlecase(self):
        self.assertEqual('', _coerce_to_titlecase(''))
        self.assertEqual('Title', _coerce_to_titlecase('Title'))
        self.assertEqual('Title', _coerce_to_titlecase('title'))
        self.assertEqual('Title', _coerce_to_titlecase('TITLE'))
        self.assertEqual('Title Case', _coerce_to_titlecase('TitleCase'))
        self.assertEqual('Snake Case', _coerce_to_titlecase('snake_case'))
        self.assertEqual('Camel Case', _coerce_to_titlecase('camelCase'))
