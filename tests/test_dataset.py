# -*- coding: utf-8 -*-
import os
import tempfile

from cuforge.core.task import Task
from cuforge.dataset import TaskDataset, export_jsonl, import_jsonl


def test_dataset_roundtrip():
    tasks = [Task(goal="g1", instruction="i1", verifier="file_exists",
                  verifier_params={"path": "x"})]
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name
    try:
        export_jsonl(tasks, path)
        loaded = import_jsonl(path)
        assert len(loaded) == 1
        assert loaded[0].goal == "g1"
    finally:
        os.unlink(path)
