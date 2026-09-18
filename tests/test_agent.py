# -*- coding: utf-8 -*-
from cuforge.agent.policy import ScriptedPolicy
from cuforge.agent.runtime import AgentRuntime
from cuforge.env.virtual_env import VirtualDesktopEnv
from cuforge.verigen.task_bank import build_task_bank


def test_scripted_policy_passes_bank():
    env = VirtualDesktopEnv()
    runtime = AgentRuntime(env, ScriptedPolicy())
    for t in build_task_bank():
        ep = runtime.run_episode(t)
        assert ep.reward.result >= 0.999, f"task failed: {t.goal}"
