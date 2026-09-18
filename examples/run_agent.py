# -*- coding: utf-8 -*-
"""示例：执行单个任务，打印完整轨迹。"""
from cuforge import CuForge


def main():
    engine = CuForge()
    task = engine.synthesize({"template": "rename_file",
                              "params": {"src": "notes.txt", "dst": "done.txt"}})
    ep = engine.run_agent(task)
    print("goal:", task.goal)
    for s in ep.trajectory.steps:
        print(f"  step{s.step_index}: {s.action.type.value} "
              f"app={s.observation.screen.foreground_app}")
    print(f"outcome={ep.trajectory.outcome} reward={ep.reward.total:.3f}")


if __name__ == "__main__":
    main()
