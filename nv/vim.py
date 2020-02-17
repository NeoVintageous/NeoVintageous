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

import logging
import traceback

from sublime import active_window as _active_window
from sublime import status_message as _status_message
from sublime import windows as _windows

_log = logging.getLogger(__name__)

# NeoVintageous always runs actions based on selections. Some Vim commands,
# however, behave differently depending on whether the current mode is NORMAL or
# VISUAL. To differentiate NORMAL mode operations (involving only an action, or
# a motion plus an action) from VISUAL mode, we need to add an additional mode
# for handling selections that won't interfere with the actual VISUAL mode. This
# is INTERNAL_NORMAL's job. INTERNAL_NORMAL is a pseudomode, because global
# state's .mode property should never set to it, yet it's set in vi_cmd_data
# often. Note that for pure motions we still use plain NORMAL mode.
INSERT = 'mode_insert'
INTERNAL_NORMAL = 'mode_internal_normal'
NORMAL = 'mode_normal'
OPERATOR_PENDING = 'mode_operator_pending'
REPLACE = 'mode_replace'
SELECT = 'mode_select'
UNKNOWN = 'mode_unknown'
VISUAL = 'mode_visual'
VISUAL_BLOCK = 'mode_visual_block'
VISUAL_LINE = 'mode_visual_line'

DIRECTION_UP = 1
DIRECTION_DOWN = 2

EOF = '\x00'
NL = '\n'

_MODES = {
    INSERT: 'INSERT',
    INTERNAL_NORMAL: '',
    NORMAL: '',
    OPERATOR_PENDING: '',
    VISUAL: 'VISUAL',
    VISUAL_BLOCK: 'VISUAL BLOCK',
    VISUAL_LINE: 'VISUAL LINE',
    UNKNOWN: 'UNKNOWN',
    REPLACE: 'REPLACE',
    SELECT: 'SELECT',
}


def mode_to_name(mode: str) -> str:
    try:
        return _MODES[mode]
    except KeyError:
        return '*UNKNOWN'


def is_visual_mode(mode: str) -> bool:
    return mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK)


def is_ex_mode(view) -> bool:
    return view.settings().get('_nv_ex_mode')


def _format_message(msg: str, *args) -> str:
    if args:
        msg = msg % args

    return msg


def status_message(msg: str, *args: str) -> None:
    _status_message(_format_message(msg, *args))


def message(msg: str, *args: str) -> None:
    print('NeoVintageous:', _format_message(msg, *args))


def run_window_command(cmd: str, args=None, window=None) -> None:
    if not window:
        window = _active_window()
    _log.info('command: %s %s', cmd, args)
    window.run_command(cmd, args)


def run_view_command(view, cmd: str, args=None) -> None:
    _log.info('command: %s %s', cmd, args)
    view.run_command(cmd, args)


def run_motion(instance, motion) -> None:
    _log.info('motion: %s', motion)
    instance.run_command(motion['motion'], motion['motion_args'])


def run_action(instance, action) -> None:
    _log.info('action: %s', action)
    instance.run_command(action['action'], action['action_args'])


def enter_normal_mode(view_or_window, mode: str = None) -> None:
    view_or_window.run_command('_enter_normal_mode', {'mode': mode})


def enter_insert_mode(view_or_window, mode: str) -> None:
    view_or_window.run_command('_enter_insert_mode', {'mode': mode})


def enter_visual_mode(view_or_window, mode: str, force: bool = False) -> None:
    view_or_window.run_command('_enter_visual_mode', {'mode': mode})


def enter_visual_line_mode(view_or_window, mode: str, force: bool = False) -> None:
    view_or_window.run_command('_enter_visual_line_mode', {'mode': mode})


def enter_visual_block_mode(view_or_window, mode: str, force: bool = False) -> None:
    view_or_window.run_command('_enter_visual_block_mode', {'mode': mode})


def clean_views():
    for window in _windows():
        for view in window.views():
            clean_view(view)


def clean_view(view):

    # Resets cursor and mode. In the case of errors loading the plugin this can
    # help prevent the normal functioning of editor becoming unusable e.g. the
    # cursor getting stuck in a block shape or the mode getting stuck in normal
    # or visual mode.

    try:
        settings = view.settings()
        settings.erase('command_mode')
        settings.erase('inverse_caret_state')
        settings.erase('vintage')
    except Exception:  # pragma: no cover
        traceback.print_exc()
