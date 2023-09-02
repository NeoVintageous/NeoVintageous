# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import ACTION_MODES
from NeoVintageous.nv.vim import SELECT


__all__ = []  # type: list


@register(seqs.CTRL_N, ACTION_MODES)
@register(seqs.GH, ACTION_MODES)
class MultipleCursorsStart(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_enter_select_mode'


@register(seqs.BIG_J, (SELECT,))
@register(seqs.TAB, (SELECT,))
@register(seqs.ESC, (SELECT,))
class MultipleCursorsExit(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_select_big_j'


@register(seqs.CTRL_N, (SELECT,))
@register(seqs.J, (SELECT,))
@register(seqs.N, (SELECT,))
class MultipleCursorsAdd(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_select_j'


@register(seqs.ALT_N, (SELECT,))
@register(seqs.BIG_A, (SELECT,))
class MultipleCursorsAddAll(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_big_a'


@register(seqs.CTRL_P, (SELECT,))
@register(seqs.K, (SELECT,))
@register(seqs.BIG_N, (SELECT,))
@register(seqs.BIG_Q, (SELECT,))
class MultipleCursorsRemove(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_select_k'


@register(seqs.CTRL_X, (SELECT,))
@register(seqs.L, (SELECT,))
@register(seqs.Q, (SELECT,))
class MultipleCursorsSkip(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'find_under_expand_skip'


@register(seqs.G_BIG_H, ACTION_MODES)
class MultipleCursorsAll(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_g_big_h'
