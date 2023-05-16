from __future__ import annotations
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

if sys.version_info >= (3, 8):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, Self, runtime_checkable


@runtime_checkable
class Json5Node(Protocol):
    """Sets the expectation from a JSON5 node: be able to convert back to source."""

    trailing_trivia_nodes: list[Json5Trivia]

    def to_source(self) -> str:
        ...

    def to_json(self) -> str:
        ...


class Json5Primitive:
    """Base class for primitive JSON types such as booleans, null, integers etc."""

    def __init__(
        self,
        source: str,
        value: object,
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        self.source = source
        self.value = value
        self.trailing_trivia_nodes = trailing_trivia_nodes

    def to_source(self) -> str:
        return self.source + "".join(
            trivia.source for trivia in self.trailing_trivia_nodes
        )

    def to_json(self) -> str:
        return self.source

    def replace(self, value: object) -> "Self":
        # TODO: pass specific source?
        source = str(value)

        primitive_class = type(self)
        return primitive_class(source, value, self.trailing_trivia_nodes.copy())


class Json5Null(Json5Primitive):
    value: None

    def __init__(self, trailing_trivia_nodes: list[Json5Trivia]) -> None:
        super().__init__(
            source="null",
            value=None,
            trailing_trivia_nodes=trailing_trivia_nodes,
        )


class Json5Boolean(Json5Primitive):
    value: bool

    def __init__(
        self,
        source: str,
        value: bool,
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        super().__init__(source, value, trailing_trivia_nodes)


class Json5Number(Json5Primitive):
    value: float

    def __init__(
        self,
        source: str,
        value: float,
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        super().__init__(source, value, trailing_trivia_nodes)


class Json5String(Json5Primitive):
    value: str

    def __init__(
        self,
        source: str,
        value: str,
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        super().__init__(source, value, trailing_trivia_nodes)


class Json5Key:
    def __init__(
        self,
        value: Json5String,  # TODO: identifier support
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        self.value = value
        self.trailing_trivia_nodes = trailing_trivia_nodes

    def to_source(self) -> str:
        return (
            self.value.to_source()
            + ":"
            + "".join(trivia.source for trivia in self.trailing_trivia_nodes)
        )

    def to_json(self) -> str:
        return self.value.to_json() + ":"


class Json5Container:
    """
    Base class for "container nodes", i.e. nodes that contain other nodes.

    This distinction is required because container nodes can have leading trivia
    nodes, while primitive nodes like ints and booleans cannot.

    Examples of container nodes include files, arrays and objects.
    """

    def __init__(
        self,
        leading_trivia_nodes: list[Json5Trivia],
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        self.leading_trivia_nodes = leading_trivia_nodes
        self.trailing_trivia_nodes = trailing_trivia_nodes

    def to_source(self) -> str:
        """Converts the node back to its original source."""
        raise NotImplementedError

    def to_json(self) -> str:
        raise NotImplementedError


class Json5File(Json5Container):
    def __init__(
        self,
        value: Json5Node,
        leading_trivia_nodes: list[Json5Trivia],
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        super().__init__(leading_trivia_nodes, trailing_trivia_nodes)
        self.value = value

    def to_source(self) -> str:
        """Converts the node back to its original source."""
        return (
            "".join(trivia.source for trivia in self.leading_trivia_nodes)
            + self.value.to_source()
            + "".join(trivia.source for trivia in self.trailing_trivia_nodes)
        )

    def to_json(self) -> str:
        """Converts the node to JSON, without whitespace."""
        return self.value.to_json()


class Json5Array(Json5Container):
    def __init__(
        self,
        members: list[Json5Node],
        leading_trivia_nodes: list[Json5Trivia],
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        super().__init__(leading_trivia_nodes, trailing_trivia_nodes)
        self.members = members

    def to_source(self) -> str:
        """Converts the node back to its original source."""
        return (
            "["
            + "".join(trivia.source for trivia in self.leading_trivia_nodes)
            + "".join(member.to_source() for member in self.members)
            + "]"
            + "".join(trivia.source for trivia in self.trailing_trivia_nodes)
        )

    def to_json(self) -> str:
        """Converts the node to JSON, without whitespace."""
        return "[" + ",".join(member.to_json() for member in self.members) + "]"


class Json5Object(Json5Container):
    def __init__(
        self,
        data: list[tuple[Json5Key, Json5Node]],  # TODO: identifier support
        leading_trivia_nodes: list[Json5Trivia],
        trailing_trivia_nodes: list[Json5Trivia],
    ) -> None:
        super().__init__(leading_trivia_nodes, trailing_trivia_nodes)
        self.keys: list[Json5Key] = []
        self.values: list[Json5Node] = []
        for key, value in data:
            self.keys.append(key)
            self.values.append(value)

    def to_source(self) -> str:
        """Converts the node back to its original source."""
        return (
            "{"
            + "".join(trivia.source for trivia in self.leading_trivia_nodes)
            + "".join(
                f"{key.to_source()}{value.to_source()}"
                for key, value in zip(self.keys, self.values)
            )
            + "}"
            + "".join(trivia.source for trivia in self.trailing_trivia_nodes)
        )

    def to_json(self) -> str:
        """Converts the node to JSON, without whitespace."""
        return (
            "{"
            + ",".join(
                f"{key.to_json()}{value.to_json()}"
                for key, value in zip(self.keys, self.values)
            )
            + "}"
        )


class Json5Trivia:
    """Base class for "trivial" information like whitespace, newlines and comments."""

    trailing_trivia_nodes = ()

    def __init__(self, source: str) -> None:
        self.source = source

    def to_source(self) -> str:
        return self.source

    def to_json(self) -> str:
        return self.source


class Json5Comment(Json5Trivia):
    """JSON5 single line comments, eg. `// foo`."""


class Json5Whitespace(Json5Trivia):
    """Any run of continuous whitespace characters in a JSON5 file."""


class Json5Newline(Json5Trivia):
    """Newline character in a JSON5 file."""

    def __init__(self) -> None:
        super().__init__(source="\n")


class Json5Comma(Json5Trivia):
    """Comma character in a JSON5 file"""

    def __init__(self) -> None:
        super().__init__(source=",")
