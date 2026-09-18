# -*- coding: utf-8 -*-
"""cuforge Python SDK：一行式便捷函数。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .config import Config
from .core.task import Task
from .engine import CuForge

_default_engine: Optional[CuForge] = None


def get_engine(config: Optional[Config] = None) -> CuForge:
    global _default_engine
    if _default_engine is None:
        _default_engine = CuForge(config)
    return _default_engine


def synthesize(spec: Dict[str, Any]) -> Task:
    return get_engine().synthesize(spec)


def run_task(task: Task):
    return get_engine().run_agent(task)


def run_goal(goal: str, **kwargs: Any):
    """按目标字符串快速构造任务并执行。"""
    spec: Dict[str, Any] = {"goal": goal, "instruction": kwargs.get("instruction", goal),
                            "verifier": kwargs.get("verifier", "file_exists"),
                            "verifier_params": kwargs.get("verifier_params", {}),
                            "initial_state": kwargs.get("initial_state", {})}
    task = synthesize(spec)
    return run_task(task)


def train(tasks: Optional[List[Task]] = None, max_episodes: int = 64) -> Dict[str, Any]:
    return get_engine().train(tasks, max_episodes=max_episodes)


def eval(tasks: Optional[List[Task]] = None) -> Dict[str, Any]:
    return get_engine().eval(tasks)
