# -*- coding: utf-8 -*-
"""DesktopState：桌面环境的完整可判定状态。"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DesktopState:
    """桌面状态 = 文件系统 + 进程 + 当前窗口/UI + 剪贴板 + 光标。"""
    files: Dict[str, str] = field(default_factory=dict)       # path -> content
    running_apps: List[str] = field(default_factory=list)      # 已启动应用
    foreground: str = "desktop"                                # 前台应用
    clipboard: str = ""
    cursor: tuple = (0, 0)
    # 交互性临时字段（对话框 / 输入框 / 选中项）
    selected_file: Optional[str] = None
    focused_input: Optional[str] = None                        # 当前输入目标字段
    pending_input: Dict[str, str] = field(default_factory=dict)  # 字段 -> 已输入内容
    dialog: Optional[str] = None                               # 当前对话框 id
    ui: List[Dict[str, Any]] = field(default_factory=list)     # 当前 UI 组件树
    logs: List[str] = field(default_factory=list)              # 事件日志

    def clone(self) -> "DesktopState":
        return copy.deepcopy(self)

    def file_exists(self, path: str) -> bool:
        return path in self.files

    def file_content(self, path: str) -> str:
        return self.files.get(path, "")

    def process_running(self, name: str) -> bool:
        return name in self.running_apps

    def ui_ids(self) -> List[str]:
        return [e.get("id", "") for e in self.ui]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "files": dict(self.files),
            "running_apps": list(self.running_apps),
            "foreground": self.foreground,
            "clipboard": self.clipboard,
            "selected_file": self.selected_file,
            "dialog": self.dialog,
            "ui_ids": self.ui_ids(),
        }
