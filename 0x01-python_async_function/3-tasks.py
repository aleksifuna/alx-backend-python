#!/usr/bin/env python3
"""Supplies one function task_wait_random"""
import asyncio
from typing import Coroutine

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Creates and returns an asyncio.Task"""
    coro = wait_random(max_delay)
    return asyncio.create_task(coro)
