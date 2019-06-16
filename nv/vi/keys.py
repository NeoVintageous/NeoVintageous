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

from NeoVintageous.nv import plugin
from NeoVintageous.nv import variables
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


def seq_to_command(view, seq, mode):
    # Return the command definition mapped for seq and mode.
    #
    # Args:
    #   view (View):
    #   seq (str): The command sequence.
    #   mode (str): Forces the use of this mode instead of the global state's.
    #
    # Returns:
    #   Mapping:
    #   ViMissingCommandDef: If not found.
    if mode in plugin.mappings:
        plugin_command = plugin.mappings[mode].get(seq)
        if plugin_command:
            is_enabled_attr = hasattr(plugin_command, 'is_enabled')
            if not is_enabled_attr or (is_enabled_attr and plugin_command.is_enabled(view.settings())):
                return plugin_command

    if mode in mappings:
        command = mappings[mode].get(seq)
        if command:
            return command

    return ViMissingCommandDef()


mappings = {
    INSERT: {},
    NORMAL: {},
    OPERATOR_PENDING: {},
    SELECT: {},
    VISUAL: {},
    VISUAL_BLOCK: {},
    VISUAL_LINE: {}
}  # type: dict


EOF = -2


class key_names:
    """Names of special keys."""

    BACKSLASH = '<bslash>'
    BACKSPACE = '<bs>'
    BAR = '<bar>'
    CR = '<cr>'
    DOWN = '<down>'
    END = '<end>'
    ENTER = '<enter>'
    ESC = '<esc>'
    HOME = '<home>'
    LEFT = '<left>'
    LESS_THAN = '<lt>'
    PAGE_DOWN = '<pagedown>'
    PAGE_UP = '<pageup>'
    RIGHT = '<right>'
    SPACE = '<sp>'
    SPACE_LONG = '<space>'
    TAB = '<tab>'
    UP = '<up>'

    F1 = '<f1>'
    F2 = '<f2>'
    F3 = '<f3>'
    F4 = '<f4>'
    F5 = '<f5>'
    F6 = '<f6>'
    F7 = '<f7>'
    F8 = '<f8>'
    F9 = '<f9>'
    F10 = '<f10>'
    F11 = '<f11>'
    F12 = '<f12>'
    F13 = '<f13>'
    F14 = '<f14>'
    F15 = '<f15>'

    Leader = '<leader>'

    as_list = [

        BACKSLASH,
        BACKSPACE,
        BAR,
        CR,
        DOWN,
        END,
        ENTER,
        ESC,
        HOME,
        LEFT,
        LESS_THAN,
        PAGE_DOWN,
        PAGE_UP,
        RIGHT,
        SPACE,
        SPACE_LONG,
        TAB,
        UP,

        F1,
        F2,
        F3,
        F4,
        F5,
        F6,
        F7,
        F8,
        F9,
        F10,
        F11,
        F12,
        F13,
        F14,
        F15,

        Leader,
    ]

    max_len = len('<leader>')


class KeySequenceTokenizer(object):
    """Takes in a sequence of key names and tokenizes it."""

    def __init__(self, source):
        """Sequence of key names in Vim notation."""
        self.idx = -1
        self.source = source

    def consume(self):
        self.idx += 1
        if self.idx >= len(self.source):
            self.idx -= -1
            return EOF
        return self.source[self.idx]

    def peek_one(self):
        if (self.idx + 1) >= len(self.source):
            return EOF
        return self.source[self.idx + 1]

    def is_named_key(self, key):
        return key.lower() in key_names.as_list

    def sort_modifiers(self, modifiers):
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

    def long_key_name(self):
        key_name = ''
        modifiers = ''

        while True:
            c = self.consume()

            if c == EOF:
                raise ValueError("expected '>' at index {0}".format(self.idx))

            elif (c.lower() in ('c', 's', 'm', 'd', 'a')) and (self.peek_one() == '-'):
                # <A-...> is aliased to <M-...>
                if c.lower() == 'a':
                    c = 'm'

                if c.lower() in modifiers.lower():
                    raise ValueError('invalid modifier sequence: {0}'.format(self.source))

                modifiers += c + self.consume()

            elif c == '>':
                modifiers = self.sort_modifiers(modifiers.lower())

                if len(key_name) == 1:
                    if not modifiers:
                        raise ValueError('wrong sequence {0}'.format(self.source))

                    return '<' + modifiers.upper() + key_name + '>'

                elif self.is_named_key('<' + key_name + '>'):
                    return '<' + modifiers.upper() + key_name.lower() + '>'

                else:
                    raise ValueError("'{0}' is not a known key".format(key_name))

            else:
                key_name += c

    def tokenize_one(self):
        c = self.consume()

        if c == '<':
            return self._expand_vars(self.long_key_name())
        else:
            return c

    def iter_tokenize(self):
        while True:
            token = self.tokenize_one()
            if token == EOF:
                break
            yield token

    def _expand_vars(self, c):
        return variables.get(c) if variables.is_key_name(c) else c


def to_bare_command_name(seq):
    # type: (str) -> str
    #
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
    new_seq = list(KeySequenceTokenizer(
        re.sub(r'^(?:".)?(?:[1-9]+)?', '', seq)
    ).iter_tokenize())

    return ''.join(k for k in new_seq if not k.isdigit())


def assign(seq, modes, *args, **kwargs):
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
