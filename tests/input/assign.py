"""Tests that variables assigned as constants with boolean values are checked."""

# pylint: disable=invalid-name

can_fly = False

is_flying: bool = False

flew = True  # [invalid-boolean-variable-name]
