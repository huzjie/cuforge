# -*- coding: utf-8 -*-
"""cuforge 异常体系。"""


class CuForgeError(Exception):
    """所有 cuforge 异常的基类。"""


class ConfigError(CuForgeError):
    """配置缺失或非法。"""


class RegistryError(CuForgeError):
    """注册表查无此条目（验证器 / LLM 后端等）。"""


class VerificationError(CuForgeError):
    """可验证判定执行失败。"""


class EnvironmentError(CuForgeError):
    """桌面环境执行动作失败。"""


class ActionError(CuForgeError):
    """非法动作或动作越界。"""


class SynthesisError(CuForgeError):
    """任务合成失败。"""


class TrainingError(CuForgeError):
    """训练循环异常。"""
