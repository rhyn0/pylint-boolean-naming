"""Tests that attributes of objects are checked properly."""

# pylint: disable=too-few-public-methods
my_obj = object()
my_obj.a = True  # [invalid-boolean-variable-name]

my_obj.is_flying = True


class Foo:
    """Declared class variables are checked."""

    b: bool  # [invalid-boolean-variable-name]
    can_bar = False

    def __init__(self) -> None:
        """AnnAssign with attributes are checked."""
        self.c: bool = False  # [invalid-boolean-variable-name]
