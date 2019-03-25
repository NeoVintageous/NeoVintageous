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

from collections import deque
import itertools

from sublime import get_clipboard
from sublime import set_clipboard

try:
    from Default.paste_from_history import g_clipboard_history as _clipboard_history

    def update_clipboard_history(text):
        _clipboard_history.push_text(text)

except Exception:
    print('NeoVintageous: could not import default package clipboard history updater')

    import traceback
    traceback.print_exc()

    def update_clipboard_history(text):
        print('NeoVintageous: could not update clipboard history: import error')

from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import VISUAL_LINE


# 1. The unnamed register ""
_UNNAMED = '"'

# 2. 10 numberd registers "0 to "9
_LAST_YANK = '0'
_LAST_DELETE = '1'
_NUMBERED = tuple('0123456789')

# 3 The small delete register "-
_SMALL_DELETE = '-'

# 4. 26 named registers "a to "z or "A to "Z
_NAMED = tuple('abcdefghijklmnopqrstuvwxyz')

# 5. Three read-only registers ":, "., "%
_LAST_EXECUTED_COMMAND = ':'
_LAST_INSERTED_TEXT = '.'
_CURRENT_FILE_NAME = '%'

# 6. Alternate buffer register "#
_ALTERNATE_FILE = '#'

# 7. The expression register "=
_EXPRESSION = '='

# 8. The selection and drop registers "*, "+, and "~
_CLIPBOARD_STAR = '*'
_CLIPBOARD_PLUS = '+'
_CLIPBOARD_TILDA = '~'

# 9. The black hole register "_
_BLACK_HOLE = '_'

# 10. Last search pattern register "/
_LAST_SEARCH_PATTERN = '/'

# Groups

_CLIPBOARD = (
    _CLIPBOARD_PLUS,
    _CLIPBOARD_STAR
)

_READ_ONLY = (
    _ALTERNATE_FILE,
    _CLIPBOARD_TILDA,
    _CURRENT_FILE_NAME,
    _LAST_EXECUTED_COMMAND,
    _LAST_INSERTED_TEXT
)

_SELECTION_AND_DROP = (
    _CLIPBOARD_PLUS,
    _CLIPBOARD_STAR,
    _CLIPBOARD_TILDA
)

_SPECIAL = (
    _ALTERNATE_FILE,
    _BLACK_HOLE,
    _CLIPBOARD_PLUS,
    _CLIPBOARD_STAR,
    _CLIPBOARD_TILDA,
    _CURRENT_FILE_NAME,
    _LAST_EXECUTED_COMMAND,
    _LAST_INSERTED_TEXT,
    _LAST_SEARCH_PATTERN,
    _SMALL_DELETE,
    _UNNAMED
)

_ALL = _SPECIAL + _NUMBERED + _NAMED


_data = {'0': None, '1-9': deque([None] * 9, maxlen=9)}  # type: dict
_linewise = {}  # type: dict


def _set_register_linewise(name, linewise):
    _linewise[name] = linewise


def _reset_data():
    _data.clear()
    _data['0'] = None
    _data['1-9'] = deque([None] * 9, maxlen=9)


def _shift_numbered_register(content):
    _data['1-9'].appendleft(content)


def _set_numbered_register(number, values):
    _data['1-9'][int(number) - 1] = values


def _get_numbered_register(number):
    return _data['1-9'][int(number) - 1]


def _is_register_linewise(register):
    return _linewise.get(register, False)


