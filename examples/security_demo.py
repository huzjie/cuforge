# -*- coding: utf-8 -*-
"""示例：安全能力（沙箱 + 白名单 + 护栏 + 审计）。"""
from cuforge.core.action import Action
from cuforge.security import Sandbox, ActionWhitelist, GuardrailEngine, AuditLog
from cuforge.security.guardrails import MAX_STEPS_RAIL


def main():
    sandbox = Sandbox()
    print("open files allowed:", sandbox.check(Action.open("files")))
    print("open evil allowed:", sandbox.check(Action.open("evil")))

    wl = ActionWhitelist()
    print("whitelist desc:", wl.block_reason(Action.click(0, 0)))

    engine = GuardrailEngine()
    engine.add(MAX_STEPS_RAIL)
    print("guardrails pass:", engine.passes(object()))

    audit = AuditLog("runs/audit.jsonl")
    audit.log("sandbox_check", {"action": "open", "app": "files"})


if __name__ == "__main__":
    main()
