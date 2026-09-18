# -*- coding: utf-8 -*-
"""训练路由。"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/train")
def train(req):
    engine = req.request.app.state.engine
    tasks = engine.synthesize_random(10, req.templates) if req.templates else None
    summary = engine.train(tasks=tasks, max_episodes=req.episodes)
    return summary
