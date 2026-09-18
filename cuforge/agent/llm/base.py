# -*- coding: utf-8 -*-
"""LLM 后端基类。"""
from __future__ import annotations

from typing import Any, Dict, Optional


class LLMBackend:
    name = "base"

    def __init__(self, model: str, **kwargs: Any) -> None:
        self.model = model
        self.kwargs = kwargs

    def generate(self, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 1024) -> str:
        raise NotImplementedError
