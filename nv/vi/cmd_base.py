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


CMD_TYPE_MOTION = 1
CMD_TYPE_ACTION = 2
CMD_TYPE_ANY = 3
CMD_TYPE_OTHER = 4
CMD_TYPE_USER = 5
CMD_TYPE_OPEN_NAME_SPACE = 6


class ViCommandDefBase:
    """Base class for all Vim commands."""

    _serializable = ['_inp', ]

    def __init__(self):
        # the name of the st command wrapped by this class
        self.command = '<unset>'
        self.input_parser = None
        self._inp = ''

    def __getitem__(self, key):
        # XXX: For compatibility. Should be removed eventually.
        return self.__dict__[key]

    def __str__(self):
        return '<{0} ({1})>'.format(self.__class__.__qualname__, self.command)

    @property
    def accept_input(self):
        return False

    @property
    def inp(self):
        """Input for this command."""
        return self._inp

    def accept(self, key):
        """Process input for this command."""
        _name = self.__class__.__name__
        assert self.input_parser, '{0} does not provide an input parser'.format(_name)
        raise NotImplementedError('{0} must implement .accept()'.format(_name))

    def reset(self):
        self._inp = ''

    def translate(self, state):
        """
        Return the command as a valid Json object containing all necessary data to be run by NeoVintageous.

        This is usually the last step before handing the command off to ST.

        Every motion and operator must override this method.

        @state
          The current state.
        """
        raise NotImplementedError('command {0} must implement .translate()'.format(self.__class__.__name__))

    @classmethod
    def from_json(cls, data):
        """
        Instantiate a command from a valid Json object representing one.

        @data
          Serialized command data as provided by .serialize().
        """
        instance = cls()
        instance.__dict__.update(data)
        return instance

    def serialize(self):
        """Return a valid Json object representing this command in a format NeoVintageous uses internally."""
        data = {'name': self.__class__.__name__,
                'data': {k: v for k, v in self.__dict__.items() if k in self._serializable}}

        return data


class ViMissingCommandDef(ViCommandDefBase):
    def translate(self):
        raise TypeError('ViMissingCommandDef should not be used as a runnable command')


class ViMotionDef(ViCommandDefBase):
    """Base class for all motions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = False
        self.scroll_into_view = False
        self.type = CMD_TYPE_MOTION


class ViOperatorDef(ViCommandDefBase):
    """Base class for all operators."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = False
        self.scroll_into_view = False
        self.motion_required = False
        self.type = CMD_TYPE_ACTION
        self.repeatable = False
