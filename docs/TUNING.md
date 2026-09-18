# 训练调优

| 现象 | 建议 |
|---|---|
| 成功率上不去 | 增大 `group_size`（组相对比较更稳） |
| 训练太慢 | 开 `frontier_sampling`，调大 `frontier_topk` |
| 轨迹过长 | 调小 `env.max_steps`，加 `max_steps` 护栏 |
| 奖励信号弱 | 检查验证器是否对终态敏感，补过程奖励 |
