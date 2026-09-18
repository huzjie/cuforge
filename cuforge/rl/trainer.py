# -*- coding: utf-8 -*-
"""RLVRTrainer：在线强化学习训练主循环。

采样 -> 打分 -> 组内相对比较（GRPO）-> 前沿更新 -> 策略更新。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..agent.runtime import AgentRuntime
from ..core.task import Task
from ..utils.io import ensure_dir, write_json
from ..utils.logging import get_logger
from ..utils.metrics import MetricsTracker
from .buffer import ExperienceSample, ReplayBuffer
from .frontier import FrontierPool
from .grpo import GRPOUpdater
from .sampler import EpisodeSampler

log = get_logger("rl")


class RLVRTrainer:
    """RLVR 训练器。"""

    def __init__(self, runtime: AgentRuntime, tasks: List[Task],
                 algorithm: str = "grpo", group_size: int = 8,
                 frontier_topk: int = 2, reward_sources: Optional[List[str]] = None,
                 output_dir: str = "./runs") -> None:
        self.runtime = runtime
        self.tasks = tasks
        self.algorithm = algorithm
        self.group_size = group_size
        self.sampler = EpisodeSampler(runtime, reward_sources)
        self.updater = GRPOUpdater()
        self.frontier = FrontierPool(topk=frontier_topk)
        self.buffer = ReplayBuffer()
        self.metrics = MetricsTracker()
        self.output_dir = ensure_dir(output_dir)

    def train(self, max_episodes: int = 64, log_every: int = 8) -> Dict[str, Any]:
        """训练主循环。"""
        total_groups = 0
        for step in range(max_episodes):
            task = self.tasks[step % len(self.tasks)]
            group = self.sampler.sample_group(
                task, group_id=total_groups, group_size=self.group_size)
            total_groups += 1

            # 组内相对比较（GRPO）
            self.updater.assign_advantages(group)

            # 前沿更新 + 经验入缓冲
            for ep in group:
                self.frontier.add(ep)
                self.buffer.push(ExperienceSample(
                    prompt=ep.task.instruction, task_id=ep.task.task_id,
                    trajectory=ep.trajectory, reward=ep.reward.total,
                    advantage=ep.advantage,
                    meta={"outcome": ep.trajectory.outcome},
                ))

            # 策略更新
            self.updater.update(self.runtime.policy, group)

            # 指标
            success = sum(1 for e in group if e.reward.result >= 0.999)
            self.metrics.record("success_rate", success / len(group))
            self.metrics.record("mean_reward", sum(e.reward.total for e in group) / len(group))
            self.metrics.record("mean_steps", sum(e.trajectory.length for e in group) / len(group))

            if (step + 1) % log_every == 0:
                log.info(
                    f"train step={step+1}/{max_episodes} "
                    f"success={success}/{len(group)} "
                    f"mean_reward={self.metrics.latest('mean_reward'):.3f} "
                    f"frontier={self.frontier.size()}"
                )

        return self.summary()

    def summary(self) -> Dict[str, Any]:
        """训练汇总。"""
        summary = {
            "algorithm": self.algorithm,
            "group_size": self.group_size,
            "frontier": self.frontier.snapshot(),
            "buffer_size": len(self.buffer),
            "metrics": self.metrics.snapshot(),
            "best_success_rate": self.metrics.mean("success_rate"),
        }
        write_json(f"{self.output_dir}/train_summary.json", summary)
        return summary
