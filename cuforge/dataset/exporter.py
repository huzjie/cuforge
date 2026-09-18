# -*- coding: utf-8 -*-
"""数据集导出/导入（JSONL）。"""
from __future__ import annotations

import json
from typing import List

from ..core.task import Task


def export_jsonl(tasks: List[Task], path: str) -> None:
    import os
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t.to_dict(), ensure_ascii=False) + "\n")


def import_jsonl(path: str) -> List[Task]:
    tasks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(Task.from_dict(json.loads(line)))
    return tasks
