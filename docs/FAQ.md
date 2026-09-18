# 常见问题

**Q: 默认策略能训出更好的策略吗？**
A: 默认 `ScriptedPolicy` 是参考基线（确定性），用于校验环境/验证器自洽。
   要训练真实策略，请接入真实 LLM（`openai_compat`/`vllm`），RLVR 通过
   `policy.update` 钩子作用于可训练策略。

**Q: 如何接入 OSWorld？**
A: 在 Docker 容器内跑真实桌面（`env.backend=docker`），用 `benchmark/osworld.py`
   加载任务 JSON。本仓库 `virtual` 后端做零依赖演示。

**Q: 零依赖吗？**
A: 核心闭环仅 stdlib；`serve`/`yaml` 为可选依赖。
