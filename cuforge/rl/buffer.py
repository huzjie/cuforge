# -*- coding: utf-8 -*-
"""ReplayBuffer：经验回放缓冲（偏好对 / 优势样本）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExperienceSample:
    """一条可用于策略更新的经验样本。"""
    prompt: str = ""
    task_id: str = ""
    trajectory: Any = None
    reward: float = 0.0
    advantage: float = 0.0
    meta: Dict[str, Any] = field(default_factory=dict)


class ReplayBuffer:
    """环形缓冲（默认上限 10000）。"""

    def __init__(self, capacity: int = 10000) -> None:
        self.capacity = capacity
        self._buf: List[ExperienceSample] = []

    def push(self, sample: ExperienceSample) -> None:
        self._buf.append(sample)
        if len(self._buf) > self.capacity:
            self._buf = self._buf[-self.capacity:]

    def all(self) -> List[ExperienceSample]:
        return list(self._buf)

    def positive(self, threshold: float = 0.999) -> List[ExperienceSample]:
        return [s for s in self._buf if s.reward >= threshold]

    def __len__(self) -> int:
        return len(self._buf)
