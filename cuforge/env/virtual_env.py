# -*- coding: utf-8 -*-
"""VirtualDesktopEnv：可运行、可判定的虚拟桌面环境。

模拟一个 Linux 桌面：文件系统（内存）、文件管理器、文本编辑器、
终端（可执行简化 shell 命令）、设置、浏览器。所有操作 deterministic，
终态可被 Verifier 确定性判定——这正是 RLVR 需要的「环境终态可验证打分」。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..core.action import Action, ActionType
from ..core.observation import Observation
from ..core.task import Task
from ..errors import ActionError, EnvironmentError
from .screen import render_screen
from .state import DesktopState

# 简化 shell 命令支持
_SHELL_CMDS = ("mv", "cp", "rm", "mkdir", "echo", "cat", "ls", "touch", "gsettings")


class VirtualDesktopEnv:
    """虚拟桌面环境（确定性、可判定、零依赖）。"""

    def __init__(self, seed: int = 42, max_steps: int = 30) -> None:
        self.seed = seed
        self.max_steps = max_steps
        self.state = DesktopState()
        self._step_count = 0

    # ------------------------------------------------------------------
    def reset(self, task: Task) -> Observation:
        """按任务初始状态重置环境。"""
        init = task.initial_state or {}
        files = init.get("files") or {}
        self.state = DesktopState(files=dict(files))
        self.state.running_apps = list(init.get("running_apps") or [])
        self.state.foreground = init.get("foreground", "desktop")
        self.state.pending_input = dict(init.get("pending_input") or {})
        self.state.logs = list(init.get("logs") or [])
        self.state.clipboard = init.get("clipboard", "")
        self._step_count = 0
        self.max_steps = task.max_steps or self.max_steps
        return self._obs(done=False)

    # ------------------------------------------------------------------
    def step(self, action: Action) -> Observation:
        """执行一个动作，返回观测。"""
        self._step_count += 1
        at = action.type
        st = self.state

        if at == ActionType.OPEN:
            st.foreground = action.app or "desktop"
            if action.app and action.app not in st.running_apps:
                st.running_apps.append(action.app)
            # 打开应用时聚焦默认输入框（与点击桌面图标一致）
            if action.app == "editor":
                st.pending_input.setdefault("editor", "")
                st.focused_input = "editor"
            elif action.app == "terminal":
                st.pending_input.setdefault("terminal", "")
                st.focused_input = "terminal"
            elif action.app == "browser":
                st.focused_input = "url"
        elif at == ActionType.CLICK:
            self._click(action.x, action.y)
        elif at == ActionType.TYPE:
            self._type(action.text or "")
        elif at == ActionType.KEY:
            self._key(action.key or "")
        elif at == ActionType.HOTKEY:
            self._hotkey(action.keys or [])
        elif at == ActionType.SCROLL:
            self._scroll(action.dx or 0, action.dy or 0)
        elif at == ActionType.DRAG:
            self._drag(action.x, action.y, action.dx, action.dy)
        elif at == ActionType.DONE:
            return self._obs(done=True, info={"reason": "agent declared done"})
        elif at == ActionType.WAIT:
            pass
        elif at == ActionType.BACK:
            st.dialog = None
            st.foreground = "desktop"
        else:
            raise ActionError(f"unsupported action: {at}")

        done = self._step_count >= self.max_steps
        return self._obs(done=done, info={"timeout": done and "max_steps" or ""})

    # ------------------------------------------------------------------
    def _obs(self, done: bool, info: Optional[Dict] = None) -> Observation:
        screen = render_screen(self.state)
        return Observation(screen=screen, done=done, info=info or {}, step=self._step_count)

    # ------------------------------------------------------------------
    def _find_component(self, x: int, y: int) -> Optional[Dict]:
        for e in self.state.ui:
            bbox = e.get("bbox")
            if bbox and len(bbox) == 4:
                x0, y0, x1, y1 = bbox
                if x0 <= x <= x1 and y0 <= y <= y1:
                    return e
        return None

    def _click(self, x: Optional[int], y: Optional[int]) -> None:
        st = self.state
        if x is None or y is None:
            # 无坐标：优先点击"确定/执行"类主按钮
            comp = self._find_by_id("btn:ok") or self._find_by_id("btn:run") or self._find_by_id("btn:save")
            if comp is not None:
                self._handle(comp)
            return
        st.cursor = (x, y)
        comp = self._find_component(x, y)
        if comp is None:
            return
        self._handle(comp)

    def _find_by_id(self, cid: str) -> Optional[Dict]:
        for e in self.state.ui:
            if e.get("id") == cid:
                return e
        return None

    def _handle(self, comp: Dict) -> None:
        cid = comp.get("id", "")
        st = self.state
        if cid.startswith("btn:"):
            self._handle_btn(cid[4:])
        elif cid.startswith("file:"):
            st.selected_file = cid[5:]
        elif cid.startswith("input:"):
            st.focused_input = cid[6:]
        elif cid.startswith("textarea:"):
            st.focused_input = cid[9:]
        elif cid.startswith("toggle:"):
            key = cid[7:]
            cur = st.pending_input.get(key, "light")
            st.pending_input[key] = "dark" if cur == "light" else "light"

    def _handle_btn(self, name: str) -> None:
        st = self.state
        if name == "open_files":
            st.foreground = "files"
        elif name == "open_editor":
            st.foreground = "editor"
            st.pending_input.setdefault("editor", "")
            st.focused_input = "editor"
        elif name == "open_terminal":
            st.foreground = "terminal"
            st.pending_input.setdefault("terminal", "")
            st.focused_input = "terminal"
        elif name == "open_settings":
            st.foreground = "settings"
        elif name == "open_browser":
            st.foreground = "browser"
            st.focused_input = "url"
        elif name == "rename":
            if st.selected_file:
                st.dialog = "rename"
                st.focused_input = "rename_value"
                st.pending_input["rename_value"] = ""
        elif name == "delete":
            if st.selected_file:
                st.files.pop(st.selected_file, None)
                st.selected_file = None
        elif name == "newfile":
            st.dialog = "newfile"
            st.focused_input = "newfile_name"
            st.pending_input["newfile_name"] = ""
        elif name == "ok":
            self._confirm_dialog()
        elif name == "cancel":
            st.dialog = None
        elif name == "save":
            if st.foreground == "editor":
                st.files["notes.txt"] = st.pending_input.get("editor", "")
                st.logs.append("[editor] saved notes.txt")
        elif name == "run":
            if st.foreground == "terminal":
                cmd = st.pending_input.get("terminal", "").strip()
                self._exec_shell(cmd)
        elif name == "goto":
            if st.foreground == "browser":
                url = st.pending_input.get("url", "")
                st.pending_input["page"] = f"页面内容 for {url}"
        elif name in ("close_files", "close_editor", "close_terminal",
                      "close_settings", "close_browser"):
            st.foreground = "desktop"
            st.dialog = None

    def _confirm_dialog(self) -> None:
        st = self.state
        dlg = st.dialog
        if dlg == "rename" and st.selected_file:
            new_name = st.pending_input.get("rename_value", "").strip()
            if new_name and "/" not in new_name:
                old = st.selected_file
                parent = old.rsplit("/", 1)[0] if "/" in old else ""
                new_path = (parent + "/" + new_name) if parent else new_name
                st.files[new_path] = st.files.pop(old)
                st.logs.append(f"[files] rename {old} -> {new_path}")
                st.selected_file = None
        elif dlg == "newfile":
            name = st.pending_input.get("newfile_name", "").strip()
            if name and "/" not in name:
                st.files[name] = ""
                st.logs.append(f"[files] create {name}")
        st.dialog = None

    def _type(self, text: str) -> None:
        st = self.state
        if st.focused_input:
            cur = st.pending_input.get(st.focused_input, "")
            st.pending_input[st.focused_input] = cur + text

    def _key(self, key: str) -> None:
        st = self.state
        if key in ("Enter", "Return", "enter"):
            if st.dialog:
                self._confirm_dialog()
            elif st.foreground == "terminal":
                self._exec_shell(st.pending_input.get("terminal", "").strip())
        elif key in ("Backspace", "backspace"):
            if st.focused_input:
                cur = st.pending_input.get(st.focused_input, "")
                st.pending_input[st.focused_input] = cur[:-1]
        elif key in ("Escape", "esc"):
            st.dialog = None

    def _hotkey(self, keys: List[str]) -> None:
        combo = "+".join(k.lower() for k in keys)
        if combo == "ctrl+c":
            self.state.clipboard = self.state.pending_input.get(
                self.state.focused_input or "", "")
        elif combo == "ctrl+v":
            if self.state.focused_input:
                self._type(self.state.clipboard)

    def _scroll(self, dx: int, dy: int) -> None:
        self.state.logs.append(f"[scroll] dx={dx} dy={dy}")

    def _drag(self, x: Optional[int], y: Optional[int],
              dx: Optional[int], dy: Optional[int]) -> None:
        self.state.logs.append(f"[drag] from ({x},{y}) by ({dx},{dy})")

    # ------------------------------------------------------------------
    def _exec_shell(self, cmd: str) -> None:
        st = self.state
        st.logs.append("$ " + cmd)
        if not cmd:
            return
        parts = cmd.split()
        head = parts[0]
        if head not in _SHELL_CMDS:
            st.logs.append(f"bash: {head}: command not found")
            return
        if head == "ls":
            st.logs.append("  " + "  ".join(sorted(st.files.keys())) or "  (empty)")
        elif head == "echo" and len(parts) > 1:
            st.logs.append("  " + " ".join(parts[1:]).strip('"').strip("'"))
        elif head == "cat" and len(parts) > 1:
            st.logs.append("  " + st.files.get(parts[1], ""))
        elif head == "mkdir" and len(parts) > 1:
            st.files[parts[1] + "/.keep"] = ""
            st.logs.append(f"  mkdir {parts[1]}")
        elif head == "touch" and len(parts) > 1:
            st.files[parts[1]] = st.files.get(parts[1], "")
            st.logs.append(f"  touch {parts[1]}")
        elif head == "mv" and len(parts) >= 3:
            if parts[1] in st.files:
                st.files[parts[2]] = st.files.pop(parts[1])
                st.logs.append(f"  mv {parts[1]} -> {parts[2]}")
            else:
                st.logs.append(f"  mv: {parts[1]}: No such file")
        elif head == "cp" and len(parts) >= 3:
            if parts[1] in st.files:
                st.files[parts[2]] = st.files[parts[1]]
                st.logs.append(f"  cp {parts[1]} -> {parts[2]}")
        elif head == "rm" and len(parts) > 1:
            st.files.pop(parts[1], None)
            st.logs.append(f"  rm {parts[1]}")
        elif head == "gsettings" and len(parts) >= 2:
            st.pending_input[parts[-1]] = parts[1]
            st.logs.append(f"  gsettings set {parts[1]} {parts[-1]}")
