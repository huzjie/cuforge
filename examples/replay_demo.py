# -*- coding: utf-8 -*-
"""示例：轨迹回放（审计 / 复现）。"""
from cuforge import CuForge
from cuforge.dataset.replay import replay_trajectory


def main():
    engine = CuForge()
    task = engine.synthesize({"template": "rename_file",
                              "params": {"src": "a.txt", "dst": "b.txt"}})
    ep = engine.run_agent(task)
    print("replay:", replay_trajectory(task, ep.trajectory))


if __name__ == "__main__":
    main()
