# -*- coding: utf-8 -*-
"""配置加载与校验（YAML / dict / dataclass）。"""
from __future__ import annotations

import copy
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
    _HAS_YAML = True
except Exception:  # pragma: no cover
    _HAS_YAML = False

from .errors import ConfigError


@dataclass
class EnvConfig:
    """桌面环境配置。"""
    backend: str = "virtual"          # virtual | docker | playwright
    max_steps: int = 30
    screen_width: int = 1280
    screen_height: int = 720
    seed: int = 42
    filesystem_root: str = "/tmp/cuforge-env"
    stateful: bool = True


@dataclass
class AgentConfig:
    """计算机使用智能体运行时配置。"""
    llm_backend: str = "mock"         # mock | openai_compat | vllm
    model: str = "qwen3.5-9b"
    temperature: float = 0.7
    max_tokens: int = 1024
    history_window: int = 8           # 视觉上下文窗口（帧数）
    vision_context_mode: str = "recent"  # recent | summary | full
    planner: str = "react"            # react | plan_execute
    reflect: bool = True


@dataclass
class RlConfig:
    """在线强化学习（RLVR）配置。"""
    algorithm: str = "grpo"           # grpo
    group_size: int = 8               # 每组采样轨迹数（组相对比较）
    max_episodes: int = 64
    learning_rate: float = 1e-4
    kl_coef: float = 0.01
    reward_sources: List[str] = field(default_factory=lambda: ["result", "process", "format"])
    frontier_sampling: bool = True
    frontier_topk: int = 2


@dataclass
class LlmConfig:
    """LLM 后端配置。"""
    provider: str = "mock"
    base_url: str = ""
    api_key: str = ""
    model: str = "qwen3.5-9b"
    timeout: float = 60.0


@dataclass
class Config:
    """cuforge 顶层配置。"""
    env: EnvConfig = field(default_factory=EnvConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    rl: RlConfig = field(default_factory=RlConfig)
    llm: LlmConfig = field(default_factory=LlmConfig)
    task_bank: str = "builtin"
    output_dir: str = "./runs"
    seed: int = 42
    log_level: str = "INFO"

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]] = None) -> "Config":
        data = data or {}
        cfg = cls()
        env = data.get("env") or {}
        agent = data.get("agent") or {}
        rl = data.get("rl") or {}
        llm = data.get("llm") or {}
        cfg.env = EnvConfig(**{k: v for k, v in env.items()
                               if k in EnvConfig.__dataclass_fields__})
        cfg.agent = AgentConfig(**{k: v for k, v in agent.items()
                                   if k in AgentConfig.__dataclass_fields__})
        cfg.rl = RlConfig(**{k: v for k, v in rl.items()
                             if k in RlConfig.__dataclass_fields__})
        cfg.llm = LlmConfig(**{k: v for k, v in llm.items()
                               if k in LlmConfig.__dataclass_fields__})
        for k in ("task_bank", "output_dir", "seed", "log_level"):
            if k in data:
                setattr(cfg, k, data[k])
        return cfg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "env": copy.deepcopy(self.env.__dict__),
            "agent": copy.deepcopy(self.agent.__dict__),
            "rl": copy.deepcopy(self.rl.__dict__),
            "llm": copy.deepcopy(self.llm.__dict__),
            "task_bank": self.task_bank,
            "output_dir": self.output_dir,
            "seed": self.seed,
            "log_level": self.log_level,
        }


def _parse_scalar(val: str) -> Any:
    """解析 YAML 标量 / 内联列表。"""
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1]
        return [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
    if val in ("true", "True"):
        return True
    if val in ("false", "False"):
        return False
    if val in ("null", "~", "none", "None", ""):
        return None
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val.strip('"').strip("'")


def _simple_yaml(text: str) -> Dict[str, Any]:
    """极简 YAML 子集解析器（stdlib only）：标量 / 内联列表 / 两层嵌套 / 注释 / 引号。

    作为无 PyYAML 时的 fallback，覆盖 cuforge 配置文件的全部结构。
    """
    result: Dict[str, Any] = {}
    current_section: Optional[str] = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip().strip('"').strip("'")
        val = val.strip()
        if " #" in val:
            val = val.split(" #", 1)[0].strip()
        if val == "":
            current_section = key
            result.setdefault(key, {})
            continue
        parsed = _parse_scalar(val)
        if indent > 0 and current_section:
            result.setdefault(current_section, {})[key] = parsed
        else:
            result[key] = parsed
            current_section = None
    return result


def load_config(path: str) -> Config:
    """从 YAML 文件加载配置（优先 PyYAML，无则用内置极简解析器）。"""
    if not os.path.exists(path):
        raise ConfigError(f"config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if _HAS_YAML:
        data = yaml.safe_load(text) or {}
    else:
        data = _simple_yaml(text)
    return Config.from_dict(data)
