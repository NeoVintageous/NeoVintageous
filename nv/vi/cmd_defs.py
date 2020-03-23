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

from NeoVintageous.nv.settings import get_last_char_search
from NeoVintageous.nv.settings import get_last_char_search_command
from NeoVintageous.nv.settings import get_xpos
from NeoVintageous.nv.settings import set_normal_insert_count
from NeoVintageous.nv.utils import InputParser
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import RequiresOneCharMixinDef
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.keys import assign
from NeoVintageous.nv.vim import ACTION_MODES
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import MOTION_MODES
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


@assign(seqs.D, ACTION_MODES)
class ViDeleteByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_d',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.D, (SELECT,))
class DeleteMultipleCursor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_d',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.BIG_O, ACTION_MODES)
class ViInsertLineBefore(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_big_o',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.O, ACTION_MODES)
class ViInsertLineAfter(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = False

    def translate(self, state):
        if state.mode in (VISUAL, VISUAL_LINE):
            return {
                'action': '_vi_visual_o',
                'action_args': {
                    'mode': state.mode,
                    'count': 1
                }
            }
        else:
            state.glue_until_normal_mode = True

            return {
                'action': '_vi_o',
                'action_args': {
                    'mode': state.mode,
                    'count': state.count
                }
            }


@assign(seqs.DEL, ACTION_MODES + (SELECT,))
@assign(seqs.X, ACTION_MODES + (SELECT,))
class ViRightDeleteChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_x',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.S, ACTION_MODES + (SELECT,))
class ViSubstituteChar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        # XXX: Handle differently from State?
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_s',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.Y, ACTION_MODES)
class ViYankByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True

    def translate(self, state):
        return {
            'action': '_vi_y',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.Y, (SELECT,))
class ViYankSelectByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_y',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.EQUAL, ACTION_MODES)
class ViReindent(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_equal',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.GREATER_THAN, ACTION_MODES)
class ViIndent(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_greater_than',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.LESS_THAN, ACTION_MODES)
class ViUnindent(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_less_than',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.C, ACTION_MODES)
class ViChangeByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_c',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.C, (SELECT,))
class ChangeMultipleCursor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_c',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.U, (NORMAL,))
class ViUndo(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_u',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.U, (VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViChangeToLowerCaseByCharsVisual(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_visual_u',
            'action_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.CTRL_R, ACTION_MODES)
class ViRedo(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_r',
            'action_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.BIG_D, ACTION_MODES)
class ViDeleteToEol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_big_d',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.BIG_C, ACTION_MODES)
class ViChangeToEol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_big_c',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.G_BIG_U_BIG_U, ACTION_MODES)
@assign(seqs.G_BIG_U_G_BIG_U, ACTION_MODES)
class ViChangeToUpperCaseByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_g_big_u_big_u',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CC, ACTION_MODES)
class ViChangeLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_cc',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.DD, ACTION_MODES)
class ViDeleteLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_dd',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.BIG_R, ACTION_MODES)
class ViEnterReplaceMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_enter_replace_mode',
            'action_args': {}
        }


@assign(seqs.GREATER_THAN_GREATER_THAN, ACTION_MODES)
class ViIndentLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_greater_than_greater_than',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.GUGU, ACTION_MODES)
@assign(seqs.GUU, ACTION_MODES)
class ViChangeToLowerCaseByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_guu',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.GU, ACTION_MODES)
class ViChangeToLowerCaseByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_gu',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.EQUAL_EQUAL, ACTION_MODES)
class ViReindentLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_equal_equal',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.LESS_THAN_LESS_THAN, ACTION_MODES)
class ViUnindentLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_less_than_less_than',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.YY, ACTION_MODES)
@assign(seqs.BIG_Y, ACTION_MODES)
class ViYankLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_yy',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.G_TILDE_TILDE, ACTION_MODES)
class ViInvertCaseByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_g_tilde_g_tilde',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.TILDE, ACTION_MODES)
class ViForceInvertCaseByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_tilde',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_S, ACTION_MODES)
class ViSubstituteByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_big_s',
            'action_args': {
                'mode': state.mode,
                'count': 1,
                'register': state.register
            }
        }


@assign(seqs.G_TILDE, ACTION_MODES)
class ViInvertCaseByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_g_tilde',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.G_BIG_U, ACTION_MODES)
class ViChangeToUpperCaseByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_g_big_u',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_J, ACTION_MODES)
class ViJoinLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_big_j',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_X, ACTION_MODES)
class ViDecrement(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_modify_numbers',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'subtract': True
            }
        }


@assign(seqs.CTRL_A, ACTION_MODES)
class ViIncrement(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_modify_numbers',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.G_BIG_J, ACTION_MODES)
class ViJoinLinesNoSeparator(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_big_j',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'dont_insert_or_remove_spaces': True
            }
        }


@assign(seqs.V, ACTION_MODES)
class ViEnterVisualMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_enter_visual_mode',
            'action_args': {
                'mode': state.mode
            }
        }


@assign(seqs.Z_ENTER, ACTION_MODES)
@assign(seqs.ZT, ACTION_MODES)
class ViScrollToScreenTop(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_z_enter',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.ZB, ACTION_MODES)
@assign(seqs.Z_MINUS, ACTION_MODES)
class ViScrollToScreenBottom(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_z_minus',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.ZZ, ACTION_MODES)
class ViScrollToScreenCenter(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_zz',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.Z_DOT, ACTION_MODES)
class ViZDot(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_zz',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'first_non_blank': True
            }
        }


@assign(seqs.GQ, ACTION_MODES)
class ViReformat(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.motion_required = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_gq',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.GQGQ, (NORMAL,))
@assign(seqs.GQQ, (NORMAL,))
class ViReformatLinewise(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_gq',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'linewise': True
            }
        }


@assign(seqs.P, ACTION_MODES)
class ViPasteAfter(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_paste',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'before_cursor': False
            }
        }


@assign(seqs.BIG_P, ACTION_MODES)
class ViPasteBefore(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_paste',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'before_cursor': True
            }
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_BIG_P, ACTION_MODES)
@assign(seqs.RIGHT_SQUARE_BRACKET_P, ACTION_MODES)
class ViPasteAfterAndIndent(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_paste',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'before_cursor': False,
                'adjust_indent': True
            }
        }


@assign(seqs.LEFT_SQUARE_BRACKET_BIG_P, ACTION_MODES)
@assign(seqs.LEFT_SQUARE_BRACKET_P, ACTION_MODES)
class ViPasteBeforeAndIndent(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_paste',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'before_cursor': True,
                'adjust_indent': True
            }
        }


@assign(seqs.GP, ACTION_MODES)
class ViPasteAfterWithAdjustedCursor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_paste',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'before_cursor': False,
                'adjust_cursor': True
            }
        }


