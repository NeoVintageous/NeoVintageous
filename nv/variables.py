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


_special_strings = {
    '<leader>': 'mapleader',
    '<localleader>': 'maplocalleader',
}


_defaults = {
    'mapleader': '<bslash>',
    'maplocalleader': '<bslash>'
}


_variables = {}  # type: dict


def expand_keys(seq: str) -> str:
    seq_lower = seq.lower()
    for key, key_value, in _special_strings.items():
        while key in seq_lower:
            index = seq_lower.index(key)
            value = _variables.get(key_value, _defaults.get(key_value))
            if value:
                seq = seq[:index] + value + seq[index + len(key):]
                seq_lower = seq.lower()
            else:

                # XXX This is a safe guard against infinite loop. Ideally
                # special keys that have no default or variable values should
                # just be replaced as-is, that will require reworking this
                # function.

                return seq

    return seq


def is_key_name(name: str) -> bool:
    return name.lower() in _special_strings


def get(name: str) -> str:
    name = name.lower()
    name = _special_strings.get(name, name)

    return _variables.get(name, _defaults.get(name))


def set(name: str, value: str) -> None:
    _variables[name] = value


def variables_clear() -> None:
    _variables.clear()
