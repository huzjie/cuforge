# Qwen3.5-9B 模型卡（计算机使用）

- **角色**：cuforge / ScaleCUA 推荐基座
- **参数量**：9B
- **参考分数**：OSWorld 68.7%，ScienceBoard 54.0%（经 ScaleCUA RLVR 训练后）
- **接入**：
  ```yaml
  agent:
    llm_backend: openai_compat
    model: qwen3.5-9b
  llm:
    provider: openai_compat
    base_url: https://your-endpoint/v1
    api_key: sk-xxxx
  ```
- **说明**：开源侧此前较强的 Kimi K2.5 为 63.3%、Claude Sonnet 4.5 为 62.9%，
  ScaleCUA 训练的 Qwen3.5-9B 以 68.7% 刷新开源 SOTA。
