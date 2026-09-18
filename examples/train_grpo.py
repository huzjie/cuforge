# -*- coding: utf-8 -*-
"""示例：RLVR / GRPO 训练。"""
from cuforge import CuForge
from cuforge.verigen.task_bank import build_task_bank


def main():
    engine = CuForge()
    tasks = build_task_bank()
    summary = engine.train(tasks=tasks, max_episodes=32)
    print("best_success_rate:", summary["best_success_rate"])
    print("frontier:", summary["frontier"])


if __name__ == "__main__":
    main()
