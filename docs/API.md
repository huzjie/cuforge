# API 文档

## 核心类

### CuForge（engine.py）
门面：`synthesize` / `run_agent` / `train` / `eval`

### TaskSynthesizer（verigen/synthesizer.py）
`synth spec`：`{"template": "rename_file", "params": {...}}`

### AgentRuntime（agent/runtime.py）
`run_episode(task) -> Episode`

### RLVRTrainer（rl/trainer.py）
`train(max_episodes) -> dict`

## REST（serving）

- `GET /health` → 状态 + 模板列表
- `POST /tasks/synthesize` → `{template, params}` 合成任务
- `POST /tasks/run` → `{template, params}` 执行任务
- `POST /train` → `{episodes}` 训练
- `POST /eval` → 评测
