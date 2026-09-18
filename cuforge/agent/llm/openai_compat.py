# -*- coding: utf-8 -*-
"""OpenAICompatBackend：OpenAI 兼容 Chat Completions 后端。"""
from __future__ import annotations

import json
import urllib.request

from .base import LLMBackend


class OpenAICompatBackend(LLMBackend):
    name = "openai_compat"

    def __init__(self, model: str, base_url: str = "", api_key: str = "",
                 timeout: float = 60.0, **kwargs) -> None:
        super().__init__(model, **kwargs)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 1024) -> str:
        url = f"{self.base_url}/chat/completions" if self.base_url else ""
        if not url:
            raise RuntimeError("openai_compat backend requires base_url")
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.api_key}"},
            method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode())
        return body["choices"][0]["message"]["content"]
