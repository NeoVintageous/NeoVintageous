"""json5kit - A Parser and CST for JSON5."""
from __future__ import annotations
import string
import sys

from typing import Sequence, cast

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


from json5kit.nodes import (
    Json5Array,
    Json5Boolean,
    Json5Comma,
    Json5Comment,
    Json5File,
    Json5Key,
    Json5Newline,
    Json5Node,
    Json5Null,
    Json5Number,
    Json5Object,
    Json5Primitive,
    Json5String,
    Json5Trivia,
    Json5Whitespace,
)
from json5kit.visitor import Json5Visitor, Json5Transformer


class Json5ParseError(Exception):
    """Raised when the JSON5 string has bad syntax."""

    def __init__(self, message: str, index: int) -> None:
        super().__init__(message)
        self.index = index


class Json5Parser:
    """Parser that converts a JSON5 string into a CST."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.current = 0

    @property
    def scanned(self) -> int:
        """Returns True if the source has been fully scanned."""
        return self.current >= len(self.source)

    def advance(self) -> None:
        """Advance the current pointer."""
        if self.scanned:
            return

        self.current += 1

    def previous(self) -> str:
        """Returns the previously read character."""
        return self.source[self.current - 1]

    def peek(self) -> str:
        """Returns the current character, without actually consuming it."""
        if self.scanned:
            return ""

        return self.source[self.current]

    def peek_next(self) -> str:
        """Returns the character one ahead of the current character."""
        if self.current + 1 >= len(self.source):
            return ""

        return self.source[self.current + 1]

    def peek_non_whitespace(self) -> str:
        """Returns the first non-whitespace character."""
        for char in self.source[self.current :]:
            if char not in string.whitespace:
                return char

        return ""

    def read_char(self) -> str:
        """
        Reads one character from the source.
        If the source has been exhausted, returns an empty string.
        """
        char = self.peek()
        self.advance()

        return char

    def match_next(self, chars: Sequence[str]) -> bool:
        """
        Returns True and reads one character from source, but only if it
        matches any of the given characters. Returns False otherwise.
        """
        if self.scanned:
            return False

        if self.source[self.current] in chars:
            self.advance()
            return True

        return False

    def consume(self, char: str) -> None:
        """
        Consumes the expected character type from source. If the character
        doesn't match current, raises a parse error.
        """
        if self.scanned:
            raise Json5ParseError(
                f"Expected to find '{char}', found EOF",
                index=self.current,
            )

        current_char = self.read_char()
        if current_char != char:
            raise Json5ParseError(
                f"Expected to find '{char}', found '{current_char}'",
                index=self.current,
            )

    def parse(self) -> Json5File:
        """Scans the source to produce a JSON5 CST."""
        leading_trivia_nodes = self.parse_trivia()
        value = self.parse_node()
        trailing_trivia_nodes = self.parse_trivia()

        # Ensure no more data exists
        if not self.scanned:
            token = self.read_char()
            raise Json5ParseError(f"Unexpected {token}", self.current)

        return Json5File(value, leading_trivia_nodes, trailing_trivia_nodes)

    def parse_node(self) -> Json5Node:
        """Returns a parsed JSON5 node."""
        if self.scanned:
            raise Json5ParseError(
                "Expected to find JSON5 data, found EOF",
                index=self.current,
            )

        if self.match_next("["):
            return self.parse_array()
        elif self.match_next("{"):
            return self.parse_object()
        else:
            return self.parse_primitive()

    def parse_primitive(self) -> Json5Primitive:
        """Returns a parsed JSON primitive."""
        node: Json5Primitive

        if self.source[self.current : self.current + 4] == "null":
            self.current += 4
            node = Json5Null(trailing_trivia_nodes=[])

        elif self.source[self.current : self.current + 4] == "true":
            self.current += 4
            node = Json5Boolean(
                source="true",
                value=True,
                trailing_trivia_nodes=[],
            )

        elif self.source[self.current : self.current + 5] == "false":
            self.current += 5
            node = Json5Boolean(
                source="false",
                value=False,
                trailing_trivia_nodes=[],
            )

        elif self.match_next(('"', "'")):
            # TODO: can remove once mypy has better type narrowing
            # ref: https://github.com/python/mypy/issues/12535
            quote_char = cast(Literal['"', "'"], self.previous())
            source, string_value = self.parse_string(quote_char)
            node = Json5String(source, string_value, trailing_trivia_nodes=[])

        # TODO: leading decimal?
        elif self.peek() in string.digits:
            source, float_value = self.parse_number()
            node = Json5Number(source, float_value, trailing_trivia_nodes=[])

        else:
            raise NotImplementedError(self.source[self.current])

        trailing_trivia_nodes = self.parse_trivia()
        node.trailing_trivia_nodes = trailing_trivia_nodes
        return node

    # def parse_identifier(self) -> Json5Key:
    #     """Scans keywords and variable names."""
    #     # TODO: not full ECMA syntax
    #     while not self.scanned and (self.peek().isalnum() or self.peek() == "_"):
    #         self.advance()

    def parse_string(self, quote_char: Literal["'", '"']) -> tuple[str, str]:
        # TODO: this is probably not all escapes
        start_index = self.current
        unescaped_chars = []
        while not self.scanned and self.peek() != quote_char:
            char = self.read_char()

            if char != "\\":
                unescaped_chars.append(char)
                continue

            # Escaping the next character
            next_char = self.peek()
            if next_char == "":
                raise Json5ParseError("Unterminated string", index=start_index)

            if next_char == "\n":
                pass  # trailing backslash means ignore the newline
            elif next_char == "\\":
                unescaped_chars.append("\\")
            elif next_char == "n":
                unescaped_chars.append("\n")
            elif next_char == "t":
                unescaped_chars.append("\t")
            elif next_char == "'":
                unescaped_chars.append("'")
            elif next_char == '"':
                unescaped_chars.append('"')
            else:
                escape = char + next_char
                raise Json5ParseError(
                    f"Unknown escape sequence: '{escape}'",
                    index=self.current,
                )

            self.advance()

        # Ensure end quote
        self.consume(quote_char)

        value = "".join(unescaped_chars)
        content = quote_char + self.source[start_index : self.current]
        return content, value

    def parse_number(self) -> tuple[str, float]:
        # TODO: exponent syntax support
        # TODO: Hexadecimal support
        start_index = self.current

        while self.peek().isdigit():
            self.advance()

        # decimal support
        if self.peek() == ".":
            if self.peek_next().isdigit():
                self.advance()
                while self.peek().isdigit():
                    self.advance()

        content = self.source[start_index : self.current]
        return content, float(content)

    def parse_array_member(self) -> Json5Node:
        value = self.parse_node()

        if self.peek() == "]":
            # Trailing comma not necessary for last element
            pass
        else:
            self.consume(",")
            value.trailing_trivia_nodes.append(Json5Comma())

        value.trailing_trivia_nodes.extend(self.parse_trivia())
        return value

    def parse_array(self) -> Json5Array:
        items: list[Json5Node] = []
        leading_trivia_nodes = self.parse_trivia()

        while not self.scanned and not self.match_next("]"):
            items.append(self.parse_array_member())

        trailing_trivia_nodes = self.parse_trivia()
        return Json5Array(items, leading_trivia_nodes, trailing_trivia_nodes)

    def parse_object_entry(self) -> tuple[Json5Key, Json5Node]:
        # TODO: identifier support
        if not self.match_next(('"', "'")):
            raise Json5ParseError(f"Expected to find identifier", index=self.current)

        quote_char = cast(Literal['"', "'"], self.previous())
        source, value = self.parse_string(quote_char)
        string_trailing_trivia = self.parse_trivia()
        string_node = Json5String(source, value, string_trailing_trivia)

        self.consume(":")
        trivia_after_colon = self.parse_trivia()
        key_node = Json5Key(string_node, trivia_after_colon)

        value_node = self.parse_node()
        if self.peek() == "}":
            # Trailing comma not necessary for last element
            pass
        else:
            self.consume(",")
            value_node.trailing_trivia_nodes.append(Json5Comma())

        value_node.trailing_trivia_nodes.extend(self.parse_trivia())
        return key_node, value_node

    def parse_object(self) -> Json5Object:
        items: list[tuple[Json5Key, Json5Node]] = []
        leading_trivia_nodes = self.parse_trivia()

        while not self.scanned and not self.match_next("}"):
            items.append(self.parse_object_entry())

        trailing_trivia_nodes = self.parse_trivia()
        return Json5Object(items, leading_trivia_nodes, trailing_trivia_nodes)

    def parse_trivia(self) -> list[Json5Trivia]:
        """
        Parses and returns all following Trivia nodes.

        Includes newlines, whitespace, and comments (comments end with newline).
        """
        trivia_nodes: list[Json5Trivia] = []
        while not self.scanned:
            if self.match_next("\n"):
                trivia_nodes.append(Json5Newline())

            elif self.peek() in string.whitespace:
                whitespace_start = self.current
                while not self.scanned and self.peek() in string.whitespace:
                    self.advance()

                whitespace = self.source[whitespace_start : self.current]
                trivia_nodes.append(Json5Whitespace(whitespace))

            elif self.match_next("/"):
                comment_start = self.current - 1
                self.consume("/")
                while not self.scanned and self.peek() != "\n":
                    self.advance()

                comment = self.source[comment_start : self.current]
                trivia_nodes.append(Json5Comment(comment))

            else:
                break

        return trivia_nodes


def parse(source: str) -> Json5Node:
    return Json5Parser(source).parse()


__all__ = [
    "Json5ParseError",
    "Json5Array",
    "Json5Boolean",
    "Json5Comma",
    "Json5Comment",
    "Json5File",
    "Json5Key",
    "Json5Newline",
    "Json5Node",
    "Json5Null",
    "Json5Number",
    "Json5Object",
    "Json5Primitive",
    "Json5String",
    "Json5Trivia",
    "Json5Whitespace",
    "Json5Parser",
    "Json5Visitor",
    "Json5Transformer",
]
