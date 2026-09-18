# -*- coding: utf-8 -*-
"""Policy：智能体策略抽象 + 脚本化基线策略 + LLM 策略。"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

from ..core.action import Action
from ..core.observation import Observation
from ..core.task import Task


class Policy:
    """策略：给定任务 + 当前观测 + 历史，输出下一个动作。"""
    name = "base"

    def act(self, task: Task, observation: Observation,
            history: List[Observation]) -> Action:
        raise NotImplementedError

    def reset(self, task: Task) -> None:
        """每个 episode 开始时调用。"""


# ---------------------------------------------------------------
# 脚本化基线策略（reference policy）：解析指令 -> 动作计划 -> 逐步执行
# ---------------------------------------------------------------
def _find_center(ui_tree: List[Dict], target_id: str) -> Optional[tuple]:
    for e in ui_tree:
        if e.get("id") == target_id:
            bbox = e.get("bbox")
            if bbox and len(bbox) == 4:
                return ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
    return None


def _plan(task: Task) -> List[Dict]:
    """把任务解析成一个抽象动作计划（open/click/type/press/done）。"""
    instr = task.instruction
    ver = task.verifier
    vp = task.verifier_params or {}
    files = list((task.initial_state or {}).get("files", {}).keys())
    src = files[0] if files else ""
    src_name = src.split("/")[-1]
    dst_path = vp.get("path", "")
    dst_name = dst_path.split("/")[-1]

    if "终端" in instr or "命令" in instr or "执行" in instr:
        cmd = _cmd_for(task, src, dst_path)
        return [
            {"op": "open", "app": "terminal"},
            {"op": "type", "text": cmd},
            {"op": "press", "key": "Enter"},
            {"op": "done"},
        ]
    if "编辑器" in instr or ver == "file_contains":
        text = vp.get("substring") or vp.get("content") or ""
        return [
            {"op": "open", "app": "editor"},
            {"op": "type", "text": text},
            {"op": "click", "id": "btn:save"},
            {"op": "done"},
        ]
    if "设置" in instr or ver == "state_match":
        return [
            {"op": "open", "app": "settings"},
            {"op": "click", "id": "toggle:theme"},
            {"op": "done"},
        ]
    if ver == "file_absent":
        return [
            {"op": "open", "app": "files"},
            {"op": "click", "id": f"file:{src}"},
            {"op": "click", "id": "btn:delete"},
            {"op": "done"},
        ]
    # 默认：文件管理器重命名（也覆盖 move 的 file_exists 目标）
    return [
        {"op": "open", "app": "files"},
        {"op": "click", "id": f"file:{src}"},
        {"op": "click", "id": "btn:rename"},
        {"op": "type", "text": dst_name},
        {"op": "press", "key": "Enter"},
        {"op": "done"},
    ]


def _cmd_for(task: Task, src: str, dst: str) -> str:
    ver = task.verifier
    vp = task.verifier_params or {}
    if ver == "file_absent":
        return f"rm {src}"
    if ver == "file_contains":
        return f"echo '{vp.get('substring','')}' > {vp.get('path','')}"
    if "mv" in task.instruction and src:
        return f"mv {src} {dst}"
    return f"touch {dst}"


class ScriptedPolicy(Policy):
    """脚本化基线策略：作为演示 / 参考策略，保证端到端可跑通。"""
    name = "scripted"

    def __init__(self) -> None:
        self._plan: List[Dict] = []
        self._idx = 0
        self._wait_turns = 0

    def reset(self, task: Task) -> None:
        self._plan = _plan(task)
        self._idx = 0
        self._wait_turns = 0

    def act(self, task: Task, observation: Observation,
            history: List[Observation]) -> Action:
        if self._idx >= len(self._plan):
            return Action.done()
        step = self._plan[self._idx]
        op = step["op"]

        if op == "open":
            self._idx += 1
            return Action.open(step["app"])
        if op == "type":
            self._idx += 1
            return Action.type_text(step["text"])
        if op == "press":
            self._idx += 1
            return Action.press(step["key"])
        if op == "click":
            center = _find_center(observation.screen.ui_tree, step["id"])
            if center is None:
                # 目标元素未出现：多等一拍（对话框/应用切换渲染）
                self._wait_turns += 1
                if self._wait_turns > 3:
                    self._idx += 1
                    self._wait_turns = 0
                return Action.wait()
            self._wait_turns = 0
            self._idx += 1
            return Action.click(center[0], center[1])
        if op == "done":
            self._idx += 1
            return Action.done()
        return Action.done()


# ---------------------------------------------------------------
# LLM 策略：调用真实 LLM 决策
# ---------------------------------------------------------------
class LLMPolicy(Policy):
    """基于 LLM 的决策策略：观测文本 -> 动作 JSON。"""
    name = "llm"

    def __init__(self, backend: Any, model: str = "qwen3.5-9b",
                 temperature: float = 0.7) -> None:
        self.backend = backend
        self.model = model
        self.temperature = temperature

    def act(self, task: Task, observation: Observation,
            history: List[Observation]) -> Action:
        prompt = self._prompt(task, observation, history)
        raw = self.backend.generate(prompt, temperature=self.temperature)
        return _parse_action(raw)

    def _prompt(self, task: Task, observation: Observation,
                history: List[Observation]) -> str:
        hist = "\n".join(
            f"step{i}: {o.screen.foreground_app} | {o.screen.text[:200]}"
            for i, o in enumerate(history[-4:])
        )
        return (
            f"你是计算机使用智能体，通过点击/输入操作桌面完成任务。\n"
            f"任务：{task.goal}\n"
            f"指令：{task.instruction}\n"
            f"当前屏幕：\n{observation.screen.text}\n"
            f"历史：\n{hist}\n"
            f"请输出下一步动作，格式 JSON："
            f'{{"type":"open|click|type|scroll|key|hotkey|done","x":..,"y":..,"text":"..","key":".."}}'
        )


_ACTION_JSON_RE = re.compile(r"\{[^{}]*\}", re.S)


def _parse_action(raw: str) -> Action:
    m = _ACTION_JSON_RE.search(raw)
    if not m:
        return Action.done()
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return Action.done()
    atype = data.get("type", "done")
    return Action(
        type=atype if atype in ("open", "click", "type", "scroll", "key",
                                "hotkey", "drag", "wait", "back", "done")
        else "done",
        x=data.get("x"), y=data.get("y"), text=data.get("text"),
        dx=data.get("dx"), dy=data.get("dy"), key=data.get("key"),
        app=data.get("app"),
    )
