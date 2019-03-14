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


class ViCommandDefBase:

    _serializable = ['_inp', ]

    def __init__(self):
        self.input_parser = None
        self.inp = ''

    # TODO For compatibility. Should be removed eventually.
    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        return '<{}>'.format(self.__class__.__qualname__)

    @property
    def accept_input(self):
        return False

    def accept(self, key):
        raise NotImplementedError('{} must implement accept()'.format(self.__class__.__name__))

    @property
    def inp(self):
        return self._inp

    @inp.setter
    def inp(self, value):
        self._inp = value

    def reset(self):
        self.inp = ''

    def translate(self, state):
        """Return the command as a JSON object."""
        raise NotImplementedError('{} must implement translate()'.format(self.__class__.__name__))

    @classmethod
    def from_json(cls, data):
        """Instantiate the command from a JSON object."""
        instance = cls()
        instance.__dict__.update(data)

        return instance

    def serialize(self):
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
