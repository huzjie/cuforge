# -*- coding: utf-8 -*-
"""MockBackend：零依赖占位后端（用于策略调试 / 离线测试）。"""
from __future__ import annotations

from .base import LLMBackend


class MockBackend(LLMBackend):
    name = "mock"

    def generate(self, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 1024) -> str:
        return '{"type": "done"}'
