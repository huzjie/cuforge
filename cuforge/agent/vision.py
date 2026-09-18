# -*- coding: utf-8 -*-
"""VisionContext：多轮截图的视觉上下文切分（token 预算控制）。"""
from __future__ import annotations

from typing import List, Optional

from ..core.observation import Observation


class VisionContext:
    """视觉上下文窗口：recent / summary / full 三种模式。"""

    def __init__(self, mode: str = "recent", window: int = 8) -> None:
        self.mode = mode
        self.window = window

    def select(self, history: List[Observation],
               current: Observation) -> List[Observation]:
        """从历史 + 当前观测中选择进入上下文的帧。"""
        if self.mode == "full":
            return list(history) + [current]
        if self.mode == "summary":
            # 摘要模式：首帧 + 最近 window 帧
            if not history:
                return [current]
            return [history[0]] + list(history[-self.window:]) + [current]
        # recent：最近 window 帧
        return list(history[-self.window:]) + [current]

    def describe(self, frames: List[Observation]) -> str:
        """把选中的帧压缩成文本描述（近似 token 预算）。"""
        parts = []
        for i, o in enumerate(frames):
            ui = o.screen.ui_tree
            labels = [e.get("label", "?") for e in ui[:12]]
            parts.append(f"f{i}[{o.screen.foreground_app}]: " + " | ".join(labels))
        return "\n".join(parts)


def vision_window(history: List[Observation], current: Observation,
                  mode: str = "recent", window: int = 8) -> List[Observation]:
    return VisionContext(mode, window).select(history, current)
