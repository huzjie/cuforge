# -*- coding: utf-8 -*-
from cuforge.core.episode import Episode
from cuforge.core.task import Task
from cuforge.rl.grpo import compute_advantages


def _ep(r):
    e = Episode(task=Task(goal="x", instruction="x"))
    e.reward.result = r
    e.reward.process = 0
    e.reward.format = 0
    return e


def test_advantages_normalize():
    eps = [_ep(1.0), _ep(1.0), _ep(0.0), _ep(0.0)]
    advs = compute_advantages(eps)
    assert advs[0] > 0
    assert advs[2] < 0
