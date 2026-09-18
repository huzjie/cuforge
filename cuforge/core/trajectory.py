# -*- coding: utf-8 -*-
"""Trajectory / Step：智能体在任务中的完整轨迹。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .action import Action
from .observation import Observation


@dataclass
class Step:
    """一步：思考 -> 动作 -> 观测。"""
    action: Action
    observation: Observation
    thought: str = ""
    step_index: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_index": self.step_index,
            "thought": self.thought,
            "action": self.action.to_dict(),
            "observation": self.observation.to_dict(),
        }


@dataclass
class Trajectory:
    """完整轨迹。"""
    task_id: str = ""
    steps: List[Step] = field(default_factory=list)
    outcome: str = "incomplete"      # success | failed | timeout | incomplete
    final_reward: float = 0.0

    def add(self, step: Step) -> None:
        step.step_index = len(self.steps)
        self.steps.append(step)

    @property
    def length(self) -> int:
        return len(self.steps)

    def actions(self) -> List[Action]:
        return [s.action for s in self.steps]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "outcome": self.outcome,
            "final_reward": self.final_reward,
            "steps": [s.to_dict() for s in self.steps],
        }

    def summary(self) -> str:
        acts = " -> ".join(a.type.value for a in self.actions())
        return f"[{self.task_id}] outcome={self.outcome} reward={self.final_reward:.3f} steps={self.length}: {acts}"
