# -*- coding: utf-8 -*-
"""JsonlExporter：把 span 写为 JSONL 文件。"""
from __future__ import annotations

import json
from typing import List

from ..tracing import Span


class JsonlExporter:
    def __init__(self, path: str = "runs/traces.jsonl") -> None:
        self.path = path

    def export(self, spans: List[Span]) -> None:
        import os
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            for s in spans:
                f.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")
