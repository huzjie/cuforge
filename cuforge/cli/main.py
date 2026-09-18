# -*- coding: utf-8 -*-
"""cuforge 命令行入口。

用法：
    python -m cuforge.cli.main synth --template rename_file
    python -m cuforge.cli.main synth --n 5
    python -m cuforge.cli.main run --task rename_file
    python -m cuforge.cli.main train --episodes 32
    python -m cuforge.cli.main eval
    python -m cuforge.cli.main serve --port 8000
    python -m cuforge.cli.main doctor
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from ..config import load_config
from ..engine import CuForge
from ..utils.logging import setup_logging
from ..verigen.task_bank import build_task_bank


def _engine(args) -> CuForge:
    return CuForge.from_config(args.config) if args.config else CuForge()


def _tasks_by_name(name: str):
    bank = {t.task_id: t for t in build_task_bank()}
    # 内置任务按 goal 首词无法直接查名，改用 verifier 映射
    for t in build_task_bank():
        bank[t.task_id] = t
    if name in bank:
        return [bank[name]]
    # 回退：按模板合成
    engine = CuForge()
    return [engine.synthesize({"template": name})]


def cmd_synth(args) -> int:
    engine = _engine(args)
    if args.template:
        tasks = engine.synthesize_random(args.n, [args.template]) if args.n > 1 else [
            engine.synthesize({"template": args.template})]
    else:
        tasks = engine.synthesize_random(args.n)
    for t in tasks:
        print(json.dumps(t.to_dict(), ensure_ascii=False))
    return 0


def cmd_run(args) -> int:
    engine = _engine(args)
    tasks = _tasks_by_name(args.task)
    for t in tasks:
        ep = engine.run_agent(t)
        print(ep.trajectory.summary())
        print(f"  reward={ep.reward.total:.3f} (result={ep.reward.result:.2f}) status={ep.status.value}")
    return 0


def cmd_train(args) -> int:
    engine = _engine(args)
    summary = engine.train(max_episodes=args.episodes)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def cmd_eval(args) -> int:
    engine = _engine(args)
    result = engine.eval()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args) -> int:
    try:
        import uvicorn  # type: ignore
    except ImportError:
        print("uvicorn required: pip install uvicorn[standard] fastapi pydantic")
        return 1
    from ..serving.app import create_app
    app = create_app(_engine(args))
    uvicorn.run(app, host=args.host, port=args.port)
    return 0


def cmd_doctor(args) -> int:
    """自检：合成 -> 执行 -> 打分 端到端冒烟。"""
    engine = CuForge()
    ok = 0
    total = 0
    for t in build_task_bank():
        ep = engine.run_agent(t)
        total += 1
        if ep.reward.result >= 0.999:
            ok += 1
        print(f"[{'OK' if ep.reward.result >= 0.999 else 'FAIL'}] {t.goal} -> reward={ep.reward.result:.2f}")
    print(f"doctor: {ok}/{total} tasks passed")
    return 0 if ok == total else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="cuforge", description="cuforge 平台 CLI")
    parser.add_argument("--config", default="config.yaml")
    sub = parser.add_subparsers(dest="cmd")

    p_synth = sub.add_parser("synth", help="合成可验证任务")
    p_synth.add_argument("--template", default=None)
    p_synth.add_argument("--n", type=int, default=5)
    p_synth.set_defaults(func=cmd_synth)

    p_run = sub.add_parser("run", help="执行单个任务")
    p_run.add_argument("--task", required=True)
    p_run.set_defaults(func=cmd_run)

    p_train = sub.add_parser("train", help="RLVR 训练")
    p_train.add_argument("--episodes", type=int, default=64)
    p_train.set_defaults(func=cmd_train)

    p_eval = sub.add_parser("eval", help="评测内置基准")
    p_eval.set_defaults(func=cmd_eval)

    p_serve = sub.add_parser("serve", help="启动 FastAPI 服务")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.set_defaults(func=cmd_serve)

    p_doctor = sub.add_parser("doctor", help="端到端自检")
    p_doctor.set_defaults(func=cmd_doctor)

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    setup_logging("INFO")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
