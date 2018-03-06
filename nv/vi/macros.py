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


class MacroRegisters(dict):
    """Crude implementation of macro registers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in ('%', '#'):
            raise ValueError('invalid register key: %s' % key)
        # TODO further restrict valid register names.
        # TODO implement a vs A register.
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        if key in ('%', '#'):
            raise ValueError('unsupported key: %s' % key)
        # TODO further restrict valid register names.
        # TODO implement a vs A register.
        return super().__getitem__(key.lower())
