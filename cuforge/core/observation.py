# -*- coding: utf-8 -*-
"""Observation / ScreenState：智能体看到的屏幕状态。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ScreenState:
    """一帧屏幕状态：UI 组件树 + 文本化渲染 + 元信息。"""
    ui_tree: List[Dict[str, Any]] = field(default_factory=list)   # 组件树（可点击元素）
    text: str = ""                                                 # 文本化截图描述
    pixels: Optional[bytes] = None                                 # 原始截图（可选）
    width: int = 1280
    height: int = 720
    foreground_app: str = "desktop"
    timestamp: float = 0.0

    def clickable(self) -> List[Dict[str, Any]]:
        return [e for e in self.ui_tree if e.get("clickable", True)]

    def describe(self) -> str:
        parts = [f"[screen {self.width}x{self.height}] app={self.foreground_app}"]
        for e in self.ui_tree[:20]:
            label = e.get("label") or e.get("id") or e.get("role", "?")
            box = e.get("bbox")
            loc = f" @({box[0]},{box[1]})" if box and len(box) >= 2 else ""
            parts.append(f"  - {label}{loc}")
        if self.text:
            parts.append("[text] " + self.text[:500])
        return "\n".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ui_tree": self.ui_tree,
            "text": self.text,
            "width": self.width,
            "height": self.height,
            "foreground_app": self.foreground_app,
            "timestamp": self.timestamp,
        }


@dataclass
class Observation:
    """一次动作后的观测。"""
    screen: ScreenState
    done: bool = False
    info: Dict[str, Any] = field(default_factory=dict)
    step: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "screen": self.screen.to_dict(),
            "done": self.done,
            "info": self.info,
            "step": self.step,
        }
