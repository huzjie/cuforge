# -*- coding: utf-8 -*-
"""示例：可观测性（tracing + 指标）。"""
from cuforge.observability import Tracer
from cuforge.observability.metrics import Registry


def main():
    tracer = Tracer()
    root = tracer.start_span("train", {"episodes": 64})
    child = tracer.start_span("sample_group", {"group_size": 8})
    child.finish()
    tracer.end_span(child)
    root.finish()

    reg = Registry()
    reg.counter("episodes").inc(64)
    reg.histogram("steps").observe(3)
    reg.histogram("steps").observe(5)
    print("metrics:", reg.snapshot())


if __name__ == "__main__":
    main()
