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
        self.assertEquals('', _coerce_to_mixedcase(''))
        self.assertEquals('M', _coerce_to_mixedcase('m'))
        self.assertEquals('Mixed', _coerce_to_mixedcase('Mixed'))
        self.assertEquals('Mixed', _coerce_to_mixedcase('mixed'))
        self.assertEquals('Mixed', _coerce_to_mixedcase('MIXED'))
        self.assertEquals('MixedCase', _coerce_to_mixedcase('MixedCase'))

    def test_coerce_to_camelcase(self):
        self.assertEquals('', _coerce_to_camelcase(''))
        self.assertEquals('c', _coerce_to_camelcase('c'))
        self.assertEquals('c', _coerce_to_camelcase('C'))
        self.assertEquals('camel', _coerce_to_camelcase('camel'))
        self.assertEquals('camel', _coerce_to_camelcase('Camel'))
        self.assertEquals('camel', _coerce_to_camelcase('CAMEL'))
        self.assertEquals('camelCase', _coerce_to_camelcase('camelCase'))
        self.assertEquals('camelCamelCase', _coerce_to_camelcase('CamelCamelCase'))
        self.assertEquals('snakeCase', _coerce_to_camelcase('snake_case'))
        self.assertEquals('snakeSnakeCase', _coerce_to_camelcase('snake_snake_case'))
        self.assertEquals('mixedCase', _coerce_to_camelcase('MixedCase'))
        self.assertEquals('upperSnakeCase', _coerce_to_camelcase('UPPER_SNAKE_CASE'))

    def test_coerce_to_snakecase(self):
        self.assertEquals('', _coerce_to_snakecase(''))
        self.assertEquals('s', _coerce_to_snakecase('S'))
        self.assertEquals('snake', _coerce_to_snakecase('snake'))
        self.assertEquals('snake', _coerce_to_snakecase('SNAKE'))
        self.assertEquals('snake', _coerce_to_snakecase('Snake'))
        self.assertEquals('snake_case', _coerce_to_snakecase('snake_case'))
        self.assertEquals('snake_case', _coerce_to_snakecase('SnakeCase'))
        self.assertEquals('snake_snake_case', _coerce_to_snakecase('SnakeSnakeCase'))
        self.assertEquals('snake2_snake2_case', _coerce_to_snakecase('Snake2Snake2Case'))
        self.assertEquals('get_http_response_code', _coerce_to_snakecase('getHTTPResponseCode'))
        self.assertEquals('get2_http_response_code', _coerce_to_snakecase('get2HTTPResponseCode'))
        self.assertEquals('http_response_code', _coerce_to_snakecase('HTTPResponseCode'))
        self.assertEquals('http_response_code_xyz', _coerce_to_snakecase('HTTPResponseCodeXYZ'))
        self.assertEquals('html_tidy', _coerce_to_snakecase('HTMLTidy'))
        self.assertEquals('html_tidy_generator', _coerce_to_snakecase('HTMLTidyGenerator'))
        self.assertEquals('free_bsd', _coerce_to_snakecase('FreeBSD'))
        self.assertEquals('html', _coerce_to_snakecase('HTML'))

    def test_coerce_to_uppercase(self):
        self.assertEquals('', _coerce_to_uppercase(''))
        self.assertEquals('U', _coerce_to_uppercase('u'))
        self.assertEquals('UPPERCASE', _coerce_to_uppercase('UPPERCASE'))
        self.assertEquals('UPPERCASE', _coerce_to_uppercase('uppercase'))
        self.assertEquals('SNAKE_CASE', _coerce_to_uppercase('snake_case'))
        self.assertEquals('CAMEL_CASE', _coerce_to_uppercase('camelCase'))
        self.assertEquals('TITLE_CASE', _coerce_to_uppercase('titleCase'))
        self.assertEquals('UPPER_UPPER_CASE', _coerce_to_uppercase('UpperUpperCase'))
        self.assertEquals('UPPER_UPPER_CASE', _coerce_to_uppercase('upper_upperCase'))
        self.assertEquals('UPPER_UPPER_CASE', _coerce_to_uppercase('UPPER_upperCase'))

    def test_coerce_to_dashcase(self):
        self.assertEquals('', _coerce_to_dashcase(''))
        self.assertEquals('dash', _coerce_to_dashcase('dash'))
        self.assertEquals('dash-case', _coerce_to_dashcase('dash-case'))
        self.assertEquals('snake-case', _coerce_to_dashcase('snake_case'))
        self.assertEquals('camel-case', _coerce_to_dashcase('camelCase'))
        self.assertEquals('title-case', _coerce_to_dashcase('TitleCase'))

    def test_coerce_to_spacecase(self):
        self.assertEquals('', _coerce_to_spacecase(''))
        self.assertEquals('space', _coerce_to_spacecase('space'))
        self.assertEquals('space case', _coerce_to_spacecase('space case'))
        self.assertEquals('snake case', _coerce_to_spacecase('snake_case'))
        self.assertEquals('camel case', _coerce_to_spacecase('camelCase'))
        self.assertEquals('title case', _coerce_to_spacecase('TitleCase'))

    def test_coerce_to_dotcase(self):
        self.assertEquals('', _coerce_to_dotcase(''))
        self.assertEquals('dot', _coerce_to_dotcase('dot'))
        self.assertEquals('dot.case', _coerce_to_dotcase('dot.case'))
        self.assertEquals('snake.case', _coerce_to_dotcase('snake_case'))
        self.assertEquals('camel.case', _coerce_to_dotcase('camelCase'))
        self.assertEquals('title.case', _coerce_to_dotcase('TitleCase'))

    def test_coerce_to_titlecase(self):
        self.assertEquals('', _coerce_to_titlecase(''))
        self.assertEquals('Title', _coerce_to_titlecase('Title'))
        self.assertEquals('Title', _coerce_to_titlecase('title'))
        self.assertEquals('Title', _coerce_to_titlecase('TITLE'))
        self.assertEquals('Title Case', _coerce_to_titlecase('TitleCase'))
        self.assertEquals('Snake Case', _coerce_to_titlecase('snake_case'))
        self.assertEquals('Camel Case', _coerce_to_titlecase('camelCase'))
