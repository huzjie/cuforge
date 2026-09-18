# -*- coding: utf-8 -*-
"""ConsoleExporter：把 span 树打印到控制台。"""
from __future__ import annotations

import json
from typing import List

from ..tracing import Span


class ConsoleExporter:
    def export(self, spans: List[Span]) -> None:
        for s in spans:
            self._dump(s, depth=0)

    def _dump(self, span: Span, depth: int) -> None:
        pad = "  " * depth
        print(f"{pad}- {span.name} ({span.duration_ms:.1f}ms) {json.dumps(span.attributes, ensure_ascii=False)}")
        for c in span.children:
            self._dump(c, depth + 1)
