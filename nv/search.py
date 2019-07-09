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

import re

from sublime import IGNORECASE
from sublime import LITERAL

from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.settings import get_setting_neo
from NeoVintageous.nv.ui import ui_region_flags


def clear_search_highlighting(view):
    view.erase_regions('_nv_search_occ')
    view.erase_regions('_nv_search_cur')
    view.erase_regions('_nv_search_inc')


def get_search_occurrences(view):
    return view.get_regions('_nv_search_occ')


def add_search_highlighting(view, occurrences, incremental=None):
    if get_option(view, 'incsearch') and incremental:
        view.add_regions(
            '_nv_search_inc',
            incremental,
            scope='support.function neovintageous_search_inc',
            flags=ui_region_flags(get_setting_neo(view, 'search_inc_style'))
        )

    if get_option(view, 'hlsearch'):
        sels = view.sel()

        # TODO Optimise
        current = []
        for region in occurrences:
            for sel in sels:
                if region.contains(sel):
                    current.append(region)

        view.add_regions(
            '_nv_search_occ',
            occurrences,
            scope='string neovintageous_search_occ',
            flags=ui_region_flags(get_setting_neo(view, 'search_occ_style'))
        )

        view.add_regions(
            '_nv_search_cur',
            current,
            scope='support.function neovintageous_search_cur',
            flags=ui_region_flags(get_setting_neo(view, 'search_cur_style'))
        )


def calculate_buffer_search_flags(view, pattern):
    flags = 0

    if get_option(view, 'ignorecase'):
        flags |= IGNORECASE

    if not get_option(view, 'magic'):
        flags |= LITERAL

    if pattern:
        # Is the pattern as regular expression or a literal? For example, in
        # "magic" mode, simple strings like "]" should be treated as a literal
        # and "[0-9]" should be treated as a regular expression.

        # TODO Should this only be done in magic mode?
        # TODO Needs improvment

        if re.match('^[a-zA-Z0-9_\\[\\]]+$', pattern):
            if '[' not in pattern or ']' not in pattern:
                flags |= LITERAL
        elif re.match('^[a-zA-Z0-9_\\(\\)]+$', pattern):
            if '(' not in pattern or ')' not in pattern:
                flags |= LITERAL

    return flags


def calculate_word_search_flags(view, pattern):
    flags = 0

    if get_option(view, 'ignorecase'):
        flags |= IGNORECASE

    return flags


def create_word_search_pattern(view, pattern):
    return r'\b{0}\b'.format(re.escape(pattern))


def find_all_buffer_search_occurrences(view, pattern):
    return view.find_all(
        pattern,
        calculate_buffer_search_flags(view, pattern)
    )


def find_all_word_search_occurrences(view, pattern):
    return view.find_all(
        create_word_search_pattern(view, pattern),
        calculate_word_search_flags(view, pattern)
    )
