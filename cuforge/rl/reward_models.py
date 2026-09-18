# -*- coding: utf-8 -*-
"""奖励模型：结果 / 过程 / 格式三路奖励。"""
from __future__ import annotations

from typing import List

from ..core.episode import Episode
from ..core.reward import RewardSource

# 正确应用名（按验证器类型启发式推导，用于过程奖励）
_APP_BY_VERIFIER = {
    "file_exists": "files",
    "file_contains": "editor",
    "file_absent": "files",
    "state_match": "settings",
    "process_running": "terminal",
    "clipboard": "editor",
}


def result_reward(episode: Episode) -> float:
    """结果奖励：环境终态可验证打分（0/1）。"""
    return episode.reward.result


def process_reward(episode: Episode) -> float:
    """过程奖励：是否打开了「正确应用」并产生有效交互。"""
    expected_app = _APP_BY_VERIFIER.get(episode.task.verifier)
    opened = any(
        s.action.type.value == "open" and s.action.app == expected_app
        for s in episode.trajectory.steps
    ) if expected_app else False
    interacted = episode.trajectory.length >= 2
    return (0.05 if opened else 0.0) + (0.05 if interacted else 0.0)


def format_reward(episode: Episode) -> float:
    """格式奖励：动作序列是否以 DONE 收尾且无空轨迹。"""
    acts = [s.action for s in episode.trajectory.steps]
    if not acts:
        return 0.0
    has_done = acts[-1].type.value == "done"
    return 0.1 if has_done else 0.0


def composite_reward(episode: Episode, sources: List[str] | None = None) -> float:
    """合成总奖励（结果 + 过程 + 格式）。"""
    sources = sources or ["result", "process", "format"]
    total = 0.0
    if "result" in sources:
        r = result_reward(episode)
        episode.reward.result = r
        episode.reward.sources[RewardSource.RESULT.value] = r
        total += r
    if "process" in sources:
        p = process_reward(episode)
        episode.reward.process = p
        episode.reward.sources[RewardSource.PROCESS.value] = p
        total += p
    if "format" in sources:
        f = format_reward(episode)
        episode.reward.format = f
        episode.reward.sources[RewardSource.FORMAT.value] = f
        total += f
    return total
