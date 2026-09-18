# -*- coding: utf-8 -*-
"""ScienceBoardAdapter：ScienceBoard 基准适配器。

参考（ScaleCUA 论文，Qwen3.5-9B）：ScienceBoard 54.0%。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..core.task import Task
from .base import Benchmark


class ScienceBoardAdapter(Benchmark):
    name = "scienceboard"

    def __init__(self, data_path: str = "data/scienceboard") -> None:
        self.data_path = Path(data_path)

    def tasks(self) -> List[Task]:
        tasks: List[Task] = []
        if not self.data_path.exists():
            return tasks
        for f in self.data_path.glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(Task(
                goal=data.get("instruction", ""),
                instruction=data.get("instruction", ""),
                verifier=data.get("verifier", "state_match"),
                verifier_params=data.get("verifier_params", {}),
                initial_state=data.get("initial_state", {}),
                metadata={"benchmark": "scienceboard", "source": f.name},
            ))
        return tasks
