# -*- coding: utf-8 -*-
"""TerminalBenchAdapter：终端基准适配器。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..core.task import Task
from .base import Benchmark


class TerminalBenchAdapter(Benchmark):
    name = "terminal_bench"

    def __init__(self, data_path: str = "data/terminal_bench") -> None:
        self.data_path = Path(data_path)

    def tasks(self) -> List[Task]:
        tasks = []
        if not self.data_path.exists():
            return tasks
        for f in self.data_path.glob("*.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(Task(goal=d.get("instruction", ""),
                              instruction=d.get("instruction", ""),
                              verifier="file_exists",
                              verifier_params=d.get("verifier_params", {}),
                              initial_state=d.get("initial_state", {}),
                              metadata={"benchmark": "terminal_bench"}))
        return tasks
