# -*- coding: utf-8 -*-
"""AuditLog：安全审计日志（追加式 JSONL）。"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional


class AuditLog:
    def __init__(self, path: str = "runs/audit.jsonl") -> None:
        self.path = path

    def log(self, event: str, detail: Optional[Dict[str, Any]] = None,
            actor: str = "agent") -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        entry = {"ts": time.time(), "actor": actor, "event": event,
                 "detail": detail or {}}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
