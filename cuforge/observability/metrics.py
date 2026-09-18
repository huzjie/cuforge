# -*- coding: utf-8 -*-
"""Prometheus 风格指标（计数器/直方图，零依赖）。"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class Counter:
    def __init__(self) -> None:
        self._value = 0.0

    def inc(self, n: float = 1.0) -> None:
        self._value += n

    def get(self) -> float:
        return self._value


class Histogram:
    def __init__(self, buckets: List[float] | None = None) -> None:
        self.buckets = buckets or [1, 5, 10, 25, 50, 100, 200, 500]
        self._counts = [0] * (len(self.buckets) + 1)
        self._sum = 0.0
        self._n = 0

    def observe(self, value: float) -> None:
        self._sum += value
        self._n += 1
        for i, b in enumerate(self.buckets):
            if value <= b:
                self._counts[i] += 1
                return
        self._counts[-1] += 1

    def snapshot(self) -> Dict:
        return {"count": self._n, "sum": round(self._sum, 3),
                "buckets": dict(zip([str(b) for b in self.buckets] + ["+inf"],
                                    self._counts))}


class Registry:
    def __init__(self) -> None:
        self._counters: Dict[str, Counter] = defaultdict(Counter)
        self._histograms: Dict[str, Histogram] = defaultdict(Histogram)

    def counter(self, name: str) -> Counter:
        return self._counters[name]

    def histogram(self, name: str) -> Histogram:
        return self._histograms[name]

    def snapshot(self) -> Dict:
        return {
            "counters": {k: v.get() for k, v in self._counters.items()},
            "histograms": {k: v.snapshot() for k, v in self._histograms.items()},
        }
