from __future__ import annotations
from collections import deque
import inspect

from typing import Callable, Iterator

from json5kit.nodes import Json5Node


def iter_child_nodes(node: Json5Node) -> Iterator[Json5Node]:
    """
    Yield all direct child nodes of `node`, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    for field in vars(node).values():
        if isinstance(field, Json5Node):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, Json5Node):
                    yield item


def walk(node: Json5Node) -> Iterator[Json5Node]:
    """
    Recursively yield all descendant nodes in the tree starting at `node`
    (including `node` itself), in no specified order.
    """
    queue = deque([node])

    while queue:
        node = queue.popleft()
        queue.extend(iter_child_nodes(node))
        yield node


def _remove_prefix(string: str, prefix: str) -> str:
    if string.startswith(prefix):
        return string[len(prefix) :]

    return string


class Json5VisitorBase:
    """Base class for Json5Visitor and Json5Transformer."""

    def _get_visitor(self, node: Json5Node) -> Callable[..., object] | None:
        """Finds a visitor method corresponding to given node"""
        object_type = _remove_prefix(node.__class__.__name__, "Json5")
        method_name = "visit_" + object_type
        method = getattr(self, method_name, None)
        if inspect.ismethod(method):
            return method

        return None

    def visit(self, node: Json5Node) -> object:
        """Finds the method to call for the given node."""
        visitor = self._get_visitor(node)
        if visitor is not None:
            return visitor(node)
        else:
            return self.generic_visit(node)

    def generic_visit(self, node: Json5Node) -> object:
        raise NotImplementedError


class Json5Visitor(Json5VisitorBase):
    """Base class to create visitors for specific nodes of JSON5 trees."""

    def visit(self, node: Json5Node) -> None:
        """Finds the method to call for the given node."""
        super().visit(node)

    def generic_visit(self, node: Json5Node) -> None:
        for child in iter_child_nodes(node):
            self.visit(child)


class Json5TransformError(Exception):
    """Raised when a Transformer method returns something other than a JSON5 node."""


class Json5Transformer(Json5VisitorBase):
    """Base class to create visitors to modify specific nodes of JSON5 trees."""

    def visit(self, node: Json5Node) -> Json5Node:
        """
        Finds the method to call for the given node, and returns the replacement
        node for the given node.
        """
        returned_node = super().visit(node)
        if not isinstance(returned_node, Json5Node):
            raise Json5TransformError(f"Expected JSON5 node, got {returned_node}")

        return returned_node

    def generic_visit(self, node: Json5Node) -> Json5Node:
        for field, old_value in vars(node).items():
            if isinstance(old_value, Json5Node):
                new_node = self.visit(old_value)
                setattr(node, field, new_node)

            elif isinstance(old_value, list):
                new_values: list[Json5Node] = []

                for value in old_value:
                    assert isinstance(value, Json5Node)
                    value = self.visit(value)
                    new_values.append(value)

                # Replace old nodes with new nodes
                old_value[:] = new_values

        return node
