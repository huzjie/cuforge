# -*- coding: utf-8 -*-
"""Action 实体：智能体在桌面环境上执行的动作。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ActionType(str, Enum):
    CLICK = "click"          # 点击坐标 (x, y)
    TYPE = "type"            # 输入文本
    SCROLL = "scroll"        # 滚动 (dx, dy)
    KEY = "key"              # 按键
    HOTKEY = "hotkey"        # 组合键
    DRAG = "drag"            # 拖拽
    WAIT = "wait"            # 等待
    OPEN = "open"            # 打开应用
    BACK = "back"            # 返回 / 关闭
    DONE = "done"            # 声明完成


@dataclass
class Action:
    """单个动作。"""
    type: ActionType
    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    key: Optional[str] = None
    keys: Optional[list] = None
    app: Optional[str] = None
    duration: Optional[float] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def click(cls, x: int, y: int) -> "Action":
        return cls(type=ActionType.CLICK, x=x, y=y)

    @classmethod
    def type_text(cls, text: str) -> "Action":
        return cls(type=ActionType.TYPE, text=text)

    @classmethod
    def scroll(cls, dx: int, dy: int) -> "Action":
        return cls(type=ActionType.SCROLL, dx=dx, dy=dy)

    @classmethod
    def press(cls, key: str) -> "Action":
        return cls(type=ActionType.KEY, key=key)

    @classmethod
    def hotkey(cls, *keys: str) -> "Action":
        return cls(type=ActionType.HOTKEY, keys=list(keys))

    @classmethod
    def open(cls, app: str) -> "Action":
        return cls(type=ActionType.OPEN, app=app)

    @classmethod
    def done(cls) -> "Action":
        return cls(type=ActionType.DONE)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"type": self.type.value}
        for k in ("x", "y", "text", "dx", "dy", "key", "keys", "app", "duration"):
            v = getattr(self, k)
            if v is not None:
                d[k] = v
        return d

    def __repr__(self) -> str:
        return f"<Action {self.type.value}>"
