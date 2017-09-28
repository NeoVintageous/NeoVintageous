# Inspired by https://github.com/tpope/vim-surround
# Initially based on https://github.com/guillermooo/Vintageous_Plugin_Surround

import re

from sublime import LITERAL
from sublime import Region
from sublime_plugin import TextCommand

from NeoVintageous.lib.plugin import inputs
from NeoVintageous.lib.plugin import INTERNAL_NORMAL_MODE
from NeoVintageous.lib.plugin import NORMAL_MODE
from NeoVintageous.lib.plugin import OPERATOR_PENDING_MODE
from NeoVintageous.lib.plugin import register
from NeoVintageous.lib.plugin import ViOperatorDef
from NeoVintageous.lib.plugin import VISUAL_BLOCK_MODE
from NeoVintageous.lib.plugin import VISUAL_MODE
from NeoVintageous.lib.vi.core import ViTextCommandBase
from NeoVintageous.lib.vi.inputs import input_types
from NeoVintageous.lib.vi.inputs import parser_def
from NeoVintageous.lib.vi.search import reverse_search
from NeoVintageous.lib.vi.utils import regions_transformer
from NeoVintageous.lib.vi.utils import translate_char


__all__ = [
    '_neovintageous_surround_cs',
    '_neovintageous_surround_ds',
    '_neovintageous_surround_ys'
]


@register(seq='ys', modes=(NORMAL_MODE,))
class _surround_ys(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.motion_required = True
        self.input_parser = parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=input_types.AFTER_MOTION
        )

    @property
    def accept_input(self):
        single = len(self.inp) == 1 and self.inp != '<'
        tag = re.match('<.*?>', self.inp)
        return not(single or tag)

    def accept(self, key):
        self._inp += translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': '_neovintageous_surround_ys',
            'action_args': {
                'mode': state.mode,
                'surround_with': self.inp
            }
        }


@register(seq='S', modes=(VISUAL_MODE, VISUAL_BLOCK_MODE))
class _surround_S(_surround_ys):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motion_required = False
        self.input_parser = parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=input_types.INMEDIATE
        )


@register(seq='ds', modes=(NORMAL_MODE, OPERATOR_PENDING_MODE))
class _surround_ds(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=input_types.INMEDIATE
        )

    # TODO Fix ds should not accept input
    @property
    def accept_input(self):
        single = len(self.inp) == 1
        tag = re.match('<.*?>', self.inp)

        return not(single or tag)

    def accept(self, key):
        self._inp += translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': '_neovintageous_surround_ds',
            'action_args': {
                'mode': state.mode,
                'target': self.inp
            }
        }


@register(seq='cs', modes=(NORMAL_MODE, OPERATOR_PENDING_MODE))
class _surround_cs(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=input_types.INMEDIATE
        )

    @property
    def accept_input(self):
        return len(self.inp) != 2

    def accept(self, key):
        self._inp += translate_char(key)

        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': '_neovintageous_surround_cs',
            'action_args': {
                'mode': state.mode,
                'replace_what': self.inp
            }
        }


def _regions_transformer_reversed(view, f):
    sels = reversed(list(view.sel()))
    new = []
    for sel in sels:
        region = f(view, sel)
        if not isinstance(region, Region):
            raise TypeError('sublime.Region required')
        new.append(region)
    view.sel().clear()
    view.sel().add_all(new)


