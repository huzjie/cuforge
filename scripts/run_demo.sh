#!/usr/bin/env bash
# 端到端演示：自检 -> 合成 -> 执行 -> 评测
set -e
python -m cuforge.cli.main doctor
python examples/synth_tasks.py
python examples/run_agent.py
python -m cuforge.cli.main eval
