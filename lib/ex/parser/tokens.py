from .tokens_base import * # noqa


class TokenEof(Token): # noqa
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_EOF, '__EOF__', *args, **kwargs)  # noqa: F405


class TokenOfSearch(TokenOfRange): # noqa
    pass


class TokenDollar(TokenOfRange): # noqa
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_DOLLAR, '$', *args, **kwargs)  # noqa: F405


class TokenComma(TokenOfRange): # noqa
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_COMMA, ',', *args, **kwargs)  # noqa: F405


class TokenSemicolon(TokenOfRange): # noqa
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_SEMICOLON, ';', *args, **kwargs)  # noqa: F405


class TokenOffset(TokenOfRange): # noqa
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_OFFSET, content, *args, **kwargs)  # noqa: F405

    def __str__(self):
        offsets = []
        for offset in self.content:
            offsets.append('{0}{1}'.format('' if offset < 0 else '+', offset))
        return ''.join(offsets)


class TokenPercent(TokenOfRange): # noqa
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_PERCENT, '%', *args, **kwargs)  # noqa: F405


class TokenDot(TokenOfRange): # noqa
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_DOT, '.', *args, **kwargs)  # noqa: F405


class TokenSearchForward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_SEARCH_FORWARD, content, *args, **kwargs)  # noqa: F405

    def __str__(self):
        return '/{0}/'.format(self.content)


class TokenSearchBackward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_SEARCH_BACKWARD, content, *args, **kwargs)  # noqa: F405

    def __str__(self):
        return '?{0}?'.format(self.content)


class TokenDigits(TokenOfRange): # noqa
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_DIGITS, content, *args, **kwargs)  # noqa: F405


class TokenMark(TokenOfRange): # noqa
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_MARK, content, *args, **kwargs)  # noqa: F405

    def __str__(self):
        return "'{}".format(self.content)

    def __repr__(self):
        return "<[{0}]('{1})>".format(self.__class__.__name__, self.content)

    @property
    def exact(self):
        return self.content and self.content.startswith('`')
