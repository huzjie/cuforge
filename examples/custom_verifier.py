# -*- coding: utf-8 -*-
"""示例：自定义并注册验证器。"""
from cuforge.verigen.verifier_registry import Verifier, VerifierRegistry


class StartsWithVerifier(Verifier):
    name = "starts_with"

    def verify(self, state, params):
        content = state.file_content(params.get("path", ""))
        return 1.0 if content.startswith(params.get("prefix", "")) else 0.0


VerifierRegistry.register("starts_with", StartsWithVerifier)
print("registered verifiers:", VerifierRegistry.list())
