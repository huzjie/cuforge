# -*- coding: utf-8 -*-
"""TaskSynthesizer：VeriGen 任务合成引擎。

从模板 + 参数空间合成「可验证」任务，保证每个任务都能被确定性判定。
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from ..core.task import Task
from ..errors import SynthesisError
from .templates import TEMPLATES, TaskTemplate


class TaskSynthesizer:
    """可验证任务合成引擎。"""

    def __init__(self, seed: int = 42, templates: Optional[Dict[str, TaskTemplate]] = None) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.templates = templates or TEMPLATES

    def synthesize(self, spec: Dict[str, Any]) -> Task:
        """按 spec 合成一个任务。

        spec 支持：
          {"template": "rename_file", "params": {...}}   显式参数
          {"template": "rename_file"}                    随机采样参数
          {"goal": "...", "instruction": "...", ...}     直接指定（含 verifier）
        """
        if "goal" in spec and "verifier" in spec:
            return Task(**spec)

        tpl_name = spec.get("template")
        if tpl_name not in self.templates:
            raise SynthesisError(f"unknown template: {tpl_name}")
        tpl = self.templates[tpl_name]

        params = spec.get("params")
        if not params:
            params = self.sample_params(tpl)
        else:
            params = dict(params)

        goal, instruction = tpl.gen_instruction(params)
        verifier, verifier_params = tpl.gen_verifier(params)
        initial_state = tpl.gen_initial_state(params)
        criteria = tpl.success_criteria(params)

        return Task(
            goal=goal, instruction=instruction,
            verifier=verifier, verifier_params=verifier_params,
            initial_state=initial_state, success_criteria=criteria,
            metadata={"template": tpl_name, "params": params},
        )

    def sample_params(self, tpl: TaskTemplate) -> Dict[str, Any]:
        """从参数空间随机采样一组参数。"""
        params: Dict[str, Any] = {}
        for key, choices in tpl.param_space.items():
            params[key] = self.rng.choice(choices)
        return params

    def synthesize_batch(self, specs: List[Dict[str, Any]]) -> List[Task]:
        return [self.synthesize(s) for s in specs]

    def synthesize_random(self, template_names: Optional[List[str]] = None, n: int = 10) -> List[Task]:
        """随机合成 n 个任务（跨模板均匀采样）。"""
        names = template_names or list(self.templates.keys())
        if not names:
            return []
        tasks = []
        for i in range(n):
            name = self.rng.choice(names)
            tasks.append(self.synthesize({"template": name}))
        return tasks

    def list_templates(self) -> List[str]:
        return sorted(self.templates.keys())
