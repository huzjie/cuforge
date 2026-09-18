# -*- coding: utf-8 -*-
"""轨迹回放：把历史轨迹在环境中重放一遍（用于审计/复现）。"""
from __future__ import annotations

from typing import Any, Dict

from ..core.episode import Episode
from ..core.trajectory import Trajectory
from ..env.virtual_env import VirtualDesktopEnv
from ..verigen.verifier_registry import VerifierRegistry


def replay_trajectory(task, trajectory: Trajectory) -> Dict[str, Any]:
    env = VirtualDesktopEnv()
    env.reset(task)
    for step in trajectory.steps:
        env.step(step.action)
    result = VerifierRegistry.verify(task.verifier, env.state, task.verifier_params or {})
    return {"task_id": task.task_id, "replayed_reward": result,
            "steps": len(trajectory.steps)}
