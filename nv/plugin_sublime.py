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

# A plugin to support functionality specific to Sublime Text.

from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import ACTION_MODES
from NeoVintageous.nv.vim import INSERT


__all__ = ()


@register(seqs.CTRL_ALT_P, ACTION_MODES)
class StQuickSwitchProject(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'prompt_select_workspace',
            'action_args': {}
        }


@register(seqs.CTRL_0, ACTION_MODES)
class StFocusSideBar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'focus_side_bar',
            'action_args': {}
        }


@register(seqs.CTRL_1, ACTION_MODES, group=0)
@register(seqs.CTRL_2, ACTION_MODES, group=1)
@register(seqs.CTRL_3, ACTION_MODES, group=2)
@register(seqs.CTRL_4, ACTION_MODES, group=3)
@register(seqs.CTRL_5, ACTION_MODES, group=4)
@register(seqs.CTRL_6, ACTION_MODES, group=5)
@register(seqs.CTRL_7, ACTION_MODES, group=6)
@register(seqs.CTRL_8, ACTION_MODES, group=7)
@register(seqs.CTRL_9, ACTION_MODES, group=8)
class StFocusGroup(ViOperatorDef):
    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('_group')
        self._group = group
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'focus_group',
            'action_args': {
                'group': self._group
            }
        }


@register(seqs.CTRL_K_CTRL_B, ACTION_MODES)
class StToggleSideBar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'toggle_side_bar',
            'action_args': {}
        }


@register(seqs.COMMAND_P, ACTION_MODES)
@register(seqs.CTRL_P, ACTION_MODES)
class StGotoAnything(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'show_overlay',
            'action_args': {
                'overlay': 'goto',
                'show_files': True
            }
        }


@register(seqs.COMMAND_BIG_B, ACTION_MODES)
@register(seqs.CTRL_BIG_B, ACTION_MODES)
class StBuildWith(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'build',
            'action_args': {
                'select': True
            }
        }


@register(seqs.COMMAND_BIG_F, ACTION_MODES)
@register(seqs.CTRL_BIG_F, ACTION_MODES)
class StFindInFiles(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'show_panel',
            'action_args': {
                'panel': 'find_in_files'
            }
        }


@register(seqs.COMMAND_BIG_P, ACTION_MODES + (INSERT,))
@register(seqs.CTRL_BIG_P, ACTION_MODES + (INSERT,))
class StCommandPalette(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        set_reset_during_init(view, False)

        return {
            'action': 'show_overlay',
            'action_args': {
                'overlay': 'command_palette'
            }
        }


@register(seqs.F2, ACTION_MODES)
class StNextBookmark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'next_bookmark',
            'action_args': {}
        }


@register(seqs.F3, ACTION_MODES)
class StFindNext(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'find_next',
            'action_args': {}
        }


@register(seqs.F4, ACTION_MODES)
class StNextResult(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'next_result',
            'action_args': {}
        }


@register(seqs.F6, ACTION_MODES)
class StToggleSpellCheck(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'toggle_setting',
            'action_args': {
                'setting': 'spell_check'
            }
        }


@register(seqs.F7, ACTION_MODES)
class StBuild(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'build',
            'action_args': {}
        }


@register(seqs.F9, ACTION_MODES)
class StSortLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'sort_lines',
            'action_args': {
                'case_sensitive': False
            }
        }


@register(seqs.F11, ACTION_MODES)
class StToggleFullScreen(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'toggle_full_screen',
            'action_args': {}
        }


@register(seqs.F12, ACTION_MODES)
class StGotoDefinition(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'goto_definition',
            'action_args': {}
        }


@register(seqs.CTRL_F2, ACTION_MODES)
class StToggleBookmark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'toggle_bookmark',
            'action_args': {}
        }


@register(seqs.CTRL_F12, ACTION_MODES)
class StGotoSymbol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'show_overlay',
            'action_args': {
                'overlay': 'goto',
                'text': '@'
            }
        }


@register(seqs.SHIFT_F2, ACTION_MODES)
class StPrevBookmark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'prev_bookmark',
            'action_args': {}
        }


@register(seqs.SHIFT_F4, ACTION_MODES)
class StPrevResult(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'prev_result',
            'action_args': {}
        }


@register(seqs.SHIFT_F11, ACTION_MODES)
class StToggleDistractionFree(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'toggle_distraction_free',
            'action_args': {}
        }


@register(seqs.CTRL_SHIFT_F2, ACTION_MODES)
class StClearBookmarks(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'clear_bookmarks',
            'action_args': {}
        }


@register(seqs.CTRL_SHIFT_F12, ACTION_MODES)
class StGotoSymbolInProject(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'goto_symbol_in_project',
            'action_args': {}
        }
