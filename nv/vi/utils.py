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


def is_ignored(view):
    # type: (...) -> bool

    # Useful for external plugins to disable NeoVintageous for specific views.

    return view.settings().get('__vi_external_disable', False)


def is_ignored_but_command_mode(view):
    # type: (...) -> bool

    # Useful for third party plugins to disable vim emulation for specific
    # views. Differs from is_ignored() in that only keys should be disabled.

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
    sels = list(view.sel())
    _regions_transformer(sels, view, f, False)

def regions_transformer_indexed(view, f):
    # type: (...) -> None
    sels = list(view.sel())
    _regions_transformer(sels, view, f, True)

# TODO: test existin uses of this function to make sure the refactor works correctly
def regions_transformer_reversed(view, f):
    # type: (...) -> None
    sels = reversed(list(view.sel()))
    _regions_transformer(sels, view, f, False)


def resolve_insertion_point_at_b(region):
    # type: (Region) -> int

    # Return the insertion point closest to region.b for a visual region. For
    # non-visual regions, the insertion point is always any of the region's
    # ends, so using this function is pointless.

    if region.a < region.b:
        return (region.b - 1)

    return region.b


def resolve_insertion_point_at_a(region):
    # type: (Region) -> int

    # Return the actual insertion point closest to region.a for a visual region.
    # For non-visual regions, the insertion point is always any of the region's
    # ends, so using this function is pointless.

    if region.size() == 0:
        raise TypeError('not a visual region')

    if region.a < region.b:
        return region.a
    elif region.b < region.a:
        return region.a - 1


# TODO [review] this function looks unused; it was refactored from an obsolete module.
@contextmanager
def restoring_sels(view):
    old_sels = list(view.sel())
    yield
    view.sel().clear()
    for s in old_sels:

        # TODO [review] Race-condition? If the buffer has changed in the
        # meantime, this won't work well.

        view.sel().add(s)


def show_if_not_visible(view):
    if view.sel():
        pt = view.sel()[0].b
        if not view.visible_region().contains(pt):
            view.show(pt)


def new_inclusive_region(a, b):
    # type: (int, int) -> Region

    # Create a region that includes the char at a or b depending on orientation.

    if a <= b:
        return Region(a, b + 1)
    else:
        return Region(a + 1, b)


def row_at(view, pt):
    # type: (...) -> int
    return view.rowcol(pt)[0]


def col_at(view, pt):
    return view.rowcol(pt)[1]


def row_to_pt(view, row, col=0):
    # type: (...) -> int
    return view.text_point(row, col)


@contextmanager
def gluing_undo_groups(view, state):
    state.processing_notation = True
    view.run_command('mark_undo_groups_for_gluing')
    yield
    view.run_command('glue_marked_undo_groups')
    state.processing_notation = False


def next_non_blank(view, pt):
    limit = view.size()
    substr = view.substr
    while (substr(pt) in '\t ') and (pt <= limit):
        pt += 1

    return pt


def next_non_white_space_char(view, pt, white_space='\t '):
    # type: (...) -> int
    limit = view.size()
    substr = view.substr
    while (substr(pt) in white_space) and (pt <= limit):
        pt += 1

    return pt


def previous_non_white_space_char(view, pt, white_space='\t \n'):
    # type: (...) -> int
    substr = view.substr
    while substr(pt) in white_space and pt > 0:
        pt -= 1

    return pt


# TODO [review] DEPRECATED; Refactor and remove.
def previous_white_space_char(view, pt, white_space='\t '):
    # type: (...) -> int
    substr = view.substr
    while pt >= 0 and substr(pt) not in white_space:
        pt -= 1

    return pt


def move_backward_while(view, pt, func):
    # type: (...) -> int
    while (pt >= 0) and func(pt):
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


_tranlsate_char_map = {
    '<enter>': '\n',
    '<cr>': '\n',
    '<sp>': ' ',
    '<space>': ' ',
    '<lt>': '<',
    '<tab>': '\t'
}


def translate_char(char):
    # type: (str) -> str
    lchar = char.lower()

    # TODO [bug] ??? What happens to keys like <home>, <up>, etc? We shouln't be
    # able to use those in some contexts, like as arguments to f, t...

    if lchar in _tranlsate_char_map:
        return _tranlsate_char_map[lchar]

    return char


@contextmanager
def restoring_sel(view):
    regs = list(view.sel())
    view.sel().clear()
    yield
    view.sel().clear()
    view.sel().add_all(regs)


def last_sel(view):
    # type: (...) -> Region
    return get_sel(view, -1)


def second_sel(view):
    # type: (...) -> Region
    return get_sel(view, 1)


def first_sel(view):
    # type: (...) -> Region
    return get_sel(view, 0)


def get_sel(view, i=0):
    # type: (...) -> Region
    return view.sel()[i]


def get_eol(view, pt, inclusive=False):
    # type: (...) -> int
    if not inclusive:
        return view.line(pt).end()

    return view.full_line(pt).end()


def get_bol(view, pt):
    # type: (...) -> int
    return view.line(pt).a


def replace_sel(view, new_sel):
    # type: (...) -> None
    if new_sel is None or new_sel == []:
        raise ValueError('no new_sel')

    view.sel().clear()
    if isinstance(new_sel, list):
        view.sel().add_all(new_sel)
        return

    view.sel().add(new_sel)


def resize_visual_region(r, b):
    # type: (Region, int) -> Region
    # Define a new visual mode region.
    #
    # Args:
    #   r (Region): Existing region.
    #   b (int): New end point.
    #
    # Returns:
    #   Region: Where x.a != x.b (XXX what does this mean?).
    if b < r.a:
        if r.b > r.a:
            return Region(r.a + 1, b)

        return Region(r.a, b)

    if b > r.a:
        if r.b < r.a:
            return Region(r.a - 1, b + 1)

        return Region(r.a, b + 1)

    return Region(b, b + 1)


@contextmanager
def adding_regions(view, name, regions, scope_name):
    view.add_regions(name, regions, scope_name)
    yield
    view.erase_regions(name)
