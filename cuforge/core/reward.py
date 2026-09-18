# -*- coding: utf-8 -*-
"""VerifiableReward：可验证确定性奖励。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class RewardSource(str, Enum):
    RESULT = "result"      # 环境终态可验证打分（0/1 或连续）
    PROCESS = "process"    # 过程奖励（是否走了关键中间状态）
    FORMAT = "format"      # 格式奖励（动作是否合法/符合规范）


@dataclass
class VerifiableReward:
    """一条轨迹的奖励分解。

    核心是 result：由可验证判定器（Verifier）对环境终态做确定性打分。
    """
    result: float = 0.0
    process: float = 0.0
    format: float = 0.0
    sources: Dict[str, float] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def total(self) -> float:
        return self.result + self.process + self.format

    def add(self, source: str, value: float) -> None:
        self.sources[source] = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result,
            "process": self.process,
            "format": self.format,
            "total": self.total,
            "sources": self.sources,
            "details": self.details,
        }

    def __repr__(self) -> str:
        return f"<Reward result={self.result:.3f} process={self.process:.3f} format={self.format:.3f}>"
