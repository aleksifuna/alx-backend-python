#!/usr/bin/env python3
"""Module has one function that takes a list and return sum of elements"""
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Takes a list and returns the sum of elements"""
    sum = 0
    for elem in mxd_lst:
        sum += elem
    return sum
