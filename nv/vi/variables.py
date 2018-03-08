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


_SPECIAL_STRINGS = {
    '<leader>': 'mapleader',
    '<localleader>': 'maplocalleader',
}


_DEFAULTS = {
    'mapleader': '\\',
    'maplocalleader': '\\'
}


_VARIABLES = {
}


def expand_keys(seq):
    seq_lower = seq.lower()
    for key, key_value, in _SPECIAL_STRINGS.items():
        while key in seq_lower:
            index = seq_lower.index(key)
            value = _VARIABLES.get(key_value, _DEFAULTS.get(key_value))
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


def is_key_name(name):
    return name.lower() in _SPECIAL_STRINGS


def get(name):
    name = name.lower()
    name = _SPECIAL_STRINGS.get(name, name)

    return _VARIABLES.get(name, _DEFAULTS.get(name))


def set_(name, value):
    _VARIABLES[name] = value


class Variables(object):

    def __get__(self, instance, owner):
        self.view = instance.view
        self.settings = instance.settings

        return self

    def get(self, name):
        return get(name)

    def set(self, name, value):
        return set_(name, value)
