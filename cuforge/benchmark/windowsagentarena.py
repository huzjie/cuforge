# -*- coding: utf-8 -*-
"""WindowsAgentArenaAdapter：Windows 智能体竞技场适配器。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..core.task import Task
from .base import Benchmark


class WindowsAgentArenaAdapter(Benchmark):
    name = "windowsagentarena"

    def __init__(self, data_path: str = "data/windowsagentarena") -> None:
        self.data_path = Path(data_path)

    def tasks(self) -> List[Task]:
        tasks = []
        if not self.data_path.exists():
            return tasks
        for f in self.data_path.glob("*.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(Task(goal=d.get("instruction", ""),
                              instruction=d.get("instruction", ""),
                              verifier="state_match",
                              verifier_params=d.get("verifier_params", {}),
                              initial_state={},
                              metadata={"benchmark": "windowsagentarena"}))
        return tasks
