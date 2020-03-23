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

from NeoVintageous.nv.utils import InputParser
from NeoVintageous.nv.utils import translate_char


class ViCommandDefBase:

    _serializable = ['_inp', ]

    def __init__(self, *args, **kwargs):
        self.input_parser = None
        self.inp = ''

    def __str__(self) -> str:
        return '<{}>'.format(self.__class__.__qualname__)

    @property
    def accept_input(self) -> bool:
        return False

    def accept(self, key: str) -> bool:
        raise NotImplementedError('{} must implement accept()'.format(self.__class__.__name__))

    @property
    def inp(self) -> str:
        return self._inp

    @inp.setter
    def inp(self, value: str) -> None:
        self._inp = value

    def reset(self) -> None:
        self.inp = ''

    def translate(self, view) -> dict:
        """Return the command as a JSON object."""
        raise NotImplementedError('{} must implement translate()'.format(self.__class__.__name__))

    @classmethod
    def from_json(cls, data: dict) -> object:
        """Instantiate the command from a JSON object."""
        instance = cls()
        instance.__dict__.update(data)

        return instance

    def serialize(self) -> dict:
        """Serialize the command as JSON object."""
        return {
            'name': self.__class__.__name__,
            'data': {k: v for k, v in self.__dict__.items() if k in self._serializable}
        }


class ViMissingCommandDef(ViCommandDefBase):

    def translate(self):
        raise TypeError('ViMissingCommandDef should not be used as a runnable command')


class ViMotionDef(ViCommandDefBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = False
        self.scroll_into_view = False


class ViOperatorDef(ViCommandDefBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = False
        self.scroll_into_view = False
        self.motion_required = False
        self.repeatable = False


class RequiresOneCharMixinDef(ViCommandDefBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_parser = InputParser(InputParser.IMMEDIATE)

    @property
    def accept_input(self) -> bool:
        return self.inp == ''

    def accept(self, key: str) -> bool:
        self.inp += translate_char(key)

        return True
