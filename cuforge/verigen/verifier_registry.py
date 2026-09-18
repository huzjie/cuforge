# -*- coding: utf-8 -*-
"""可验证判定器注册表：确定性终态打分。"""
from __future__ import annotations

from typing import Dict, List, Optional, Type

from ..env.state import DesktopState
from ..errors import RegistryError


class Verifier:
    """可验证判定器基类：对桌面终态做确定性打分（0~1）。"""
    name = "base"

    def verify(self, state: DesktopState, params: Dict) -> float:
        raise NotImplementedError


class FileExistsVerifier(Verifier):
    name = "file_exists"

    def verify(self, state: DesktopState, params: Dict) -> float:
        return 1.0 if state.file_exists(params["path"]) else 0.0


class FileContainsVerifier(Verifier):
    name = "file_contains"

    def verify(self, state: DesktopState, params: Dict) -> float:
        content = state.file_content(params.get("path", ""))
        return 1.0 if params.get("substring", "") in content else 0.0


class FileAbsentVerifier(Verifier):
    name = "file_absent"

    def verify(self, state: DesktopState, params: Dict) -> float:
        return 1.0 if not state.file_exists(params["path"]) else 0.0


class ProcessRunningVerifier(Verifier):
    name = "process_running"

    def verify(self, state: DesktopState, params: Dict) -> float:
        return 1.0 if state.process_running(params["name"]) else 0.0


class UiElementVerifier(Verifier):
    name = "ui_element"

    def verify(self, state: DesktopState, params: Dict) -> float:
        return 1.0 if params.get("id", "") in state.ui_ids() else 0.0


class StateMatchVerifier(Verifier):
    name = "state_match"

    def verify(self, state: DesktopState, params: Dict) -> float:
        field = params.get("field", "")
        expected = params.get("value")
        actual = state.pending_input.get(field)
        return 1.0 if actual == expected else 0.0


class ClipboardVerifier(Verifier):
    name = "clipboard"

    def verify(self, state: DesktopState, params: Dict) -> float:
        return 1.0 if params.get("value", "") in state.clipboard else 0.0


class VerifierRegistry:
    _registry: Dict[str, Type[Verifier]] = {}

    @classmethod
    def register(cls, name: str, verifier: Type[Verifier]) -> Type[Verifier]:
        cls._registry[name] = verifier
        return verifier

    @classmethod
    def get(cls, name: str) -> Verifier:
        if name not in cls._registry:
            raise RegistryError(f"verifier not registered: {name}")
        return cls._registry[name]()

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._registry.keys())

    @classmethod
    def verify(cls, name: str, state: DesktopState, params: Dict) -> float:
        return cls.get(name).verify(state, params)


VerifierRegistry.register("file_exists", FileExistsVerifier)
VerifierRegistry.register("file_contains", FileContainsVerifier)
VerifierRegistry.register("file_absent", FileAbsentVerifier)
VerifierRegistry.register("process_running", ProcessRunningVerifier)
VerifierRegistry.register("ui_element", UiElementVerifier)
VerifierRegistry.register("state_match", StateMatchVerifier)
VerifierRegistry.register("clipboard", ClipboardVerifier)
