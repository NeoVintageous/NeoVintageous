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
        self.content = content

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.content)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return False


class TokenCommand(Token):

    def __init__(self, name: str, target: str = None, params: dict = None, forced: bool = False, addressable: bool = False, cooperates_with_global: bool = False) -> None:  # noqa: E501
        # Args:
        #   :name (str): The name of the command.
        #   :target (str): The name of the ex command to execute. Defaults to
        #       the name. SHOULD NOT include the prefix "ex_".
        #   :params (dict): Default is {}.
        #   :forced (bool): Indicates if the bang character ! was placed
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
        #   :addressable (bool): Indicates if the command accepts ranges.
        #   :cooperates_with_global (bool): Indicates if the command cooperates
        #       with the :global command. This is special flag, because ex
        #       commands don't yet support a global_lines argument. It seems
        #       that, in Vim, some ex commands work well with :global and others
        #       ignore :global ranges. However, according to the docs, all ex
        #       commands should work with :global ranges. At the time of
        #       writing, the only command that supports the global_lines
        #       argument is the "print" command e.g. print all lines matching
        #       \d+ into new buffer: ":%global/\d+/print".
        super().__init__(content=name)

        self.name = name
        self.target = target or name
        self.params = params or {}
        # TODO Make forced a param and rename it "forceit", because this is sometimes required by ex commands.
        self.forced = forced
        self.addressable = addressable
        self.cooperates_with_global = cooperates_with_global

    def __str__(self) -> str:
        return '{} {}'.format(self.content, self.__dict__)


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
    pass


class TokenPercent(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__('%')


class TokenDot(TokenOfRange):
    def __init__(self, *args, **kwargs):
        super().__init__('.')


class TokenOfSearch(TokenOfRange):
    pass


class TokenSearchForward(TokenOfSearch):
    pass


class TokenSearchBackward(TokenOfSearch):
    pass


class TokenDigits(TokenOfRange):
    pass


class TokenMark(TokenOfRange):
    pass
