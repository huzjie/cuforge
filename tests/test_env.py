# -*- coding: utf-8 -*-
from cuforge.core.action import Action
from cuforge.core.task import Task
from cuforge.env.virtual_env import VirtualDesktopEnv


def _task():
    return Task(goal="rename", instruction="rename a.txt to b.txt",
                verifier="file_exists", verifier_params={"path": "b.txt"},
                initial_state={"files": {"a.txt": "x"}, "foreground": "desktop"})


def test_rename_flow():
    env = VirtualDesktopEnv()
    task = _task()
    env.reset(task)
    env.step(Action.open("files"))
    # 选中 a.txt（点击 file:a.txt 组件）
    from cuforge.env.screen import render_screen
    ui = env.state.ui
    target = next(e for e in ui if e["id"] == "file:a.txt")
    bbox = target["bbox"]
    env.step(Action.click((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2))
    env.step(Action.click(None, None))  # 无坐标 -> 优先 ok/run/save（此处无，故需找 rename）
    assert env.state.selected_file == "a.txt"
