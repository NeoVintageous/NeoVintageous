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


# FIXME Some command token constants values are the same as the some _TOKEN* contants.
# TODO [review] Do we need the token constants?


_TOKEN_EOF = -1
_TOKEN_UNKNOWN = 0
_TOKEN_DOT = 1
_TOKEN_DOLLAR = 2
_TOKEN_SEARCH_FORWARD = 3
_TOKEN_SEARCH_BACKWARD = 4
_TOKEN_COMMA = 5
_TOKEN_SEMICOLON = 6
_TOKEN_OFFSET = 7
_TOKEN_PERCENT = 8
_TOKEN_DIGITS = 9
_TOKEN_MARK = 10


# TODO [refactor] Look into getting rid of token_types and content, I don't
#   think they are used for anything. They can probably be inferred by the
#   extending class name.
class Token:

    # Attributes:
    #   :token_type (int):
    #   :content (str):

    def __init__(self, token_type, content):
        # type: (int, str) -> None
        self.token_type = token_type
        self.content = content

    def __str__(self):
        # type: () -> str
        return '{}({})'.format(self.__class__.__name__, self.content)

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Token):
            return False

        return other.__dict__ == self.__dict__


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
    #   :target_command (str): The name of the Sublime Text command to execute.

    def __init__(self, params, *args, forced=False, **kwargs):
        self.params = params or {}
        self.forced = forced
        self.addressable = False
        self.cooperates_with_global = False
        self.target_command = None

        super().__init__(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.content, self.__dict__)


class TokenCommand(TokenOfCommand):
    def __init__(self, name, target=None, params=None, forced=False, addressable=False, cooperates_with_global=False):
        super().__init__(token_type=100, content=name, forced=forced, params=params)

        if target is None:
            target = 'ex_' + name

        self.name = name
        self.target = target

        # FIXME TMP BC
        self.target_command = target

        self.addressable = addressable
        self.cooperates_with_global = cooperates_with_global


class TokenOfRange(Token):
    pass


class TokenEof(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(_TOKEN_EOF, '__EOF__')


class TokenDollar(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(_TOKEN_DOLLAR, '$')


class TokenComma(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(_TOKEN_COMMA, ',')


class TokenSemicolon(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(_TOKEN_SEMICOLON, ';')


class TokenOffset(TokenOfRange):
    def __init__(self, content, *args, **kwargs):
        super().__init__(_TOKEN_OFFSET, content)


class TokenPercent(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(_TOKEN_PERCENT, '%')


class TokenDot(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__(_TOKEN_DOT, '.')


class TokenOfSearch(TokenOfRange):
    pass


class TokenSearchForward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(_TOKEN_SEARCH_FORWARD, content)


class TokenSearchBackward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(_TOKEN_SEARCH_BACKWARD, content)


class TokenDigits(TokenOfRange):
    def __init__(self, content, *args, **kwargs):
        super().__init__(_TOKEN_DIGITS, content)


class TokenMark(TokenOfRange):
    def __init__(self, content, *args, **kwargs):
        super().__init__(_TOKEN_MARK, content)

    @property
    def exact(self):
        return self.content and self.content.startswith('`')
