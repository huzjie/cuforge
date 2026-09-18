# -*- coding: utf-8 -*-
"""TaskDataset：任务数据集容器。"""
from __future__ import annotations

from typing import Iterator, List, Optional

from ..core.task import Task


class TaskDataset:
    def __init__(self, tasks: Optional[List[Task]] = None) -> None:
        self.tasks = list(tasks or [])

    def __len__(self) -> int:
        return len(self.tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)

    def __getitem__(self, i) -> Task:
        return self.tasks[i]

    def shuffle(self, seed: int = 42) -> "TaskDataset":
        import random
        r = random.Random(seed)
        r.shuffle(self.tasks)
        return self

    def to_list(self) -> List[dict]:
        return [t.to_dict() for t in self.tasks]

    @classmethod
    def from_list(cls, data: List[dict]) -> "TaskDataset":
        return cls([Task.from_dict(d) for d in data])
