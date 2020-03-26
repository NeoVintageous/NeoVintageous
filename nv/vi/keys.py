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

import re

from NeoVintageous.nv import variables
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


mappings = {
    INSERT: {},
    NORMAL: {},
    OPERATOR_PENDING: {},
    SELECT: {},
    VISUAL: {},
    VISUAL_BLOCK: {},
    VISUAL_LINE: {}
}  # type: dict


_NAMED_KEYS = [

    seqs.BACKSLASH,
    seqs.BACKSPACE,
    seqs.BAR,
    seqs.DEL,
    seqs.DOWN,
    seqs.END,
    seqs.ENTER,
    seqs.ESC,
    seqs.HOME,
    seqs.INSERT,
    seqs.KEYPAD_0,
    seqs.KEYPAD_1,
    seqs.KEYPAD_2,
    seqs.KEYPAD_3,
    seqs.KEYPAD_4,
    seqs.KEYPAD_5,
    seqs.KEYPAD_6,
    seqs.KEYPAD_7,
    seqs.KEYPAD_8,
    seqs.KEYPAD_9,
    seqs.KEYPAD_DIVIDE,
    seqs.KEYPAD_ENTER,
    seqs.KEYPAD_MINUS,
    seqs.KEYPAD_MULTIPLY,
    seqs.KEYPAD_PERIOD,
    seqs.KEYPAD_PLUS,
    seqs.LEADER,
    seqs.LEFT,
    seqs.LESS_THAN,
    seqs.PAGE_DOWN,
    seqs.PAGE_UP,
    seqs.RIGHT,
    seqs.SPACE,
    seqs.TAB,
    seqs.UP,

    seqs.F1,
    seqs.F2,
    seqs.F3,
    seqs.F4,
    seqs.F5,
    seqs.F6,
    seqs.F7,
    seqs.F8,
    seqs.F9,
    seqs.F10,
    seqs.F11,
    seqs.F12,
    seqs.F13,
    seqs.F14,
    seqs.F15,
    seqs.F16,
    seqs.F17,
    seqs.F18,
    seqs.F19,
    seqs.F20,

]


_NAMED_KEY_ALIASES = {
    'enter': 'cr',
    'return': 'cr'
}


def _resolve_named_key_alias(key: str):
    try:
        return _NAMED_KEY_ALIASES[key]
    except KeyError:
        return key


class KeySequenceTokenizer():
    """Takes in a sequence of key names and tokenizes it."""

    _EOF = -2

    def __init__(self, source: str):
        """Sequence of key names in Vim notation."""
        self.idx = -1
        self.source = source

    def _consume(self):
        self.idx += 1
        if self.idx >= len(self.source):
            self.idx -= -1
            return self._EOF
        return self.source[self.idx]

    def _peek_one(self):
        if (self.idx + 1) >= len(self.source):
            return self._EOF
        return self.source[self.idx + 1]

    def _is_named_key(self, key: str) -> bool:
        return key.lower() in _NAMED_KEYS

    def _sort_modifiers(self, modifiers: str) -> str:
        """Ensure consistency in the order of modifier letters according to c > m > s."""
        if len(modifiers) == 6:
            modifiers = 'c-m-s-'
        elif len(modifiers) > 2:
            if modifiers.startswith('s-') and modifiers.endswith('c-'):
                modifiers = 'c-s-'
            elif modifiers.startswith('s-') and modifiers.endswith('m-'):
                modifiers = 'm-s-'
            elif modifiers.startswith('m-') and modifiers.endswith('c-'):
                modifiers = 'c-m-'
        return modifiers

    def _long_key_name(self) -> str:
        key_name = ''
        modifiers = ''

        while True:
            c = self._consume()

            if c == self._EOF:
                raise ValueError("expected '>' at index {0}".format(self.idx))

            elif (c.lower() in ('c', 's', 'm', 'd', 'a')) and (self._peek_one() == '-'):
                # <A-...> is aliased to <M-...>
                if c.lower() == 'a':
                    c = 'm'

                if c.lower() in modifiers.lower():
                    raise ValueError('invalid modifier sequence: {0}'.format(self.source))

                modifiers += c + self._consume()

            elif c == '>':
                modifiers = self._sort_modifiers(modifiers.lower())

                if len(key_name) == 1:
                    if not modifiers:
                        raise ValueError('wrong sequence {0}'.format(self.source))

                    return '<' + modifiers.upper() + key_name + '>'

                elif self._is_named_key('<' + _resolve_named_key_alias(key_name.lower()) + '>'):
                    return '<' + modifiers.upper() + _resolve_named_key_alias(key_name.lower()) + '>'

                else:
                    raise ValueError("'<{0}>' is not a known key".format(key_name))

            else:
                key_name += c

    def _tokenize_one(self):
        c = self._consume()

        if c == '<':
            return self._expand_vars(self._long_key_name())
        else:
            return c

    def _iter_tokenize(self):
        while True:
            token = self._tokenize_one()
            if token == self._EOF:
                break
            yield token

    def _expand_vars(self, c: str) -> str:
        return variables.get(c) if variables.is_key_name(c) else c


def tokenize_keys(keys: str) -> list:
    return KeySequenceTokenizer(keys)._iter_tokenize()


_BARE_COMMAND_NAME_PATTERN = re.compile(r'^(?:".)?(?:[1-9]+)?')


def to_bare_command_name(seq: str) -> str:
    # Args:
    #   seq (str): The command sequence.
    #
    # Return:
    #   str: The command sequence with register and counts strips e.g. 2daw ->
    #       daw, "a2d2aw -> daw, etc. The special case '0' is returned
    #       unmodified.
    if seq == '0':
        return seq

    # Account for d2d and similar sequences.
    new_seq = list(tokenize_keys(_BARE_COMMAND_NAME_PATTERN.sub('', seq)))

    return ''.join(k for k in new_seq if not k.isdigit())


def assign(seq: str, modes, *args, **kwargs):
    """
    Register a 'key sequence' to 'command' mapping with NeoVintageous.

    The registered key sequence must be known to NeoVintageous. The
    registered command must be a ViMotionDef or ViOperatorDef.

    The decorated class is instantiated with `*args` and `**kwargs`.

    @keys
      A list of (`mode:tuple`, `sequence:string`) pairs to map the decorated
      class to.
    """
    def inner(cls):
        for mode in modes:
            mappings[mode][seq] = cls(*args, **kwargs)
        return cls
    return inner
