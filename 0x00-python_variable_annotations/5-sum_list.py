#!/usr/bin/env python3
"""Module has one function sum_list"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """computes the sum of elements in a list and retuns the sum"""
    sum = 0
    for elem in input_list:
        sum += elem
    return sum
