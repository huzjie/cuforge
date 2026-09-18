# 模型卡目录

cuforge 支持接入任意 OpenAI 兼容 / vLLM 模型作为决策后端。以下为推荐的
计算机使用智能体基座模型（均与 ScaleCUA 的 9B 量级路线一致）。

| 模型卡 | 参数 | 说明 |
|---|---|---|
| [qwen3.5-9b.md](./qwen3.5-9b.md) | 9B | ScaleCUA 基线，OSWorld 68.7% |
| [qwen3.5-14b.md](./qwen3.5-14b.md) | 14B | 更大容量变体 |
| [kimi-k2.5.md](./kimi-k2.5.md) | — | 开源侧此前较强基线（OSWorld 63.3%） |
| [intern-s2-397b.md](./intern-s2-397b.md) | 397B | 上海 AI Lab 科学/长程智能体旗舰 |
