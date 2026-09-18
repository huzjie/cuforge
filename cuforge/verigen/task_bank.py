# -*- coding: utf-8 -*-
"""内置任务库：一批手工定义的可验证任务（含黄金解法提示，供评测/示例）。"""
from __future__ import annotations

from typing import Dict, List

from ..core.task import Task

BUILTIN_TASKS: List[Dict] = [
    {
        "goal": "把 notes.txt 重命名为 done.txt",
        "instruction": "打开文件管理器，选中 notes.txt，点击重命名，输入 done.txt 并确认。",
        "verifier": "file_exists", "verifier_params": {"path": "done.txt"},
        "initial_state": {"files": {"notes.txt": "hello"}, "foreground": "desktop"},
        "success_criteria": ["done.txt 存在"],
        "gold_plan": ["open files", "click notes.txt", "rename", "type done.txt", "confirm"],
    },
    {
        "goal": "用编辑器写入 hello world 并保存到 notes.txt",
        "instruction": "打开文本编辑器，输入 hello world，点击保存。",
        "verifier": "file_contains",
        "verifier_params": {"path": "notes.txt", "substring": "hello world"},
        "initial_state": {"files": {}, "foreground": "desktop"},
        "success_criteria": ["notes.txt 内容含 hello world"],
        "gold_plan": ["open editor", "type hello world", "save"],
    },
    {
        "goal": "删除桌面文件 tmp.txt",
        "instruction": "打开文件管理器，选中 tmp.txt，点击删除。",
        "verifier": "file_absent", "verifier_params": {"path": "tmp.txt"},
        "initial_state": {"files": {"tmp.txt": "junk"}, "foreground": "desktop"},
        "success_criteria": ["tmp.txt 不存在"],
        "gold_plan": ["open files", "click tmp.txt", "delete"],
    },
    {
        "goal": "用终端把 a.txt 移动到 b.txt",
        "instruction": "打开终端，执行命令 mv a.txt b.txt。",
        "verifier": "file_exists", "verifier_params": {"path": "b.txt"},
        "initial_state": {"files": {"a.txt": "data"}, "foreground": "desktop"},
        "success_criteria": ["b.txt 存在"],
        "gold_plan": ["open terminal", "type mv a.txt b.txt", "run"],
    },
    {
        "goal": "把系统主题切换为暗色",
        "instruction": "打开设置，点击主题切换开关，使主题变为 dark。",
        "verifier": "state_match",
        "verifier_params": {"field": "theme", "value": "dark"},
        "initial_state": {"files": {}, "foreground": "desktop", "pending_input": {"theme": "light"}},
        "success_criteria": ["theme == dark"],
        "gold_plan": ["open settings", "click toggle:theme"],
    },
]


def build_task_bank() -> List[Task]:
    return [Task(**{k: v for k, v in d.items() if k != "gold_plan"}) for d in BUILTIN_TASKS]
