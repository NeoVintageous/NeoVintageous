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

# A port of https://github.com/tpope/vim-commentary.

from sublime import Region
from sublime_plugin import TextCommand

from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.utils import next_non_blank
from NeoVintageous.nv.utils import regions_transformer
from NeoVintageous.nv.utils import regions_transformer_reversed
from NeoVintageous.nv.utils import row_at
from NeoVintageous.nv.utils import set_selection
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import ACTION_MODES
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import run_motion


__all__ = [
    'nv_commentary_command'
]


@register(seqs.GC, ACTION_MODES)
class CommentaryMotion(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, view):
        return {
            'action': 'nv_commentary',
            'action_args': {
                'action': 'c',
                'mode': get_mode(view),
                'count': get_count(view)
            }
        }


@register(seqs.GCC, (NORMAL,))
class CommentaryLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, view):
        return {
            'action': 'nv_commentary',
            'action_args': {
                'action': 'cc',
                'mode': get_mode(view),
                'count': get_count(view)
            }
        }


# NOTE The command (gC) is not defined in the original Commentary plugin, it's
# from a plugin called tComment: https://github.com/tomtom/tcomment_vim.
@register(seqs.G_BIG_C, ACTION_MODES)
class CommentaryBlock(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, view):
        return {
            'action': 'nv_commentary',
            'action_args': {
                'action': 'C',
                'mode': get_mode(view),
                'count': get_count(view)
            }
        }


class nv_commentary_command(TextCommand):
    def run(self, edit, action, **kwargs):
        if action == 'c':
            _do_c(self.view, edit, **kwargs)
        elif action == 'cc':
            _do_cc(self.view, edit, **kwargs)
        elif action == 'C':
            _do_C(self.view, edit, **kwargs)


def _do_c(view, edit, mode, count=1, motion=None):
    def f(view, s):
        return Region(s.begin())

    if motion:
        run_motion(view, motion)
    elif mode not in (VISUAL, VISUAL_LINE):
        return ui_bell()

    view.run_command('toggle_comment', {'block': False})

    regions_transformer(view, f)

    line = view.line(view.sel()[0].begin())
    pt = line.begin()

    if line.size() > 0:
        line = view.find('^\\s*', line.begin())
        pt = line.end()

    set_selection(view, pt)
    enter_normal_mode(view, mode)


def _do_cc(view, edit, mode: str, count: int = 1) -> None:
    def f(view, s):
        if mode == INTERNAL_NORMAL:
            view.run_command('toggle_comment')
            if row_at(view, s.a) != row_at(view, view.size()):
                pt = next_non_blank(view, s.a)
            else:
                pt = next_non_blank(view, view.line(s.a).a)

            s.a = s.b = pt

        return s

    def _motion(view, edit, mode: str, count: int) -> None:
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                end = view.text_point(row_at(view, s.b) + (count - 1), 0)
                begin = view.line(s.b).a

                row_at_end = row_at(view, end)
                row_at_size = row_at(view, view.size())

                if ((row_at_end == row_at_size) and (view.substr(begin - 1) == '\n')):
                    begin -= 1

                s.a = begin
                s.b = view.full_line(end).b

            return s

        regions_transformer(view, f)

    _motion(view, edit, mode, count)

    line = view.line(view.sel()[0].begin())
    pt = line.begin()

    if line.size() > 0:
        line = view.find('^\\s*', line.begin())
        pt = line.end()

    regions_transformer_reversed(view, f)
    set_selection(view, pt)


def _do_C(view, edit, mode: str, count: int = 1, motion=None) -> None:
    def f(view, s):
        return Region(s.begin())

    if motion:
        run_motion(view, motion)
    elif mode not in (VISUAL, VISUAL_LINE):
        return ui_bell()

    view.run_command('toggle_comment', {'block': True})
    regions_transformer(view, f)
    enter_normal_mode(view, mode)
