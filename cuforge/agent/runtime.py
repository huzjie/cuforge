# -*- coding: utf-8 -*-
"""AgentRuntime：计算机使用智能体运行时。

闭环：观测 -> 策略决策 -> 动作 -> 环境执行 -> 新观测，直到 done 或超时。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..core.episode import Episode, EpisodeStatus
from ..core.observation import Observation
from ..core.reward import VerifiableReward
from ..core.task import Task
from ..core.trajectory import Step, Trajectory
from ..env.virtual_env import VirtualDesktopEnv
from ..utils.io import now_ms
from ..verigen.verifier_registry import VerifierRegistry
from .policy import Policy
from .vision import vision_window


class AgentRuntime:
    """计算机使用智能体运行时：策略在环境中执行任务并打分。"""

    def __init__(self, env: VirtualDesktopEnv, policy: Policy,
                 vision_mode: str = "recent", vision_window_size: int = 8,
                 reflect: bool = False) -> None:
        self.env = env
        self.policy = policy
        self.vision_mode = vision_mode
        self.vision_window_size = vision_window_size
        self.reflect = reflect

    def run_episode(self, task: Task, group_id: int = 0) -> Episode:
        """执行一个任务，返回带奖励的 Episode。"""
        t0 = now_ms()
        self.policy.reset(task)
        obs = self.env.reset(task)
        traj = Trajectory(task_id=task.task_id)
        history: List[Observation] = []

        while not obs.done:
            action = self.policy.act(task, obs, history)
            if action.type.value == "done":
                obs = self.env.step(action)
                break
            traj.add(Step(action=action, observation=obs, thought=""))
            history.append(obs)
            obs = self.env.step(action)

        reward = self._score(task)
        outcome = "success" if reward.result >= 0.999 else (
            "timeout" if obs.done and obs.info.get("timeout") else "failed")
        traj.outcome = outcome
        traj.final_reward = reward.total

        return Episode(
            task=task, trajectory=traj, reward=reward,
            status=(EpisodeStatus.SUCCESS if reward.result >= 0.999
                    else (EpisodeStatus.TIMEOUT if outcome == "timeout"
                          else EpisodeStatus.FAILED)),
            duration_ms=now_ms() - t0, group_id=group_id,
        )

    def _score(self, task: Task) -> VerifiableReward:
        """用可验证判定器对终态打分。"""
        result = VerifierRegistry.verify(
            task.verifier, self.env.state, task.verifier_params or {})
        reward = VerifiableReward(result=result)
        reward.details = {"verifier": task.verifier,
                          "verifier_params": task.verifier_params}
        return reward

    def run(self, task: Task) -> Episode:
        return self.run_episode(task)
