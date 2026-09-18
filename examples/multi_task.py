# -*- coding: utf-8 -*-
"""示例：批量合成 + 批量评测。"""
from cuforge import CuForge


def main():
    engine = CuForge()
    tasks = engine.synthesize_random(n=12)
    result = engine.eval(tasks)
    print(f"success_rate={result['success_rate']:.2%} "
          f"({result['passed']}/{result['total']})")
    for p in result["per_task"]:
        mark = "OK" if p["passed"] else "FAIL"
        print(f"  [{mark}] {p['goal']}")


if __name__ == "__main__":
    main()
