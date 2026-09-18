# -*- coding: utf-8 -*-
"""Task 实体：可验证的计算机使用任务。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class Task:
    """一个可验证的 GUI 任务。

    由 VeriGen 合成：自然语言指令 + 初始桌面状态 + 可验证判定器。
    """
    goal: str                            # 任务目标（自然语言）
    instruction: str                     # 详细指令（智能体阅读）
    verifier: str = "file_exists"        # 验证器类型名
    verifier_params: Dict[str, Any] = field(default_factory=dict)
    initial_state: Dict[str, Any] = field(default_factory=dict)  # 初始桌面状态
    success_criteria: List[str] = field(default_factory=list)    # 成功判据（人类可读）
    max_steps: int = 30
    task_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.task_id:
            self.task_id = _slug(self.goal)[:40] or "task"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "instruction": self.instruction,
            "verifier": self.verifier,
            "verifier_params": self.verifier_params,
            "initial_state": self.initial_state,
            "success_criteria": self.success_criteria,
            "max_steps": self.max_steps,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(**data)

    def __repr__(self) -> str:
        return f"<Task {self.task_id!r} verifier={self.verifier!r}>"


def _slug(text: str) -> str:
    import re
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", s)
    return s.strip("-")
