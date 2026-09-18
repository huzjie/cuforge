# -*- coding: utf-8 -*-
"""任务模板库：每种模板定义「指令生成 + 初始状态 + 验证器」三元组。

VeriGen 的核心思想：不是随便造一句指令，而是把「可验证的判据」和任务绑定，
保证每个合成出来的任务都能被环境终态确定性打分（RLVR 的前提）。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class TaskTemplate:
    name: str
    description: str
    # 指令生成器：参数 -> (goal, instruction)
    gen_instruction: Callable[[Dict[str, Any]], tuple]
    # 初始状态生成器：参数 -> initial_state dict
    gen_initial_state: Callable[[Dict[str, Any]], Dict[str, Any]]
    # 验证器生成器：参数 -> (verifier_type, verifier_params)
    gen_verifier: Callable[[Dict[str, Any]], tuple]
    # 成功判据（人类可读）
    success_criteria: Callable[[Dict[str, Any]], List[str]]
    # 参数空间（用于随机化合成多样任务）
    param_space: Dict[str, List[Any]] = field(default_factory=dict)


# ---- 模板 1：文件重命名 --------------------------------------------------
def _rename_instruction(p):
    src = p["src"]; dst = p["dst"]
    return (
        f"把桌面文件 {src} 重命名为 {dst}",
        f"打开文件管理器，选中 {src}，点击重命名，输入新名称 {dst} 并确认。",
    )


def _rename_initial(p):
    return {"files": {p["src"]: p.get("content", "hello")}, "foreground": "desktop"}


def _rename_verifier(p):
    return ("file_exists", {"path": p["dst"]})


def _rename_criteria(p):
    return [f"文件 {p['dst']} 存在（{p['src']} 已改名）"]


# ---- 模板 2：编辑器写文件 --------------------------------------------------
def _edit_instruction(p):
    return (
        f"用文本编辑器把内容写入 {p.get('target', 'notes.txt')}",
        f"打开文本编辑器，输入内容「{p.get('content', '')}」，点击保存。",
    )


def _edit_initial(p):
    return {"files": {}, "foreground": "desktop"}


def _edit_verifier(p):
    return ("file_contains", {"path": p.get("target", "notes.txt"),
                              "substring": p.get("content", "")})


def _edit_criteria(p):
    return [f"文件 {p.get('target','notes.txt')} 内容包含「{p.get('content','')}」"]


# ---- 模板 3：删除文件 --------------------------------------------------
def _delete_instruction(p):
    return (
        f"删除桌面文件 {p['src']}",
        f"打开文件管理器，选中 {p['src']}，点击删除。",
    )


def _delete_initial(p):
    return {"files": {p["src"]: "x"}, "foreground": "desktop"}


def _delete_verifier(p):
    return ("file_absent", {"path": p["src"]})


def _delete_criteria(p):
    return [f"文件 {p['src']} 已不存在"]


# ---- 模板 4：终端 mv --------------------------------------------------
def _mv_instruction(p):
    return (
        f"用终端把 {p['src']} 移动到 {p['dst']}",
        f"打开终端，执行命令 mv {p['src']} {p['dst']}。",
    )


def _mv_initial(p):
    return {"files": {p["src"]: "data"}, "foreground": "desktop"}


def _mv_verifier(p):
    return ("file_exists", {"path": p["dst"]})


def _mv_criteria(p):
    return [f"文件 {p['dst']} 存在"]


# ---- 模板 5：终端写文件（echo） --------------------------------------------------
def _echo_instruction(p):
    return (
        f"用终端创建文件 {p['dst']} 并写入 {p.get('content','x')}",
        f"打开终端，执行命令 echo {p.get('content','x')} > {p['dst']}（或 touch + 编辑）。",
    )


def _echo_initial(p):
    return {"files": {}, "foreground": "desktop"}


def _echo_verifier(p):
    return ("file_exists", {"path": p["dst"]})


def _echo_criteria(p):
    return [f"文件 {p['dst']} 存在"]


# ---- 模板 6：设置切换主题 --------------------------------------------------
def _theme_instruction(p):
    target = p.get("target", "dark")
    return (
        f"把系统主题切换为{ '暗色' if target=='dark' else '亮色' }",
        "打开设置，点击主题切换开关，使主题变为目标值。",
    )


def _theme_initial(p):
    cur = "light" if p.get("target", "dark") == "dark" else "dark"
    return {"files": {}, "foreground": "desktop", "pending_input": {"theme": cur}}


def _theme_verifier(p):
    return ("state_match", {"field": "theme", "value": p.get("target", "dark")})


def _theme_criteria(p):
    return [f"theme == {p.get('target','dark')}"]


TEMPLATES: Dict[str, TaskTemplate] = {
    "rename_file": TaskTemplate(
        name="rename_file", description="文件管理器重命名",
        gen_instruction=_rename_instruction, gen_initial_state=_rename_initial,
        gen_verifier=_rename_verifier, success_criteria=_rename_criteria,
        param_space={"src": ["notes.txt", "report.md", "photo.jpg"],
                     "dst": ["done.txt", "final.md", "backup.jpg"],
                     "content": ["hello", "data-123"]},
    ),
    "edit_file": TaskTemplate(
        name="edit_file", description="编辑器写内容并保存",
        gen_instruction=_edit_instruction, gen_initial_state=_edit_initial,
        gen_verifier=_edit_verifier, success_criteria=_edit_criteria,
        param_space={"target": ["notes.txt"], "content": ["hello world", "cuforge"]},
    ),
    "delete_file": TaskTemplate(
        name="delete_file", description="文件管理器删除",
        gen_instruction=_delete_instruction, gen_initial_state=_delete_initial,
        gen_verifier=_delete_verifier, success_criteria=_delete_criteria,
        param_space={"src": ["tmp.txt", "junk.log"]},
    ),
    "move_file": TaskTemplate(
        name="move_file", description="终端 mv 移动文件",
        gen_instruction=_mv_instruction, gen_initial_state=_mv_initial,
        gen_verifier=_mv_verifier, success_criteria=_mv_criteria,
        param_space={"src": ["a.txt"], "dst": ["b.txt", "c.txt"]},
    ),
    "echo_file": TaskTemplate(
        name="echo_file", description="终端创建文件",
        gen_instruction=_echo_instruction, gen_initial_state=_echo_initial,
        gen_verifier=_echo_verifier, success_criteria=_echo_criteria,
        param_space={"dst": ["out.txt", "log.txt"], "content": ["ok", "done"]},
    ),
    "toggle_theme": TaskTemplate(
        name="toggle_theme", description="设置切换主题",
        gen_instruction=_theme_instruction, gen_initial_state=_theme_initial,
        gen_verifier=_theme_verifier, success_criteria=_theme_criteria,
        param_space={"target": ["dark", "light"]},
    ),
}
