# cuforge — 可验证任务合成驱动的计算机使用智能体在线强化学习平台

> 基于清华 × Z.AI 开源 **ScaleCUA**（可扩展任务合成 + 在线强化学习 GUI Agent 框架，9B 模型刷新开源 SOTA）的工程化落地。
> 不是示例，不是演示，而是一套**填写配置即可完整运行**的计算机使用智能体训练与推理平台。

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](./.github/workflows/ci.yml)

---

## 这是什么

**cuforge** 把 ScaleCUA 论文里最难复现的三件事，做成了一个可运行、可扩展、可评测的完整工程：

1. **VeriGen 可验证任务合成** —— 不是随便造一句指令，而是把「任务」和「可判定的验收判据」绑在一起生成。每个任务自带确定性验证器，环境终态可被程序打分（0/1）。
2. **计算机使用智能体运行时** —— 智能体「看截图 → 规划 → 点鼠标/敲键盘 → 观测」，在隔离桌面环境里完成真实 GUI 任务。
3. **RLVR 在线强化学习** —— 采样一组轨迹 → 环境终态确定性打分 → **组内相对比较（GRPO）** → 策略更新，配合**前沿采样（frontier sampling）**省着训。

一句话：**把「造可验证题」和「省着训」绑在同一条流水线上**，让 GUI 智能体能被数据、被奖励持续训出来，而不是靠 prompt 硬调。

---

## 为什么值得用

| 痛点 | cuforge 的解法 |
|---|---|
| GUI 任务没有现成判题器 | VeriGen 内置 6 类任务模板 + 7 类可验证判定器，任务天然可打分 |
| 多轮截图又长又贵 | 视觉上下文切分（recent / summary / full 三模式）控制 token 预算 |
| 全成功/全失败的轨迹学不到信号 | GRPO 组内相对比较，组内归一化得到有效梯度信号 |
| 反复探索太烧钱 | 前沿采样维护每任务 top-k 最优轨迹，新采样热身复用 |

---

## 快速开始

### 1. 安装

```bash
# 核心零依赖，Python 3.9+ 直接跑
pip install -e .

# 若要 FastAPI 服务 / YAML 配置
pip install -e ".[serve]"
```

### 2. 填写配置（config.yaml）

```yaml
env:
  backend: virtual            # virtual | docker | playwright
  max_steps: 30
agent:
  llm_backend: scripted       # scripted | openai_compat | vllm
  model: qwen3.5-9b
  vision_context_mode: recent
rl:
  algorithm: grpo
  group_size: 8
  max_episodes: 64
```

### 3. 端到端自检（合成 → 执行 → 打分）

```bash
python -m cuforge.cli.main doctor
```

输出类似：

```
[OK] 把 notes.txt 重命名为 done.txt -> reward=1.00
[OK] 用编辑器写入 hello world 并保存到 notes.txt -> reward=1.00
[OK] 删除桌面文件 tmp.txt -> reward=1.00
[OK] 用终端把 a.txt 移动到 b.txt -> reward=1.00
[OK] 把系统主题切换为暗色 -> reward=1.00
doctor: 5/5 tasks passed
```

### 4. 一键训练（RLVR）

```bash
python -m cuforge.cli.main train --episodes 64
```

### 5. 评测

```bash
python -m cuforge.cli.main eval
```

### 6. 启动 REST 服务

```bash
python -m cuforge.cli.main serve --port 8000
# GET  /health
# POST /tasks/synthesize  合成可验证任务
# POST /tasks/run         执行任务
# POST /train             RLVR 训练
# POST /eval              评测
```

### 7. Docker

```bash
docker build -t cuforge .
docker run --rm cuforge doctor
```

---

## 四大支柱

### ① VeriGen — 可验证任务合成引擎

- 6 类任务模板：文件重命名 / 编辑器写文件 / 删除文件 / 终端 mv / 终端创建文件 / 设置切换主题
- 7 类可验证判定器：`file_exists` / `file_contains` / `file_absent` / `process_running` / `ui_element` / `state_match` / `clipboard`
- 参数空间随机化合成多样任务，保证「合成即验证」

### ② Desktop Env — 隔离桌面环境

- 内存文件系统 + 运行进程 + UI 组件树 + 剪贴板 + 光标
- 5 个可交互应用：文件管理器 / 文本编辑器 / 终端（简化 shell）/ 设置 / 浏览器
- 支持 click / type / scroll / key / hotkey / drag / open / done 动作
- 一切 deterministic，终态可判定 —— RLVR 的前提

### ③ Agent — 计算机使用智能体运行时

- 闭环：观测 → 策略决策 → 动作 → 环境执行
- 策略：`ScriptedPolicy`（参考基线，端到端可跑通）+ `LLMPolicy`（接真实 LLM）
- 视觉上下文切分：recent / summary / full 三模式控制 token 预算

### ④ RLVR — 在线强化学习

- 采样组 → 组内相对比较 → 优势 → 策略更新
- 三路奖励：结果（verifier 打分）+ 过程（关键中间态）+ 格式（动作合法性）
- 前沿采样：每任务 top-k 最优轨迹，新采样热身复用

---

## 评测基准

| 基准 | 说明 | 参考分数（ScaleCUA, Qwen3.5-9B） |
|---|---|---|
| mini（内置） | 内置任务库端到端成功率 | 本平台 100%（脚本基线） |
| OSWorld | 真实操作系统 GUI 基准，Docker 环境接入 | **68.7%** |
| ScienceBoard | 科学桌面任务基准 | **54.0%** |

> 注：真实 OSWorld/ScienceBoard 需在 Docker 容器内跑真实桌面（`env.backend=docker`），本仓库提供 `virtual` 后端做零依赖演示 + 数据集适配器 `benchmark/osworld.py` / `scienceboard.py`。

---

## 目录结构

```
cuforge/
├── cuforge/
│   ├── core/          # 实体：Task/Action/Observation/Trajectory/Reward/Episode
│   ├── env/           # 虚拟桌面环境：状态/渲染/动作执行
│   ├── verigen/       # 任务合成：模板/合成器/验证器/任务库
│   ├── agent/         # 智能体：运行时/策略/视觉上下文/LLM 后端
│   ├── rl/            # RLVR：训练器/GRPO/前沿采样/奖励模型/采样器/缓冲
│   ├── serving/       # FastAPI 服务 + 路由
│   ├── benchmark/     # 评测：mini/OSWorld/ScienceBoard
│   ├── cli/           # 命令行入口
│   ├── engine.py      # 顶层门面 CuForge
│   └── sdk.py         # Python SDK
├── examples/          # 示例脚本
├── tests/             # 单元测试
├── docs/              # 架构/使用/RLVR/VeriGen/模型卡
├── k8s/               # Kubernetes 部署
├── Dockerfile / docker-compose.yml
└── config.yaml        # 配置文件（填写即可运行）
```

---

## 接入真实模型

默认 `scripted` 策略零依赖可跑通全流程；要接入真实 LLM 决策：

```yaml
agent:
  llm_backend: openai_compat
  model: qwen3.5-9b
llm:
  provider: openai_compat
  base_url: https://your-endpoint/v1
  api_key: sk-xxxx
```

支持 `openai_compat`（任意 OpenAI 兼容端点）、`vllm`（本地 vLLM）、`mock`（占位）。

---

## License

[MIT](./LICENSE)
