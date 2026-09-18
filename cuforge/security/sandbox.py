# -*- coding: utf-8 -*-
"""Sandbox：动作级隔离沙箱（在动作执行前做隔离检查）。"""
from __future__ import annotations

from typing import Any, Dict, Optional

from ..core.action import Action


class Sandbox:
    """虚拟/容器沙箱策略：限制动作可影响的资源范围。"""

    def __init__(self, allowed_apps: Optional[set] = None,
                 allowed_keys: Optional[set] = None) -> None:
        self.allowed_apps = allowed_apps or {"files", "editor", "terminal",
                                             "settings", "browser"}
        self.allowed_keys = allowed_keys or {
            "Enter", "Return", "Backspace", "Escape", "esc",
            "Tab", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"}

    def check(self, action: Action) -> bool:
        """动作是否允许。"""
        at = action.type.value
        if at == "open":
            return action.app in self.allowed_apps
        if at == "key":
            return action.key in self.allowed_keys
        if at == "type":
            return len(action.text or "") <= 10000
        return True

    def describe(self) -> Dict[str, Any]:
        return {"allowed_apps": sorted(self.allowed_apps),
                "allowed_keys": sorted(self.allowed_keys)}
