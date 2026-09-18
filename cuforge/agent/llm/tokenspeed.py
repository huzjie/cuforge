# -*- coding: utf-8 -*-
"""TokenSpeedBackend：TokenSpeed 推理后端（OpenAI 兼容协议）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatBackend


class TokenSpeedBackend(OpenAICompatBackend):
    name = "tokenspeed"

    def __init__(self, model: str, base_url: str = "http://localhost:8001/v1",
                 api_key: str = "EMPTY", **kwargs) -> None:
        super().__init__(model, base_url=base_url, api_key=api_key, **kwargs)
