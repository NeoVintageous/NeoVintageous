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
# Initially based on https://github.com/guillermooo/Vintageous_Plugin_Surround.

import re

from sublime import LITERAL
from sublime import Region
from sublime_plugin import TextCommand

from NeoVintageous.nv.plugin import INPUT_AFTER_MOTION
from NeoVintageous.nv.plugin import INPUT_IMMEDIATE
from NeoVintageous.nv.plugin import inputs
from NeoVintageous.nv.plugin import INTERNAL_NORMAL
from NeoVintageous.nv.plugin import NORMAL
from NeoVintageous.nv.plugin import OPERATOR_PENDING
from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.plugin import ViOperatorDef
from NeoVintageous.nv.plugin import VISUAL
from NeoVintageous.nv.plugin import VISUAL_BLOCK
from NeoVintageous.nv.vi.core import ViTextCommandBase
from NeoVintageous.nv.vi.search import reverse_search
from NeoVintageous.nv.vi.utils import translate_char
from NeoVintageous.nv.vim import enter_normal_mode


__all__ = [
    '_nv_surround_command',
    '_nv_surround_ys_command'
]


@register(seq='ys', modes=(NORMAL,))
class _surround_ys(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.motion_required = True
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_AFTER_MOTION
        )

    @property
    def accept_input(self):
        single = len(self.inp) == 1 and self.inp != '<'
        tag = re.match('<.*?>', self.inp)
        return not(single or tag)

    def accept(self, key):
        self.inp += translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': '_nv_surround_ys',
            'action_args': {
                'mode': state.mode,
                'surround_with': self.inp
            }
        }


@register(seq='yss', modes=(NORMAL,))
class _surround_yss(_surround_ys):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motion_required = False
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_IMMEDIATE
        )

    def translate(self, state):
        return {
            'action': '_nv_surround_ys',
            'action_args': {
                'mode': state.mode,
                'surround_with': self.inp,
                'motion': {
                    'motion': '_vi_select_text_object',
                    'motion_args': {
                        'mode': INTERNAL_NORMAL,
                        'count': 1,
                        'inclusive': False,
                        'text_object': 'l'
                    }
                }
            }
        }


@register(seq='S', modes=(VISUAL, VISUAL_BLOCK))
class _surround_S(_surround_ys):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motion_required = False
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_IMMEDIATE
        )


@register(seq='ds', modes=(NORMAL, OPERATOR_PENDING))
class _surround_ds(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_IMMEDIATE
        )

    # TODO Fix ds should not accept input
    @property
    def accept_input(self):
        single = len(self.inp) == 1
        tag = re.match('<.*?>', self.inp)

        return not(single or tag)

    def accept(self, key):
        self.inp += translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': '_nv_surround',
            'action_args': {
                'action': 'ds',
                'mode': state.mode,
                'target': self.inp
            }
        }


@register(seq='cs', modes=(NORMAL, OPERATOR_PENDING))
class _surround_cs(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_IMMEDIATE
        )

    @property
    def accept_input(self):
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

    def accept(self, key):
        self.inp += translate_char(key)

        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': '_nv_surround',
            'action_args': {
                'action': 'cs',
                'mode': state.mode,
                'target': self.inp[0],
                'replacement': self.inp[1:]
            }
        }


def _rsynced_regions_transformer(view, f):
    sels = reversed(list(view.sel()))
    view_sel = view.sel()
    for sel in sels:
        view_sel.subtract(sel)

        new_sel = f(view, sel)
        if not isinstance(new_sel, Region):
            raise TypeError('sublime.Region required')

        view_sel.add(new_sel)


class _nv_surround_command(TextCommand):
    def run(self, edit, **kwargs):
        action = kwargs.get('action')
        if action == 'cs':
            _do_surround_cs(self.view, edit, kwargs.get('target'), kwargs.get('replacement'), kwargs.get('mode'))
        elif action == 'ds':
            _do_surround_ds(self.view, edit, kwargs.get('target'), kwargs.get('mode'))
        else:
            raise Exception('unknown action')


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


def _resolve_punctuation_aliases(target):
    return _PUNCTUTION_MARK_ALIASES.get(target, target)


# Eight punctuation marks, (, ), {, }, [, ], <, and >, represent themselves and
# their counterparts. The targets b, B, r, and a are aliases for ), }, ], and >
# (the first two mirror Vim; the second two are completely arbitrary and subject
# to change).
def _get_punctuation_marks(target):
    target = _resolve_punctuation_aliases(target)

    return _PUNCTUATION_MARKS.get(target, (target, target))