@assign(seqs.G_BIG_P, ACTION_MODES)
class ViPasteBeforeWithAdjustedCursor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_paste',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'before_cursor': True,
                'adjust_cursor': True
            }
        }


@assign(seqs.BIG_X, ACTION_MODES)
class ViLeftDeleteChar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_big_x',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@assign(seqs.CTRL_PAGEDOWN, ACTION_MODES)
@assign(seqs.GT, ACTION_MODES)
class ViActivateNextTab(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_gt',
            'action_args': {
                'mode': state.mode,
                'count': state.count_default_zero
            }
        }


@assign(seqs.CTRL_PAGEUP, ACTION_MODES)
@assign(seqs.G_BIG_T, ACTION_MODES)
class ViActivatePreviousTab(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_g_big_t',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_B, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_B, ACTION_MODES)
class ViMoveCursorToBottomRightWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'b'
            }
        }


@assign(seqs.CTRL_W_BIG_H, ACTION_MODES)
class ViMoveCurrentWindowToFarLeft(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'H'
            }
        }


@assign(seqs.CTRL_W_BIG_J, ACTION_MODES)
class ViMoveCurrentWindowToVeryTop(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'J'
            }
        }


@assign(seqs.CTRL_W_BIG_K, ACTION_MODES)
class ViMoveCurrentWindowToVeryBottom(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'K'
            }
        }


