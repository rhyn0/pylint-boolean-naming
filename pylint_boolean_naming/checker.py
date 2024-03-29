"""Implementation of the boolean naming checker."""

from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING
from typing import ClassVar

# External Party
from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    # Standard Library
    from collections.abc import Generator

default_boolean_variable_prefixes = ("is", "has", "can")


class BooleanNamingChecker(BaseChecker):
    """Checks for boolean variable names that do not start with a valid prefix."""

    name = "boolean_naming"
    msgs: ClassVar = {
        "W9901": (
            "Invalid boolean variable name '%s'",
            "invalid-boolean-variable-name",
            "Use a prefix to indicate that the variable is a boolean.",
        )
    }
    options = (
        (
            "valid-prefixes",
            {
                "default": default_boolean_variable_prefixes,
                "type": "csv",
                "metavar": "<prefixes>",
                "help": "List of valid prefixes for boolean variables.",
            },
        ),
    )

    def _name_starts_with_prefix(self, name: str) -> bool:
        return any(
            name.startswith(prefix) for prefix in self.linter.config.valid_prefixes
        )

    @staticmethod
    def _contains_bool_value(*elements: nodes.NodeNG) -> Generator[int, None, None]:
        """Returns first index of a boolean value in the elements, -1 if not found."""
        yield from (
            idx
            for idx, element in enumerate(elements)
            if isinstance(element, nodes.Const) and isinstance(element.value, bool)
        )

    def _individual_assign_check(
        self, node: nodes.List | nodes.Tuple | nodes.AssignName, index: int
    ) -> None:
        assign_target = (
            node.elts[index] if isinstance(node, (nodes.Tuple, nodes.List)) else node
        )
        if not isinstance(
            assign_target, (nodes.AssignName, nodes.Attribute, nodes.AssignAttr)
        ):
            return
        name = (
            assign_target.name
            if isinstance(assign_target, nodes.AssignName)
            else assign_target.attrname
        )
        if not self._name_starts_with_prefix(name):
            self.add_message(
                "invalid-boolean-variable-name",
                node=assign_target,
                args=name,
            )

    def visit_assign(self, node: nodes.Assign) -> None:
        """Visit an assignment node to check for boolean value assignment."""
        if not isinstance(node.value, (nodes.Tuple, nodes.List, nodes.Const)):
            return
        # make sure there is a boolean value being assigned
        elts = node.value.elts if hasattr(node.value, "elts") else (node.value,)
        # targets is a list of left hand side operators, usually compressed to one
        target = node.targets[0]
        # if left side is a name, and right side is a container don't check it
        if isinstance(target, nodes.AssignName) and isinstance(
            node.value, (nodes.Tuple, nodes.List)
        ):
            return
        for idx in self._contains_bool_value(*elts):
            self._individual_assign_check(target, idx)

    def visit_annassign(self, node: nodes.AnnAssign) -> None:
        """Visit an annotated assignment node to check for boolean annotation."""
        if (
            not isinstance(node.annotation, nodes.Name)
            or node.annotation.name != "bool"
        ):
            return
        name = (
            node.target.name
            if isinstance(node.target, nodes.AssignName)
            else node.target.attrname
        )
        if not self._name_starts_with_prefix(name):
            self.add_message(
                "invalid-boolean-variable-name", node=node.target, args=name
            )
