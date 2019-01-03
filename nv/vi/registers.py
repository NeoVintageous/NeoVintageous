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


_UNNAMED = '"'
_SMALL_DELETE = '-'
_BLACK_HOLE = '_'
_LAST_INSERTED_TEXT = '.'
_FILE_NAME = '%'
_ALT_FILE_NAME = '#'
_EXPRESSION = '='

_SYS_CLIPBOARD_1 = '*'
_SYS_CLIPBOARD_2 = '+'
_SYS_CLIPBOARD_ALL = (
    _SYS_CLIPBOARD_1,
    _SYS_CLIPBOARD_2
)

_VALID_NAMES = tuple('abcdefghijklmnopqrstuvwxyz')
_VALID_NUMBERS = tuple('0123456789')

_SPECIAL = (
    _UNNAMED,
    _SMALL_DELETE,
    _BLACK_HOLE,
    _LAST_INSERTED_TEXT,
    _FILE_NAME,
    _ALT_FILE_NAME,
    _SYS_CLIPBOARD_1,
    _SYS_CLIPBOARD_2
)

_ALL = _SPECIAL + _VALID_NUMBERS + _VALID_NAMES

# TODO "* and "+ don't do what they should in linux.


def init_register_data():
    return {
        '0': None,
        # init registers 1-9
        '1-9': [None] * 9,
    }


_data = init_register_data()


class Registers:

    # Registers hold global data used mainly by yank, delete and paste.
    #
    # This class is meant to be used a descriptor.
    #
    #     class State(object):
    #         registers = Registers()
    #         ...
    #
    #     state = State()
    #     state.registers['%'] # now state.registers has access to the
    #                          # current view.
    #
    # And this is how you access registers:
    #
    # Setting registers...
    #
    #     state.registers['a'] = "foo" # => a == "foo"
    #     state.registers['A'] = "bar" # => a == "foobar"
    #     state.registers['1'] = "baz" # => 1 == "baz"
    #     state.registers[1] = "fizz"  # => 1 == "fizz"
    #
    # Retrieving registers...
    #
    #     state.registers['a'] # => "foobar"
    #     state.registers['A'] # => "foobar" (synonyms)

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
        # Check whether the option is set to a bool; could be any JSON type
        if (name in _SYS_CLIPBOARD_ALL or
           self.settings.view['vintageous_use_sys_clipboard'] is True):
                # Take care of multiple selections.
                if len(value) > 1:
                    self.view.run_command('copy')
                else:
                    set_clipboard(value[0])

    def set_expression(self, values):
        self.set(_EXPRESSION, values)

    def set(self, name, values):
        # Set an a-z or 0-9 register.
        # In order to honor multiple selections in Sublime Text, we need to
        # store register data as lists, one per selection. The paste command
        # will then make the final decision about what to insert into the buffer
        # when faced with unbalanced selection number / available register data.

        # We accept integers as register names.
        name = str(name)
        assert len(str(name)) == 1, "Register names must be 1 char long: " + name

        if name == _BLACK_HOLE:
            return

        assert isinstance(values, list), "Register values must be inside a list."

        # Coerce all values into strings.
        values = [str(v) for v in values]

        # Special registers and invalid registers won't be set.
        if (not (name.isalpha() or name.isdigit() or
                 name.isupper() or name == _UNNAMED or
                 name in _SYS_CLIPBOARD_ALL or
                 name == _EXPRESSION or
                 name == _SMALL_DELETE)):
                    # Vim fails silently.
                    # raise Exception("Can only set a-z and 0-9 registers.")
                    return None

        _data[name] = values

        if name not in (_EXPRESSION,):
            self._set_default_register(values)
            self._maybe_set_sys_clipboard(name, values)

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
        #   name (str|int)
        #
        # Returns:
        #   (list|str|None)

        # We accept integers or strings a register names.
        name = str(name)

        assert len(name) == 1, "Register names must be 1 char long."

        # Did we request a special register?
        if name == _BLACK_HOLE:
            return

        if name == _FILE_NAME:
            try:
                return [self.view.file_name()]
            except AttributeError:
                return ''

        if name in _SYS_CLIPBOARD_ALL:
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

    def yank(self, synthetize_new_line_at_eof=False, yanks_linewise=False, populates_small_delete_register=False, register=None, operation='yank'):  # noqa: E501
        # Args:
        #   cmd (ViTextCommandBase)
        #   register (str)
        #   operation (str)
        #
        # Returns:
        #   None
        #
        # Raises:
        #   ValueError:
        #       If operation is not supported.
        if register == _BLACK_HOLE:
            return

        # Populate registers if we have to.
        if register and register != _UNNAMED:
            self[register] = self.get_selected_text(synthetize_new_line_at_eof, yanks_linewise)
        else:
            self[_UNNAMED] = self.get_selected_text(synthetize_new_line_at_eof, yanks_linewise)

            # if yanking, the 0 register gets set
            if operation == 'yank':
                _data['0'] = self.get_selected_text(synthetize_new_line_at_eof, yanks_linewise)

            # if changing or deleting, the numbered registers get set
            elif operation in ('change', 'delete'):
                # TODO: very inefficient
                _data['1-9'].insert(0, self.get_selected_text(synthetize_new_line_at_eof, yanks_linewise))

                if len(_data['1-9']) > 10:
                    _data['1-9'].pop()

            else:
                raise ValueError('unsupported operation: ' + operation)

        # XXX: Small register delete. Improve this implementation.
        if populates_small_delete_register:
            is_same_line = (lambda r: self.view.line(r.begin()) == self.view.line(r.end() - 1))
            if all(is_same_line(x) for x in list(self.view.sel())):
                self[_SMALL_DELETE] = self.get_selected_text(synthetize_new_line_at_eof, yanks_linewise)

    def get_selected_text(self, synthetize_new_line_at_eof=False, yanks_linewise=False):  # noqa: E501
        # Inspect settings and populate registers as needed.
        #
        # Args:
        #   cmd (ViTextCommandBase)
        #
        # Returns:
        #   list
        fragments = [self.view.substr(r) for r in list(self.view.sel())]

        # Add new line at EOF, but don't add too many new lines.
        if (synthetize_new_line_at_eof and not yanks_linewise):
            # XXX: It appears regions can end beyond the buffer's EOF (?).
            if (not fragments[-1].endswith('\n') and self.view.sel()[-1].b >= self.view.size()):
                fragments[-1] += '\n'

        if fragments and yanks_linewise:
            for i, f in enumerate(fragments):
                # When should we add a newline character? Always except when we
                # have a non-\n-only string followed by a newline char.
                if (not f.endswith('\n')) or f.endswith('\n\n'):
                    fragments[i] = f + '\n'

        return fragments

    def to_dict(self):
        # XXX: Stopgap solution until we sublass from dict
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
