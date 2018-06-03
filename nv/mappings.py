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

from NeoVintageous.nv.variables import expand_keys
from NeoVintageous.nv.vi.cmd_base import CMD_TYPE_USER
from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import seq_to_command
from NeoVintageous.nv.vi.keys import to_bare_command_name
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
}


class Mapping:

    def __init__(self, head, mapping, tail):
        self.mapping = mapping
        self.head = head
        self.tail = tail

    @property
    def sequence(self):
        try:
            return self.head + self.tail
        except TypeError:
            raise ValueError('no mapping found')


def _get_seqs(mode):
    # TODO [review] Do the mappings need to be sorted?
    return sorted(_mappings[mode])


def _find_partial_match(mode, seq):
    return [x for x in _get_seqs(mode) if x.startswith(seq)]


# TODO [review] Should this really accept empty string i.e. if seq='' then this all sequences for the mode are returned? # noqa
# TODO [review] Should this raise an IndexError error?
def _find_full_match(mode, seq):
    # Args:
    #   mode (str):
    #   seq (str):
    #
    # Returns:
    #   A 2-tuple Tuple[str, str], Tuple[None, None] if not found.
    #
    # Raises:
    #   IndexError: If has partial sequences found, but not a full match.

    # TODO [refactor] There doesn't look there is a need to use partials.
    partials = _find_partial_match(mode, seq)

    try:

        name = [x for x in partials if x == seq][0]

        return (name, _mappings[mode][name])
    except IndexError:
        return (None, None)


def mappings_add(mode, new, target):
    # type: (str, str, str) -> None
    # Raises:
    #   KeyError: If mode does not exist.
    _mappings[mode][expand_keys(new)] = {'name': target, 'type': CMD_TYPE_USER}


def mappings_remove(mode, new):
    # type: (str, str) -> None
    # Raises:
    #   KeyError: If mapping not found.
    try:
        del _mappings[mode][expand_keys(new)]
    except KeyError:
        raise KeyError('mapping not found')


def mappings_clear():
    # type: () -> None
    for mode in _mappings:
        _mappings[mode] = {}


# XXX: Provisional. Get rid of this as soon as possible.
def _can_be_long_user_mapping(mode, key):
    # Args:
    #   mode (str):
    #   seq (str):
    #
    # Returns:
    #   2-tuple (True, str) or (False, True) if not _can_be_long_user_mapping.
    full_match = _find_full_match(mode, key)
    partial_matches = _find_partial_match(mode, key)
    if partial_matches:
        return (True, full_match[0])

    return (False, True)


def _expand_first(mode, seq):
    # Args:
    #   mode (str):
    #   seq (str):
    #
    # Returns:
    #   Mapping or None if no mapping for mode and seq found.
    head = ''

    keys, mapped_to = _find_full_match(mode, seq)
    if keys:
        return Mapping(seq, mapped_to['name'], seq[len(keys):])

    for key in KeySequenceTokenizer(seq).iter_tokenize():
        head += key
        keys, mapped_to = _find_full_match(mode, head)
        if keys:
            return Mapping(head, mapped_to['name'], seq[len(head):])
        else:
            break

    if _find_partial_match(mode, seq):
        return Mapping(seq, '', '')


# XXX: Provisional. Get rid of this as soon as possible.
# e.g. we may have typed 'aa' and there's an 'aaa' mapping, so we need to keep collecting input.
def mappings_is_incomplete(mode, partial_sequence):
    # type: (str, str) -> bool
    (maybe_mapping, complete) = _can_be_long_user_mapping(mode, partial_sequence)
    if maybe_mapping and not complete:
        return True

    return False


def mappings_resolve(state, sequence=None, mode=None, check_user_mappings=True):
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
    seq = to_bare_command_name(sequence or state.partial_sequence)

    # TODO: Use same structure as in mappings (nested dict).
    command = None
    if check_user_mappings:
        # TODO: We should be able to force a mode here too as, below.
        command = _expand_first(state.mode, seq)

    if not command:
        command = seq_to_command(state, seq, mode=mode)

    _log.debug('resolved %s -> %s -> %s', sequence, seq, command)

    return command
