# -*- coding: utf-8 -*-
from cuforge import CuForge
from cuforge.verigen.templates_extra import EXTRA_TEMPLATES


def test_copy_template_runs():
    engine = CuForge()
    engine.synthesizer.templates.update(EXTRA_TEMPLATES)
    task = engine.synthesize({"template": "copy_file",
                              "params": {"src": "a.txt", "dst": "a.bak"}})
    ep = engine.run_agent(task)
    assert ep.reward.result >= 0.999
