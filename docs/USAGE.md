# 使用指南

## 安装

```bash
pip install -e .              # 核心（零依赖）
pip install -e ".[serve,yaml]" # 服务 + 配置
```

## 命令行

```bash
python -m cuforge.cli.main synth --template rename_file --n 5   # 合成任务
python -m cuforge.cli.main run --task rename_file               # 执行任务
python -m cuforge.cli.main train --episodes 64                  # RLVR 训练
python -m cuforge.cli.main eval                                 # 评测
python -m cuforge.cli.main serve --port 8000                    # 服务
python -m cuforge.cli.main doctor                               # 自检
```

## Python SDK

```python
from cuforge import CuForge
from cuforge.sdk import synthesize, run_task, train

engine = CuForge()

# 合成可验证任务
task = engine.synthesize({"template": "rename_file",
                          "params": {"src": "a.txt", "dst": "b.txt"}})

# 执行
ep = engine.run_agent(task)
print(ep.trajectory.summary(), ep.reward.total)

# 训练
summary = engine.train(max_episodes=32)
print(summary)
```

## REST API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /health | 健康检查 + 模板列表 |
| POST | /tasks/synthesize | 合成任务 |
| POST | /tasks/run | 执行任务 |
| POST | /train | RLVR 训练 |
| POST | /eval | 评测 |

## 接入真实模型

`config.yaml` 里把 `agent.llm_backend` 和 `llm.provider` 切到 `openai_compat`
或 `vllm`，填 `base_url` / `api_key` 即可，决策走真实 LLM。