# If either ), }, ], or > is used, the text is wrapped in the appropriate pair
# of characters. Similar behavior can be found with (, {, and [ (but not <),
# which append an additional space to the inside. Like with the targets above,
# b, B, r, and a are aliases for ), }, ], and >.
def _get_punctuation_mark_replacements(target):
    target = _resolve_punctuation_aliases(target)
    append_addition_space = True if target in '({[' else False
    begin, end = _get_punctuation_marks(target)
    if append_addition_space:
        begin = begin + ' '
        end = ' ' + end

    return (begin, end)


# TODO [refactor] to use _nv_surround proxy command
class _nv_surround_ys_command(ViTextCommandBase):

    def run(self, edit, mode=None, surround_with='"', count=1, motion=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                self.surround(edit, s, surround_with)
                return Region(s.begin())
            elif mode in (VISUAL, VISUAL_BLOCK):
                self.surround(edit, s, surround_with)
                return Region(s.begin())

            return s

        if not motion and not self.view.has_non_empty_selection_region():
            enter_normal_mode(self.view, mode)
            raise ValueError('motion required')

        if mode == INTERNAL_NORMAL:
            self.view.run_command(motion['motion'], motion['motion_args'])

        if surround_with:
            _rsynced_regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)

    def surround(self, edit, s, surround_with):
        open_, close_ = _get_punctuation_mark_replacements(surround_with)

        # Takes <q class="foo"> and produces: <q class="foo">text</q>
        if open_.startswith('<'):
            name = open_[1:].strip()[:-1].strip()
            name = name.split(' ', 1)[0]
            self.view.insert(edit, s.b, "</{0}>".format(name))
            self.view.insert(edit, s.a, surround_with)
            return

        self.view.insert(edit, s.end(), close_)
        self.view.insert(edit, s.begin(), open_)


def _find(view, sub, start, flags=0):
    # TODO Implement end param.
    # TODO Make start and end optional arguments interpreted as in slice notation.
    # TODO [refactor] into reusable api.
    return view.find(sub, start, flags)


def _rfind(view, sub, start, end, flags=0):
    # TODO Make start and end optional arguments interpreted as in slice notation.
    # TODO [refactor] into reusable api.
    res = reverse_search(view, sub, start, end, flags)
    if res is None:
        return Region(-1)

    return res


# TODO Add punctuation aliases
def _do_surround_cs(view, edit, target, replacement, mode=None):
    # Targets are always one character.
    if len(target) != 1:
        # TODO [review] should an exception be raised, and if yes, what type of exception e.g. package, module, plugin, generic?  # noqa: E501
        return

    # Replacements must be one character long, except for tags which must be at
    # least three character long.
    if len(replacement) >= 3:
        if replacement[0] not in ('t', '<') or not replacement.endswith('>'):
            return  # TODO [review] should an exception be raised, and if yes, what type of exception e.g. package, module, plugin, generic?  # noqa: E501
    elif len(replacement) != 1:
        return  # TODO [review] should an exception be raised, and if yes, what type of exception e.g. package, module, plugin, generic?  # noqa: E501

    def _f(view, s):
        if mode == INTERNAL_NORMAL:
            old = target
            new = replacement
            open_, close_ = _get_punctuation_marks(old)
            new_open, new_close = _get_punctuation_mark_replacements(new)

            # Replacements > 1 are always tags, and the first character could be
            # "t", which is an alias for "<".
            if len(replacement) > 1:
                new_open = '<' + new_open[1:]

            # Replacements > 1 are always tags, and the first character could be
            # "t", which is an alias for "<".
            if len(replacement) > 1:
                new_close = '</' + new_close[1:]

            if open_ == 't':
                open_, close_ = ('<[^>\\/]+>', '<\\/[^>]+>')
                next_ = view.find(close_, s.b)
                if next_:
                    prev_ = reverse_search(view, open_, end=next_.begin(), start=0)
                else:
                    prev_ = None
            else:
                next_ = view.find(close_, s.b, flags=LITERAL)
                if next_:
                    prev_ = reverse_search(view, open_, end=s.b, start=0, flags=LITERAL)
                else:
                    next_ = None

            if not (next_ and prev_):
                return s

            view.replace(edit, next_, new_close)
            view.replace(edit, prev_, new_open)

            return Region(prev_.begin())

        return s

    if target and replacement:
        _rsynced_regions_transformer(view, _f)


