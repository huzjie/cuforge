# 评测基准

| 基准 | 类型 | 接入方式 | ScaleCUA 参考（Qwen3.5-9B） |
|---|---|---|---|
| mini | 内置 | `python -m cuforge.cli.main eval` | 脚本基线 100% |
| OSWorld | 真实 OS GUI | `benchmark/osworld.py`，`env.backend=docker` | 68.7% |
| ScienceBoard | 科学桌面任务 | `benchmark/scienceboard.py`，`env.backend=docker` | 54.0% |

## mini 基准

内置 5 类任务（重命名/编辑/删除/mv/主题），端到端评测成功率。
脚本基线策略可 100% 通过，作为「环境 + 验证器」自洽性校验。
