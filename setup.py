# -*- coding: utf-8 -*-
"""setuptools 入口（兼容旧工具链）。"""
from setuptools import setup, find_packages

setup(
    name="cuforge",
    version="0.1.0",
    description="Verifiable task synthesis + online RL for computer-use agents",
    packages=find_packages(include=["cuforge", "cuforge.*"]),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "serve": ["fastapi", "uvicorn[standard]", "pydantic>=2.0"],
        "yaml": ["PyYAML>=6.0"],
    },
    entry_points={"console_scripts": ["cuforge=cuforge.cli.main:main"]},
)
