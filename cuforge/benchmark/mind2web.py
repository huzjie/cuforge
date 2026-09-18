# -*- coding: utf-8 -*-
"""Mind2WebAdapter：Mind2Web 网页任务适配器。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..core.task import Task
from .base import Benchmark


class Mind2WebAdapter(Benchmark):
    name = "mind2web"

    def __init__(self, data_path: str = "data/mind2web") -> None:
        self.data_path = Path(data_path)

    def tasks(self) -> List[Task]:
        tasks = []
        if not self.data_path.exists():
            return tasks
        for f in self.data_path.glob("*.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(Task(goal=d.get("confirmed_task", ""),
                              instruction=d.get("confirmed_task", ""),
                              verifier="state_match",
                              verifier_params=d.get("verifier_params", {}),
                              initial_state={"foreground": "browser"},
                              metadata={"benchmark": "mind2web"}))
        return tasks
