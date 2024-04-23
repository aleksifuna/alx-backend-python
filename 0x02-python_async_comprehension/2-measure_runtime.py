#!/usr/bin/env python3
"""
Supplies one function measure_runtime
"""

from time import time
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    measure the total runtime for an 4 parallel coroutines
    """
    start = time()
    tasks = [async_comprehension() for i in range(4)]
    await asyncio.gather(*tasks)
    end = time()
    return (end - start)
