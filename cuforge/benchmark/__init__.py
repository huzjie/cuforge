# -*- coding: utf-8 -*-
"""benchmark 包：评测基准。"""
from .base import Benchmark, EvalResult
from .mini_bench import evaluate
from .osworld import OSWorldAdapter
from .scienceboard import ScienceBoardAdapter

__all__ = ["Benchmark", "EvalResult", "evaluate", "OSWorldAdapter", "ScienceBoardAdapter"]

# 扩展基准（独立文件，按需导入，避免影响核心包加载）
def __getattr__(name):
    if name == "TerminalBenchAdapter":
        from .terminal_bench import TerminalBenchAdapter
        return TerminalBenchAdapter
    if name == "WebArenaAdapter":
        from .webarena import WebArenaAdapter
        return WebArenaAdapter
    if name == "WindowsAgentArenaAdapter":
        from .windowsagentarena import WindowsAgentArenaAdapter
        return WindowsAgentArenaAdapter
    if name == "Mind2WebAdapter":
        from .mind2web import Mind2WebAdapter
        return Mind2WebAdapter
    raise AttributeError(f"module 'cuforge.benchmark' has no attribute {name!r}")
