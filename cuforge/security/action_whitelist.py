# -*- coding: utf-8 -*-
"""ActionWhitelist：动作白名单过滤器。"""
from __future__ import annotations

from typing import Iterable, Optional

from ..core.action import Action, ActionType


class ActionWhitelist:
    """仅允许白名单内的动作类型。"""

    def __init__(self, allowed: Optional[Iterable[ActionType]] = None) -> None:
        self.allowed = set(allowed) if allowed else set(ActionType)

    def allow(self, action: Action) -> bool:
        return action.type in self.allowed

    def block_reason(self, action: Action) -> str:
        return "" if self.allow(action) else f"action blocked: {action.type.value}"
