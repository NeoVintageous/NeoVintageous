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

from sublime_plugin import TextCommand

from NeoVintageous.nv.plugin import INTERNAL_NORMAL
from NeoVintageous.nv.plugin import NORMAL
from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.plugin import ViOperatorDef
from NeoVintageous.nv.plugin import VISUAL
from NeoVintageous.nv.plugin import VISUAL_BLOCK
from NeoVintageous.nv.plugin import VISUAL_LINE
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.vi.utils import next_non_white_space_char
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vi.utils import regions_transformer_reversed
from NeoVintageous.nv.vi.utils import row_at
from NeoVintageous.nv.vim import enter_normal_mode
from sublime import Region


__all__ = [
    '_nv_commentary_command'
]

_MODES_ACTION = (NORMAL, VISUAL, VISUAL_LINE, VISUAL_BLOCK)


@register(seq='gc', modes=_MODES_ACTION)
class CommentLinesMotion(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_nv_commentary',
            'action_args': {
                'action': 'c',
                'mode': state.mode,
                'count': state.count
            }
        }


@register(seq='gcc', modes=(NORMAL,))
class CommentLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_nv_commentary',
            'action_args': {
                'action': 'cc',
                'mode': state.mode,
                'count': state.count
            }
        }


# NOTE Not a standard Commentary command.
# See also tComment plugin.
@register(seq='gC', modes=_MODES_ACTION)
class ToggleBlockComments(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_nv_commentary',
            'action_args': {
                'action': 'C',
                'mode': state.mode,
                'count': state.count
            }
        }


class _nv_commentary_command(TextCommand):
    def run(self, edit, action, **kwargs):
        if action == 'c':
            _do_c(self.view, edit, **kwargs)
        elif action == 'cc':
            _do_cc(self.view, edit, **kwargs)
        elif action == 'C':
            _do_C(self.view, edit, **kwargs)
        else:
            raise Exception('unknown action')


def _do_c(view, edit, mode, count=1, motion=None):
    def f(view, s):
        return Region(s.begin())

    if motion:
        view.run_command(motion['motion'], motion['motion_args'])
    elif mode not in (VISUAL, VISUAL_LINE):
        return ui_bell()

    view.run_command('toggle_comment', {'block': False})

    regions_transformer(view, f)

    line = view.line(view.sel()[0].begin())
    pt = line.begin()

    if line.size() > 0:
        line = view.find('^\\s*', line.begin())
        pt = line.end()

    view.sel().clear()
    view.sel().add(pt)
    enter_normal_mode(view, mode)


def _do_cc(view, edit, mode, count=1):
    def f(view, s):
        if mode == INTERNAL_NORMAL:
            view.run_command('toggle_comment')
            if row_at(view, s.a) != row_at(view, view.size()):
                pt = next_non_white_space_char(view, s.a, white_space=' \t')
            else:
                pt = next_non_white_space_char(view, view.line(s.a).a, white_space=' \t')

            return Region(pt)

        return s

    def _motion(view, edit, mode, count):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                end = view.text_point(row_at(view, s.b) + (count - 1), 0)
                begin = view.line(s.b).a

                row_at_end = row_at(view, end)
                row_at_size = row_at(view, view.size())

                if ((row_at_end == row_at_size) and (view.substr(begin - 1) == '\n')):
                    begin -= 1

                return Region(begin, view.full_line(end).b)

            return s

        regions_transformer(view, f)

    _motion(view, edit, mode, count)

    line = view.line(view.sel()[0].begin())
    pt = line.begin()

    if line.size() > 0:
        line = view.find('^\\s*', line.begin())
        pt = line.end()

    regions_transformer_reversed(view, f)

    view.sel().clear()
    view.sel().add(pt)


def _do_C(view, edit, mode, count=1, motion=None):
    def f(view, s):
        return Region(s.begin())

    if motion:
        view.run_command(motion['motion'], motion['motion_args'])
    elif mode not in (VISUAL, VISUAL_LINE):
        return ui_bell()

    view.run_command('toggle_comment', {'block': True})
    regions_transformer(view, f)
    enter_normal_mode(view, mode)
