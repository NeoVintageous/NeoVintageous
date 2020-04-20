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

from NeoVintageous.nv.vim import INSERT as _INSERT
from NeoVintageous.nv.vim import NORMAL as _NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING as _OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT as _SELECT
from NeoVintageous.nv.vim import VISUAL as _VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK as _VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE as _VISUAL_LINE


mappings = {
    _INSERT: {},
    _NORMAL: {},
    _OPERATOR_PENDING: {},
    _SELECT: {},
    _VISUAL: {},
    _VISUAL_BLOCK: {},
    _VISUAL_LINE: {}
}  # type: dict


classes = {}  # type: dict


def register(seq: str, modes: tuple, *args, **kwargs):
    """
    Register a 'key sequence' to 'command' mapping with NeoVintageous.

    The registered key sequence must be known to NeoVintageous. The
    registered command must be a ViMotionDef or ViOperatorDef.

    The decorated class is instantiated with `*args` and `**kwargs`.

    @keys
      A list of (`mode`, `sequence`) pairs to map the decorated
      class to.
    """
    def inner(cls):
        for mode in modes:
            mappings[mode][seq] = cls(*args, **kwargs)
            classes[cls.__name__] = cls
        return cls
    return inner
