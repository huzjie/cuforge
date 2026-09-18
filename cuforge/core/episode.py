# -*- coding: utf-8 -*-
"""Episode 实体：一次完整的任务执行（任务 + 轨迹 + 奖励）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from .task import Task
from .trajectory import Trajectory
from .reward import VerifiableReward


class EpisodeStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class Episode:
    """任务执行的一个 episode，是 RLVR 采样的最小单位。"""
    task: Task
    trajectory: Trajectory = field(default_factory=Trajectory)
    reward: VerifiableReward = field(default_factory=VerifiableReward)
    status: EpisodeStatus = EpisodeStatus.FAILED
    duration_ms: float = 0.0
    group_id: int = 0            # 组相对比较时所属组
    advantage: float = 0.0       # 组内相对优势（GRPO 用）
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.trajectory.task_id:
            self.trajectory.task_id = self.task.task_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task.task_id,
            "status": self.status.value,
            "reward": self.reward.to_dict(),
            "advantage": self.advantage,
            "duration_ms": self.duration_ms,
            "trajectory": self.trajectory.to_dict(),
        }

    def __repr__(self) -> str:
        return f"<Episode {self.task.task_id} {self.status.value} reward={self.reward.total:.3f}>"
