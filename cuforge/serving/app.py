# -*- coding: utf-8 -*-
"""FastAPI 应用工厂。"""
from __future__ import annotations

from fastapi import FastAPI

from .routes import eval as eval_route
from .routes import tasks as tasks_route
from .routes import train as train_route


def create_app(engine=None) -> FastAPI:
    app = FastAPI(title="cuforge", version="0.1.0",
                  description="可验证任务合成驱动的计算机使用智能体在线强化学习平台")

    if engine is None:
        from ..engine import CuForge
        engine = CuForge()
    app.state.engine = engine

    @app.get("/health")
    def health():
        return {"status": "ok", "version": "0.1.0",
                "templates": engine.synthesizer.list_templates()}

    app.include_router(tasks_route.router)
    app.include_router(train_route.router)
    app.include_router(eval_route.router)
    return app
