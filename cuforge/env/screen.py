# -*- coding: utf-8 -*-
"""屏幕渲染：把桌面状态渲染为 ScreenState（组件树 + 文本描述）。"""
from __future__ import annotations

import time
from typing import Dict, List

from ..core.observation import ScreenState
from .state import DesktopState

# 组件树布局：从上到下排列，每个组件一个 bbox 行（y 递增）
_ROW_HEIGHT = 40
_ROW_Y0 = 80


def _bbox(index: int, width: int = 1280) -> List[int]:
    y = _ROW_Y0 + index * _ROW_HEIGHT
    return [40, y, width - 40, y + _ROW_HEIGHT - 8]


def build_ui(state: DesktopState, width: int = 1280) -> List[Dict]:
    """根据前台应用生成 UI 组件树。"""
    ui: List[Dict] = []

    def _add(component_id: str, label: str, clickable: bool = True,
             role: str = "button", extra: Dict | None = None) -> None:
        item = {
            "id": component_id,
            "label": label,
            "role": role,
            "clickable": clickable,
            "bbox": _bbox(len(ui), width),
        }
        if extra:
            item.update(extra)
        ui.append(item)

    app = state.foreground

    if app == "desktop":
        _add("btn:open_files", "文件管理器 (Files)", True)
        _add("btn:open_editor", "文本编辑器 (Editor)", True)
        _add("btn:open_terminal", "终端 (Terminal)", True)
        _add("btn:open_settings", "设置 (Settings)", True)
        _add("btn:open_browser", "浏览器 (Browser)", True)

    elif app == "files":
        _add("title:files", "文件管理器", clickable=False, role="title")
        for path in sorted(state.files.keys()):
            name = path.split("/")[-1]
            mark = " [已选中]" if state.selected_file == path else ""
            _add(f"file:{path}", name + mark, True, "file")
        if not state.files:
            _add("empty:files", "(空文件夹)", clickable=False, role="text")
        _add("btn:rename", "重命名", True)
        _add("btn:delete", "删除", True)
        _add("btn:newfile", "新建文件", True)
        _add("btn:close_files", "关闭", True)

    elif app == "editor":
        _add("title:editor", "文本编辑器", clickable=False, role="title")
        content = state.pending_input.get("editor", "")
        _add("textarea:editor", content[:60] or "(空白)", True, "textarea")
        _add("btn:save", "保存", True)
        _add("btn:close_editor", "关闭", True)

    elif app == "terminal":
        _add("title:terminal", "终端", clickable=False, role="title")
        out = "\n".join(state.logs[-6:])
        _add("out:terminal", out[-200:] or "$", clickable=False, role="output")
        cmd = state.pending_input.get("terminal", "")
        _add("input:terminal", "$ " + cmd, True, "input")
        _add("btn:run", "执行 (Enter)", True)
        _add("btn:close_terminal", "关闭", True)

    elif app == "settings":
        _add("title:settings", "设置", clickable=False, role="title")
        theme = "亮色" if state.pending_input.get("theme", "light") == "light" else "暗色"
        _add("toggle:theme", f"主题: {theme}", True, "toggle")
        _add("btn:close_settings", "关闭", True)

    elif app == "browser":
        _add("title:browser", "浏览器", clickable=False, role="title")
        url = state.pending_input.get("url", "")
        _add("input:url", "地址栏: " + url, True, "input")
        page = state.pending_input.get("page", "(未加载)")
        _add("page:browser", page[:160], clickable=False, role="output")
        _add("btn:goto", "前往", True)
        _add("btn:close_browser", "关闭", True)

    else:
        _add("empty:unknown", f"应用 {app} 无 UI", clickable=False, role="text")

    return ui


def render_screen(state: DesktopState, width: int = 1280, height: int = 720) -> ScreenState:
    """渲染当前桌面状态为一帧 ScreenState。"""
    ui = build_ui(state, width)
    state.ui = ui
    text_lines = [f"前台应用: {state.foreground}"]
    for e in ui:
        b = e.get("bbox", [0, 0])
        text_lines.append(f"  [{e['id']}] {e['label']} ({b[0]},{b[1]})")
    if state.dialog:
        text_lines.append(f"  [对话框] {state.dialog}")
    return ScreenState(
        ui_tree=ui,
        text="\n".join(text_lines),
        width=width,
        height=height,
        foreground_app=state.foreground,
        timestamp=time.time(),
    )
