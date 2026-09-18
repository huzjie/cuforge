# 贡献指南

1. Fork 本仓库，基于 `main` 分支开发
2. 新增任务模板：`cuforge/verigen/templates.py` 加 `TaskTemplate`
3. 新增验证器：`cuforge/verigen/verifiers_extra.py` 加类并注册
4. 新增 LLM 后端：`cuforge/agent/llm/` 加类
5. 提交前：`python -m cuforge.cli.main doctor` + `python -m pytest -q`
