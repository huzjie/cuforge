# -*- coding: utf-8 -*-
"""FrontierPool：前沿采样（frontier sampling）。

维护每个任务的历史最优轨迹（top-k），新采样时可从前沿「热身」，
减少无效探索——这是 ScaleCUA「省着训」的关键之一。
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from ..core.episode import Episode


class FrontierPool:
    """前沿经验池：每任务保留 top-k 高分轨迹。"""

    def __init__(self, topk: int = 2) -> None:
        self.topk = topk
        self._pool: Dict[str, List[Episode]] = {}

    def add(self, episode: Episode) -> None:
        tid = episode.task.task_id
        lst = self._pool.setdefault(tid, [])
        lst.append(episode)
        lst.sort(key=lambda e: e.reward.total, reverse=True)
        del lst[self.topk:]

    def best(self, task_id: str) -> Optional[Episode]:
        lst = self._pool.get(task_id)
        return lst[0] if lst else None

    def best_reward(self, task_id: str) -> float:
        e = self.best(task_id)
        return e.reward.total if e else 0.0

    def task_ids(self) -> List[str]:
        return sorted(self._pool.keys())

    def size(self) -> int:
        return sum(len(v) for v in self._pool.values())

    def snapshot(self) -> Dict[str, float]:
        return {tid: self.best_reward(tid) for tid in self.task_ids()}
