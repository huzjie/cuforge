# -*- coding: utf-8 -*-
"""GRPO：组相对策略优化（Group Relative Policy Optimization）。

核心：同一任务的一组采样轨迹，用组内均值/方差归一化奖励得到优势，
再进行策略更新——不依赖外部价值网络。
"""
from __future__ import annotations

import math
from typing import List

from ..core.episode import Episode


def compute_advantages(episodes: List[Episode], eps: float = 1e-8) -> List[float]:
    """组内奖励归一化 -> 优势。"""
    rewards = [e.reward.total for e in episodes]
    n = len(rewards)
    if n == 0:
        return []
    mean = sum(rewards) / n
    var = sum((r - mean) ** 2 for r in rewards) / n
    std = math.sqrt(var) + eps
    return [(r - mean) / std for r in rewards]


class GRPOUpdater:
    """GRPO 更新器：把优势写回 episode，并可调用策略 update。"""
    kl_coef: float = 0.01

    def __init__(self, kl_coef: float = 0.01) -> None:
        self.kl_coef = kl_coef

    def assign_advantages(self, episodes: List[Episode]) -> None:
        advs = compute_advantages(episodes, eps=1e-8)
        for e, a in zip(episodes, advs):
            e.advantage = a

    def update(self, policy, episodes: List[Episode]) -> dict:
        """调用策略的 update 钩子（若支持），返回更新统计。"""
        self.assign_advantages(episodes)
        if hasattr(policy, "update"):
            return policy.update(episodes, kl_coef=self.kl_coef)
        return {"updated": False, "reason": "policy has no update hook"}