def _is_writable_register(register):
    if register == _UNNAMED:
        return True

    if register == _SMALL_DELETE:
        return True

    if register in _CLIPBOARD:
        return True

    if register.isdigit():
        return True

    if register.isalpha():
        return True

    if register.isupper():
        return True

    if register == _EXPRESSION:
        return True

    return False


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
#     # Digits can be given a str or int:
#     state.registers['1'] = "baz" # => 1 == "baz"
#     state.registers[1] = "fizz"  # => 1 == "fizz"
#
# Retrieving registers:
#
#     state.registers['a'] # => "foobar"
#     state.registers['A'] # => "foobar"
class Registers:

    def __get__(self, instance, owner):
        self.view = instance.view
        self.settings = instance.settings

        return self

    def _maybe_set_sys_clipboard(self, name, value):
        if (name in _CLIPBOARD or self.settings.view['vintageous_use_sys_clipboard'] is True):
            value = '\n'.join(value)
            set_clipboard(value)
            update_clipboard_history(value)

    # Set a register.
    # In order to honor multiple selections in Sublime Text, we need to store
    # register data as lists, one per selection. The paste command will then
    # make the final decision about what to insert into the buffer when faced
    # with unbalanced selection number / available register data.
    def _set(self, name, values, linewise=False):
        name = str(name)

        assert len(name) == 1, "Register names must be 1 char long: " + name

        if name == _BLACK_HOLE:
            return

        if not _is_writable_register(name):
            return None  # Vim fails silently.

        assert isinstance(values, list), "Register values must be inside a list."

        values = [str(v) for v in values]

        if name.isdigit() and name != '0':
            _set_numbered_register(name, values)
        else:
            _data[name] = values
            _linewise[name] = linewise

        if name not in (_EXPRESSION,):
            self._set_unnamed(values, linewise)
            self._maybe_set_sys_clipboard(name, values)

    def _set_unnamed(self, values, linewise=False):
        assert isinstance(values, list)
        _data[_UNNAMED] = [str(v) for v in values]
        _linewise[_UNNAMED] = linewise

    def set_expression(self, values):
        # Coerce all values into strings.
        _data[_EXPRESSION] = [str(v) for v in values]

    def _append(self, name, suffixes):
        assert len(name) == 1, "Register names must be 1 char long."
        assert name in "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "Can only append to A-Z registers."

        existing_values = _data.get(name.lower(), '')
        new_values = itertools.zip_longest(existing_values, suffixes, fillvalue='')
        new_values = [(prefix + suffix) for (prefix, suffix) in new_values]

        _data[name.lower()] = new_values

        self._set_unnamed(new_values)
        self._maybe_set_sys_clipboard(name, new_values)

    def _get(self, name=_UNNAMED):
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

        if name in _CLIPBOARD:
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

        if name.isdigit():
            if name == _LAST_YANK:
                return _data[name]

            return _get_numbered_register(name)

        try:
            return _data[name.lower()]
        except KeyError:
            pass

    def op_change(self, register=None, linewise=False):
        self._op('change', register=register, linewise=linewise)

    def op_delete(self, register=None, linewise=False):
        self._op('delete', register=register, linewise=linewise)

    def op_yank(self, register=None, linewise=False):
        self._op('yank', register=register, linewise=linewise)

    def _op(self, operation, register=None, linewise=False):
        if register == _BLACK_HOLE:
            return

        if linewise == 'maybe':
            linewise = False
            linewise_if_multiline = True
        else:
            linewise_if_multiline = False

        selected_text = self._get_selected_text(linewise=linewise)

        multiline = False
        for fragment in selected_text:
            if '\n' in fragment:
                multiline = True
                break

        if linewise_if_multiline and multiline:
            linewise = True

        if register and register != _UNNAMED:
            self[register] = selected_text
        else:
            self._set(_UNNAMED, selected_text, linewise)

            # Numbered register 0 contains the text from the most recent yank.
            if operation == 'yank':
                self._set(_LAST_YANK, selected_text, linewise)

            # Numbered register 1 contains the text deleted by the most
            # recent delete or change command, unless the command specified
            # another register or the text is less than one line (the small
            # delete register is used then).
            # With each successive deletion or change, Vim shifts the previous
            # contents of register 1 into register 2, 2 into 3, and so forth,
            # losing the previous contents of register 9.
            elif operation in ('change', 'delete'):
                if linewise or multiline:
                    _shift_numbered_register(selected_text)
            else:
                raise ValueError('unsupported operation: ' + operation)

        # The small delete register.
        if operation in ('change', 'delete') and not multiline:
            # TODO Improve small delete register implementation.
            is_same_line = (lambda r: self.view.line(r.begin()) == self.view.line(r.end() - 1))
            if all(is_same_line(x) for x in list(self.view.sel())):
                self._set(_SMALL_DELETE, selected_text, linewise)

    def get_for_big_p(self, register, mode):
        if not register:
            register = _UNNAMED

        as_str = ''
        values = self._get(register)
        linewise = _is_register_linewise(register)

        if values:
            # Populate unnamed register with the text we're about to paste into
            # (the text we're about to replace), but only if there was something
            # in requested register (not empty), and we're in VISUAL mode.
            if is_visual_mode(mode):
                current_content = self._get_selected_text(linewise=(mode == VISUAL_LINE))
                if current_content:
                    self._set(_UNNAMED, current_content, linewise=(mode == VISUAL_LINE))

            # If register content is from a linewise operation, and in VISUAL
            # mode, and doesn't begin with newline, then a newline is prefixed.
            as_str = ''.join(values)
            if as_str and linewise and is_visual_mode(mode) and as_str[0] != '\n':
                as_str = '\n' + as_str

        return as_str, linewise

    def get_for_p(self, register, mode):
        if not register:
            register = _UNNAMED

        values = self._get(register)
        linewise = _is_register_linewise(register)

        # Populate unnamed register with the text we're about to paste into (the
        # text we're about to replace), but only if there was something in
        # requested register (not empty), and we're in VISUAL mode.
        if values and is_visual_mode(mode):
            content = self._get_selected_text(linewise=(mode == VISUAL_LINE))
            if content:
                self._set(_UNNAMED, content, linewise=(mode == VISUAL_LINE))

        return values, linewise

    def _get_selected_text(self, new_line_at_eof=False, linewise=False):
        # Inspect settings and populate registers as needed.
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
        return {name: self._get(name) for name in _ALL}

    def __getitem__(self, key):
        return self._get(key)

    def __setitem__(self, key, value):
        # TODO logic to _set() so that uppercase is handled properly when using _set()
        try:
            if key.isupper():
                self._append(key, value)
            else:
                self._set(key, value)
        except AttributeError:
            # TODO [review] Looks like a bug: If set() above raises AttributeError so will this.
            self._set(key, value)
