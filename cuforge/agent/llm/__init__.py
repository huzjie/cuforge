# -*- coding: utf-8 -*-
"""llm 包：多 LLM 后端（mock / OpenAI 兼容 / vLLM）。"""
from .base import LLMBackend
from .mock import MockBackend
from .openai_compat import OpenAICompatBackend
from .vllm import VLLMBackend
from .registry import build_backend

__all__ = ["LLMBackend", "MockBackend", "OpenAICompatBackend", "VLLMBackend", "build_backend"]
