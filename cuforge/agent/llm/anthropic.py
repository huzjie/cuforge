# -*- coding: utf-8 -*-
"""AnthropicBackend：Anthropic Messages API 后端。"""
from __future__ import annotations

import json
import urllib.request

from .base import LLMBackend


class AnthropicBackend(LLMBackend):
    name = "anthropic"

    def __init__(self, model: str, api_key: str = "",
                 base_url: str = "https://api.anthropic.com", **kwargs) -> None:
        super().__init__(model, **kwargs)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 1024) -> str:
        url = f"{self.base_url}/v1/messages"
        payload = {"model": self.model, "max_tokens": max_tokens,
                   "temperature": temperature,
                   "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json",
                     "x-api-key": self.api_key,
                     "anthropic-version": "2023-06-01"}, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
        return "".join(b.get("text", "") for b in body.get("content", []))
