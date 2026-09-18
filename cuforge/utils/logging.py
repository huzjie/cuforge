# -*- coding: utf-8 -*-
"""日志工具（零依赖，仅 stdlib）。"""
from __future__ import annotations

import logging
import sys
from typing import Optional

_LOGGER_NAME = "cuforge"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(_LOGGER_NAME if name is None else f"{_LOGGER_NAME}.{name}")
