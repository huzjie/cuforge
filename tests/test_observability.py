# -*- coding: utf-8 -*-
from cuforge.observability import Tracer
from cuforge.observability.metrics import Registry


def test_tracer_spans():
    t = Tracer()
    s = t.start_span("a")
    t.end_span(s)
    assert s.duration_ms >= 0


def test_registry():
    r = Registry()
    r.counter("x").inc(2)
    r.histogram("h").observe(3)
    snap = r.snapshot()
    assert snap["counters"]["x"] == 2.0
