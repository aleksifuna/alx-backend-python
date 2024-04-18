#!/usr/bin/env python3
"""Supplies one function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function that multiplies a float by multiplier"""
    def ret_function(num: float):
        """returns num * multiplier"""
        return num * multiplier
    return ret_function
