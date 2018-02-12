import re


EOF = '__EOF__'


class ScannerState:

    # Args:
    #   :source: The string to be scanned.
    #
    # Attributes:
    #   :source (str): The string to be scanned.
    #   :position (int): The current scan position. Default is 0.
    #   :start (int): The most recent scan start. Default is 0.

    def __init__(self, source):
        # type: (str) -> None
        self.source = source
        self.position = 0
        self.start = 0

    def consume(self):
        # type: () -> str
        # Consume one character from source.
        #
        # Returns:
        #   str: One character or EOF constant ("__EOF__") if no characters left
        #       in source.
        if self.position >= len(self.source):
            return EOF

        c = self.source[self.position]

        self.position += 1

        return c

    def backup(self):
        # type: () -> None
        """Backs up scanner position by 1 character."""
        self.position -= 1

    def ignore(self):
        # type: () -> None
        """Discards the current span of characters that would normally be `.emit()`ted."""
        self.start = self.position

    def emit(self):
        # type: () -> str
        """
        Return the `source` substring spanning from [`start`, `position`).

        Also advances `start`.
        """
        content = self.source[self.start:self.position]
        self.ignore()

        return content

    def skip(self, character):
        # type: (str) -> None
        """Consumes @character while it matches."""
        while True:
            c = self.consume()
            if c == EOF or c != character:
                break

        if c != EOF:
            self.backup()

    def skip_run(self, characters):
        # type: (str) -> None
        """Skips @characters while there's a match."""
        while True:
            c = self.consume()
            if c == EOF or c not in characters:
                break

        if c != EOF:
            self.backup()

    def expect(self, item, on_error=None):
        # type: (...) -> str
        """
        Require @item to match at the current `position`.

        Raises a ValueError if @item does not match.

        @item
          A character.

        @on_error
          A function that returns an error. The error returned overrides
          the default ValueError.
        """
        c = self.consume()
        if c != item:
            if on_error:
                raise on_error()
            raise ValueError('expected {0}, got {1} instead'.format(item, c))

        return c

    def expect_match(self, pattern, on_error=None):
        """
        Require item to match at the current position.

        Raises a ValueError if item does not match.

        Args:
            pattern (str): A regular expression.
            on_error (Callable): A function that returns an error. The error
                returned overrides the default ValueError.

        """
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m

        if not on_error:
            raise ValueError('expected match with \'{0}\', at \'{1}\''.format(pattern, self.source[self.position:]))

        raise on_error()

    def peek(self, item):
        # type: (str) -> bool
        """
        Return True if item matches at the current position, False otherwise.

        Args:
            item (str):

        """
        return self.source[self.position:self.position + len(item)] == item

    def match(self, pattern):
        """
        Return the match obtained by searching @pattern.

        The current `position` will advance as many characters as the match's
        length.

        Args:
            pattern (str): A regular expression.

        """
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m

        return
