
# TODO REVIEW Do we actually need these IDs?

TOKEN_EOF = -1
TOKEN_UNKNOWN = 0
TOKEN_DOT = 1
TOKEN_DOLLAR = 2
TOKEN_SEARCH_FORWARD = 3
TOKEN_SEARCH_BACKWARD = 4
TOKEN_COMMA = 5
TOKEN_SEMICOLON = 6
TOKEN_OFFSET = 7
TOKEN_PERCENT = 8
TOKEN_DIGITS = 9
TOKEN_MARK = 10

TOKEN_COMMAND_UNKNOWN = 0
TOKEN_COMMAND_SUBSTITUTE = 1
TOKEN_COMMAND_ONLY = 2
TOKEN_COMMAND_REGISTERS = 3
TOKEN_COMMAND_WRITE = 4
TOKEN_COMMAND_GOTO = 5
TOKEN_COMMAND_BUFFERS = 6
TOKEN_COMMAND_ABBREVIATE = 7
TOKEN_COMMAND_VSPLIT = 8
TOKEN_COMMAND_SHELL_OUT = 9
TOKEN_COMMAND_SHELL = 10
TOKEN_COMMAND_READ_SHELL_OUT = 11
TOKEN_COMMAND_MAP = 12
TOKEN_COMMAND_UNMAP = 13
TOKEN_COMMAND_NMAP = 14
TOKEN_COMMAND_NUNMAP = 15
TOKEN_COMMAND_OMAP = 16
TOKEN_COMMAND_OUNMAP = 17
TOKEN_COMMAND_VMAP = 18
TOKEN_COMMAND_VUNMAP = 19
TOKEN_COMMAND_UNABBREVIATE = 20
TOKEN_COMMAND_PRINT_WORKING_DIR = 21
TOKEN_COMMAND_WRITE_FILE = 22
TOKEN_COMMAND_REPLACE_FILE = 23
TOKEN_COMMAND_WRITE_ALL = 24
TOKEN_COMMAND_NEW_FILE = 25
TOKEN_COMMAND_FILE = 26
TOKEN_COMMAND_MOVE = 27
TOKEN_COMMAND_COPY = 28
TOKEN_COMMAND_DOUBLE_AMPERSAND = 30
TOKEN_COMMAND_DELETE = 32
TOKEN_COMMAND_GLOBAL = 33
TOKEN_COMMAND_PRINT = 34
TOKEN_COMMAND_QUIT = 35
TOKEN_COMMAND_QUIT_ALL = 36
TOKEN_COMMAND_WRITE_AND_QUIT = 37
TOKEN_COMMAND_BROWSE = 38
TOKEN_COMMAND_EDIT = 39
TOKEN_COMMAND_CQUIT = 40
TOKEN_COMMAND_EXIT = 41
TOKEN_COMMAND_NEW = 42
TOKEN_COMMAND_YANK = 43
TOKEN_COMMAND_TAB_NEXT = 45
TOKEN_COMMAND_TAB_PREV = 46
TOKEN_COMMAND_TAB_LAST = 47
TOKEN_COMMAND_TAB_FIRST = 48
TOKEN_COMMAND_TAB_ONLY = 49
TOKEN_COMMAND_CD = 50
TOKEN_COMMAND_CDD = 51
TOKEN_COMMAND_UNVSPLIT = 52
TOKEN_COMMAND_SET_LOCAL = 53
TOKEN_COMMAND_SET = 54
TOKEN_COMMAND_LET = 55
TOKEN_COMMAND_WRITE_AND_QUIT_ALL = 56
TOKEN_COMMAND_CLOSE = 57
TOKEN_COMMAND_SMAP = 58
TOKEN_COMMAND_HELP = 59
TOKEN_COMMAND_SPLIT = 60


class Token():

    # Args:
    #   :token_type (int):
    #   :content (str):
    #
    # Todo:
    #   Look into getting rid of token_types and content, I don't think they are
    #   used for anything. They can probably be inferred by the extending class
    #   name.

    def __init__(self, token_type, content):
        self.token_type = token_type
        self.content = content

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return '<[{0}]({1})>'.format(self.__class__.__name__, self.content)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False

        return (other.content == self.content and
                other.token_type == self.token_type)


class TokenOfRange(Token):
    pass


class TokenOfCommand(Token):

    # Args:
    #   :params (dict): Default is {}.
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
    #   :addressable (bool): Indicates if the command accepts ranges.
    #   :cooperates (bool): Indicates if the command cooperates with :global.
    #       XXX: It seems that, in Vim, some ex commands work well with :global
    #       and others ignore global's ranges. However, according to the docs,
    #       all ex commands should work with :global ranges?
    #   :target_command (str): The name of the Sublime Text command to execute.

    def __init__(self, params, *args, forced=False, **kwargs):
        self.params = params or {}
        self.forced = forced
        self.addressable = False
        self.cooperates_with_global = False
        self.target_command = None

        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        return super().__eq__(other) and other.params == self.params

    def __str__(self):
        return '{0} {1}'.format(self.content, self.params)
