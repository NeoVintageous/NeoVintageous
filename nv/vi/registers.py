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

import itertools

from sublime import get_clipboard
from sublime import set_clipboard

from NeoVintageous.nv.vim import VISUAL


# 1. The unnamed register ""
_UNNAMED = '"'

# 2. 10 numberd registers "0 to "9
_NUMBERS = tuple('0123456789')

# 3 The small delete register "-
_SMALL_DELETE = '-'

# 4. 26 named registers "a to "z or "A to "Z
_NAMES = tuple('abcdefghijklmnopqrstuvwxyz')

# 5. Three read-only registers ":, "., "%
_LAST_EXECUTED_COMMAND = ':'
_LAST_INSERTED_TEXT = '.'
_CURRENT_FILE_NAME = '%'

# 6. Alternate buffer register "#
_ALT_FILE = '#'

_READ_ONLY = (
    _LAST_EXECUTED_COMMAND,
    _LAST_INSERTED_TEXT,
    _CURRENT_FILE_NAME,
    _ALT_FILE
)

# 7. The expression register "=
_EXPRESSION = '='

# 8. The selection and drop registers "*, "+, and "~
_CLIPBOARD_STAR = '*'
_CLIPBOARD_PLUS = '+'
_CLIPBOARD_TILDA = '~'
_CLIPBOARD_ALL = (_CLIPBOARD_STAR, _CLIPBOARD_PLUS)
_SELECTION_AND_DROP = (_CLIPBOARD_STAR, _CLIPBOARD_PLUS, _CLIPBOARD_TILDA)

# 9. The black hole register "_
_BLACK_HOLE = '_'

# 10. Last search pattern register "/
_LAST_SEARCH_PATTERN = '/'

_SPECIAL = (
    _UNNAMED,
    _SMALL_DELETE,
    _BLACK_HOLE,
    _LAST_INSERTED_TEXT,
    _LAST_EXECUTED_COMMAND,
    _LAST_SEARCH_PATTERN,
    _CURRENT_FILE_NAME,
    _ALT_FILE,
    _CLIPBOARD_STAR,
    _CLIPBOARD_PLUS,
    _CLIPBOARD_TILDA
)

_ALL = _SPECIAL + _NUMBERS + _NAMES


def init_register_data():
    return {
        '0': None,
        # init registers 1-9
        '1-9': [None] * 9,
    }


_data = init_register_data()


