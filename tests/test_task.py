# -*- coding: utf-8 -*-
from cuforge.core.task import Task, TaskStatus
from cuforge.verigen.synthesizer import TaskSynthesizer


def test_synthesize_rename():
    s = TaskSynthesizer(seed=1)
    t = s.synthesize({"template": "rename_file",
                      "params": {"src": "a.txt", "dst": "b.txt"}})
    assert t.verifier == "file_exists"
    assert t.verifier_params == {"path": "b.txt"}
    assert t.initial_state["files"] == {"a.txt": "hello"}


def test_task_status_enum():
    assert TaskStatus.SUCCESS.value == "success"
