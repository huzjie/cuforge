# -*- coding: utf-8 -*-
"""GeminiBackend：Google Gemini generateContent 后端。"""
from __future__ import annotations

import json
import urllib.request

from .base import LLMBackend


class GeminiBackend(LLMBackend):
    name = "gemini"

    def __init__(self, model: str, api_key: str = "", **kwargs) -> None:
        super().__init__(model, **kwargs)
        self.api_key = api_key

    def generate(self, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 1024) -> str:
        url = (f"https://generativelanguage.googleapis.com/v1beta/"
               f"models/{self.model}:generateContent?key={self.api_key}")
        payload = {"contents": [{"parts": [{"text": prompt}]}],
                   "generationConfig": {"temperature": temperature,
                                        "maxOutputTokens": max_tokens}}
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
        return body["candidates"][0]["content"]["parts"][0].get("text", "")
