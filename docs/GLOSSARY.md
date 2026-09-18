# 术语表

| 术语 | 说明 |
|---|---|
| CUA | Computer-Use Agent，计算机使用智能体：看截图、点鼠标、敲键盘完成桌面任务 |
| VeriGen | 可验证任务合成：把「任务」和「可判定判据」绑在一起生成 |
| RLVR | Reinforcement Learning with Verifiable Rewards，可验证奖励的强化学习 |
| GRPO | Group Relative Policy Optimization，组相对策略优化，组内奖励归一化 |
| 前沿采样 | Frontier Sampling，维护每任务 top-k 最优轨迹，新采样热身复用 |
| 视觉上下文切分 | Vision Context Windowing，recent/summary/full 控制多轮截图 token |
| 组内相对比较 | 同一任务一组轨迹互相比较，避免全成功/全失败学不到信号 |
