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

from NeoVintageous.nv import plugin
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_partial_sequence
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.variables import expand_keys
from NeoVintageous.nv.vi import keys
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.keys import tokenize_keys
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE

_log = logging.getLogger(__name__)

_mappings = {
    INSERT: {},
    NORMAL: {},
    OPERATOR_PENDING: {},
    SELECT: {},
    VISUAL_BLOCK: {},
    VISUAL_LINE: {},
    VISUAL: {}
}  # type: dict


class Mapping:

    def __init__(self, lhs: str, rhs: str):
        self.lhs = lhs
        self.rhs = rhs


def _find_partial_matches(mode: str, lhs: str) -> list:
    return [x for x in _mappings[mode] if x.startswith(lhs)]


def _find_full_match(mode: str, lhs: str):
    if lhs in _mappings[mode]:
        return _mappings[mode][lhs]


def _normalise_lhs(lhs: str) -> str:
    try:
        return ''.join(tokenize_keys(expand_keys(lhs)))
    except ValueError:
        traceback.print_exc()
        return lhs


def mappings_add(mode: str, lhs: str, rhs: str) -> None:
    _mappings[mode][_normalise_lhs(lhs)] = rhs


def mappings_remove(mode: str, lhs: str) -> None:
    del _mappings[mode][_normalise_lhs(lhs)]


def mappings_clear() -> None:
    for mode in _mappings:
        _mappings[mode] = {}


def mappings_is_incomplete(mode: str, seq: str) -> bool:
    full_match = _find_full_match(mode, seq)
    if full_match:
        return False

    partial_matches = _find_partial_matches(mode, seq)
    if partial_matches:
        return True

    return False


def mappings_can_resolve(mode: str, sequence: str) -> bool:
    full_match = _find_full_match(mode, sequence)
    if full_match:
        return True

    partial_matches = _find_partial_matches(mode, sequence)
    if partial_matches:
        return True

    return False


def _seq_to_mapping(mode: str, seq: str):
    full_match = _find_full_match(mode, seq)
    if full_match:
        return Mapping(seq, full_match)


def _seq_to_command(view, seq: str, mode: str):
    # Return the command definition mapped for seq and mode.
    #
    # Args:
    #   view (View):
    #   seq (str): The command sequence.
    #   mode (str): Forces the use of this mode instead of the global state's.
    #
    # Returns:
    #   ViCommandDefBase:
    #   ViMissingCommandDef: If not found.
    if mode in plugin.mappings:
        plugin_command = plugin.mappings[mode].get(seq)
        if plugin_command:
            plugin_name = plugin_command.__class__.__module__[24:]
            is_plugin_enabled = get_setting(view, 'enable_%s' % plugin_name)
            if is_plugin_enabled:
                return plugin_command

    if mode in keys.mappings:
        command = keys.mappings[mode].get(seq)
        if command:
            return command

    return ViMissingCommandDef()


def mappings_resolve(view, sequence: str = None, mode: str = None, check_user_mappings: bool = True):
    # Look at the current global state and return the command mapped to the available sequence.
    #
    # Args:
    #   sequence (str): The command sequence. If a sequence is passed, it is
    #       used instead of the global state's. This is necessary for some
    #       commands that aren't name spaces but act as them (for example,
    #       ys from the surround plugin).
    #   mode (str): If different than None, it will be used instead of the
    #       global state's. This is necessary when we are in operator
    #       pending mode and we receive a new action. By combining the
    #       existing action's name with name of the action just received we
    #       could find a new action.
    #   check_user_mappings (bool):
    #
    # Returns:
    #   Mapping:
    #   ViMissingCommandDef: If not found.

    # We usually need to look at the partial sequence, but some commands do
    # weird things, like ys, which isn't a namespace but behaves as such
    # sometimes.
    seq = sequence or get_partial_sequence(view)

    command = None

    if check_user_mappings:
        # Resolve the full sequence rather than the "bare" sequence, because the
        # user may have defined some mappings that start with numbers (counts),
        # or " (register character), which are stripped from the bare sequences.
        # See https://github.com/NeoVintageous/NeoVintageous/issues/434.

        # XXX The reason these does not pass the mode, and instead uses the
        # get_mode(), is because implementation of commands like dd are a bit
        # hacky. For example, the dd definition does is not assigned to operator
        # pending mode, the second d is instead caught by the feed key command
        # and resolved by specifying NORMAL mode explicitly, which resolves the
        # delete line command definition. Commands like this can probably be
        # fixed by allowing the definitions to handle the OPERATOR PENDING and
        # let the definition handle any special-cases itself instead of passing
        # off the responsibility to the feed key command.

        command = _seq_to_mapping(get_mode(view), seq)

    if not command:
        command = _seq_to_command(view, to_bare_command_name(seq), mode or get_mode(view))

    _log.info('resolved %s mode=%s sequence=%s %s', command, mode, sequence, command.__class__.__mro__)

    return command
