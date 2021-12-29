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

# A port of https://github.com/tpope/vim-surround.

import re

from sublime import Region
from sublime_plugin import TextCommand

from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.polyfill import view_find
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.utils import InputParser
from NeoVintageous.nv.utils import translate_char
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.search import reverse_search
from NeoVintageous.nv.vi.text_objects import get_text_object_region
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import run_motion


__all__ = [
    'nv_surround_command'
]


@register(seqs.YS, (NORMAL,))
class Surroundys(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.motion_required = True
        self.input_parser = InputParser(InputParser.AFTER_MOTION)

    @property
    def accept_input(self) -> bool:
        single = len(self.inp) == 1 and self.inp != '<'
        tag = re.match('<.*?>', self.inp)

        return not (single or tag)

    def accept(self, key: str) -> bool:
        self.inp += translate_char(key)

        return True

    def translate(self, view):
        return {
            'action': 'nv_surround',
            'action_args': {
                'action': 'ys',
                'mode': get_mode(view),
                'replacement': self.inp
            }
        }


@register(seqs.YSS, (NORMAL,))
class Surroundyss(Surroundys):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motion_required = False
        self.input_parser = InputParser(InputParser.IMMEDIATE)

    def translate(self, view):
        return {
            'action': 'nv_surround',
            'action_args': {
                'action': 'ys',
                'mode': get_mode(view),
                'motion': {
                    'motion': 'nv_vi_select_text_object',
                    'motion_args': {
                        'mode': INTERNAL_NORMAL,
                        'count': 1,
                        'inclusive': False,
                        'text_object': 'l'
                    }
                },
                'replacement': self.inp
            }
        }


@register(seqs.BIG_S, (VISUAL, VISUAL_BLOCK))
class SurroundS(Surroundys):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motion_required = False
        self.input_parser = InputParser(InputParser.IMMEDIATE)


@register(seqs.DS, (NORMAL, OPERATOR_PENDING))
class Surroundds(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = InputParser(InputParser.IMMEDIATE)

    # TODO Fix ds should not accept input
    @property
    def accept_input(self) -> bool:
        single = len(self.inp) == 1
        tag = re.match('<.*?>', self.inp)

        return not (single or tag)

    def accept(self, key: str) -> bool:
        self.inp += translate_char(key)

        return True

    def translate(self, view):
        return {
            'action': 'nv_surround',
            'action_args': {
                'action': 'ds',
                'mode': get_mode(view),
                'target': self.inp
            }
        }


@register(seqs.CS, (NORMAL, OPERATOR_PENDING))
class Surroundcs(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = InputParser(InputParser.IMMEDIATE)

    @property
    def accept_input(self) -> bool:
        # Requires at least two characters (target and replacement).

        # A tag replacement is indicated by "<" ("t" is an alias for "<"). Tag
        # replacements can accept more than one character. A tag name is
        # terminated by ">".

        if len(self.inp) > 1 and self.inp[1] in ('t', '<'):
            # Guard against runaway input collecting.
            if len(self.inp) > 20:
                return False

            # Terminates input collecting for tag.
            return not self.inp.endswith('>')

        return len(self.inp) < 2

    def accept(self, key: str) -> bool:
        self.inp += translate_char(key)

        return True

    def translate(self, view):
        return {
            'action': 'nv_surround',
            'action_args': {
                'action': 'cs',
                'mode': get_mode(view),
                'target': self.inp[0],
                'replacement': self.inp[1:]
            }
        }


class nv_surround_command(TextCommand):
    def run(self, edit, action, **kwargs):
        if action == 'cs':
            _do_cs(self.view, edit, **kwargs)
        elif action == 'ds':
            _do_ds(self.view, edit, **kwargs)
        elif action == 'ys':
            _do_ys(self.view, edit, **kwargs)


_PUNCTUATION_MARKS = {
    '(': ('(', ')'),
    ')': ('(', ')'),
    '{': ('{', '}'),
    '}': ('{', '}'),
    '[': ('[', ']'),
    ']': ('[', ']'),
    '<': ('<', '>'),
    '>': ('<', '>'),
}


_PUNCTUTION_MARK_ALIASES = {
    'b': ')',
    'B': '}',
    'r': ']',
    'a': '>',
}


# Expand target punctuation marks. Eight punctuation marks, (, ), {, }, [, ], <,
# and >, represent themselves and their counterparts. The targets b, B, r, and
# a are aliases for ), }, ], and > (the first two mirror Vim; the second two
# are completely arbitrary and subject to change). Some marks and their
# counterparts are the same for example quote marks: ', ", `.
def _expand_targets(target: str) -> tuple:
    target = _resolve_target_aliases(target)

    return _PUNCTUATION_MARKS.get(target, (target, target))


def _resolve_target_aliases(target: str) -> str:
    return _PUNCTUTION_MARK_ALIASES.get(target, target)


# If either ), }, ], or > is used, the text is wrapped in the appropriate pair
# of characters. Similar behavior can be found with (, {, and [ (but not <),
# which append an additional space to the inside. Like with the targets above,
# b, B, r, and a are aliases for ), }, ], and >.
def _expand_replacements(target: str) -> tuple:
    if target[0] in ('t', '<') and len(target) >= 3:
        # Attributes are stripped in the closing tag. The first character if
        # "t", which is an alias for "<", is replaced too.
        return ('<' + target[1:], '</' + target[1:].strip()[:-1].strip().split(' ', 1)[0] + '>')

    target = _resolve_target_aliases(target)
    append_addition_space = True if target in '({[' else False
    begin, end = _expand_targets(target)
    if append_addition_space:
        begin = begin + ' '
        end = ' ' + end

    return (begin, end)


def _rsynced_regions_transformer(view, f) -> None:
    sels = reversed(list(view.sel()))
    view_sel = view.sel()
    for sel in sels:
        view_sel.subtract(sel)

        new_sel = f(view, sel)
        if not isinstance(new_sel, Region):
            raise TypeError('sublime.Region required')

        view_sel.add(new_sel)


def _do_cs(view, edit, mode: str, target: str, replacement: str) -> None:
    if not target and replacement:
        return

    if len(target) != 1:
        return

    # Replacements must be 1 character long or at least 3 characters for tags.
    if len(replacement) >= 3:
        if replacement[0] not in ('t', '<') or not replacement.endswith('>'):
            return
    elif len(replacement) != 1:
        return

    # Targets.
    target_open, target_close = _expand_targets(target)

    # Replacements
    replacement_open, replacement_close = _expand_replacements(replacement)

    def _f(view, s):
        if mode == INTERNAL_NORMAL:
            if target == 't':
                target_tag_open, target_tag_close = ('<[^>\\/]+>', '<\\/[^>]+>')
                region_begin = None
                region_end = view.find(target_tag_close, s.b)
                if region_end:
                    region_begin = reverse_search(view, target_tag_open, end=region_end.begin(), start=0)
            else:
                region_begin, region_end = _get_regions_for_target(view, s, target_open)

            if not (region_end and region_begin):
                return s

            # It's important that the regions are replaced in reverse because
            # otherwise the buffer size would be reduced by the number of
            # characters replaced and would result in an off-by-n bugs.
            view.replace(edit, region_end, replacement_close)
            view.replace(edit, region_begin, replacement_open)

            return Region(region_begin.begin())

        return s

    _rsynced_regions_transformer(view, _f)


def _do_ds(view, edit, mode: str, target: str) -> None:
    if not target:
        return

    if len(target) != 1:
        return

    # The target letters w, W, s, and p correspond to a word, a WORD, a
    # sentence, and a paragraph respectively. These are special in that they
    # have nothing to delete, and used with ds they are a no-op.
    noop_targets = 'wWsp'
    if target in noop_targets:
        return

    # Includes targets for plugin https://github.com/wellle/targets.vim
    valid_targets = '\'"`b()B{}r[]a<>t.,-_;:@#~*\\/|+=&$'
    if target not in valid_targets:
        return

    # Trim contained whitespace for opening punctuation mark targets.
    should_trim_contained_whitespace = True if target in '({[<' else False

    # Targets.
    target_open, target_close = _expand_targets(target)

    def _f(view, s):
        if mode == INTERNAL_NORMAL:
            # A t is a pair of HTML or XML tags.
            if target == 't':
                # TODO test dst works when cursor position is inside tag begin <a|bc>x</abc> -> dst -> |x
                # TODO test dst works when cursor position is inside tag end   <abc>x</a|bc> -> dst -> |x
                region_end = view.find('<\\/.*?>', s.b)
                region_begin = reverse_search(view, '<.*?>', start=0, end=s.b)
            else:
                region_begin, region_end = _get_regions_for_target(view, s, target_open)
                if should_trim_contained_whitespace and (region_begin and region_end):
                    region_begin, region_end = _trim_regions(view, region_begin, region_end)

            if not (region_begin and region_end):
                return s

            # It's important that the regions are replaced in reverse because
            # otherwise the buffer size would be reduced by the number of
            # characters replaced and would result in an off-by-one bug.
            view.replace(edit, region_end, '')
            view.replace(edit, region_begin, '')

            return Region(region_begin.begin())

        return s

    _rsynced_regions_transformer(view, _f)


def _get_regions_for_target(view, s: Region, target: str) -> tuple:
    text_object = get_text_object_region(view, s, target, inclusive=True)
    if not text_object:
        return (None, None)

    begin = Region(text_object.begin(), text_object.begin() + 1)
    end = Region(text_object.end(), text_object.end() - 1)

    return (begin, end)


def _view_rfind(view, sub: str, start: int, end: int, flags: int = 0):
    match = reverse_search(view, sub, start, end, flags)
    if match is None or match.b == -1:
        return None

    return match


def _trim_regions(view, start: Region, end: Region) -> tuple:
    start_ws = view_find(view, '\\s*.', start_pt=start.end())
    if start_ws and start_ws.size() > 1:
        start = Region(start.begin(), start_ws.end() - 1)

    end_ws = _view_rfind(view, '.\\s*', start=start.end(), end=end.begin())
    if end_ws and end_ws.size() > 1:
        end = Region(end_ws.begin() + 1, end.end())

    return (start, end)


def _do_ys(view, edit, mode: str = None, motion=None, replacement: str = '"', count: int = 1) -> None:
    def _surround(view, edit, s, replacement: str) -> None:
        replacement_open, replacement_close = _expand_replacements(replacement)
        if replacement_open.startswith('<'):
            view.insert(edit, s.b, replacement_close)
            view.insert(edit, s.a, replacement_open)
            return

        view.insert(edit, s.end(), replacement_close)
        view.insert(edit, s.begin(), replacement_open)

    def f(view, s):
        if mode == INTERNAL_NORMAL:
            _surround(view, edit, s, replacement)
            return Region(s.begin())
        elif mode in (VISUAL, VISUAL_BLOCK):
            _surround(view, edit, s, replacement)
            return Region(s.begin())
        return s

    if not motion and not view.has_non_empty_selection_region():
        enter_normal_mode(view, mode)
        raise ValueError('motion required')

    if mode == INTERNAL_NORMAL:
        run_motion(view, motion)

    if replacement:
        _rsynced_regions_transformer(view, f)

    enter_normal_mode(view, mode)
