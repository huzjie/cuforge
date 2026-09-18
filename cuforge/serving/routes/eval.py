# -*- coding: utf-8 -*-
"""评测路由。"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/eval")
def evaluate(req):
    engine = req.request.app.state.engine
    tasks = engine.synthesize_random(10, req.templates) if req.templates else None
    return engine.eval(tasks)
