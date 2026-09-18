# -*- coding: utf-8 -*-
from cuforge.env.state import DesktopState
from cuforge.verigen.verifier_registry import VerifierRegistry


def test_file_exists():
    st = DesktopState(files={"a.txt": "x"})
    assert VerifierRegistry.verify("file_exists", st, {"path": "a.txt"}) == 1.0
    assert VerifierRegistry.verify("file_exists", st, {"path": "b.txt"}) == 0.0


def test_file_contains():
    st = DesktopState(files={"a.txt": "hello world"})
    assert VerifierRegistry.verify(
        "file_contains", st, {"path": "a.txt", "substring": "world"}) == 1.0
