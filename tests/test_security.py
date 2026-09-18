# -*- coding: utf-8 -*-
from cuforge.core.action import Action
from cuforge.security import Sandbox, ActionWhitelist, GuardrailEngine
from cuforge.security.guardrails import MAX_STEPS_RAIL


def test_sandbox():
    s = Sandbox()
    assert s.check(Action.open("files"))
    assert not s.check(Action.open("evil"))


def test_whitelist():
    wl = ActionWhitelist()
    assert wl.allow(Action.click(0, 0))


def test_guardrail():
    g = GuardrailEngine()
    g.add(MAX_STEPS_RAIL)
    assert g.passes(object())
