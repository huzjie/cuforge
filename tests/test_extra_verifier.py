# -*- coding: utf-8 -*-
from cuforge.env.state import DesktopState
from cuforge.verigen import verifiers_extra  # noqa: F401  注册扩展验证器
from cuforge.verigen.verifier_registry import VerifierRegistry


def test_count_verifier():
    st = DesktopState(files={"a.txt": "x", "b.txt": "y"})
    assert VerifierRegistry.verify("file_count", st, {"count": 2}) == 1.0


def test_regex_verifier():
    st = DesktopState(files={"a.txt": "hello 123"})
    assert VerifierRegistry.verify("regex_match", st,
                                   {"path": "a.txt", "pattern": r"\d+"}) == 1.0
