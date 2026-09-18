# -*- coding: utf-8 -*-
"""示例：合成一批可验证任务并打印。"""
from cuforge import CuForge


def main():
    engine = CuForge()
    tasks = engine.synthesize_random(n=6)
    for t in tasks:
        print(f"- {t.goal}  [verifier={t.verifier} {t.verifier_params}]")
        print(f"    success_criteria: {t.success_criteria}")


if __name__ == "__main__":
    main()
