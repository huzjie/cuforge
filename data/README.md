# data 目录

存放外部基准数据集（OSWorld / ScienceBoard / Terminal-Bench / WebArena 等）的 JSON 任务文件。

- `data/osworld/` — OSWorld 任务（`*.json`）
- `data/scienceboard/` — ScienceBoard 任务
- `data/terminal_bench/` — Terminal-Bench 任务

每个 JSON 至少含 `instruction` 字段；可含 `verifier` / `verifier_params` / `initial_state`。
