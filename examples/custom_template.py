# -*- coding: utf-8 -*-
"""示例：注册并合成自定义任务模板。"""
from cuforge import CuForge
from cuforge.verigen.templates_extra import EXTRA_TEMPLATES


def main():
    engine = CuForge()
    engine.synthesizer.templates.update(EXTRA_TEMPLATES)
    task = engine.synthesize({"template": "copy_file",
                              "params": {"src": "a.txt", "dst": "a.bak"}})
    ep = engine.run_agent(task)
    print(task.goal, "->", ep.trajectory.outcome, ep.reward.total)


if __name__ == "__main__":
    main()
