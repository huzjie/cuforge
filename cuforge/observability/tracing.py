# -*- coding: utf-8 -*-
"""Tracer / Span：轻量分布式追踪（零依赖）。"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional


class Span:
    def __init__(self, name: str, parent: Optional["Span"] = None,
                 attributes: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.parent = parent
        self.trace_id = parent.trace_id if parent else uuid.uuid4().hex[:16]
        self.span_id = uuid.uuid4().hex[:16]
        self.attributes = attributes or {}
        self.children: List["Span"] = []
        self.start = time.time()
        self.end: Optional[float] = None

    def finish(self) -> None:
        self.end = time.time()

    @property
    def duration_ms(self) -> float:
        return ((self.end or time.time()) - self.start) * 1000

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id, "span_id": self.span_id,
            "parent_id": self.parent.span_id if self.parent else None,
            "name": self.name, "attributes": self.attributes,
            "duration_ms": round(self.duration_ms, 3),
            "children": [c.to_dict() for c in self.children],
        }


class Tracer:
    def __init__(self) -> None:
        self._current: Optional[Span] = None

    def start_span(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> Span:
        span = Span(name, parent=self._current, attributes=attributes)
        if self._current is not None:
            self._current.children.append(span)
        self._current = span
        return span

    def end_span(self, span: Optional[Span] = None) -> None:
        target = span or self._current
        if target is not None:
            target.finish()
            self._current = target.parent

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass


_default = Tracer()


def get_tracer() -> Tracer:
    return _default