@assign(seqs.CTRL_W_BIG_L, ACTION_MODES)
class ViMoveCurrentWindowToFarRight(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'L'
            }
        }


@assign(seqs.CTRL_W_C, ACTION_MODES)
class ViCloseTheCurrentWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'c'
            }
        }


@assign(seqs.CTRL_W_EQUAL, ACTION_MODES)
class ViMakeAllWindowsAlmostEquallyHighAndWide(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '='
            }
        }


@assign(seqs.CTRL_W_GREATER_THAN, ACTION_MODES)
class ViIncreaseCurrentWindowWidthByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '>',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_H, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_H, ACTION_MODES)
@assign(seqs.CTRL_W_LEFT, ACTION_MODES)
@assign(seqs.CTRL_W_BACKSPACE, ACTION_MODES)
class ViMoveCursorToNthWindowLeftOfCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'h',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_J, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_J, ACTION_MODES)
@assign(seqs.CTRL_W_DOWN, ACTION_MODES)
class ViMoveCursorToNthWindowBelowOfCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'j',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_K, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_K, ACTION_MODES)
@assign(seqs.CTRL_W_UP, ACTION_MODES)
class ViMoveCursorToNthWindowAboveCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'k',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_L, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_L, ACTION_MODES)
@assign(seqs.CTRL_W_RIGHT, ACTION_MODES)
class ViMoveCursorToNthWindowRightOfCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'l',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_LESS_THAN, ACTION_MODES)
class ViDecreaseCurrentWindowWidthByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '<',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_MINUS, ACTION_MODES)
class ViDecreaseCurrentWindowHeightByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '-',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_N, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_N, ACTION_MODES)
class ViCreateNewWindowAndStartEditingAnEmptyFileInIt(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'n',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_O, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_O, ACTION_MODES)
class ViMakeTheCurrentWindowTheOnlyOneOnTheScreen(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'o'
            }
        }


@assign(seqs.CTRL_W_BAR, ACTION_MODES)
class ViSetCurrentWindowWidthToNOrWidestPossible(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '|',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_PLUS, ACTION_MODES)
class ViIncreaseCurrentWindowHeightByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '+',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_Q, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_Q, ACTION_MODES)
class ViQuitTheCurrentWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'q'
            }
        }


@assign(seqs.CTRL_W_S, ACTION_MODES)
@assign(seqs.CTRL_W_BIG_S, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_S, ACTION_MODES)
class ViSplitTheCurrentWindowInTwo(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 's',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_T, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_T, ACTION_MODES)
class ViMoveCursorToTopLeftWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 't'
            }
        }


@assign(seqs.CTRL_W_UNDERSCORE, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_UNDERSCORE, ACTION_MODES)
class ViSetCurrentGroupHeightOrHighestPossible(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': '_',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_V, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_V, ACTION_MODES)
class ViSplitTheCurrentWindowInTwoVertically(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'v',
                'count': state.count
            }
        }


@assign(seqs.CTRL_W_X, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_X, ACTION_MODES)
class ViExchangeCurrentWindowWithNextOrPreviousNthWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w',
            'action_args': {
                'action': 'x',
                'count': state.count
            }
        }


@assign(seqs.BIG_V, ACTION_MODES)
class ViEnterVisualLineMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_enter_visual_line_mode',
            'action_args': {
                'mode': state.mode
            }
        }


