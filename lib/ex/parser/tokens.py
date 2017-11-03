from .tokens_base import *  # FIXME # noqa: F403


class TokenEof(Token):  # FIXME # noqa: F405
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_EOF, '__EOF__', *args, **kwargs)  # FIXME # noqa: F405


class TokenOfSearch(TokenOfRange):  # FIXME # noqa: F405
    pass


class TokenDollar(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_DOLLAR, '$', *args, **kwargs)  # FIXME # noqa: F405


class TokenComma(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_COMMA, ',', *args, **kwargs)  # FIXME # noqa: F405


class TokenSemicolon(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_SEMICOLON, ';', *args, **kwargs)  # FIXME # noqa: F405


class TokenOffset(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_OFFSET, content, *args, **kwargs)  # FIXME # noqa: F405

    def __str__(self):
        offsets = []
        for offset in self.content:
            offsets.append('{0}{1}'.format('' if offset < 0 else '+', offset))

        return ''.join(offsets)


class TokenPercent(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_PERCENT, '%', *args, **kwargs)  # FIXME # noqa: F405


class TokenDot(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, *args, **kwargs):
        super().__init__(TOKEN_DOT, '.', *args, **kwargs)  # FIXME # noqa: F405


class TokenSearchForward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_SEARCH_FORWARD, content, *args, **kwargs)  # FIXME # noqa: F405

    def __str__(self):
        return '/{0}/'.format(self.content)


class TokenSearchBackward(TokenOfSearch):
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_SEARCH_BACKWARD, content, *args, **kwargs)  # FIXME # noqa: F405

    def __str__(self):
        return '?{0}?'.format(self.content)


class TokenDigits(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_DIGITS, content, *args, **kwargs)  # FIXME # noqa: F405


class TokenMark(TokenOfRange):  # FIXME # noqa: F405
    def __init__(self, content, *args, **kwargs):
        super().__init__(TOKEN_MARK, content, *args, **kwargs)  # FIXME # noqa: F405

    def __str__(self):
        return "'{}".format(self.content)

    def __repr__(self):
        return "<[{0}]('{1})>".format(self.__class__.__name__, self.content)

    @property
    def exact(self):
        return self.content and self.content.startswith('`')
