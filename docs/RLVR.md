# RLVR — 在线强化学习（可验证奖励）

## 为什么 GUI 智能体难用普通 RL

- 任务只有指令和环境，没有数学题那种现成判题器；
- 多轮截图又长又贵；
- 同题采一组轨迹，全成功/全失败时组内学不到信号。

## cuforge 的做法

1. **VeriGen 造可验证题**：任务自带确定性验证器，环境终态可打分。
2. **组相对策略优化（GRPO）**：不依赖价值网络，组内奖励归一化得到优势：
   `advantage_i = (r_i - mean) / (std + eps)`
3. **前沿采样**：维护每任务 top-k 最优轨迹，新采样热身复用，减少无效探索。
4. **三路奖励**：结果（verifier）+ 过程（关键中间态）+ 格式（动作合法性）。

## 训练流程

```
for step in range(max_episodes):
    task = tasks[step % len(tasks)]
    group = sample_group(task, group_size)   # 采样 N 条轨迹
    assign_advantages(group)                 # 组内相对比较
    update_frontier(group)                   # 前沿更新
    policy.update(group)                     # 策略更新
```

## 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| algorithm | grpo | 算法 |
| group_size | 8 | 每组采样轨迹数 |
| max_episodes | 64 | 最大训练轮数 |
| kl_coef | 0.01 | KL 散度系数 |
| frontier_topk | 2 | 前沿每任务保留数 |
