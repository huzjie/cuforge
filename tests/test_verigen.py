# -*- coding: utf-8 -*-
from cuforge.verigen.synthesizer import TaskSynthesizer


def test_random_synthesis():
    s = TaskSynthesizer(seed=42)
    tasks = s.synthesize_random(n=10)
    assert len(tasks) == 10
    for t in tasks:
        assert t.goal
        assert t.verifier in ("file_exists", "file_contains", "file_absent",
                              "state_match", "process_running", "ui_element",
                              "clipboard")


def test_list_templates():
    s = TaskSynthesizer()
    assert "rename_file" in s.list_templates()
