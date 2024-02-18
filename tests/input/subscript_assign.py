"""Tests that subscript assignments are checked properly."""

# Standard Library
from typing import List

my_list = [True, False]
my_list[0] = False

my_other_list: List[bool]
