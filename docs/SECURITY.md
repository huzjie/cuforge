# 安全说明

cuforge 提供多层安全能力（见 `cuforge/security/`）：

- **Sandbox**：动作级隔离（限制可打开应用、可按键、输入长度）
- **ActionWhitelist**：动作类型白名单
- **GuardrailEngine**：可组合护栏（如轨迹长度上限）
- **AuditLog**：追加式 JSONL 审计日志

## 生产建议

- 真实桌面/容器环境请启用 `env.backend=docker`，勿用 `virtual` 跑不可信输入
- 终端命令执行请加命令白名单（`env/virtual_env.py` 中 `_SHELL_CMDS`）
- 接入真实 LLM 决策时，务必叠加护栏与白名单
