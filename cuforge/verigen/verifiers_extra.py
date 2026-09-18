# -*- coding: utf-8 -*-
"""扩展验证器（import 本模块即自动注册到 VerifierRegistry）。"""
from __future__ import annotations

from typing import Dict

from ..env.state import DesktopState
from .verifier_registry import Verifier, VerifierRegistry


class CountVerifier(Verifier):
    name = "file_count"

    def verify(self, state: DesktopState, params: Dict) -> float:
        expected = params.get("count", 0)
        return 1.0 if len(state.files) == expected else 0.0


class JsonVerifier(Verifier):
    name = "json_field"

    def verify(self, state: DesktopState, params: Dict) -> float:
        import json
        content = state.file_content(params.get("path", ""))
        try:
            obj = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return 0.0
        return 1.0 if obj.get(params.get("field", "")) == params.get("value") else 0.0


class RegexVerifier(Verifier):
    name = "regex_match"

    def verify(self, state: DesktopState, params: Dict) -> float:
        import re
        content = state.file_content(params.get("path", ""))
        return 1.0 if re.search(params.get("pattern", ""), content) else 0.0


class ArithmeticVerifier(Verifier):
    name = "arithmetic"

    def verify(self, state: DesktopState, params: Dict) -> float:
        expr = params.get("expr", "1+1")
        try:
            expected = eval(expr, {"__builtins__": {}})  # noqa: S307 - 受限求值
            actual = state.pending_input.get("calc", None)
            return 1.0 if actual == expected else 0.0
        except Exception:
            return 0.0


VerifierRegistry.register("file_count", CountVerifier)
VerifierRegistry.register("json_field", JsonVerifier)
VerifierRegistry.register("regex_match", RegexVerifier)
VerifierRegistry.register("arithmetic", ArithmeticVerifier)
