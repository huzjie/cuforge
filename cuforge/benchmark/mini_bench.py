# -*- coding: utf-8 -*-
"""迷你基准：用内置任务库做端到端评测（真实可运行）。"""
from __future__ import annotations

from typing import List, Optional

from ..core.task import Task
from ..verigen.task_bank import build_task_bank
from .base import Benchmark, EvalResult


class MiniBench(Benchmark):
    name = "mini"

    def __init__(self, tasks: Optional[List[Task]] = None) -> None:
        self._tasks = tasks or build_task_bank()

    def tasks(self) -> List[Task]:
        return self._tasks


def evaluate(runtime, tasks: Optional[List[Task]] = None) -> dict:
    bench = MiniBench(tasks)
    result = bench.run(runtime)
    return {"benchmark": "mini", **result.to_dict()}