def _do_surround_ds(view, edit, target, mode=None):
    def _f(view, s):
        if mode == INTERNAL_NORMAL:
            if len(target) != 1:
                return s  # TODO [review] should an exception be raised, and if yes, what type of exception e.g. package, module, plugin, generic?  # noqa: E501

            # The *target* letters w, W, s, and p correspond to a |word|, a
            # |WORD|, a |sentence|, and a |paragraph| respectively.  These are
            # special in that they have nothing to delete, and used with |ds| they
            # are a no-op. With |cs|, one could consider them a slight shortcut for
            # ysi (cswb == ysiwb, more or less).

            noop = 'wWsp'
            if target in noop:
                return s  # TODO [review] should a message be displayed or logged e.g. status, console?

            valid_targets = '\'"`b()B{}r[]a<>t.,-_;:@#~*\\/'
            if target not in valid_targets:
                return s  # TODO [review] should an exception be raised, or message displayed or logged e.g. status console?  # noqa: E501

            # All marks, except punctuation marks, are only searched for on the
            # current line.

            # If opening punctuation mark is used, contained whitespace is also trimmed.
            trim_contained_whitespace = True if target in '({[<' else False
            search_current_line_only = False if target in 'b()B{}r[]a<>' else True

            # Expand targets into begin and end variables because punctuation marks
            # and their aliases represent themselves and their counterparts e.g. (),
            # []. Target is the same for begin and end for all other valid marks
            # e.g. ', ", `, -, _, etc.

            t_char_begin, t_char_end = _get_punctuation_marks(target)

            s_rowcol_begin = view.rowcol(s.begin())
            s_rowcol_end = view.rowcol(s.end())

            # A t is a pair of HTML or XML tags.
            if target == 't':
                # TODO test dst works when cursor position is inside tag begin <a|bc>x</abc> -> dst -> |x
                # TODO test dst works when cursor position is inside tag end   <abc>x</a|bc> -> dst -> |x
                t_region_end = view.find('<\\/.*?>', s.b)
                t_region_begin = reverse_search(view, '<.*?>', start=0, end=s.b)
            else:
                current = view.substr(s.begin())
                # TODO test ds{char} works when cursor position is on target begin |"x" -> ds" -> |x
                # TODO test ds{char} works when cursor position is on target end   "x|" -> ds" -> |x

                if current == t_char_begin:
                    t_region_begin = Region(s.begin(), s.begin() + 1)
                else:
                    t_region_begin = _rfind(view, t_char_begin, start=0, end=s.begin(), flags=LITERAL)

                t_region_begin_rowcol = view.rowcol(t_region_begin.begin())

                t_region_end = _find(view, t_char_end, start=t_region_begin.end(), flags=LITERAL)
                t_region_end_rowcol = view.rowcol(t_region_end.end())

                if search_current_line_only:
                    if t_region_begin_rowcol[0] != s_rowcol_begin[0]:
                        return s

                    if t_region_end_rowcol[0] != s_rowcol_end[0]:
                        return s

                if trim_contained_whitespace:
                    t_region_begin_ws = _find(view, '\\s*.', start=t_region_begin.end())
                    t_region_end_ws = _rfind(view, '.\\s*', start=t_region_begin.end(), end=t_region_end.begin())

                    if t_region_begin_ws.size() > 1:
                        t_region_begin = Region(t_region_begin.begin(), t_region_begin_ws.end() - 1)

                    if t_region_end_ws.size() > 1:
                        t_region_end = Region(t_region_end_ws.begin() + 1, t_region_end.end())

            # Note: Be careful using boolean evaluation on a Region because an empty
            # Region evaluates to False. It evaluates to False because Region
            # invokes `__len__()` which will be zero if the Region is empty e.g.
            # `Region(3).size()` is `0`, whereas `Region(3, 4).size()` is `1`.
            # `sublime.View.find(sub)` returns `Region(-1)` if *sub* not found. This
            # is similar to how the python `str.find(sub)` function works i.e. it
            # returns `-1` if *sub* not found, because *sub* could be found at
            # position `0`. To check if a Region was found use `Region(3) >= 0`. To
            # check if a Region is non empty you can use boolean evaluation i.e. `if
            # Region(3): ...`. In the following case boolean evaluation is
            # intentional.

            if not (t_region_end and t_region_begin):
                return s

            # It's important that the end is replaced first. If we replaced the
            # begin region first then the end replacement would be off-by-one
            # because the begin is reducing the size of the internal buffer by one
            # i.e. it's deleting a character.

            view.replace(edit, t_region_end, '')
            view.replace(edit, t_region_begin, '')

            return Region(t_region_begin.begin())

        return s

    if target:
        _rsynced_regions_transformer(view, _f)
