from NeoVintageous.lib.vi import inputs
from NeoVintageous.lib.vi import keys
from NeoVintageous.lib.vi import utils
from NeoVintageous.lib.vi.cmd_base import ViMotionDef
from NeoVintageous.lib.vi.cmd_base import ViOperatorDef
from NeoVintageous.lib.vi.inputs import parser_def
from NeoVintageous.lib.vi.keys import seqs
from NeoVintageous.lib.vi.utils import INPUT_INMEDIATE
from NeoVintageous.lib.vi.utils import INPUT_VIA_PANEL
from NeoVintageous.lib.vi.utils import modes


_MODES_MOTION = (
    modes.NORMAL,
    modes.OPERATOR_PENDING,
    modes.VISUAL,
    modes.VISUAL_LINE,
    modes.VISUAL_BLOCK
)

_MODES_ACTION = (
    modes.NORMAL,
    modes.VISUAL,
    modes.VISUAL_LINE,
    modes.VISUAL_BLOCK
)


@keys.assign(seq=seqs.D, modes=_MODES_ACTION)
class ViDeleteByChars(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = '_vi_d'
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': self.command,
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@keys.assign(seq=seqs.BIG_O, modes=_MODES_ACTION)
class ViInsertLineBefore(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = '_vi_big_o'
        self.scroll_into_view = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': self.command,
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.O, modes=_MODES_ACTION)
class ViInsertLineAfter(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = False

    def translate(self, state):
        # XXX: Create a separate command?
        if state.mode in (modes.VISUAL, modes.VISUAL_LINE):
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


@keys.assign(seq=seqs.X, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.S, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.Y, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.EQUAL, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GREATER_THAN, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.LESS_THAN, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.C, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.U, modes=[modes.NORMAL])
class ViUndo(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_u',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.U, modes=[modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK])
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


@keys.assign(seq=seqs.CTRL_R, modes=_MODES_ACTION)
class ViRedo(ViOperatorDef):
    def __init__(self, inclusive=False, *args, **kwargs):
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


@keys.assign(seq=seqs.BIG_D, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.BIG_C, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.G_BIG_U_BIG_U, modes=_MODES_ACTION)
@keys.assign(seq=seqs.G_BIG_U_G_BIG_U, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.CC, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.DD, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.BIG_R, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GREATER_THAN_GREATER_THAN, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GUGU, modes=_MODES_ACTION)
@keys.assign(seq=seqs.GUU, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GU, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.EQUAL_EQUAL, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.LESS_THAN_LESS_THAN, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.YY, modes=_MODES_ACTION)
@keys.assign(seq=seqs.BIG_Y, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.G_TILDE_TILDE, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.TILDE, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.BIG_S, modes=_MODES_ACTION)
class ViSubstituteByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': '_vi_big_s_action',
            'action_args': {
                'mode': state.mode,
                'count': 1,
                'register': state.register
            }
        }


@keys.assign(seq=seqs.G_TILDE, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.G_BIG_U, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.BIG_J, modes=_MODES_ACTION + (modes.SELECT,))
class ViJoinLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        if state.mode == modes.SELECT:
            return {
                'action': '_vi_select_big_j',
                'action_args': {
                    'mode': state.mode,
                    'count': state.count
                }
            }
        else:
            return {
                'action': '_vi_big_j',
                'action_args': {
                    'mode': state.mode,
                    'count': state.count
                }
            }


@keys.assign(seq=seqs.CTRL_X, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.CTRL_A, modes=_MODES_ACTION)
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


# FIXME: Doesn't work.
@keys.assign(seq=seqs.G_BIG_J, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.V, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.Z_ENTER, modes=_MODES_ACTION)
@keys.assign(seq=seqs.ZT, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.ZB, modes=_MODES_ACTION)
@keys.assign(seq=seqs.Z_MINUS, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.ZZ, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GQ, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.P, modes=_MODES_ACTION)
class ViPasteAfter(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_p',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@keys.assign(seq=seqs.BIG_P, modes=_MODES_ACTION)
class ViPasteBefore(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_big_p',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'register': state.register
            }
        }


@keys.assign(seq=seqs.BIG_X, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GT, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.G_BIG_T, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.CTRL_W_B, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_B, modes=_MODES_ACTION)
class ViMoveCursorToBottomRightWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_b',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_BIG_H, modes=_MODES_ACTION)
class ViMoveCurrentWindowToFarLeft(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_big_h',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_BIG_J, modes=_MODES_ACTION)
class ViMoveCurrentWindowToVeryTop(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_big_j',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_BIG_K, modes=_MODES_ACTION)
class ViMoveCurrentWindowToVeryBottom(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_big_k',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_BIG_L, modes=_MODES_ACTION)
class ViMoveCurrentWindowToFarRight(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_big_l',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_C, modes=_MODES_ACTION)
class ViCloseTheCurrentWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_c',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_EQUAL, modes=_MODES_ACTION)
class ViMakeAllWindowsAlmostEquallyHighAndWide(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_equal',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_GREATER_THAN, modes=_MODES_ACTION)
class ViIncreaseCurrentWindowWidthByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_greater_than',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_H, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_H, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_LEFT, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_BACKSPACE, modes=_MODES_ACTION)
class ViMoveCursorToNthWindowLeftOfCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_h',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_J, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_J, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_DOWN, modes=_MODES_ACTION)
class ViMoveCursorToNthWindowBelowOfCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_j',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_K, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_K, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_UP, modes=_MODES_ACTION)
class ViMoveCursorToNthWindowAboveCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_k',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_L, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_L, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_RIGHT, modes=_MODES_ACTION)
class ViMoveCursorToNthWindowRightOfCurrentOne(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_l',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_LESS_THAN, modes=_MODES_ACTION)
class ViDecreaseCurrentWindowWidthByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_less_than',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_MINUS, modes=_MODES_ACTION)
class ViDecreaseCurrentWindowHeightByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_minus',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_N, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_N, modes=_MODES_ACTION)
class ViCreateNewWindowAndStartEditingAnEmptyFileInIt(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_n',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_O, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_O, modes=_MODES_ACTION)
class ViMakeTheCurrentWindowTheOnlyOneOnTheScreen(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_o',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_PIPE, modes=_MODES_ACTION)
class ViSetCurrentWindowWidthToNOrWidestPossible(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_pipe',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_PLUS, modes=_MODES_ACTION)
class ViIncreaseCurrentWindowHeightByN(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_plus',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_Q, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_Q, modes=_MODES_ACTION)
class ViQuitTheCurrentWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_q',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_S, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_BIG_S, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_S, modes=_MODES_ACTION)
class ViSplitTheCurrentWindowInTwo(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_s',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_T, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_T, modes=_MODES_ACTION)
class ViMoveCursorToTopLeftWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_t',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_W_UNDERSCORE, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_UNDERSCORE, modes=_MODES_ACTION)
class ViSetCurrentGroupHeightOrHighestPossible(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_underscore',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_V, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_V, modes=_MODES_ACTION)
class ViSplitTheCurrentWindowInTwoVertically(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_v',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_W_X, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_W_CTRL_X, modes=_MODES_ACTION)
class ViExchangeCurrentWindowWithNextOrPreviousNthWindow(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_w_x',
            'action_args': {
                'count': state.count
            }
        }


@keys.assign(seq=seqs.BIG_V, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GV, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.GX, modes=_MODES_ACTION)
class NetrwGx(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_vi_gx',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_K_CTRL_B, modes=_MODES_ACTION)
class StToggleSidebar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'toggle_side_bar',
            'action_args': {}
        }


@keys.assign(seq=seqs.COMMAND_BIG_B, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_SHIFT_B, modes=_MODES_ACTION)
class StShowBuildSystemsMenu(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'build',
            'action_args': {
                'select': True
            }
        }


@keys.assign(seq=seqs.COMMAND_BIG_F, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_BIG_F, modes=_MODES_ACTION)
class StFinInFiles(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'show_panel',
            'action_args': {
                'panel': 'find_in_files'
            }
        }


@keys.assign(seq=seqs.CTRL_O, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.CTRL_I, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.SHIFT_CTRL_F12, modes=_MODES_ACTION)
class StGotoSymbolInProject(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'goto_symbol_in_project',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_F12, modes=_MODES_ACTION)
class StGotoSymbolInFile(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'show_overlay',
            'action_args': {
                'overlay': 'goto',
                'text': '@'
            }
        }


@keys.assign(seq=seqs.F12, modes=_MODES_ACTION)
class StGotoDefinition(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'goto_definition',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_F2, modes=_MODES_ACTION)
class StToggleBookmark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'toggle_bookmark',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_SHIFT_F2, modes=_MODES_ACTION)
class StClearBookmarks(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'clear_bookmarks',
            'action_args': {}
        }


@keys.assign(seq=seqs.F2, modes=_MODES_ACTION)
class StPrevBookmark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'prev_bookmark',
            'action_args': {}
        }


@keys.assign(seq=seqs.SHIFT_F2, modes=_MODES_ACTION)
class StNextBookmark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'next_bookmark',
            'action_args': {}
        }


@keys.assign(seq=seqs.DOT, modes=_MODES_ACTION)
class ViRepeat(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['action'] = '_vi_dot'
        cmd['action_args'] = {
            'mode': state.mode,
            'count': state.count,
            'repeat_data': state.repeat_data,
        }

        return cmd


@keys.assign(seq=seqs.CTRL_R, modes=_MODES_ACTION)
class ViOpenRegisterFromInsertMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_r',
            'action_args': {
                'count': state.count,
                'mode': state.mode
            }
        }


@keys.assign(seq=seqs.CTRL_Y, modes=_MODES_ACTION)
class ViScrollByLinesUp(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_y',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.BIG_U, modes=[modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK])
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


@keys.assign(seq=seqs.CTRL_E, modes=_MODES_ACTION)
class ViScrollByLinesDown(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_ctrl_e',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.F11, modes=_MODES_ACTION)
class StToggleFullScreen(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'toggle_full_screen',
            'action_args': {}
        }


@keys.assign(seq=seqs.F7, modes=_MODES_ACTION)
class StBuild(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'build',
            'action_args': {}
        }


@keys.assign(seq=seqs.SHIFT_F4, modes=_MODES_ACTION)
class StFindPrev(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'find_prev',
            'action_args': {}
        }


@keys.assign(seq=seqs.AT, modes=_MODES_ACTION)
class ViOpenMacrosForRepeating(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        assert len(key) == 1, '`@` only accepts a single char'
        self._inp = key

        return True

    def translate(self, state):
        return {
            'action': '_vi_at',
            'action_args': {
                'name': self.inp,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.Q, modes=_MODES_ACTION)
class ViToggleMacroRecorder(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        assert len(key) == 1, '`q` only accepts a single char'
        self._inp = key

        return True

    def translate(self, state):
        return {
            'action': '_vi_q',
            'action_args': {
                'name': self.inp
            }
        }


@keys.assign(seq=seqs.F3, modes=_MODES_ACTION)
class StFindNext(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'find_next',
            'action_args': {}
        }


@keys.assign(seq=seqs.F4, modes=_MODES_ACTION)
class StFindNextResult(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'next_result',
            'action_args': {}
        }


@keys.assign(seq=seqs.SHIFT_F4, modes=_MODES_ACTION)
class StFindPrevResult(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'prev_result',
            'action_args': {}
        }


@keys.assign(seq=seqs.G_BIG_H, modes=_MODES_ACTION)
class ViEnterSelectModeForSearch(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_g_big_h',
            'action_args': {}
        }


@keys.assign(seq=seqs.SHIFT_F4, modes=_MODES_ACTION)
class StPrevResult(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'prev_result',
            'action_args': {}
        }


@keys.assign(seq=seqs.GH, modes=_MODES_ACTION)
class ViEnterSelectMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_enter_select_mode',
            'action_args': {
                'mode': state.mode
            }
        }


@keys.assign(seq=seqs.CTRL_V, modes=_MODES_ACTION)
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


@keys.assign(seq=seqs.COMMAND_P, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_P, modes=_MODES_ACTION)
class StShowGotoAnything(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'show_overlay',
            'action_args': {
                'overlay': 'goto',
                'show_files': True
            }
        }


@keys.assign(seq=seqs.GA, modes=(modes.NORMAL,))
class ViShowAsciiValueOfCharacterUnderCursor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {
            'action': '_vi_ga',
            'action_args': {}
        }


@keys.assign(seq=seqs.J, modes=(modes.SELECT,))
class ViAddSelection(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': '_vi_select_j',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.ALT_CTRL_P, modes=_MODES_ACTION)
class StShowSwitchProject(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'prompt_select_workspace',
            'action_args': {}
        }


@keys.assign(seq=seqs.COMMAND_BIG_P, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_BIG_P, modes=_MODES_ACTION)
class StShowCommandPalette(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'show_overlay',
            'action_args': {
                'overlay': 'command_palette'
            }
        }


@keys.assign(seq=seqs.SHIFT_F11, modes=_MODES_ACTION)
class StEnterDistractionFreeMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'toggle_distraction_free',
            'action_args': {}
        }


@keys.assign(seq=seqs.CTRL_1, group=0, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_2, group=1, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_3, group=2, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_4, group=3, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_5, group=4, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_6, group=5, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_7, group=6, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_8, group=7, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_9, group=8, modes=_MODES_ACTION)
class StFocusGroup(ViOperatorDef):
    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('_group')
        self._group = group
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'focus_group',
            'action_args': {
                'group': self._group
            }
        }


@keys.assign(seq=seqs.CTRL_0, modes=_MODES_ACTION)
class StFocusSideBar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = 'focus_side_bar'
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': self.command,
            'action_args': {}
        }


@keys.assign(seq=seqs.I, modes=_MODES_ACTION + (modes.SELECT,))
class ViEnterInserMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = '_enter_insert_mode'
        self.scroll_into_view = True

    def translate(self, state):
        state.glue_until_normal_mode = True

        return {
            'action': self.command,
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.ESC, modes=_MODES_ACTION)
@keys.assign(seq=seqs.CTRL_C, modes=_MODES_ACTION + (modes.SELECT,))
@keys.assign(seq=seqs.CTRL_LEFT_SQUARE_BRACKET, modes=_MODES_ACTION + (modes.SELECT,))
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


@keys.assign(seq=seqs.CTRL_RIGHT_SQUARE_BRACKET, modes=_MODES_ACTION)
class ViJumpToDefinition(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {
            'action': '_vi_ctrl_right_square_bracket',
            'action_args': {}
        }


@keys.assign(seq=seqs.A, modes=_MODES_ACTION)
class ViInsertAfterChar(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['action'] = '_vi_a'
        cmd['action_args'] = {'mode': state.mode, 'count': 1}

        if state.mode != modes.SELECT:
            state.glue_until_normal_mode = True
            state.normal_insert_count = state.count

        return cmd


@keys.assign(seq=seqs.BIG_A, modes=_MODES_ACTION + (modes.SELECT,))
class ViInsertAtEol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['action'] = '_vi_big_a'
        cmd['action_args'] = {'mode': state.mode, 'count': state.count}

        if state.mode != modes.SELECT:
            state.glue_until_normal_mode = True

        return cmd


@keys.assign(seq=seqs.BIG_I, modes=_MODES_ACTION)
class ViInsertAtBol(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['action'] = '_vi_big_i'
        cmd['action_args'] = {'mode': state.mode, 'count': state.count}

        if state.mode != modes.SELECT:
            state.glue_until_normal_mode = True

        return cmd


@keys.assign(seq=seqs.COLON, modes=_MODES_ACTION)
class ViEnterCommandLineMode(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'vi_colon_input',
            'action_args': {}
        }


@keys.assign(seq=seqs.F9, modes=_MODES_ACTION)
class StSortLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'sort_lines',
            'action_args': {
                'case_sensitive': False
            }
        }


@keys.assign(seq=seqs.CTRL_G, modes=_MODES_ACTION)
class ViShowFileStatus(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'ex_file',
            'action_args': {}
        }


@keys.assign(seq=seqs.BIG_Z_BIG_Q, modes=_MODES_ACTION)
class ViExitEditor(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'ex_quit',
            'action_args': {
                'command_line': 'q!'
            }
        }


@keys.assign(seq=seqs.BIG_Z_BIG_Z, modes=_MODES_ACTION)
class ViCloseFile(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'ex_exit',
            'action_args': {}
        }


@keys.assign(seq=seqs.F6, modes=_MODES_ACTION)
class StToggleSpelling(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'action': 'toggle_setting',
            'action_args': {
                'setting': 'spell_check'
            }
        }


@keys.assign(seq=seqs.G_BIG_D, modes=_MODES_ACTION)
class ViGotoSymbolInProject(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['action'] = '_vi_go_to_symbol'
        cmd['action_args'] = {
            'mode': state.mode,
            'count': state.count,
            'globally': True
        }

        return cmd


@keys.assign(seq=seqs.K, modes=(modes.SELECT,))
class ViDeselectInstance(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        # Non-standard
        if state.mode != modes.SELECT:
            raise ValueError(
                'bad mode, expected mode_select, got {0}'.format(state.mode))

        return {
            'action': 'soft_undo',
            'action_args': {}
        }


@keys.assign(seq=seqs.L, modes=(modes.SELECT,))
class ViSkipInstance(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        # Non-standard
        if state.mode != modes.SELECT:
            raise ValueError(
                'bad mode, expected mode_select, got {0}'.format(state.mode))

        return {
            'action': 'find_under_expand_skip',
            'action_args': {}
        }


@keys.assign(seq=seqs.GD, modes=_MODES_MOTION)
class ViGotoSymbolInFile(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_go_to_symbol'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'globally': False
        }

        return cmd


@keys.assign(seq=seqs.L, modes=_MODES_MOTION)
@keys.assign(seq=seqs.RIGHT, modes=_MODES_MOTION)
@keys.assign(seq=seqs.SPACE, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.SHIFT_ENTER, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.B, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.BIG_B, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.BIG_W, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.E, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.BIG_H, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.GE, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.G_BIG_E, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.BIG_L, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.BIG_M, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.CTRL_D, modes=_MODES_MOTION)
class ViMoveHalfScreenDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_ctrl_d',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_U, modes=_MODES_MOTION)
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
                'count': state.count
            }
        }


@keys.assign(seq=seqs.CTRL_F, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.CTRL_B, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.BACKTICK, modes=_MODES_MOTION)
class ViGotoExactMarkXpos(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        assert len(key) == 1, '``` only accepts a single char'
        self._inp = key

        return True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_backtick'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'character': self.inp
        }

        return cmd


@keys.assign(seq=seqs.DOLLAR, modes=_MODES_MOTION)
@keys.assign(seq=seqs.END, modes=_MODES_MOTION)
class ViMoveToEol(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_dollar'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.ENTER, modes=_MODES_MOTION)
@keys.assign(seq=seqs.PLUS, modes=_MODES_MOTION)
class ViMotionEnter(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_enter'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.MINUS, modes=_MODES_MOTION)
class ViMoveBackOneLine(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_minus'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.G_UNDERSCORE, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.GJ, modes=_MODES_MOTION)
class ViMoveByScreenLineDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_gj'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.GK, modes=_MODES_MOTION)
class ViMoveByScreenLineUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_gk'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.LEFT_BRACE, modes=_MODES_MOTION)
class ViMoveByBlockUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_left_brace'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.SEMICOLON, modes=_MODES_MOTION)
class ViRepeatCharSearchForward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        forward = state.last_char_search_command in ('vi_t', 'vi_f')
        inclusive = state.last_char_search_command in ('vi_f', 'vi_big_f')
        skipping = state.last_char_search_command in ('vi_t', 'vi_big_t')

        cmd = {}
        cmd['motion'] = ('_vi_find_in_line' if forward else '_vi_reverse_find_in_line')
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'char': state.last_character_search,
            'inclusive': inclusive,
            'skipping': skipping
        }

        return cmd


@keys.assign(seq=seqs.QUOTE, modes=_MODES_MOTION)
class ViGotoMark(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        assert len(key) == 1, '`\'` only accepts a single char'
        self._inp = key

        return True

    def translate(self, state):
        cmd = {}

        if self.inp == "'":
            cmd['is_jump'] = True
            cmd['motion'] = '_vi_quote_quote'
            cmd['motion_args'] = {}

            return cmd

        cmd['is_jump'] = True
        cmd['motion'] = '_vi_quote'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'character': self.inp
        }

        return cmd


@keys.assign(seq=seqs.RIGHT_BRACE, modes=_MODES_MOTION)
class ViMoveByBlockDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_right_brace'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.LEFT_PAREN, modes=_MODES_MOTION)
class ViMoveBySentenceUp(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_left_paren'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.RIGHT_PAREN, modes=_MODES_MOTION)
class ViMoveBySentenceDown(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_right_paren'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.LEFT_SQUARE_BRACKET, modes=_MODES_MOTION)
class ViGotoOpeningBracket(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = parser_def(command=inputs.vi_left_square_bracket,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`[` only accepts a single char'
        self._inp = translated

        return True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_left_square_bracket'
        cmd['motion_args'] = {
            'char': self.inp,
            'mode': state.mode,
            'count': state.count,
        }

        return cmd


@keys.assign(seq=seqs.LEFT_SQUARE_BRACKET_C, modes=_MODES_ACTION)
class ViBackwardToStartOfChange(ViMotionDef):

    def translate(self, state):
        return {
            'motion': '_vi_left_square_bracket_c',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.RIGHT_SQUARE_BRACKET_C, modes=_MODES_ACTION)
class ViForwardToStartOfChange(ViMotionDef):

    def translate(self, state):
        return {
            'motion': '_vi_right_square_bracket_c',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.RIGHT_SQUARE_BRACKET, modes=_MODES_MOTION)
class ViGotoClosingBracket(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = parser_def(command=inputs.vi_left_square_bracket,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`]` only accepts a single char'
        self._inp = translated

        return True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_right_square_bracket'
        cmd['motion_args'] = {
            'char': self.inp,
            'mode': state.mode,
            'count': state.count,
        }

        return cmd


# TODO [review]
@keys.assign(seq=seqs.PERCENT, modes=_MODES_MOTION)
class ViGotoLinesPercent(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        percent = None
        if state.motion_count or state.action_count:
            percent = state.count

        return {
            'motion': '_vi_percent',
            'motion_args': {'mode': state.mode, 'percent': percent}
        }


@keys.assign(seq=seqs.COMMA, modes=_MODES_MOTION)
class ViRepeatCharSearchBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        forward = state.last_char_search_command in ('vi_t', 'vi_f')
        inclusive = state.last_char_search_command in ('vi_f', 'vi_big_f')
        skipping = state.last_char_search_command in ('vi_t', 'vi_big_t')

        cmd = {}
        cmd['motion'] = ('_vi_find_in_line' if not forward else '_vi_reverse_find_in_line')
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'char': state.last_character_search,
            'inclusive': inclusive,
            'skipping': skipping
        }

        return cmd


@keys.assign(seq=seqs.PIPE, modes=_MODES_MOTION)
class ViMoveByLineCols(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_pipe',
            'motion_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.BIG_E, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.H, modes=_MODES_MOTION)
@keys.assign(seq=seqs.LEFT, modes=_MODES_MOTION)
@keys.assign(seq=seqs.BACKSPACE, modes=_MODES_MOTION)
class ViMoveLeftByChars(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}

        if state.mode == modes.SELECT:
            cmd['motion'] = 'find_under_expand_skip'
            cmd['motion_args'] = {}

            return cmd

        cmd['motion'] = '_vi_h'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.W, modes=_MODES_MOTION)
class ViMoveByWords(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, state):
        return {
            'motion': '_vi_w',
            'motion_args': {'mode': state.mode, 'count': state.count}
        }


@keys.assign(seq=seqs.J, modes=_MODES_MOTION)
@keys.assign(seq=seqs.DOWN, modes=_MODES_MOTION)
@keys.assign(seq=seqs.CTRL_J, modes=_MODES_MOTION)
@keys.assign(seq=seqs.CTRL_N, modes=_MODES_MOTION)
class ViMoveDownByLines(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_j'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'xpos': state.xpos
        }

        return cmd


@keys.assign(seq=seqs.K, modes=_MODES_MOTION)
@keys.assign(seq=seqs.UP, modes=_MODES_MOTION)
class ViMoveUpByLines(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_k'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'xpos': state.xpos
        }

        return cmd


@keys.assign(seq=seqs.HAT, modes=_MODES_MOTION)
@keys.assign(seq=seqs.HOME, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.UNDERSCORE, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.ZERO, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.N, modes=_MODES_MOTION)
class ViRepeatSearchForward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_repeat_buffer_search'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'reverse': False
        }

        return cmd


@keys.assign(seq=seqs.BIG_N, modes=_MODES_MOTION)
class ViRepeatSearchBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_repeat_buffer_search'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'reverse': True
        }

        return cmd


@keys.assign(seq=seqs.STAR, modes=_MODES_MOTION)
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


@keys.assign(seq=seqs.OCTOTHORP, modes=_MODES_MOTION)
class ViReverseFindWord(ViMotionDef):
    # Trivia: Octothorp seems to be a symbol used in maps to represent a
    # small village surrounded by eight fields.

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


@keys.assign(seq=seqs.LEFT_SQUARE_BRACKET, modes=_MODES_MOTION)
@keys.assign(seq=seqs.RIGHT_SQUARE_BRACKET, modes=_MODES_MOTION)
@keys.assign(seq=seqs.BIG_Z, modes=_MODES_MOTION)
@keys.assign(seq=seqs.CTRL_K, modes=_MODES_MOTION)
@keys.assign(seq=seqs.CTRL_W, modes=_MODES_MOTION)
@keys.assign(seq=seqs.G, modes=_MODES_MOTION)
@keys.assign(seq=seqs.Z, modes=_MODES_MOTION)
# Non-standard modes:
@keys.assign(seq=seqs.CTRL_DOT, modes=_MODES_MOTION)
@keys.assign(seq=seqs.CTRL_SHIFT_DOT, modes=_MODES_MOTION)
# XXX: This is called a 'submode' in the vim docs:
@keys.assign(seq=seqs.CTRL_X, modes=[modes.INSERT])
# TODO This should not be a motion.
class ViOpenNameSpace(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {}


@keys.assign(seq=seqs.DOUBLE_QUOTE, modes=_MODES_MOTION)
class ViOpenRegister(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate(self, state):
        return {}


@keys.assign(seq=seqs.GG, modes=_MODES_MOTION)
class ViGotoBof(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}

        if state.action_count or state.motion_count:
            cmd['motion'] = '_vi_go_to_line'
            cmd['motion_args'] = {'line': state.count, 'mode': state.mode}

            return cmd

        cmd['motion'] = '_vi_gg'
        cmd['motion_args'] = {'mode': state.mode, 'count': state.count}

        return cmd


@keys.assign(seq=seqs.BIG_G, modes=_MODES_MOTION)
class ViGotoEof(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True

    def translate(self, state):
        cmd = {}

        if state.action_count or state.motion_count:
            cmd['motion'] = '_vi_go_to_line'
            cmd['motion_args'] = {'line': state.count, 'mode': state.mode}
        else:
            cmd['motion'] = '_vi_big_g'
            cmd['motion_args'] = {'mode': state.mode}

        return cmd


@keys.assign(seq=seqs.R, modes=_MODES_ACTION)
class ViReplaceCharacters(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.repeatable = True
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`r` only accepts a single char'
        self._inp = translated

        return True

    def translate(self, state):
        cmd = {}
        cmd['action'] = '_vi_r'
        cmd['action_args'] = {
            'mode': state.mode,
            'count': state.count,
            'register': state.register,
            'char': self.inp
        }

        return cmd


@keys.assign(seq=seqs.M, modes=_MODES_ACTION)
class ViSetMark(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        assert len(key) == 1, '`m` only accepts a single char'
        self._inp = key

        return True

    def translate(self, state):
        cmd = {}
        cmd['action'] = '_vi_m'
        cmd['action_args'] = {
            'mode': state.mode,
            'count': state.count,
            'character': self.inp
        }

        return cmd


@keys.assign(seq=seqs.T, modes=_MODES_MOTION)
@keys.assign(seq=seqs.F, modes=_MODES_MOTION, inclusive=True)
class ViSearchCharForward(ViMotionDef):
    def __init__(self, inclusive=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('inclusive')
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inclusive = inclusive
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`f`, `t`, `F`, `T` only accept a single char'
        self._inp = translated

        return True

    def translate(self, state):
        if self.inclusive:
            state.last_char_search_command = 'vi_f'
        else:
            state.last_char_search_command = 'vi_t'

        state.last_character_search = self.inp

        cmd = {}
        cmd['motion'] = '_vi_find_in_line'
        cmd['motion_args'] = {
            'char': self.inp,
            'mode': state.mode,
            'count': state.count,
            'inclusive': self.inclusive
        }

        return cmd


@keys.assign(seq=seqs.A, modes=[modes.OPERATOR_PENDING, modes.VISUAL, modes.VISUAL_BLOCK])
class ViATextObject(ViMotionDef):
    def __init__(self, inclusive=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inclusive = inclusive
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`a` only accepts a single char'
        self._inp = translated

        return True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_select_text_object'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'text_object': self.inp,
            'inclusive': True
        }

        return cmd


@keys.assign(seq=seqs.I, modes=[modes.OPERATOR_PENDING, modes.VISUAL, modes.VISUAL_BLOCK])
class ViITextObject(ViMotionDef):
    def __init__(self, inclusive=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inclusive = inclusive
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`i` only accepts a single char'
        self._inp = translated

        return True

    def translate(self, state):
        cmd = {}
        cmd['motion'] = '_vi_select_text_object'
        cmd['motion_args'] = {
            'mode': state.mode,
            'count': state.count,
            'text_object': self.inp,
            'inclusive': False
        }

        return cmd


@keys.assign(seq=seqs.BIG_T, modes=_MODES_MOTION)
@keys.assign(seq=seqs.BIG_F, modes=_MODES_MOTION, inclusive=True)
class ViSearchCharBackward(ViMotionDef):
    def __init__(self, inclusive=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._serializable.append('inclusive')
        self.scroll_into_view = True
        self.updates_xpos = True
        self.inclusive = inclusive
        self.input_parser = parser_def(command=inputs.one_char,
                                       interactive_command=None,
                                       input_param=None,
                                       on_done=None,
                                       type=INPUT_INMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        translated = utils.translate_char(key)
        assert len(translated) == 1, '`t` only accepts a single char'
        self._inp = translated

        return True

    def translate(self, state):
        if self.inclusive:
            state.last_char_search_command = 'vi_big_f'
        else:
            state.last_char_search_command = 'vi_big_t'

        state.last_character_search = self.inp

        cmd = {}
        cmd['motion'] = '_vi_reverse_find_in_line'
        cmd['motion_args'] = {
            'char': self.inp,
            'mode': state.mode,
            'count': state.count,
            'inclusive': self.inclusive
        }

        return cmd


@keys.assign(seq=seqs.SLASH, modes=_MODES_MOTION)
class ViSearchForward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = parser_def(command='_vi_slash',
                                       interactive_command='_vi_slash',
                                       type=INPUT_VIA_PANEL,
                                       on_done=None,
                                       input_param='default')

    @property
    def accept_input(self):
        if not self.inp:
            return True

        return not self.inp.lower().endswith('<cr>')

    def accept(self, key):
        self._inp += key

        return True

    def translate(self, state):
        cmd = {}
        if self.accept_input:
            cmd['motion'] = '_vi_slash'
            cmd['motion_args'] = {}
        else:
            # We'll end up here, for example, when repeating via '.'.
            return ViSearchForwardImpl(term=self._inp[:-4]).translate(state)

        return cmd


class ViSearchForwardImpl(ViMotionDef):
    def __init__(self, *args, term='', **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self._inp = term
        self.updates_xpos = True

    def translate(self, state):
        if not self.inp:
            self._inp = state.last_buffer_search

        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_slash_impl'
        cmd['motion_args'] = {
            'search_string': self.inp,
            'mode': state.mode,
            'count': state.count,
        }

        return cmd


@keys.assign(seq=seqs.QUESTION_MARK, modes=_MODES_MOTION)
class ViSearchBackward(ViMotionDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = parser_def(command='_vi_question_mark',
                                       interactive_command='_vi_question_mark',
                                       type=INPUT_VIA_PANEL,
                                       on_done=None,
                                       input_param='default')

    @property
    def accept_input(self):
        if not self.inp:
            return True

        return not self.inp.lower().endswith('<cr>')

    def accept(self, key):
        self._inp += key

        return True

    def translate(self, state):
        if self.accept_input:
            cmd = {}
            cmd['motion'] = '_vi_question_mark'
            cmd['motion_args'] = {}

            return cmd
        else:
            # We'll end up here, for example, when repeating via '.'.
            return ViSearchBackwardImpl(term=self._inp[:-4]).translate(state)


class ViSearchBackwardImpl(ViMotionDef):
    def __init__(self, *args, term='', **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self._inp = term

    def translate(self, state):
        if not self.inp:
            self._inp = state.last_buffer_search

        cmd = {}
        cmd['is_jump'] = True
        cmd['motion'] = '_vi_question_mark_impl'
        cmd['motion_args'] = {
            'search_string': self.inp,
            'mode': state.mode,
            'count': state.count
        }

        return cmd


@keys.assign(seq=seqs.CTRL_X_CTRL_L, modes=[modes.INSERT])
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


@keys.assign(seq=seqs.GM, modes=_MODES_MOTION)
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


# TODO gc is a non-standard Vim command. It looks like it based on
# vim-commentary. It should be refactored into an out-of-the-box
# plugin like the surround, unimpaired, abolish, etc. plugins.
# See https://github.com/tpope/vim-commentary.
@keys.assign(seq=seqs.GC, modes=_MODES_ACTION)
class ViToggleCommentByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_gc',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.GCC, modes=_MODES_ACTION)
class ViCommentLine(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_gcc_action',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@keys.assign(seq=seqs.G_BIG_C, modes=_MODES_ACTION)
class ViToggleBlockCommentByLines(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True
        self.motion_required = True
        self.repeatable = True

    def translate(self, state):
        return {
            'action': '_vi_g_big_c',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }
