# -*- coding: utf-8 -*-
"""Guardrail：可组合护栏规则引擎。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Guardrail:
    name: str
    check: Callable[[Any], bool]     # 返回 True 表示通过
    message: str = ""


class GuardrailEngine:
    def __init__(self) -> None:
        self._rails: List[Guardrail] = []

    def add(self, rail: Guardrail) -> None:
        self._rails.append(rail)

    def evaluate(self, obj: Any) -> List[str]:
        """返回未通过护栏的消息列表（空 = 全部通过）。"""
        return [r.message or r.name for r in self._rails if not r.check(obj)]

    def passes(self, obj: Any) -> bool:
        return not self.evaluate(obj)


# 内置护栏
MAX_STEPS_RAIL = Guardrail("max_steps", lambda ep: ep.trajectory.length <= 200,
                           "trajectory too long")