class _neovintageous_surround_ys(ViTextCommandBase):

    _pairs = {
        ')': ('(', ')'),
        '(': ('( ', ' )'),
        ']': ('[', ']'),
        '[': ('[ ', ' ]'),
        '}': ('{', '}'),
        '{': ('{ ', ' }'),
    }

    def run(self, edit, mode=None, surround_with='"', count=1, motion=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL_MODE:
                self.surround(edit, s, surround_with)
                return Region(s.begin())
            elif mode in (VISUAL_MODE, VISUAL_BLOCK_MODE):
                self.surround(edit, s, surround_with)
                return Region(s.begin())

            return s

        if not motion and not self.view.has_non_empty_selection_region():
            self.enter_normal_mode(mode)
            raise ValueError('motion required')

        if mode == INTERNAL_NORMAL_MODE:
            self.view.run_command(motion['motion'], motion['motion_args'])

        if surround_with:
            _regions_transformer_reversed(self.view, f)

        self.enter_normal_mode(mode)

    def surround(self, edit, s, surround_with):
        open_, close_ = self._pairs.get(surround_with, (surround_with, surround_with))

        # Takes <q class="foo"> and produces: <q class="foo">text</q>
        if open_.startswith('<'):
            name = open_[1:].strip()[:-1].strip()
            name = name.split(' ', 1)[0]
            self.view.insert(edit, s.b, "</{0}>".format(name))
            self.view.insert(edit, s.a, surround_with)
            return

        self.view.insert(edit, s.end(), close_)
        self.view.insert(edit, s.begin(), open_)


# TODO Fix cst<x> <div>x</div> -> cst<p> |<p>x</p>
# TODO Add punctuation aliases
class _neovintageous_surround_cs(TextCommand):
    def run(self, edit, mode=None, replace_what=''):
        def f(view, s):
            if mode == INTERNAL_NORMAL_MODE:
                return self._replace(edit, s, replace_what)

            return s

        if replace_what:
            regions_transformer(self.view, f)

    def _replace(self, edit, s, replace_what):
        if len(replace_what) != 2:
            # TODO REVIEW replace single argument with two: *target* and *replacement*
            # TODO REVIEW should an exception be raised, and if yes, what type of exception e.g. package, module, plugin, generic?  # noqa: E501
            return s

        target_pairs = {
            ')': ('(', ')'),
            '(': ('(', ')'),
            ']': ('[', ']'),
            '[': ('[', ']'),
            '}': ('{', '}'),
            '{': ('{', '}'),
            '>': ('<', '>'),
        }

        replacement_pairs = {
            ')': ('(', ')'),
            '(': ('( ', ' )'),
            ']': ('[', ']'),
            '[': ('[ ', ' ]'),
            '}': ('{', '}'),
            '{': ('{ ', ' }'),
            '>': ('<', '>'),
        }

        old, new = tuple(replace_what)
        open_, close_ = target_pairs.get(old, (old, old))
        new_open, new_close = replacement_pairs.get(new, (new, new))

        if len(open_) == 1 and open_ == 't':
            open_, close_ = ('<.*?>', '</.*?>')
            next_ = self.view.find(close_, s.b)
            prev_ = reverse_search(self.view, open_, end=s.b, start=0)
        else:
            # brute force
            next_ = self.view.find(close_, s.b, flags=LITERAL)
            prev_ = reverse_search(self.view, open_, end=s.b, start=0, flags=LITERAL)

        if not (next_ and prev_):
            return s

        self.view.replace(edit, next_, new_close)
        self.view.replace(edit, prev_, new_open)

        return Region(prev_.begin())


def _find(view, sub, start, flags=0):
    # TODO Implement end param.
    # TODO Make start and end optional arguments interpreted as in slice notation.
    # TODO Refactor into reusable api.
    return view.find(sub, start, flags)


def _rfind(view, sub, start, end, flags=0):
    # TODO Make start and end optional arguments interpreted as in slice notation.
    # TODO Refactor into reusable api.
    res = reverse_search(view, sub, start, end, flags)
    if res is None:
        return Region(-1)

    return res


class _neovintageous_surround_ds(TextCommand):

    def run(self, edit, mode=None, target=''):

        def f(view, s):
            if mode == INTERNAL_NORMAL_MODE:
                return self._replace(edit, s, target)
            return s

        if target:
            regions_transformer(self.view, f)

    def _replace(self, edit, s, target):
        if len(target) != 1:
            # TODO REVIEW should an exception be raised, and if yes, what type of exception e.g. package, module, plugin, generic?  # noqa: E501
            return s

        # The *target* letters w, W, s, and p correspond to a |word|, a
        # |WORD|, a |sentence|, and a |paragraph| respectively.  These are
        # special in that they have nothing to delete, and used with |ds| they
        # are a no-op. With |cs|, one could consider them a slight shortcut for
        # ysi (cswb == ysiwb, more or less).

        noop = 'wWsp'
        if target in noop:
            # TODO REVIEW should a message be displayed or logged e.g. status, console?
            return s

        valid_targets = '\'"`b()B{}r[]a<>t.,-_'
        if target not in valid_targets:
            # TODO REVIEW should an exception be raised, or message displayed or logged e.g. status console?
            return s

        # Three quote marks are only searched for on the current line.
        # quote_marks = '\'"`'

        # punctuation_mark_aliases = 'bBra'

        # All marks, except punctuation marks, are only searched for on the
        # current line.

        # Eight punctuation marks, (, ), {, }, [, ], <, and >, represent
        # themselves and their counterparts. The targets b, B, r, and a are
        # aliases for ), }, ], and > (the first two mirror Vim; the second two
        # are completely arbitrary and subject to change).

        punctuation_marks = {
            '(': ('(', ')'),
            ')': ('(', ')'),
            'b': ('(', ')'),  # alias of )
            '{': ('{', '}'),
            '}': ('{', '}'),
            'B': ('{', '}'),  # alias of }
            '[': ('[', ']'),
            ']': ('[', ']'),
            'r': ('[', ']'),  # alias of ]
            '<': ('<', '>'),
            '>': ('<', '>'),
            'a': ('<', '>'),  # alias of >
        }

        # If opening punctuation mark is used, contained whitespace is also trimmed.
        trim_contained_whitespace = True if target in '({[<' else False
        search_current_line_only = False if target in 'b()B{}r[]a<>' else True

        # Expand targets into begin and end variables because punctuation marks
        # and their aliases represent themselves and their counterparts e.g. (),
        # []. Target is the same for begin and end for all other valid marks
        # e.g. ', ", `, -, _, etc.

        t_char_begin, t_char_end = punctuation_marks.get(target, (target, target))

        s_rowcol_begin = self.view.rowcol(s.begin())
        s_rowcol_end = self.view.rowcol(s.end())

        # A t is a pair of HTML or XML tags.
        if target == 't':
            # TODO test dst works when cursor position is inside tag begin <a|bc>x</abc> -> dst -> |x
            # TODO test dst works when cursor position is inside tag end   <abc>x</a|bc> -> dst -> |x
            t_region_end = self.view.find('<\\/.*?>', s.b)
            t_region_begin = reverse_search(self.view, '<.*?>', start=0, end=s.b)
        else:
            current = self.view.substr(s.begin())
            # TODO test ds{char} works when cursor position is on target begin |"x" -> ds" -> |x
            # TODO test ds{char} works when cursor position is on target end   "x|" -> ds" -> |x

            if current == t_char_begin:
                t_region_begin = Region(s.begin(), s.begin() + 1)
            else:
                t_region_begin = _rfind(self.view, t_char_begin, start=0, end=s.begin(), flags=LITERAL)

            t_region_begin_rowcol = self.view.rowcol(t_region_begin.begin())

            t_region_end = _find(self.view, t_char_end, start=t_region_begin.end(), flags=LITERAL)
            t_region_end_rowcol = self.view.rowcol(t_region_end.end())

            if search_current_line_only:
                if t_region_begin_rowcol[0] != s_rowcol_begin[0]:
                    return s

                if t_region_end_rowcol[0] != s_rowcol_end[0]:
                    return s

            if trim_contained_whitespace:
                t_region_begin_ws = _find(self.view, '\\s*.', start=t_region_begin.end())
                t_region_end_ws = _rfind(self.view, '.\\s*', start=t_region_begin.end(), end=t_region_end.begin())

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

        self.view.replace(edit, t_region_end, '')
        self.view.replace(edit, t_region_begin, '')

        return Region(t_region_begin.begin())
