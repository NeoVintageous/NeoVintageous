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

# A port of https://github.com/terryma/vim-multiple-cursors.

from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import ACTION_MODES
from NeoVintageous.nv.vim import SELECT


__all__ = ()


@register(seqs.CTRL_N, ACTION_MODES)
@register(seqs.GH, ACTION_MODES)
class MultipleCursorsStart(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'nv_enter_select_mode',
            'action_args': {
                'mode': get_mode(view)
            }
        }


@register(seqs.BIG_J, (SELECT,))
@register(seqs.ESC, (SELECT,))
class MultipleCursorsExit(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, view):
        return {
            'action': 'nv_vi_select_big_j',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view)
            }
        }


@register(seqs.CTRL_N, (SELECT,))
@register(seqs.J, (SELECT,))
class MultipleCursorsAdd(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'nv_vi_select_j',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view)
            }
        }


@register(seqs.CTRL_P, (SELECT,))
@register(seqs.K, (SELECT,))
class MultipleCursorsRemove(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'nv_vi_select_k',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view)
            }
        }


@register(seqs.CTRL_X, (SELECT,))
@register(seqs.L, (SELECT,))
class MultipleCursorsSkip(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'find_under_expand_skip',
            'action_args': {}
        }


@register(seqs.G_BIG_H, ACTION_MODES)
class MultipleCursorsAll(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'nv_vi_g_big_h',
            'action_args': {}
        }
