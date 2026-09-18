# -*- coding: utf-8 -*-
"""评测基准基类。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from ..core.task import Task


@dataclass
class EvalResult:
    total: int = 0
    passed: int = 0
    success_rate: float = 0.0
    per_task: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total, "passed": self.passed,
            "success_rate": self.success_rate, "per_task": self.per_task,
        }


class Benchmark:
    """评测基准基类。"""
    name = "base"

    def tasks(self) -> List[Task]:
        raise NotImplementedError

    def run(self, runtime) -> EvalResult:
        tasks = self.tasks()
        passed = 0
        per_task = []
        for t in tasks:
            ep = runtime.run_episode(t)
            ok = ep.reward.result >= 0.999
            passed += int(ok)
            per_task.append({"task_id": t.task_id, "goal": t.goal,
                             "reward": ep.reward.result, "passed": ok,
                             "steps": ep.trajectory.length})
        return EvalResult(total=len(tasks), passed=passed,
                          success_rate=(passed / len(tasks)) if tasks else 0.0,
                          per_task=per_task)
