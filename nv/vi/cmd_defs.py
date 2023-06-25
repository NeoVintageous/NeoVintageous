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

from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_last_char_search_character
from NeoVintageous.nv.settings import get_last_char_search_command
from NeoVintageous.nv.settings import get_partial_sequence
from NeoVintageous.nv.settings import get_xpos
from NeoVintageous.nv.utils import InputParser
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import RequireOneCharMixin
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.cmd_base import translate_action
from NeoVintageous.nv.vi.cmd_base import translate_motion
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
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_d'


@assign(seqs.D, (SELECT,))
class ViDeleteMultipleCursor(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_d'


@assign(seqs.BIG_O, ACTION_MODES)
class ViInsertLineBefore(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_big_o'


@assign(seqs.O, (NORMAL,))
class ViInsertLineAfter(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = False
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_o'


@assign(seqs.O, (VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViGoToOtherEnd(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = False
        self.command = 'nv_vi_visual_o'


@assign(seqs.DEL, ACTION_MODES + (SELECT,))
@assign(seqs.X, ACTION_MODES + (SELECT,))
class ViRightDeleteChars(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.command = 'nv_vi_x'


@assign(seqs.S, ACTION_MODES + (SELECT,))
class ViSubstituteChar(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_s'


@assign(seqs.Y, ACTION_MODES)
class ViYankByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.command = 'nv_vi_y'


@assign(seqs.Y, (SELECT,))
class ViYankSelectByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_y'


@assign(seqs.EQUAL, ACTION_MODES)
class ViReindent(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_equal'


@assign(seqs.GREATER_THAN, ACTION_MODES)
class ViIndent(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_greater_than'


@assign(seqs.LESS_THAN, ACTION_MODES)
class ViUnindent(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_less_than'


@assign(seqs.C, ACTION_MODES)
class ViChangeByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_c'


@assign(seqs.C, (SELECT,))
class ViChangeMultipleCursor(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_c'


@assign(seqs.U, (NORMAL,))
class ViUndo(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_u'


@assign(seqs.U, (VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViChangeToLowerCaseByCharsVisual(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_visual_u'


@assign(seqs.CTRL_R, ACTION_MODES)
class ViRedo(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_ctrl_r'


@assign(seqs.BIG_D, ACTION_MODES)
class ViDeleteToEol(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_big_d'


@assign(seqs.BIG_C, ACTION_MODES)
class ViChangeToEol(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_big_c'


@assign(seqs.G_BIG_U_BIG_U, ACTION_MODES)
@assign(seqs.G_BIG_U_G_BIG_U, ACTION_MODES)
class ViChangeToUpperCaseByLines(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_g_big_u_big_u'


@assign(seqs.CC, ACTION_MODES)
class ViChangeLine(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_cc'


@assign(seqs.DD, ACTION_MODES)
class ViDeleteLine(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_dd'


@assign(seqs.BIG_R, ACTION_MODES)
class ViEnterReplaceMode(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_enter_replace_mode'


@assign(seqs.GREATER_THAN_GREATER_THAN, ACTION_MODES)
class ViIndentLine(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_greater_than_greater_than'


@assign(seqs.GUGU, ACTION_MODES)
@assign(seqs.GUU, ACTION_MODES)
class ViChangeToLowerCaseByLines(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_guu'


@assign(seqs.GU, ACTION_MODES)
class ViChangeToLowerCaseByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_gu'


@assign(seqs.EQUAL_EQUAL, ACTION_MODES)
class ViReindentLine(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_equal_equal'


@assign(seqs.LESS_THAN_LESS_THAN, ACTION_MODES)
class ViUnindentLine(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_less_than_less_than'


@assign(seqs.YY, ACTION_MODES)
@assign(seqs.BIG_Y, ACTION_MODES)
class ViYankLine(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_yy'


@assign(seqs.G_TILDE_TILDE, ACTION_MODES)
class ViInvertCaseByLines(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_g_tilde_g_tilde'


@assign(seqs.TILDE, ACTION_MODES)
class ViForceInvertCaseByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_tilde'


@assign(seqs.BIG_S, ACTION_MODES)
class ViSubstituteByLines(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_big_s'


@assign(seqs.G_TILDE, ACTION_MODES)
class ViInvertCaseByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_g_tilde'


@assign(seqs.G_BIG_U, ACTION_MODES)
class ViChangeToUpperCaseByChars(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True
        self.command = 'nv_vi_g_big_u'


@assign(seqs.BIG_J, ACTION_MODES)
class ViJoinLines(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_big_j'


@assign(seqs.CTRL_X, ACTION_MODES)
class ViDecrement(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_modify_numbers'
        self.command_args = {
            'subtract': True
        }


@assign(seqs.CTRL_A, ACTION_MODES)
class ViIncrement(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_modify_numbers'


@assign(seqs.G_BIG_J, ACTION_MODES)
class ViJoinLinesNoSeparator(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_big_j'
        self.command_args = {
            'dont_insert_or_remove_spaces': True
        }


@assign(seqs.V, ACTION_MODES)
class ViEnterVisualMode(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_enter_visual_mode'


@assign(seqs.Z_ENTER, ACTION_MODES)
@assign(seqs.ZT, ACTION_MODES)
class ViScrollToScreenTop(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_z_enter'


@assign(seqs.ZB, ACTION_MODES)
@assign(seqs.Z_MINUS, ACTION_MODES)
class ViScrollToScreenBottom(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_z_minus'


@assign(seqs.ZZ, ACTION_MODES)
class ViScrollToScreenCenter(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_zz'


@assign(seqs.Z_DOT, ACTION_MODES)
class ViZDot(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_zz'
        self.command_args = {
            'first_non_blank': True
        }


@assign(seqs.GQ, ACTION_MODES)
class ViReformat(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.motion_required = True
        self.scroll_into_view = True
        self.command = 'nv_vi_gq'


@assign(seqs.GQGQ, (NORMAL,))
@assign(seqs.GQQ, (NORMAL,))
class ViReformatLinewise(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_gq'
        self.command_args = {
            'linewise': True
        }


@assign(seqs.P, ACTION_MODES + (SELECT,))
class ViPasteAfter(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_paste'
        self.command_args = {
            'before_cursor': False
        }


@assign(seqs.BIG_P, ACTION_MODES + (SELECT,))
class ViPasteBefore(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_paste'
        self.command_args = {
            'before_cursor': True
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_BIG_P, ACTION_MODES + (SELECT,))
@assign(seqs.RIGHT_SQUARE_BRACKET_P, ACTION_MODES + (SELECT,))
class ViPasteAfterAndIndent(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_paste'
        self.command_args = {
            'before_cursor': False,
            'adjust_indent': True
        }


@assign(seqs.LEFT_SQUARE_BRACKET_BIG_P, ACTION_MODES + (SELECT,))
@assign(seqs.LEFT_SQUARE_BRACKET_P, ACTION_MODES + (SELECT,))
class ViPasteBeforeAndIndent(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_paste'
        self.command_args = {
            'before_cursor': True,
            'adjust_indent': True
        }


@assign(seqs.GP, ACTION_MODES + (SELECT,))
class ViPasteAfterWithAdjustedCursor(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_paste'
        self.command_args = {
            'before_cursor': False,
            'adjust_cursor': True
        }


@assign(seqs.G_BIG_P, ACTION_MODES + (SELECT,))
class ViPasteBeforeWithAdjustedCursor(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_paste'
        self.command_args = {
            'before_cursor': True,
            'adjust_cursor': True
        }


@assign(seqs.BIG_X, ACTION_MODES)
class ViLeftDeleteChar(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_big_x'


@assign(seqs.CTRL_PAGEDOWN, ACTION_MODES)
@assign(seqs.GT, ACTION_MODES)
class ViActivateNextTab(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True

    def translate(self, view):
        return translate_action(view, 'nv_vi_gt', {
            'count': get_count(view, default=0)
        })


@assign(seqs.CTRL_PAGEUP, ACTION_MODES)
@assign(seqs.G_BIG_T, ACTION_MODES)
class ViActivatePreviousTab(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_g_big_t'


@assign(seqs.CTRL_W, (INSERT,))
class ViDeleteUpToCursor(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'


@assign(seqs.CTRL_W_B, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_B, ACTION_MODES)
class ViMoveCursorToBottomRightWindow(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'b'
        }


@assign(seqs.CTRL_W_BIG_H, ACTION_MODES)
class ViMoveCurrentWindowToFarLeft(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'H'
        }


@assign(seqs.CTRL_W_BIG_J, ACTION_MODES)
class ViMoveCurrentWindowToVeryTop(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'J'
        }


@assign(seqs.CTRL_W_BIG_K, ACTION_MODES)
class ViMoveCurrentWindowToVeryBottom(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'K'
        }


@assign(seqs.CTRL_6, ACTION_MODES)
@assign(seqs.CTRL_HAT, ACTION_MODES)
class ViGotoAlternateFile(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_hat'


@assign(seqs.CTRL_W_BIG_L, ACTION_MODES)
class ViMoveCurrentWindowToFarRight(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'L'
        }


@assign(seqs.CTRL_W_C, ACTION_MODES)
class ViCloseTheCurrentWindow(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'c'
        }


@assign(seqs.CTRL_W_EQUAL, ACTION_MODES)
class ViMakeAllWindowsAlmostEquallyHighAndWide(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '='
        }


@assign(seqs.CTRL_W_GREATER_THAN, ACTION_MODES)
class ViIncreaseCurrentWindowWidthByN(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '>',
        }


@assign(seqs.CTRL_W_H, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_H, ACTION_MODES)
@assign(seqs.CTRL_W_LEFT, ACTION_MODES)
@assign(seqs.CTRL_W_BACKSPACE, ACTION_MODES)
class ViMoveCursorToNthWindowLeftOfCurrentOne(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'h',
        }


@assign(seqs.CTRL_W_J, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_J, ACTION_MODES)
@assign(seqs.CTRL_W_DOWN, ACTION_MODES)
class ViMoveCursorToNthWindowBelowOfCurrentOne(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'j',
        }


@assign(seqs.CTRL_W_K, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_K, ACTION_MODES)
@assign(seqs.CTRL_W_UP, ACTION_MODES)
class ViMoveCursorToNthWindowAboveCurrentOne(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'k',
        }


@assign(seqs.CTRL_W_L, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_L, ACTION_MODES)
@assign(seqs.CTRL_W_RIGHT, ACTION_MODES)
class ViMoveCursorToNthWindowRightOfCurrentOne(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'l',
        }


@assign(seqs.CTRL_W_LESS_THAN, ACTION_MODES)
class ViDecreaseCurrentWindowWidthByN(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '<',
        }


@assign(seqs.CTRL_W_MINUS, ACTION_MODES)
class ViDecreaseCurrentWindowHeightByN(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '-',
        }


@assign(seqs.CTRL_W_N, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_N, ACTION_MODES)
class ViCreateNewWindowAndStartEditingAnEmptyFileInIt(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'n',
        }


@assign(seqs.CTRL_W_O, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_O, ACTION_MODES)
class ViMakeTheCurrentWindowTheOnlyOneOnTheScreen(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'o'
        }


@assign(seqs.CTRL_W_BAR, ACTION_MODES)
class ViSetCurrentWindowWidthToNOrWidestPossible(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '|',
        }


@assign(seqs.CTRL_W_PLUS, ACTION_MODES)
class ViIncreaseCurrentWindowHeightByN(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '+',
        }


@assign(seqs.CTRL_W_Q, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_Q, ACTION_MODES)
class ViQuitTheCurrentWindow(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'q'
        }


@assign(seqs.CTRL_W_S, ACTION_MODES)
@assign(seqs.CTRL_W_BIG_S, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_S, ACTION_MODES)
class ViSplitTheCurrentWindowInTwo(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 's',
        }


@assign(seqs.CTRL_W_T, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_T, ACTION_MODES)
class ViMoveCursorToTopLeftWindow(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 't'
        }


@assign(seqs.CTRL_W_UNDERSCORE, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_UNDERSCORE, ACTION_MODES)
class ViSetCurrentGroupHeightOrHighestPossible(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': '_',
        }


@assign(seqs.CTRL_W_V, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_V, ACTION_MODES)
class ViSplitTheCurrentWindowInTwoVertically(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'v',
        }


@assign(seqs.CTRL_W_BIG_W, ACTION_MODES)
class ViCtrlW_W(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'W',
        }


@assign(seqs.CTRL_W_X, ACTION_MODES)
@assign(seqs.CTRL_W_CTRL_X, ACTION_MODES)
class ViExchangeCurrentWindowWithNextOrPreviousNthWindow(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': 'x',
        }


@assign(seqs.BIG_V, ACTION_MODES)
class ViEnterVisualLineMode(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_enter_visual_line_mode'


@assign(seqs.GV, ACTION_MODES)
class ViRestoreVisualSelections(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_gv'


@assign(seqs.GX, ACTION_MODES)
class ViNetrwGx(ViOperatorDef):
    def init(self):
        self.command = 'nv_vi_gx'


@assign(seqs.CTRL_O, ACTION_MODES)
class ViJumpBack(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_jump_back'


@assign(seqs.CTRL_I, ACTION_MODES)
@assign(seqs.TAB, ACTION_MODES)
class ViJumpForward(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_jump_forward'


@assign(seqs.DOT, ACTION_MODES)
class ViRepeat(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_dot'


@assign(seqs.CTRL_Y, ACTION_MODES)
class ViScrollByLinesUp(ViMotionDef):
    def init(self):
        self.command = 'nv_vi_ctrl_y'


@assign(seqs.BIG_U, (VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViChangeToUpperCaseByCharsVisual(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True
        self.command = 'nv_vi_visual_big_u'


@assign(seqs.CTRL_E, ACTION_MODES)
class ViScrollByLinesDown(ViMotionDef):
    def init(self):
        self.command = 'nv_vi_ctrl_e'


@assign(seqs.AT, ACTION_MODES)
class ViOpenMacrosForRepeating(RequireOneCharMixin, ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return translate_action(view, 'nv_vi_at', {
            'name': self.inp
        })


@assign(seqs.Q, ACTION_MODES)
class ViToggleMacroRecorder(RequireOneCharMixin, ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return translate_action(view, 'nv_vi_q', {
            'name': self.inp
        })


@assign(seqs.CTRL_V, ACTION_MODES)
class ViEnterVisualBlockMode(ViOperatorDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_enter_visual_block_mode'


@assign(seqs.GA, ACTION_MODES)
class ViShowAsciiValueOfChar(ViOperatorDef):
    def init(self):
        self.command = 'nv_vi_ga'


@assign(seqs.CTRL_W_GF, ACTION_MODES)
@assign(seqs.GF, ACTION_MODES)
class Vigf(ViOperatorDef):
    def init(self):
        self.command = 'nv_vi_g'
        self.command_args = {
            'action': 'f'
        }


@assign(seqs.CTRL_W_G_BIG_F, ACTION_MODES)
@assign(seqs.G_BIG_F, ACTION_MODES)
class VigF(ViOperatorDef):
    def init(self):
        self.command = 'nv_vi_g'
        self.command_args = {
            'action': 'F'
        }


@assign(seqs.I, (NORMAL, SELECT))
@assign(seqs.INSERT, (NORMAL, SELECT))
class ViEnterInserMode(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.glue_until_normal_mode = True
        self.command = 'nv_enter_insert_mode'


@assign(seqs.V, (SELECT, ))
@assign(seqs.ESC, ACTION_MODES)
@assign(seqs.CTRL_C, ACTION_MODES + (INSERT, SELECT))
@assign(seqs.CTRL_LEFT_SQUARE_BRACKET, ACTION_MODES + (INSERT, SELECT))
class ViEnterNormalMode(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_enter_normal_mode'


@assign(seqs.CTRL_RIGHT_SQUARE_BRACKET, ACTION_MODES)
class ViJumpToDefinition(ViOperatorDef):
    def init(self):
        self.command = 'nv_vi_ctrl_right_square_bracket'


@assign(seqs.CTRL_W_CTRL_RIGHT_SQUARE_BRACKET, ACTION_MODES)
@assign(seqs.CTRL_W_RIGHT_SQUARE_BRACKET, ACTION_MODES)
class ViSplitAndJumpToDefinition(ViOperatorDef):
    def init(self):
        self.command = 'nv_vi_ctrl_w'
        self.command_args = {
            'action': ']'
        }


@assign(seqs.A, (NORMAL,))
class ViInsertAfterChar(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_a'


@assign(seqs.BIG_A, ACTION_MODES)
class ViInsertAtEol(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_big_a'


@assign(seqs.BIG_I, ACTION_MODES + (SELECT,))
class ViInsertAtBol(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.glue_until_normal_mode = True
        self.command = 'nv_vi_big_i'


@assign(seqs.COLON, ACTION_MODES)
class ViEnterCommandLineMode(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_cmdline'


@assign(seqs.CTRL_G, ACTION_MODES)
class ViShowFileStatus(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_g'


@assign(seqs.BIG_Z_BIG_Q, (NORMAL,))
class ViExitEditor(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_big_z_big_q'


@assign(seqs.BIG_Z_BIG_Z, (NORMAL,))
class ViCloseFile(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_big_z_big_z'


@assign(seqs.G_BIG_D, ACTION_MODES)
class ViGotoSymbolInProject(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.command = 'nv_vi_go_to_symbol'
        self.command_args = {
            'globally': True
        }


@assign(seqs.GD, MOTION_MODES)
class ViGotoSymbolInFile(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_go_to_symbol'
        self.command_args = {
            'globally': False
        }


@assign(seqs.ALT_RIGHT, MOTION_MODES)
@assign(seqs.L, MOTION_MODES)
@assign(seqs.RIGHT, MOTION_MODES)
@assign(seqs.SPACE, MOTION_MODES)
class ViMoveRightByChars(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_l'


@assign(seqs.SHIFT_ENTER, MOTION_MODES)
class ViShiftEnterMotion(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_shift_enter'


@assign(seqs.B, MOTION_MODES)
@assign(seqs.SHIFT_LEFT, MOTION_MODES)
class ViMoveByWordsBackward(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_b'


@assign(seqs.BIG_B, MOTION_MODES)
@assign(seqs.CTRL_LEFT, MOTION_MODES)
class ViMoveByBigWordsBackward(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_big_b'


@assign(seqs.BIG_W, MOTION_MODES)
@assign(seqs.CTRL_RIGHT, MOTION_MODES)
class ViMoveByBigWords(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_big_w'


@assign(seqs.E, MOTION_MODES)
class ViMoveByWordEnds(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_e'


@assign(seqs.BIG_H, MOTION_MODES)
class ViGotoScreenTop(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_big_h'


@assign(seqs.GE, MOTION_MODES)
class ViMoveByWordEndsBackward(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_ge'


@assign(seqs.G_BIG_E, MOTION_MODES)
class ViMoveByBigWordEndsBackward(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_g_big_e'


@assign(seqs.BIG_L, MOTION_MODES)
class ViGotoScreenBottom(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_big_l'


@assign(seqs.BIG_M, MOTION_MODES)
class ViGotoScreenMiddle(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_big_m'


@assign(seqs.CTRL_D, MOTION_MODES)
class ViMoveHalfScreenDown(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = False

    def translate(self, view):
        return translate_motion(view, 'nv_vi_ctrl_d', {
            'count': get_count(view, default=0)
        })


@assign(seqs.CTRL_U, MOTION_MODES + (INSERT,))
class ViMoveHalfScreenUp(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_ctrl_u', {
            'count': get_count(view, default=0)
        })


@assign(seqs.CTRL_F, MOTION_MODES)
@assign(seqs.PAGE_DOWN, MOTION_MODES)
@assign(seqs.SHIFT_DOWN, MOTION_MODES)
class ViMoveScreenDown(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_f'


@assign(seqs.CTRL_B, MOTION_MODES)
@assign(seqs.PAGE_UP, MOTION_MODES)
@assign(seqs.SHIFT_UP, MOTION_MODES)
class ViMoveScreenUp(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_ctrl_b'


@assign(seqs.BACKTICK, MOTION_MODES)
class ViGotoExactMarkXpos(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_backtick', {
            'character': self.inp
        })


@assign(seqs.DOLLAR, MOTION_MODES)
@assign(seqs.END, MOTION_MODES)
class ViMoveToEol(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_dollar'


@assign(seqs.ENTER, MOTION_MODES)
@assign(seqs.PLUS, MOTION_MODES)
class ViMotionEnter(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_enter'


@assign(seqs.MINUS, MOTION_MODES)
class ViMoveBackOneLine(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_minus'


@assign(seqs.G_UNDERSCORE, MOTION_MODES)
class ViMoveToSoftEol(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_g__'


@assign(seqs.G_DOWN, MOTION_MODES)
@assign(seqs.GJ, MOTION_MODES)
class ViMoveByScreenLineDown(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_gj'


@assign(seqs.G_UP, MOTION_MODES)
@assign(seqs.GK, MOTION_MODES)
class ViMoveByScreenLineUp(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_gk'


@assign(seqs.LEFT_BRACE, MOTION_MODES)
class ViMoveByBlockUp(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_left_brace'


@assign(seqs.SEMICOLON, MOTION_MODES)
class ViRepeatCharSearchForward(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    # TODO Refactor settings dependencies into the command being called
    def translate(self, view):
        last_search_cmd = get_last_char_search_command(view)
        if 'sneak' in last_search_cmd:
            return translate_motion(view, 'nv_sneak', {
                'forward': last_search_cmd == 'sneak_s',
                'save': False
            })

        forward = last_search_cmd in ('vi_t', 'vi_f')
        inclusive = last_search_cmd in ('vi_f', 'vi_big_f')
        skipping = last_search_cmd in ('vi_t', 'vi_big_t')
        motion = 'nv_vi_find_in_line' if forward else 'nv_vi_reverse_find_in_line'

        return translate_motion(view, motion, {
            'char': get_last_char_search_character(view),
            'inclusive': inclusive,
            'skipping': skipping,
            'save': False
        })


@assign(seqs.QUOTE, MOTION_MODES)
class ViGotoMark(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_quote', {
            'character': self.inp
        })


@assign(seqs.RIGHT_BRACE, MOTION_MODES)
class ViMoveByBlockDown(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_right_brace'


@assign(seqs.LEFT_PAREN, MOTION_MODES)
class ViMoveBySentenceUp(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_left_paren'


@assign(seqs.RIGHT_PAREN, MOTION_MODES)
class ViMoveBySentenceDown(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_right_paren'


@assign(seqs.LEFT_SQUARE_BRACKET_LEFT_BRACE, MOTION_MODES)
class ViGotoOpeningBrace(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_left_square_bracket'
        self.command_args = {
            'action': 'target',
            'target': '{'
        }


@assign(seqs.LEFT_SQUARE_BRACKET_LEFT_PAREN, MOTION_MODES)
class ViGotoOpeningParen(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_left_square_bracket'
        self.command_args = {
            'action': 'target',
            'target': '('
        }


@assign(seqs.LEFT_SQUARE_BRACKET_C, ACTION_MODES)
class ViBackwardToStartOfChange(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_left_square_bracket'
        self.command_args = {
            'action': 'c',
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_C, ACTION_MODES)
class ViForwardToStartOfChange(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_right_square_bracket'
        self.command_args = {
            'action': 'c',
        }


@assign(seqs.LEFT_SQUARE_BRACKET_S, ACTION_MODES)
class ViPrevMisppelledWord(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_left_square_bracket'
        self.command_args = {
            'action': 's',
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_S, ACTION_MODES)
class ViNextMispelledWord(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_right_square_bracket'
        self.command_args = {
            'action': 's',
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_RIGHT_BRACE, MOTION_MODES)
class ViGotoClosingBrace(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_right_square_bracket'
        self.command_args = {
            'action': 'target',
            'target': '}'
        }


@assign(seqs.RIGHT_SQUARE_BRACKET_RIGHT_PAREN, MOTION_MODES)
class ViGotoClosingParen(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_right_square_bracket'
        self.command_args = {
            'action': 'target',
            'target': ')'
        }


@assign(seqs.PERCENT, MOTION_MODES)
class ViPercent(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_percent', {
            'count': get_count(view, default=0)
        })


@assign(seqs.BACKSLASH, MOTION_MODES)
@assign(seqs.COMMA, MOTION_MODES)
class ViRepeatCharSearchBackward(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True

    # TODO Refactor settings dependencies into the command being called
    def translate(self, view):
        last_search_cmd = get_last_char_search_command(view)
        if 'sneak' in last_search_cmd:
            return translate_motion(view, 'nv_sneak', {
                'forward': last_search_cmd == 'sneak_big_s',
                'save': False
            })

        forward = last_search_cmd in ('vi_t', 'vi_f')
        inclusive = last_search_cmd in ('vi_f', 'vi_big_f')
        skipping = last_search_cmd in ('vi_t', 'vi_big_t')
        motion = 'nv_vi_find_in_line' if not forward else 'nv_vi_reverse_find_in_line'

        return translate_motion(view, motion, {
            'char': get_last_char_search_character(view),
            'inclusive': inclusive,
            'skipping': skipping,
            'save': False
        })


@assign(seqs.BAR, MOTION_MODES)
class ViMoveByLineCols(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_bar'


@assign(seqs.BIG_E, MOTION_MODES)
class ViMoveByBigWordEnds(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_big_e'


@assign(seqs.ALT_LEFT, MOTION_MODES)
@assign(seqs.BACKSPACE, MOTION_MODES)
@assign(seqs.CTRL_BACKSPACE, MOTION_MODES)
@assign(seqs.CTRL_H, MOTION_MODES)
@assign(seqs.H, MOTION_MODES)
@assign(seqs.LEFT, MOTION_MODES)
class ViMoveLeftByChars(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_h'


@assign(seqs.SHIFT_RIGHT, MOTION_MODES)
@assign(seqs.W, MOTION_MODES)
class ViMoveByWords(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_w'


@assign(seqs.CTRL_DOWN, MOTION_MODES)
@assign(seqs.CTRL_J, MOTION_MODES)
@assign(seqs.CTRL_N, MOTION_MODES)
@assign(seqs.DOWN, MOTION_MODES)
@assign(seqs.J, MOTION_MODES)
class ViMoveDownByLines(ViMotionDef):
    def init(self):
        self.scroll_into_view = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_j', {
            'xpos': get_xpos(view)
        })


@assign(seqs.CTRL_P, MOTION_MODES)
@assign(seqs.CTRL_UP, MOTION_MODES)
@assign(seqs.K, MOTION_MODES)
@assign(seqs.UP, MOTION_MODES)
class ViMoveUpByLines(ViMotionDef):
    def init(self):
        self.scroll_into_view = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_k', {
            'xpos': get_xpos(view)
        })


@assign(seqs.HAT, MOTION_MODES)
@assign(seqs.HOME, MOTION_MODES)
class ViMoveToBol(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_hat'


@assign(seqs.UNDERSCORE, MOTION_MODES)
class ViMoveToSoftBol(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_underscore'


@assign(seqs.KEYPAD_0, MOTION_MODES)
@assign(seqs.ZERO, MOTION_MODES)
class ViMoveToHardBol(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_zero'


@assign(seqs.GN, MOTION_MODES)
class ViSearchLastUsedPattern(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_search'


@assign(seqs.G_BIG_N, MOTION_MODES)
class ViSearchLastUsedPatternReverse(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_search'
        self.command_args = {
            'forward': False
        }


@assign(seqs.N, MOTION_MODES)
class ViRepeatSearchForward(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_repeat_buffer_search'
        self.command_args = {
            'reverse': False
        }


@assign(seqs.BIG_N, MOTION_MODES)
class ViRepeatSearchBackward(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_repeat_buffer_search'
        self.command_args = {
            'reverse': True
        }


@assign(seqs.STAR, MOTION_MODES)
class ViFindWord(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_star'


@assign(seqs.OCTOTHORP, MOTION_MODES)
class ViReverseFindWord(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_octothorp'


@assign(seqs.BIG_Z, MOTION_MODES)
@assign(seqs.CTRL_K, MOTION_MODES)
@assign(seqs.CTRL_W, MOTION_MODES)
@assign(seqs.CTRL_W_G, MOTION_MODES)
@assign(seqs.CTRL_X, (INSERT,))
@assign(seqs.G, MOTION_MODES)
@assign(seqs.LEFT_SQUARE_BRACKET, MOTION_MODES)
@assign(seqs.RIGHT_SQUARE_BRACKET, MOTION_MODES)
@assign(seqs.Z, MOTION_MODES)
@assign(seqs.ZU, MOTION_MODES)
class ViOpenNameSpace(ViMotionDef):  # TODO This should not be a motion.

    def translate(self, view):
        return {}


@assign(seqs.DOUBLE_QUOTE, MOTION_MODES)
class ViOpenRegister(ViMotionDef):

    def translate(self, view):
        return {}


@assign(seqs.CTRL_HOME, MOTION_MODES)
@assign(seqs.GG, MOTION_MODES)
class ViGotoBof(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_gg', {
            'count': get_count(view, default=0)
        })


@assign(seqs.BIG_G, MOTION_MODES)
class ViGotoEof(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_big_g', {
            'count': get_count(view, default=0)
        })


@assign(seqs.R, ACTION_MODES)
class ViReplaceCharacters(RequireOneCharMixin, ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True

    def translate(self, view):
        return translate_action(view, 'nv_vi_r', {
            'char': self.inp
        })


@assign(seqs.M, ACTION_MODES)
class ViSetMark(RequireOneCharMixin, ViOperatorDef):
    def init(self):
        self.scroll_into_view = True

    def translate(self, view):
        return translate_action(view, 'nv_vi_m', {
            'character': self.inp
        })


@assign(seqs.F, MOTION_MODES)
class ViSearchCharForward(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_find_in_line', {
            'char': self.inp,
            'inclusive': True
        })


@assign(seqs.T, MOTION_MODES)
class ViSearchCharForwardTill(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_find_in_line', {
            'char': self.inp,
            'inclusive': False
        })


@assign(seqs.A, (OPERATOR_PENDING, VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViATextObject(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_select_text_object', {
            'text_object': self.inp,
            'inclusive': True
        })


@assign(seqs.I, (OPERATOR_PENDING, VISUAL, VISUAL_LINE, VISUAL_BLOCK))
class ViITextObject(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_select_text_object', {
            'text_object': self.inp,
            'inclusive': False
        })


@assign(seqs.BIG_F, MOTION_MODES)
class ViSearchCharBackward(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_reverse_find_in_line', {
            'char': self.inp,
            'inclusive': True
        })


@assign(seqs.BIG_T, MOTION_MODES)
class ViSearchCharBackwardTill(RequireOneCharMixin, ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_reverse_find_in_line', {
            'char': self.inp,
            'inclusive': False
        })


@assign(seqs.SLASH, MOTION_MODES)
class ViSearchForward(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = InputParser(
            InputParser.PANEL,
            command='nv_vi_slash',
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

    def translate(self, view):
        if self.accept_input:
            return translate_motion(view, 'nv_vi_slash')

        # We'll end up here, for example, when repeating via '.'.
        return ViSearchForwardImpl(term=self.inp[:-4]).translate(view)


class ViSearchForwardImpl(ViMotionDef):
    def __init__(self, *args, term='', **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.inp = term
        self.updates_xpos = True

    def translate(self, view):
        return translate_motion(view, 'nv_vi_slash_impl', {
            'pattern': self.inp,
        })


@assign(seqs.QUESTION_MARK, MOTION_MODES)
class ViSearchBackward(ViMotionDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = InputParser(
            InputParser.PANEL,
            command='nv_vi_question_mark',
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

    def translate(self, view):
        if self.accept_input:
            return translate_motion(view, 'nv_vi_question_mark')

        # We'll end up here, for example, when repeating via '.'.
        return ViSearchBackwardImpl(term=self.inp[:-4]).translate(view)


class ViSearchBackwardImpl(ViMotionDef):
    def __init__(self, *args, term='', **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inp = term

    def translate(self, view):
        return translate_motion(view, 'nv_vi_question_mark_impl', {
            'pattern': self.inp,
        })


@assign(seqs.CTRL_X_CTRL_L, (INSERT,))
class ViInsertLineWithCommonPrefix(ViOperatorDef):
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True
        self.command = 'nv_vi_ctrl_x_ctrl_l'


@assign(seqs.GM, MOTION_MODES)
class ViMoveHalfScreenHorizontally(ViMotionDef):
    def init(self):
        self.updates_xpos = True
        self.scroll_into_view = True
        self.command = 'nv_vi_gm'


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
    def init(self):
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, view):
        return translate_action(view, 'nv_vi_z', {
            'action': get_partial_sequence(view)[1:],
        })
