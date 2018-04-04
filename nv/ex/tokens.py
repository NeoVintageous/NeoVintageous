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


class Token:

    def __init__(self, content):
        # type: (str) -> None
        self.content = content

    def __str__(self):
        # type: () -> str
        return '{}({})'.format(self.__class__.__name__, self.content)

    def __eq__(self, other):
        # type: (object) -> bool
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return False


class TokenOfCommand(Token):

    # Args:
    #   :params (dict): Default is {}.
    #
    #   :forced (bool): Indicates if the '!' (bang) character was placed
    #       immediatley after the command. The '!' (bang) character after an
    #       Ex command makes a command behave in a different way. The '!'
    #       should be placed immediately after the command, without any
    #       blanks in between. If you insert blanks the '!' will be seen as
    #       an argument for the command, which has a different meaning. For
    #       example:
    #           :w! name        Write the current buffer to file "name",
    #                           overwriting any existing file.
    #           :w !name        Send the current buffer as standard input to
    #                           command "name".
    #
    # Attributes:
    #
    #   :addressable (bool): Indicates if the command accepts ranges.
    #
    #   :cooperates_with_global (bool): Indicates if the command cooperates with
    #       the :global command. This is special flag, because ex commands don't
    #       yet support a global_lines argument. It seems that, in Vim, some ex
    #       commands work well with :global and others ignore :global ranges.
    #       However, according to the docs, all ex commands should work with
    #       :global ranges. At the time of writing, the only command that
    #       supports the global_lines argument is the "print" command e.g. print
    #       all lines matching \d+ into new buffer: ":%global/\d+/print".
    #
    #   :target (str): The name of the Sublime Text command to execute.

    def __init__(self, params, *args, forced=False, **kwargs):
        self.params = params or {}
        self.forced = forced
        self.addressable = False
        self.cooperates_with_global = False
        self.target = None

        super().__init__(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.content, self.__dict__)


class TokenCommand(TokenOfCommand):
    def __init__(self, name, target=None, params=None, forced=False, addressable=False, cooperates_with_global=False):
        super().__init__(content=name, forced=forced, params=params)

        if target is None:
            target = 'ex_' + name

        self.name = name
        self.target = target
        self.addressable = addressable
        self.cooperates_with_global = cooperates_with_global


class TokenOfRange(Token):
    pass


class TokenEof(Token):
    def __init__(self, *args, **kwargs):
        super().__init__('__EOF__')


class TokenDollar(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__('$')


class TokenComma(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(',')


class TokenSemicolon(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(';')


class TokenOffset(TokenOfRange):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content)


class TokenPercent(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__('%')


class TokenDot(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__('.')


class TokenOfSearch(TokenOfRange):
    pass


class TokenSearchForward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content)


class TokenSearchBackward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content)


class TokenDigits(TokenOfRange):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content)


class TokenMark(TokenOfRange):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content)
