# -*- coding: utf-8 -*-
"""OSWorldAdapter：真实 OSWorld 基准适配器。

说明：OSWorld 是真实操作系统上的 GUI 智能体基准。本适配器提供
「从 OSWorld JSON 任务文件加载 -> 映射为 cuforge Task」的接口，
真实评测需在 Docker 容器内跑真实桌面环境（本项目提供 virtual 后端
做零依赖演示；接入真实 OSWorld 请将 env.backend 切为 docker）。

参考（ScaleCUA 论文，Qwen3.5-9B）：OSWorld 68.7%。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..core.task import Task
from .base import Benchmark


class OSWorldAdapter(Benchmark):
    name = "osworld"

    def __init__(self, data_path: str = "data/osworld") -> None:
        self.data_path = Path(data_path)

    def tasks(self) -> List[Task]:
        tasks: List[Task] = []
        if not self.data_path.exists():
            return tasks
        for f in self.data_path.glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(Task(
                goal=data.get("instruction", ""),
                instruction=data.get("instruction", ""),
                verifier=data.get("verifier", "state_match"),
                verifier_params=data.get("verifier_params", {}),
                initial_state=data.get("initial_state", {}),
                metadata={"benchmark": "osworld", "source": f.name},
            ))
        return tasks
