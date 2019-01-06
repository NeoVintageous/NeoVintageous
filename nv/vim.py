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

from sublime import active_window as _active_window
from sublime import status_message as _status_message

_log = logging.getLogger(__name__)

INSERT = 'mode_insert'
NORMAL = 'mode_normal'
OPERATOR_PENDING = 'mode_operator_pending'
REPLACE = 'mode_replace'
SELECT = 'mode_select'
UNKNOWN = 'mode_unknown'
VISUAL = 'mode_visual'
VISUAL_BLOCK = 'mode_visual_block'
VISUAL_LINE = 'mode_visual_line'

# NeoVintageous always runs actions based on selections. Some Vim commands,
# however, behave differently depending on whether the current mode is NORMAL or
# VISUAL. To differentiate NORMAL mode operations (involving only an action, or
# a motion plus an action) from VISUAL mode, we need to add an additional mode
# for handling selections that won't interfere with the actual VISUAL mode. This
# is INTERNAL_NORMAL's job. INTERNAL_NORMAL is a pseudomode, because global
# state's .mode property should never set to it, yet it's set in vi_cmd_data
# often. Note that for pure motions we still use plain NORMAL mode.
INTERNAL_NORMAL = 'mode_internal_normal'

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


def mode_to_name(mode):
    # type: (str) -> str
    try:
        return _MODES[mode]
    except KeyError:
        return 'REALLY UNKNOWN'


def is_visual_mode(mode):
    return mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK)


INPUT_IMMEDIATE = 1
INPUT_VIA_PANEL = 2
INPUT_AFTER_MOTION = 3


DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4


def console_message(msg):
    # type: (str) -> None
    print('NeoVintageous:', msg)


def status_message(msg):
    # type: (str) -> None
    _status_message(msg)


def message(msg):
    # type: (str) -> None
    status_message(msg)
    console_message(msg)


def run_window_command(cmd, args=None, window=None):
    if not window:
        window = _active_window()
    _log.info('command: %s %s', cmd, args)
    window.run_command(cmd, args)


def run_view_command(view, cmd, args=None):
    _log.info('command: %s %s', cmd, args)
    view.run_command(cmd, args)
