# -*- coding: utf-8 -*-
"""Pydantic 请求/响应模型。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    BaseModel = object  # type: ignore
    Field = lambda *a, **k: None  # noqa: E731


class TaskSpec(BaseModel if BaseModel is not object else object):
    template: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    goal: Optional[str] = None
    instruction: Optional[str] = None
    verifier: Optional[str] = None
    verifier_params: Optional[Dict[str, Any]] = None
    initial_state: Optional[Dict[str, Any]] = None


class TrainRequest(BaseModel if BaseModel is not object else object):
    episodes: int = 64
    templates: Optional[List[str]] = None


class EvalRequest(BaseModel if BaseModel is not object else object):
    templates: Optional[List[str]] = None
