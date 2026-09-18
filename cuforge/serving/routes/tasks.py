# -*- coding: utf-8 -*-
"""任务相关路由：合成 + 执行。"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ...core.task import Task

router = APIRouter()


def _spec_to_dict(spec) -> dict:
    if spec is None:
        return {}
    return {k: v for k, v in spec.__dict__.items() if v is not None}


@router.post("/tasks/synthesize")
def synthesize(spec):
    engine = spec.request.app.state.engine
    d = _spec_to_dict(spec)
    if "template" in d and d["template"]:
        task = engine.synthesize({"template": d["template"], "params": d.get("params") or {}})
    elif "goal" in d and d["goal"]:
        task = Task(**{k: v for k, v in d.items() if v is not None})
    else:
        raise HTTPException(400, "need template or goal")
    return task.to_dict()


@router.post("/tasks/run")
def run_task(spec):
    engine = spec.request.app.state.engine
    d = _spec_to_dict(spec)
    if "template" in d and d["template"]:
        task = engine.synthesize({"template": d["template"], "params": d.get("params") or {}})
    else:
        task = Task(**{k: v for k, v in d.items() if v is not None})
    ep = engine.run_agent(task)
    return ep.to_dict()
