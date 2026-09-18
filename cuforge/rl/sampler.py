# -*- coding: utf-8 -*-
"""EpisodeSampler：采样一个 episode 组（用于组相对比较）。"""
from __future__ import annotations

from typing import List

from ..agent.runtime import AgentRuntime
from ..core.episode import Episode
from ..core.task import Task
from ..rl.reward_models import composite_reward


class EpisodeSampler:
    """对同一任务采样 group_size 条轨迹，计算奖励。"""

    def __init__(self, runtime: AgentRuntime, reward_sources: List[str] | None = None) -> None:
        self.runtime = runtime
        self.reward_sources = reward_sources or ["result", "process", "format"]

    def sample_group(self, task: Task, group_id: int = 0,
                     group_size: int = 8) -> List[Episode]:
        episodes: List[Episode] = []
        for i in range(group_size):
            ep = self.runtime.run_episode(task, group_id=group_id)
            composite_reward(ep, self.reward_sources)
            episodes.append(ep)
        return episodes