@assign(seqs.GV, ACTION_MODES)
class ViRestoreVisualSelections(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_gv',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.GX, ACTION_MODES)
class NetrwGx(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_vi_gx',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_O, ACTION_MODES)
class ViJumpBack(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'jump_back',
            'action_args': {}
        }


@assign(seqs.CTRL_I, ACTION_MODES)
@assign(seqs.TAB, ACTION_MODES)
class ViJumpForward(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'jump_forward',
            'action_args': {}
        }


@assign(seqs.DOT, ACTION_MODES)
class ViRepeat(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_dot',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_Y, ACTION_MODES)
class ViScrollByLinesUp(ViOperatorDef):

    def translate(self, state):
        return {
            'action': '_vi_ctrl_y',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_U, (VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViChangeToUpperCaseByCharsVisual(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_visual_big_u',
            'action_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.CTRL_E, ACTION_MODES)
class ViScrollByLinesDown(ViOperatorDef):

    def translate(self, state):
        return {
            'action': '_vi_ctrl_e',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.AT, ACTION_MODES)
class ViOpenMacrosForRepeating(RequiresOneCharMixinDef, ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_at',
            'action_args': {
                'name': self.inp,
                'count': state.count
            }
        }


@assign(seqs.Q, ACTION_MODES)
class ViToggleMacroRecorder(RequiresOneCharMixinDef, ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_q',
            'action_args': {
                'name': self.inp
            }
        }


@assign(seqs.CTRL_V, ACTION_MODES)
class ViEnterVisualBlockMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_enter_visual_block_mode',
            'action_args': {
                'mode': state.mode
            }
        }


@assign(seqs.GA, ACTION_MODES)
class ViShowAsciiValueOfChar(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_vi_ga',
            'action_args': {}
        }


@assign(seqs.GF, (NORMAL,))
class Vi_gf(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_vi_g',
            'action_args': {
                'action': 'f'
            }
        }


@assign(seqs.I, (NORMAL, SELECT))
@assign(seqs.INSERT, (NORMAL, SELECT))
class ViEnterInserMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_enter_insert_mode',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.V, (SELECT, ))
@assign(seqs.ESC, ACTION_MODES)
@assign(seqs.CTRL_C, ACTION_MODES + (SELECT,))
@assign(seqs.CTRL_LEFT_SQUARE_BRACKET, ACTION_MODES + (SELECT,))
class ViEnterNormalMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_enter_normal_mode',
            'action_args': {
                'mode': state.mode
            }
        }


@assign(seqs.CTRL_RIGHT_SQUARE_BRACKET, ACTION_MODES)
class ViJumpToDefinition(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {
            'action': '_vi_ctrl_right_square_bracket',
            'action_args': {}
        }


@assign(seqs.A, (NORMAL,))
class ViInsertAfterChar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        state.glue_until_normal_mode = True
        set_normal_insert_count(state.view, state.count)

        return {
            'action': '_vi_a',
            'action_args': {
                'mode': state.mode,
                'count': 1
            }
        }


@assign(seqs.ALT_N, (SELECT,))
@assign(seqs.BIG_A, ACTION_MODES + (SELECT,))
class ViInsertAtEol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        if state.mode != SELECT:
            state.glue_until_normal_mode = True

        return {
            'action': '_vi_big_a',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_I, ACTION_MODES + (SELECT,))
class ViInsertAtBol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        if state.mode != SELECT:
            state.glue_until_normal_mode = True

        return {
            'action': '_vi_big_i',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.COLON, ACTION_MODES)
class ViEnterCommandLineMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_nv_cmdline',
            'action_args': {}
        }


@assign(seqs.CTRL_G, ACTION_MODES)
class ViShowFileStatus(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_g',
            'action_args': {}
        }


@assign(seqs.BIG_Z_BIG_Q, ACTION_MODES)
class ViExitEditor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_big_z_big_q',
            'action_args': {}
        }


@assign(seqs.BIG_Z_BIG_Z, ACTION_MODES)
class ViCloseFile(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_big_z_big_z',
            'action_args': {}
        }


@assign(seqs.G_BIG_D, ACTION_MODES)
class ViGotoSymbolInProject(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_go_to_symbol',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'globally': True
            }
        }


@assign(seqs.GD, MOTION_MODES)
class ViGotoSymbolInFile(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_go_to_symbol',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'globally': False
            }
        }


@assign(seqs.ALT_RIGHT, MOTION_MODES)
@assign(seqs.L, MOTION_MODES)
@assign(seqs.RIGHT, MOTION_MODES)
@assign(seqs.SPACE, MOTION_MODES)
class ViMoveRightByChars(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_l',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.SHIFT_ENTER, MOTION_MODES)
class ViShiftEnterMotion(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_shift_enter',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.B, MOTION_MODES)
@assign(seqs.SHIFT_LEFT, MOTION_MODES)
class ViMoveByWordsBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_b',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_B, MOTION_MODES)
@assign(seqs.CTRL_LEFT, MOTION_MODES)
class ViMoveByBigWordsBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_big_b',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_W, MOTION_MODES)
@assign(seqs.CTRL_RIGHT, MOTION_MODES)
class ViMoveByBigWords(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_big_w',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.E, MOTION_MODES)
class ViMoveByWordEnds(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_e',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_H, MOTION_MODES)
class ViGotoScreenTop(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_big_h',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.GE, MOTION_MODES)
class ViMoveByWordEndsBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_ge',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.G_BIG_E, MOTION_MODES)
class ViMoveByBigWordEndsBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_g_big_e',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_L, MOTION_MODES)
class ViGotoScreenBottom(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_big_l',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_M, MOTION_MODES)
class ViGotoScreenMiddle(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_big_m',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_D, MOTION_MODES)
class ViMoveHalfScreenDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = False

    def translate(self, state):
        return {
            'motion': '_vi_ctrl_d',
            'motion_args': {
                'mode': state.mode,
                'count': state.count_default_zero
            }
        }


@assign(seqs.CTRL_U, MOTION_MODES)
class ViMoveHalfScreenUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_ctrl_u',
            'motion_args': {
                'mode': state.mode,
                'count': state.count_default_zero
            }
        }


@assign(seqs.CTRL_F, MOTION_MODES)
@assign(seqs.PAGE_DOWN, MOTION_MODES)
@assign(seqs.SHIFT_DOWN, MOTION_MODES)
class ViMoveScreenDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_ctrl_f',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_B, MOTION_MODES)
@assign(seqs.PAGE_UP, MOTION_MODES)
@assign(seqs.SHIFT_UP, MOTION_MODES)
class ViMoveScreenUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_ctrl_b',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BACKTICK, MOTION_MODES)
class ViGotoExactMarkXpos(RequiresOneCharMixinDef, ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_backtick',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'character': self.inp
            }
        }


@assign(seqs.DOLLAR, MOTION_MODES)
@assign(seqs.END, MOTION_MODES)
class ViMoveToEol(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_dollar',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.ENTER, MOTION_MODES)
@assign(seqs.PLUS, MOTION_MODES)
class ViMotionEnter(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_enter',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.MINUS, MOTION_MODES)
class ViMoveBackOneLine(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_minus',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.G_UNDERSCORE, MOTION_MODES)
class ViMoveToSoftEol(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_g__',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.G_DOWN, MOTION_MODES)
@assign(seqs.GJ, MOTION_MODES)
class ViMoveByScreenLineDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_gj',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.G_UP, MOTION_MODES)
@assign(seqs.GK, MOTION_MODES)
class ViMoveByScreenLineUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_gk',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.LEFT_BRACE, MOTION_MODES)
class ViMoveByBlockUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_left_brace',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.SEMICOLON, MOTION_MODES)
class ViRepeatCharSearchForward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    # TODO Refactor settings dependencies into the command being called
    def translate(self, state):
        view = state.view
        last_search_cmd = get_last_char_search_command(view)
        forward = last_search_cmd in ('vi_t', 'vi_f')
        inclusive = last_search_cmd in ('vi_f', 'vi_big_f')
        skipping = last_search_cmd in ('vi_t', 'vi_big_t')
        motion = '_vi_find_in_line' if forward else '_vi_reverse_find_in_line'

        return {
            'motion': motion,
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'char': get_last_char_search(view),
                'inclusive': inclusive,
                'skipping': skipping,
                'save': False
            }
        }


@assign(seqs.QUOTE, MOTION_MODES)
class ViGotoMark(RequiresOneCharMixinDef, ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_quote',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'character': self.inp
            }
        }


@assign(seqs.RIGHT_BRACE, MOTION_MODES)
class ViMoveByBlockDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_right_brace',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.LEFT_PAREN, MOTION_MODES)
class ViMoveBySentenceUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_left_paren',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.RIGHT_PAREN, MOTION_MODES)
class ViMoveBySentenceDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_right_paren',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.LEFT_SQUARE_BRACKET_LEFT_BRACE, MOTION_MODES)
class ViGotoOpeningBrace(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_left_square_bracket',
            'motion_args': {
                'action': 'target',
                'mode': state.mode,
                'count': state.count,
                'target': '{'
            }
        }


@assign(seqs.LEFT_SQUARE_BRACKET_LEFT_PAREN, MOTION_MODES)
class ViGotoOpeningParen(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_left_square_bracket',
            'motion_args': {
                'action': 'target',
                'mode': state.mode,
                'count': state.count,
                'target': '('
            }
        }


@assign(seqs.LEFT_SQUARE_BRACKET_C, ACTION_MODES)
class ViBackwardToStartOfChange(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_left_square_bracket',
            'motion_args': {
                'action': 'c',
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_C, ACTION_MODES)
class ViForwardToStartOfChange(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_right_square_bracket',
            'motion_args': {
                'action': 'c',
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.LEFT_SQUARE_BRACKET_S, ACTION_MODES)
class ViPrevMisppelledWord(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_left_square_bracket',
            'motion_args': {
                'action': 's',
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_S, ACTION_MODES)
class VINextMispelledWord(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_right_square_bracket',
            'motion_args': {
                'action': 's',
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_RIGHT_BRACE, MOTION_MODES)
class ViGotoClosingBrace(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_right_square_bracket',
            'motion_args': {
                'action': 'target',
                'mode': state.mode,
                'count': state.count,
                'target': '}'
            }
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_RIGHT_PAREN, MOTION_MODES)
class ViGotoClosingParen(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_right_square_bracket',
            'motion_args': {
                'action': 'target',
                'mode': state.mode,
                'count': state.count,
                'target': ')'
            }
        }


@assign(seqs.PERCENT, MOTION_MODES)
class ViPercent(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_percent',
            'motion_args': {
                'mode': state.mode,
                'count': state.count_default_zero
            }
        }


@assign(seqs.COMMA, MOTION_MODES)
class ViRepeatCharSearchBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    # TODO Refactor settings dependencies into the command being called
    def translate(self, state):
        view = state.view
        last_search_cmd = get_last_char_search_command(view)
        forward = last_search_cmd in ('vi_t', 'vi_f')
        inclusive = last_search_cmd in ('vi_f', 'vi_big_f')
        skipping = last_search_cmd in ('vi_t', 'vi_big_t')
        motion = '_vi_find_in_line' if not forward else '_vi_reverse_find_in_line'

        return {
            'motion': motion,
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'char': get_last_char_search(view),
                'inclusive': inclusive,
                'skipping': skipping,
                'save': False
            }
        }


@assign(seqs.BAR, MOTION_MODES)
class ViMoveByLineCols(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_bar',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.BIG_E, MOTION_MODES)
class ViMoveByBigWordEnds(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_big_e',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.ALT_LEFT, MOTION_MODES)
@assign(seqs.BACKSPACE, MOTION_MODES)
@assign(seqs.CTRL_BACKSPACE, MOTION_MODES)
@assign(seqs.CTRL_H, MOTION_MODES)
@assign(seqs.H, MOTION_MODES)
@assign(seqs.LEFT, MOTION_MODES)
class ViMoveLeftByChars(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_h',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.SHIFT_RIGHT, MOTION_MODES)
@assign(seqs.W, MOTION_MODES)
class ViMoveByWords(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_w',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_DOWN, MOTION_MODES)
@assign(seqs.CTRL_J, MOTION_MODES)
@assign(seqs.CTRL_N, MOTION_MODES)
@assign(seqs.DOWN, MOTION_MODES)
@assign(seqs.J, MOTION_MODES)
class ViMoveDownByLines(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_j',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'xpos': get_xpos(state.view)
            }
        }


@assign(seqs.CTRL_P, MOTION_MODES)
@assign(seqs.CTRL_UP, MOTION_MODES)
@assign(seqs.K, MOTION_MODES)
@assign(seqs.UP, MOTION_MODES)
class ViMoveUpByLines(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_k',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'xpos': get_xpos(state.view)
            }
        }


@assign(seqs.HAT, MOTION_MODES)
@assign(seqs.HOME, MOTION_MODES)
class ViMoveToBol(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_hat',
            'motion_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.UNDERSCORE, MOTION_MODES)
class ViMoveToSoftBol(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_underscore',
            'motion_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.ZERO, MOTION_MODES)
class ViMoveToHardBol(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_zero',
            'motion_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.GN, MOTION_MODES)
@assign(seqs.G_BIG_N, MOTION_MODES, forward=False)
class ViSearchLastUsedPattern(ViMotionDef):
    def __init__(self, *args, forward=True, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('forward')
        self.scroll_into_view = True
        self.updates_xpos = True
        self.forward = forward

    def translate(self, state):
        return {
            'motion': '_vi_search',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'forward': self.forward
            }
        }


@assign(seqs.N, MOTION_MODES)
class ViRepeatSearchForward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_repeat_buffer_search',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'reverse': False
            }
        }


@assign(seqs.BIG_N, MOTION_MODES)
class ViRepeatSearchBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_repeat_buffer_search',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'reverse': True
            }
        }


@assign(seqs.STAR, MOTION_MODES)
class ViFindWord(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_star',
            'motion_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.OCTOTHORP, MOTION_MODES)
class ViReverseFindWord(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_octothorp',
            'motion_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@assign(seqs.BIG_Z, MOTION_MODES)
@assign(seqs.CTRL_K, MOTION_MODES)
@assign(seqs.CTRL_W, MOTION_MODES)
@assign(seqs.CTRL_X, (INSERT,))
@assign(seqs.G, MOTION_MODES)
@assign(seqs.LEFT_SQUARE_BRACKET, MOTION_MODES)
@assign(seqs.RIGHT_SQUARE_BRACKET, MOTION_MODES)
@assign(seqs.Z, MOTION_MODES)
@assign(seqs.ZU, MOTION_MODES)
class ViOpenNameSpace(ViMotionDef):  # TODO This should not be a motion.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {}


@assign(seqs.DOUBLE_QUOTE, MOTION_MODES)
class ViOpenRegister(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {}


@assign(seqs.CTRL_HOME, MOTION_MODES)
@assign(seqs.GG, MOTION_MODES)
class ViGotoBof(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_gg',
            'motion_args': {
                'mode': state.mode,
                'count': state.count if (state.action_count or state.motion_count) else None
            }
        }


@assign(seqs.BIG_G, MOTION_MODES)
class ViGotoEof(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_big_g',
            'motion_args': {
                'mode': state.mode,
                'count': state.count if (state.action_count or state.motion_count) else None
            }
        }


@assign(seqs.R, ACTION_MODES)
class ViReplaceCharacters(RequiresOneCharMixinDef, ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_r',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register,
                'char': self.inp
            }
        }


@assign(seqs.M, ACTION_MODES)
class ViSetMark(RequiresOneCharMixinDef, ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_m',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'character': self.inp
            }
        }


@assign(seqs.T, MOTION_MODES)
@assign(seqs.F, MOTION_MODES, inclusive=True)
class ViSearchCharForward(RequiresOneCharMixinDef, ViMotionDef):
    def __init__(self, inclusive=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('inclusive')
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inclusive = inclusive

    def translate(self, state):
        return {
            'motion': '_vi_find_in_line',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'char': self.inp,
                'inclusive': self.inclusive
            }
        }


@assign(seqs.A, (OPERATOR_PENDING, VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViATextObject(RequiresOneCharMixinDef, ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_select_text_object',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'text_object': self.inp,
                'inclusive': True
            }
        }


@assign(seqs.I, (OPERATOR_PENDING, VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViITextObject(RequiresOneCharMixinDef, ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_select_text_object',
            'motion_args': {
                'mode': state.mode,
                'count': state.count,
                'text_object': self.inp,
                'inclusive': False
            }
        }


@assign(seqs.BIG_T, MOTION_MODES)
@assign(seqs.BIG_F, MOTION_MODES, inclusive=True)
class ViSearchCharBackward(RequiresOneCharMixinDef, ViMotionDef):
    def __init__(self, inclusive=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('inclusive')
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inclusive = inclusive

    def translate(self, state):
        return {
            'motion': '_vi_reverse_find_in_line',
            'motion_args': {
                'char': self.inp,
                'mode': state.mode,
                'count': state.count,
                'inclusive': self.inclusive
            }
        }


@assign(seqs.SLASH, MOTION_MODES)
class ViSearchForward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = InputParser(
            InputParser.PANEL,
            command='_vi_slash',
            param='pattern'
        )

    @property
    def accept_input(self) -> bool:
        if not self.inp:
            return True

        return not self.inp.lower().endswith('<cr>')

    def accept(self, key: str) -> bool:
        self.inp += key

        return True

    def translate(self, state):
        if self.accept_input:
            return {
                'motion': '_vi_slash',
                'motion_args': {}
            }

        # We'll end up here, for example, when repeating via '.'.
        return ViSearchForwardImpl(term=self.inp[:-4]).translate(state)


class ViSearchForwardImpl(ViMotionDef):
    def __init__(self, *args, term='', **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.inp = term
        self.updates_xpos = True

    def translate(self, state):
        return {
            'motion': '_vi_slash_impl',
            'motion_args': {
                'pattern': self.inp,
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.QUESTION_MARK, MOTION_MODES)
class ViSearchBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = InputParser(
            InputParser.PANEL,
            command='_vi_question_mark',
            param='pattern'
        )

    @property
    def accept_input(self) -> bool:
        if not self.inp:
            return True

        return not self.inp.lower().endswith('<cr>')

    def accept(self, key: str) -> bool:
        self.inp += key

        return True

    def translate(self, state):
        if self.accept_input:
            return {
                'motion': '_vi_question_mark',
                'motion_args': {}
            }
        else:
            # We'll end up here, for example, when repeating via '.'.
            return ViSearchBackwardImpl(term=self.inp[:-4]).translate(state)


class ViSearchBackwardImpl(ViMotionDef):
    def __init__(self, *args, term='', **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inp = term

    def translate(self, state):
        return {
            'motion': '_vi_question_mark_impl',
            'motion_args': {
                'pattern': self.inp,
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.CTRL_X_CTRL_L, (INSERT,))
class ViInsertLineWithCommonPrefix(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_x_ctrl_l',
            'action_args': {
                'mode': state.mode,
                'register': state.register
            }
        }


@assign(seqs.GM, MOTION_MODES)
class ViMoveHalfScreenHorizontally(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_gm',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@assign(seqs.ZC, ACTION_MODES)
@assign(seqs.ZG, ACTION_MODES)
@assign(seqs.ZH, ACTION_MODES)
@assign(seqs.ZL, ACTION_MODES)
@assign(seqs.ZO, ACTION_MODES)
@assign(seqs.ZUG, ACTION_MODES)
@assign(seqs.Z_BIG_H, ACTION_MODES)
@assign(seqs.Z_BIG_L, ACTION_MODES)
@assign(seqs.Z_BIG_M, ACTION_MODES)
@assign(seqs.Z_BIG_R, ACTION_MODES)
@assign(seqs.Z_EQUAL, ACTION_MODES)
@assign(seqs.Z_LEFT, ACTION_MODES)
@assign(seqs.Z_RIGHT, ACTION_MODES)
class Viz(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        return {
            'action': '_vi_z',
            'action_args': {
                'action': state.partial_sequence[1:],
                'mode': state.mode,
                'count': state.count
            }
        }
