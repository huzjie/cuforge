# -*- coding: utf-8 -*-
"""训练/评估指标追踪器。"""
from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any, Dict, List


class MetricsTracker:
    """滚动窗口指标聚合。"""

    def __init__(self) -> None:
        self._series: Dict[str, List[float]] = defaultdict(list)
        self._scalars: Dict[str, Any] = {}

    def record(self, name: str, value: float) -> None:
        self._series[name].append(value)

    def set_scalar(self, name: str, value: Any) -> None:
        self._scalars[name] = value

    def mean(self, name: str, window: int = 0) -> float:
        vals = self._series.get(name, [])
        if window and len(vals) > window:
            vals = vals[-window:]
        return statistics.fmean(vals) if vals else 0.0

    def latest(self, name: str) -> float:
        vals = self._series.get(name, [])
        return vals[-1] if vals else 0.0

    def success_rate(self, name: str = "reward", threshold: float = 0.999) -> float:
        vals = self._series.get(name, [])
        if not vals:
            return 0.0
        return sum(1 for v in vals if v >= threshold) / len(vals)

    def snapshot(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"scalars": dict(self._scalars)}
        for k, v in self._series.items():
            out[k] = {
                "count": len(v),
                "mean": statistics.fmean(v) if v else 0.0,
                "last": v[-1] if v else 0.0,
            }
        return out
