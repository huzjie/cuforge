# -*- coding: utf-8 -*-
"""cuforge — 可验证任务合成驱动的计算机使用智能体在线强化学习平台。

基于清华 × Z.AI 开源 ScaleCUA 的核心理念：
把「造可验证题（VeriGen）」和「省着训（前沿采样 + 组相对策略优化）」绑在同一条流水线上，
让计算机使用智能体（Computer-Use Agent, CUA）通过「看截图、点鼠标、敲键盘」完成真实桌面任务，
并用环境终态的可验证判定器给出确定性奖励，驱动在线强化学习（RLVR）持续提升。

四大支柱：
- VeriGen     可验证任务合成引擎（指令 -> 初始状态 + 程序化验证器）
- Desktop Env 隔离桌面环境（文件系统 / UI 组件树 / 进程，可运行可判定）
- Agent       计算机使用智能体运行时（截图观测 -> 规划 -> 动作 -> 执行）
- RLVR       在线强化学习训练循环（采样 -> 打分 -> 组内相对比较 -> 策略更新）

用法：
    from cuforge import CuForge
    engine = CuForge.from_config("config.yaml")
    result = engine.run_agent(task=engine.synthesize("把桌面的 notes.txt 重命名为 done.txt"))

    # 或训练
    engine.train(episodes=32)
"""

__version__ = "0.1.0"
__author__ = "cuforge contributors"
__license__ = "MIT"

from .core.task import Task, TaskStatus
from .core.action import Action, ActionType
from .core.observation import Observation, ScreenState
from .core.trajectory import Trajectory, Step
from .core.reward import VerifiableReward, RewardSource
from .core.episode import Episode, EpisodeStatus
from .config import Config, load_config
from .errors import CuForgeError, RegistryError, VerificationError, EnvironmentError

__all__ = [
    "Task", "TaskStatus",
    "Action", "ActionType",
    "Observation", "ScreenState",
    "Trajectory", "Step",
    "VerifiableReward", "RewardSource",
    "Episode", "EpisodeStatus",
    "Config", "load_config",
    "CuForgeError", "RegistryError", "VerificationError", "EnvironmentError",
    "__version__",
]