# Registers hold global data used mainly by yank, delete and paste.
#
# This class is meant to be used a descriptor.
#
#     class State(object):
#         registers = Registers()
#         ...
#
#     # now state.registers has access to the current view.
#     state = State()
#     state.registers['%']
#
# And this is how you access registers:
#
# Setting registers:
#
#     state.registers['a'] = "foo" # => a == "foo"
#     state.registers['A'] = "bar" # => a == "foobar"
#     state.registers['1'] = "baz" # => 1 == "baz"
#     state.registers[1] = "fizz"  # => 1 == "fizz"
#
# Retrieving registers:
#
#     state.registers['a'] # => "foobar"
#     state.registers['A'] # => "foobar" (synonyms)
class Registers:

    def __get__(self, instance, owner):
        self.view = instance.view
        self.settings = instance.settings

        return self

    def _set_default_register(self, values):
        assert isinstance(values, list)
        # Coerce all values into strings.
        values = [str(v) for v in values]
        _data[_UNNAMED] = values

    def _maybe_set_sys_clipboard(self, name, value):
        if (name in _CLIPBOARD_ALL or self.settings.view['vintageous_use_sys_clipboard'] is True):
            # Take care of multiple selections.
            if len(value) > 1:
                self.view.run_command('copy')
            else:
                set_clipboard(value[0])

    # Set a register.
    # In order to honor multiple selections in Sublime Text, we need to store
    # register data as lists, one per selection. The paste command will then
    # make the final decision about what to insert into the buffer when faced
    # with unbalanced selection number / available register data.
    def set(self, name, values):
        name = str(name)

        assert len(name) == 1, "Register names must be 1 char long: " + name

        if name == _BLACK_HOLE:
            return

        assert isinstance(values, list), "Register values must be inside a list."

        # Coerce all values into strings.
        values = [str(v) for v in values]

        # Special registers and invalid registers won't be set.
        if (not (name.isalpha() or name.isdigit() or
                 name.isupper() or name == _UNNAMED or
                 name in _CLIPBOARD_ALL or
                 name == _EXPRESSION or
                 name == _SMALL_DELETE)):
                    # Vim fails silently.
                    return None

        _data[name] = values

        if name not in (_EXPRESSION,):
            self._set_default_register(values)
            self._maybe_set_sys_clipboard(name, values)

    def set_expression(self, values):
        self.set(_EXPRESSION, values)

    def append_to(self, name, suffixes):
        """Append to an a-z register. `name` must be a capital in A-Z."""
        assert len(name) == 1, "Register names must be 1 char long."
        assert name in "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "Can only append to A-Z registers."

        existing_values = _data.get(name.lower(), '')
        new_values = itertools.zip_longest(existing_values, suffixes, fillvalue='')
        new_values = [(prefix + suffix) for (prefix, suffix) in new_values]
        _data[name.lower()] = new_values
        self._set_default_register(new_values)
        self._maybe_set_sys_clipboard(name, new_values)

    def get(self, name=_UNNAMED):
        # Args:
        #   name (str|int) Accepts integers or strings as register names.
        #
        # Returns:
        #   (list|str|None)
        name = str(name)

        assert len(name) == 1, "Register names must be 1 char long."

        if name == _CURRENT_FILE_NAME:
            try:
                return [self.view.file_name()]
            except AttributeError:
                return ''

        if name in _CLIPBOARD_ALL:
            return [get_clipboard()]

        if ((name not in (_UNNAMED, _SMALL_DELETE)) and (name in _SPECIAL)):
            return

        # Special case lumped among these --user always wants the sys clipboard
        if ((name == _UNNAMED) and (self.settings.view['vintageous_use_sys_clipboard'] is True)):
            return [get_clipboard()]

        # If the expression register holds a value and we're requesting the
        # unnamed register, return the expression register and clear it
        # aftwerwards.
        if name == _UNNAMED and _data.get(_EXPRESSION, ''):
            value = _data[_EXPRESSION]
            _data[_EXPRESSION] = ''

            return value

        # We requested an [a-z0-9"] register.
        if name.isdigit():
            if name == '0':
                return _data[name]

            return _data['1-9'][int(name) - 1]

        try:
            # In Vim, "A and "a seem to be synonyms, so accept either.
            return _data[name.lower()]
        except KeyError:
            pass

    def op_yank(self, new_line_at_eof=False, linewise=False, small_delete=False, register=None):
        self._op(new_line_at_eof, linewise, small_delete, register, operation='yank')

    def op_change(self, new_line_at_eof=False, linewise=False, small_delete=False, register=None):
        self._op(new_line_at_eof, linewise, small_delete, register, operation='change')

    def op_delete(self, new_line_at_eof=False, linewise=False, small_delete=False, register=None):
        self._op(new_line_at_eof, linewise, small_delete, register, operation='delete')

    def _op(self, new_line_at_eof=False, linewise=False, small_delete=False, register=None, operation=None):
        if register == _BLACK_HOLE:
            return

        selected_text = self._get_selected_text(new_line_at_eof, linewise)

        if register and register != _UNNAMED:
            self[register] = selected_text
        else:
            self[_UNNAMED] = selected_text

            if operation == 'yank':  # if yanking, the 0 register gets set
                _data['0'] = selected_text
            elif operation in ('change', 'delete'):  # if changing or deleting, the numbered registers get set
                # TODO: very inefficient
                _data['1-9'].insert(0, selected_text)
                if len(_data['1-9']) > 10:
                    _data['1-9'].pop()
            else:
                raise ValueError('unsupported operation: ' + operation)

        # XXX: Small register delete. Improve this implementation.
        if small_delete:
            is_same_line = (lambda r: self.view.line(r.begin()) == self.view.line(r.end() - 1))
            if all(is_same_line(x) for x in list(self.view.sel())):
                self[_SMALL_DELETE] = selected_text

    def get_for_paste(self, register, mode):
        if not register:
            register = _UNNAMED

        values = self[register]

        # Populate unnamed register with the text we're about to paste into (the
        # text we're about to replace), but only if there was something in
        # requested register (not empty), and we're in VISUAL mode.
        if values and (mode == VISUAL):
            self[_UNNAMED] = self._get_selected_text(new_line_at_eof=True)

        return values

    def _get_selected_text(self, new_line_at_eof=False, linewise=False):
        # Inspect settings and populate registers as needed.
        #
        # Args:
        #   cmd (ViTextCommandBase)
        #
        # Returns:
        #   list
        fragments = [self.view.substr(r) for r in list(self.view.sel())]

        # Add new line at EOF, but don't add too many new lines.
        if (new_line_at_eof and not linewise):
            # XXX: It appears regions can end beyond the buffer's EOF (?).
            if (not fragments[-1].endswith('\n') and self.view.sel()[-1].b >= self.view.size()):
                fragments[-1] += '\n'

        if fragments and linewise:
            for i, f in enumerate(fragments):
                # When should we add a newline character? Always except when we
                # have a non-\n-only string followed by a newline char.
                if (not f.endswith('\n')) or f.endswith('\n\n'):
                    fragments[i] = f + '\n'

        return fragments

    def to_dict(self):
        return {name: self.get(name) for name in _ALL}

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        try:
            if key.isupper():
                self.append_to(key, value)
            else:
                self.set(key, value)
        except AttributeError:
            # TODO [review] Looks like a bug: If set() above raises AttributeError so will this.
            self.set(key, value)
