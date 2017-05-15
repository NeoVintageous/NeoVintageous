# Based on https://github.com/guillermooo/Vintageous_Plugin_Surround
#
# For some reason this has to be at the top level or else the commands don't
# load, I have no idea why, if I figure it out I'll move this into an "extras"
# dir.

import re

import sublime
import sublime_plugin

from NeoVintageous.lib.api import plugin
from NeoVintageous.lib.vi import inputs
from NeoVintageous.lib.vi import utils
from NeoVintageous.lib.vi.cmd_defs import ViOperatorDef
from NeoVintageous.lib.vi.core import ViTextCommandBase
from NeoVintageous.lib.vi.inputs import input_types
from NeoVintageous.lib.vi.inputs import parser_def
from NeoVintageous.lib.vi.search import reverse_search
from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.utils import regions_transformer


__all__ = [
    'nvim_surround_cs',
    'nvim_surround_ds',
    'nvim_surround_ys'
]


@plugin.register(seq='ys', modes=(modes.NORMAL,))
class _nvim_surround_def_ys(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        ViOperatorDef.__init__(self, *args, **kwargs)

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
        self._inp += utils.translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': 'nvim_surround_ys',
            'action_args': {
                'mode': state.mode,
                'surround_with': self.inp
            }
        }


@plugin.register(seq='S', modes=(modes.VISUAL, modes.VISUAL_BLOCK))
class _nvim_surround_def_big_s(_nvim_surround_def_ys):

    def __init__(self, *args, **kwargs):
        _nvim_surround_def_ys.__init__(self, *args, **kwargs)

        self.motion_required = False

        self.input_parser = parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=input_types.INMEDIATE
        )


@plugin.register(seq='ds', modes=(modes.NORMAL, modes.OPERATOR_PENDING))
class _nvim_surround_def_ds(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        ViOperatorDef.__init__(self, *args, **kwargs)

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
        single = len(self.inp) == 1 and self.inp != '<'
        tag = re.match('<.*?>', self.inp)
        return not(single or tag)

    def accept(self, key):
        self._inp += utils.translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': 'nvim_surround_ds',
            'action_args': {
                'mode': state.mode,
                'replace_what': self.inp
            }
        }


@plugin.register(seq='cs', modes=(modes.NORMAL, modes.OPERATOR_PENDING))
class _nvim_surround_def_cs(ViOperatorDef):

    def __init__(self, *args, **kwargs):
        ViOperatorDef.__init__(self, *args, **kwargs)

        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True

        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=input_types.INMEDIATE)

    @property
    def accept_input(self):
        return len(self.inp) != 2

    def accept(self, key):
        self._inp += utils.translate_char(key)
        return True

    def is_enabled(self, state):
        return state.settings.view['vintageous_enable_surround']

    def translate(self, state):
        return {
            'action': 'nvim_surround_cs',
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
        if not isinstance(region, sublime.Region):
            raise TypeError('sublime.Region required')
        new.append(region)
    view.sel().clear()
    view.sel().add_all(new)


_PAIRS_DEFAULT_PLAIN = {
    '(': ('(', ')'),
    ')': ('( ', ' )'),
    '[': ('[', ']'),
    ']': ('[ ', ' ]'),
    '{': ('{', '}'),
    '}': ('{ ', ' }'),
}

_PAIRS_DEFAULT_SPACE = {
    ')': ('(', ')'),
    '(': ('( ', ' )'),
    ']': ('[', ']'),
    '[': ('[ ', ' ]'),
    '}': ('{', '}'),
    '{': ('{ ', ' }'),
}


def _get_surround_pairs(view):
    if view.settings().get("vintageous_surround_spaces", False):
        return _PAIRS_DEFAULT_SPACE
    else:
        return _PAIRS_DEFAULT_PLAIN


class nvim_surround_ys(ViTextCommandBase):

    def run(self, edit, mode=None, surround_with='"', count=1, motion=None):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                self.surround(edit, s, surround_with)
                return sublime.Region(s.begin())
            elif mode in (modes.VISUAL, modes.VISUAL_BLOCK):
                self.surround(edit, s, surround_with)
                return sublime.Region(s.begin())

            return s

        if not motion and not self.view.has_non_empty_selection_region():
            self.enter_normal_mode(mode)
            raise ValueError('motion required')

        if mode == modes.INTERNAL_NORMAL:
            self.view.run_command(motion['motion'], motion['motion_args'])

        if surround_with:
            _regions_transformer_reversed(self.view, f)

        self.enter_normal_mode(mode)

    def surround(self, edit, s, surround_with):
        open_, close_ = _get_surround_pairs(self.view).get(surround_with, (surround_with, surround_with))

        # Takes <q class="foo"> and produces: <q class="foo">text</q>
        if open_.startswith('<'):
            name = open_[1:].strip()[:-1].strip()
            name = name.split(' ', 1)[0]
            self.view.insert(edit, s.b, "</{0}>".format(name))
            self.view.insert(edit, s.a, surround_with)
            return

        self.view.insert(edit, s.end(), close_)
        self.view.insert(edit, s.begin(), open_)


class nvim_surround_cs(sublime_plugin.TextCommand):

    PAIRS = {
        '(': ('(', ')'),
        ')': ('( ', ' )'),
        '[': ('[', ']'),
        ']': ('[ ', ' ]'),
        '{': ('{', '}'),
        '}': ('{ ', ' }'),
    }

    def run(self, edit, mode=None, replace_what=''):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                self.replace(edit, s, replace_what)
                return s
            return s

        if replace_what:
            regions_transformer(self.view, f)

    def replace(self, edit, s, replace_what):
        old, new = tuple(replace_what)
        pairs = _get_surround_pairs(self.view)
        open_, close_ = pairs.get(old, (old, old))
        new_open, new_close = pairs.get(new, (new, new))

        if len(open_) == 1 and open_ == 't':
            open_, close_ = ('<.*?>', '</.*?>')
            next_ = self.view.find(close_, s.b)
            prev_ = reverse_search(self.view, open_, end=s.b, start=0)
        else:
            # brute force
            next_ = self.view.find(close_, s.b, sublime.LITERAL)
            prev_ = reverse_search(self.view, open_, end=s.b, start=0, flags=sublime.LITERAL)

        if not (next_ and prev_):
            return

        self.view.replace(edit, next_, new_close)
        self.view.replace(edit, prev_, new_open)


class nvim_surround_ds(sublime_plugin.TextCommand):

    PAIRS = {
        '(': ('(', ')'),
        ')': ('( ', ' )'),
        '[': ('[', ']'),
        ']': ('[ ', ' ]'),
        '{': ('{', '}'),
        '}': ('{ ', ' }'),
    }

    def run(self, edit, mode=None, replace_what=''):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                self.replace(edit, s, replace_what)
                return s
            return s

        if replace_what:
            regions_transformer(self.view, f)

    def replace(self, edit, s, replace_what):
        old, new = (replace_what, '')
        open_, close_ = _get_surround_pairs(self.view).get(old, (old, old))

        if len(open_) == 1 and open_ == 't':
            open_, close_ = ('<.*?>', '</.*?>')
            next_ = self.view.find(close_, s.b)
            prev_ = reverse_search(self.view, open_, end=s.b, start=0)
        else:
            # brute force
            next_ = self.view.find(close_, s.b, sublime.LITERAL)
            prev_ = reverse_search(self.view, open_, end=s.b, start=0, flags=sublime.LITERAL)

        if not (next_ and prev_):
            return

        self.view.replace(edit, next_, new)
        self.view.replace(edit, prev_, new)
