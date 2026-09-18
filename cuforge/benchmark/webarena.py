# -*- coding: utf-8 -*-
"""WebArenaAdapter：网页智能体基准适配器。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..core.task import Task
from .base import Benchmark


class WebArenaAdapter(Benchmark):
    name = "webarena"

    def __init__(self, data_path: str = "data/webarena") -> None:
        self.data_path = Path(data_path)

    def tasks(self) -> List[Task]:
        tasks = []
        if not self.data_path.exists():
            return tasks
        for f in self.data_path.glob("*.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(Task(goal=d.get("intent", ""),
                              instruction=d.get("intent", ""),
                              verifier="state_match",
                              verifier_params=d.get("verifier_params", {}),
                              initial_state={"foreground": "browser"},
                              metadata={"benchmark": "webarena"}))
        return tasks
