#!/usr/bin/env python3
"""Supplies one function element_length"""
from typing import Iterable, Tuple, Sequence, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples with sequence and int"""
    return [(i, len(i)) for i in lst]
