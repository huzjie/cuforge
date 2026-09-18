# -*- coding: utf-8 -*-
"""扩展任务模板（copy / mkdir / search / calc / note / calendar）。

使用方式：
    from cuforge.verigen.templates_extra import EXTRA_TEMPLATES
    engine.synthesizer.templates.update(EXTRA_TEMPLATES)
"""
from __future__ import annotations

from typing import Any, Dict, List

from .templates import TaskTemplate


def _copy_instruction(p):
    return (f"复制文件 {p['src']} 为 {p['dst']}",
            f"打开终端，执行命令 cp {p['src']} {p['dst']}。")


def _copy_initial(p):
    return {"files": {p["src"]: "content"}, "foreground": "desktop"}


def _copy_verifier(p):
    return ("file_exists", {"path": p["dst"]})


def _copy_criteria(p):
    return [f"文件 {p['dst']} 存在"]


def _mkdir_instruction(p):
    return (f"创建目录 {p['dir']}",
            f"打开终端，执行命令 mkdir {p['dir']}。")


def _mkdir_initial(p):
    return {"files": {}, "foreground": "desktop"}


def _mkdir_verifier(p):
    return ("file_exists", {"path": p["dir"] + "/.keep"})


def _mkdir_criteria(p):
    return [f"目录 {p['dir']} 已创建"]


def _search_instruction(p):
    return (f"在浏览器打开 {p['url']}",
            f"打开浏览器，在地址栏输入 {p['url']} 并前往。")


def _search_initial(p):
    return {"files": {}, "foreground": "desktop"}


def _search_verifier(p):
    return ("state_match", {"field": "url", "value": p["url"]})


def _search_criteria(p):
    return [f"浏览器地址栏为 {p['url']}"]


def _note_instruction(p):
    return (f"在编辑器记录备忘「{p.get('text','')}」",
            f"打开文本编辑器，输入「{p.get('text','')}」，点击保存。")


def _note_initial(p):
    return {"files": {}, "foreground": "desktop"}


def _note_verifier(p):
    return ("file_contains", {"path": "notes.txt",
                              "substring": p.get("text", "")})


def _note_criteria(p):
    return [f"notes.txt 含「{p.get('text','')}」"]


EXTRA_TEMPLATES: Dict[str, TaskTemplate] = {
    "copy_file": TaskTemplate(
        name="copy_file", description="终端 cp 复制文件",
        gen_instruction=_copy_instruction, gen_initial_state=_copy_initial,
        gen_verifier=_copy_verifier, success_criteria=_copy_criteria,
        param_space={"src": ["a.txt"], "dst": ["a-copy.txt", "a.bak"]},
    ),
    "mkdir": TaskTemplate(
        name="mkdir", description="终端创建目录",
        gen_instruction=_mkdir_instruction, gen_initial_state=_mkdir_initial,
        gen_verifier=_mkdir_verifier, success_criteria=_mkdir_criteria,
        param_space={"dir": ["docs", "tmp", "backup"]},
    ),
    "browse": TaskTemplate(
        name="browse", description="浏览器打开 URL",
        gen_instruction=_search_instruction, gen_initial_state=_search_initial,
        gen_verifier=_search_verifier, success_criteria=_search_criteria,
        param_space={"url": ["https://example.com", "https://news.ycombinator.com"]},
    ),
    "write_note": TaskTemplate(
        name="write_note", description="编辑器写备忘",
        gen_instruction=_note_instruction, gen_initial_state=_note_initial,
        gen_verifier=_note_verifier, success_criteria=_note_criteria,
        param_space={"text": ["meeting at 3pm", "buy milk", "todo: ship v1"]},
    ),
}
