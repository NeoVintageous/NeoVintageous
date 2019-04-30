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

from contextlib import contextmanager

from sublime import Region


def has_dirty_buffers(window):
    # type: (...) -> bool
    for v in window.views():
        if v.is_dirty():
            return True

    return False


# Useful for external plugins to disable NeoVintageous for specific views.
def is_ignored(view):
    # type: (...) -> bool
    return view.settings().get('__vi_external_disable', False)


# Useful for third party plugins to disable vim emulation for specific views.
# Differs from is_ignored() in that only keys should be disabled.
def is_ignored_but_command_mode(view):
    # type: (...) -> bool
    return view.settings().get('__vi_external_disable_keys', False)


def is_widget(view):
    # type: (...) -> bool
    get = view.settings().get

    return get('is_widget') or get('is_vintageous_widget')


def is_console(view):
    # type: (...) -> bool
    # TODO [review] Is this reliable?
    return (getattr(view, 'settings') is None)


def is_view(view):
    # type: (...) -> bool
    return not any((
        is_widget(view),
        is_console(view),
        is_ignored(view),
        is_ignored_but_command_mode(view)
    ))


def _regions_transformer(sels, view, f, with_idx):
    # type: (...) -> None
    new = []
    for idx, sel in enumerate(sels):
        if with_idx:
            regions = f(view, sel, idx)
        else:
            regions = f(view, sel)

        if isinstance(regions, Region):
            new.append(regions)
        elif isinstance(regions, list):
            for region in regions:
                if not isinstance(region, Region):
                    raise TypeError('region or array of region required')
                new.append(region)
        else:
            raise TypeError('region or array of region required')

    view.sel().clear()
    view.sel().add_all(new)


def regions_transformer(view, f):
    # type: (...) -> None
    _regions_transformer(list(view.sel()), view, f, False)


def regions_transformer_indexed(view, f):
    # type: (...) -> None
    _regions_transformer(list(view.sel()), view, f, True)


def regions_transformer_reversed(view, f):
    # type: (...) -> None
    _regions_transformer(reversed(list(view.sel())), view, f, False)


def replace_sel(view, new_sel):
    # type: (...) -> None
    if new_sel is None or new_sel == []:
        raise ValueError('no new_sel')

    view.sel().clear()
    if isinstance(new_sel, list):
        view.sel().add_all(new_sel)
        return

    view.sel().add(new_sel)


def get_insertion_point_at_b(region):
    # type: (Region) -> int
    if region.a < region.b:
        return region.b - 1

    return region.b


def get_insertion_point_at_a(region):
    # type: (Region) -> int
    if region.b < region.a:
        return region.a - 1

    return region.a


# Save selection, but only if it's not empty.
def save_previous_selection(view, mode):
    # type: (...) -> None
    if view.has_non_empty_selection_region():
        view.add_regions('visual_sel', list(view.sel()))
        view.settings().set('_nv_visual_sel_mode', mode)


def get_previous_selection(view):
    # type: (...) -> tuple
    return (view.get_regions('visual_sel'), view.settings().get('_nv_visual_sel_mode'))


def show_if_not_visible(view):
    # type: (...) -> None
    if view.sel():
        pt = view.sel()[0].b
        if not view.visible_region().contains(pt):
            view.show(pt)


# Create a region that includes the char at a or b depending on orientation.
def new_inclusive_region(a, b):
    # type: (int, int) -> Region
    if a <= b:
        return Region(a, b + 1)
    else:
        return Region(a + 1, b)


def row_at(view, pt):
    # type: (...) -> int
    return view.rowcol(pt)[0]


def col_at(view, pt):
    # type: (...) -> int
    return view.rowcol(pt)[1]


def row_to_pt(view, row, col=0):
    # type: (...) -> int
    return view.text_point(row, col)


def next_non_blank(view, pt):
    # type: (...) -> int
    limit = view.size()
    substr = view.substr
    while (substr(pt) in '\t ') and (pt <= limit):
        pt += 1

    return pt


def prev_non_blank(view, pt):
    # type: (...) -> int
    substr = view.substr
    while substr(pt) in '\t ' and pt > 0:
        pt -= 1

    return pt


def prev_blank(view, pt):
    # type: (...) -> int
    substr = view.substr
    while pt >= 0 and substr(pt) not in '\t ':
        pt -= 1

    return pt


def prev_non_nl(view, pt):
    # type: (...) -> int
    substr = view.substr
    while substr(pt) in '\n' and pt > 0:
        pt -= 1

    return pt


def prev_non_ws(view, pt):
    # type: (...) -> int
    substr = view.substr
    while substr(pt) in ' \t\n' and pt > 0:
        pt -= 1

    return pt


def is_at_eol(view, reg):
    # type: (...) -> bool
    return view.line(reg.b).b == reg.b


def is_at_bol(view, reg):
    # type: (...) -> bool
    return view.line(reg.b).a == reg.b


def first_row(view):
    # type: (...) -> int
    return view.rowcol(0)[0]


def last_row(view):
    # type: (...) -> int
    return view.rowcol(view.size())[0]


# Used, for example, by commands like f{char} and t{char}.
_tranlsate_char_map = {
    '<bar>': '|',
    '<bslash>': '\\',
    '<cr>': '\n',
    '<enter>': '\n',
    '<lt>': '<',
    '<sp>': ' ',
    '<space>': ' ',
    '<tab>': '\t',
}


def translate_char(char):
    # type: (str) -> str
    lchar = char.lower()

    if lchar in _tranlsate_char_map:
        return _tranlsate_char_map[lchar]

    return char


@contextmanager
def gluing_undo_groups(view, state):
    state.processing_notation = True
    view.run_command('mark_undo_groups_for_gluing')

    yield

    view.run_command('glue_marked_undo_groups')
    state.processing_notation = False


@contextmanager
def adding_regions(view, name, regions, scope_name):
    view.add_regions(name, regions, scope_name)

    yield

    view.erase_regions(name)
