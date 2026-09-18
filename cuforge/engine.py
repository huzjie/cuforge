# -*- coding: utf-8 -*-
"""CuForge：顶层门面，聚合任务合成 / 智能体执行 / RLVR 训练 / 评测。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .agent.policy import Policy, ScriptedPolicy, LLMPolicy
from .agent.runtime import AgentRuntime
from .config import Config, load_config
from .core.episode import Episode
from .core.task import Task
from .env.virtual_env import VirtualDesktopEnv
from .rl.trainer import RLVRTrainer
from .verigen.synthesizer import TaskSynthesizer
from .verigen.task_bank import build_task_bank


class CuForge:
    """cuforge 平台门面。"""

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self.synthesizer = TaskSynthesizer(seed=self.config.seed)
        self.env = VirtualDesktopEnv(
            seed=self.config.env.seed, max_steps=self.config.env.max_steps)
        self.policy = self._build_policy()
        self.runtime = AgentRuntime(
            self.env, self.policy,
            vision_mode=self.config.agent.vision_context_mode,
            vision_window_size=self.config.agent.history_window,
            reflect=self.config.agent.reflect,
        )

    def _build_policy(self) -> Policy:
        if self.config.agent.llm_backend in ("mock", "scripted"):
            return ScriptedPolicy()
        from .agent.llm.registry import build_backend
        backend = build_backend(self.config.llm)
        return LLMPolicy(backend, model=self.config.agent.model,
                         temperature=self.config.agent.temperature)

    @classmethod
    def from_config(cls, path: str) -> "CuForge":
        return cls(load_config(path))

    # ---- 任务合成 -------------------------------------------------
    def synthesize(self, spec: Dict[str, Any]) -> Task:
        return self.synthesizer.synthesize(spec)

    def synthesize_random(self, n: int = 10, templates: Optional[List[str]] = None) -> List[Task]:
        return self.synthesizer.synthesize_random(templates, n)

    # ---- 智能体执行 -------------------------------------------------
    def run_agent(self, task: Task) -> Episode:
        return self.runtime.run_episode(task)

    # ---- 训练 -------------------------------------------------
    def train(self, tasks: Optional[List[Task]] = None,
              max_episodes: Optional[int] = None) -> Dict[str, Any]:
        tasks = tasks or build_task_bank()
        max_episodes = max_episodes or self.config.rl.max_episodes
        trainer = RLVRTrainer(
            self.runtime, tasks,
            algorithm=self.config.rl.algorithm,
            group_size=self.config.rl.group_size,
            frontier_topk=self.config.rl.frontier_topk,
            reward_sources=self.config.rl.reward_sources,
            output_dir=self.config.output_dir,
        )
        return trainer.train(max_episodes=max_episodes)

    # ---- 评测 -------------------------------------------------
    def eval(self, tasks: Optional[List[Task]] = None) -> Dict[str, Any]:
        from .benchmark.mini_bench import evaluate
        tasks = tasks or build_task_bank()
        return evaluate(self.runtime, tasks)
