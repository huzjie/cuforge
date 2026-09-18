# VeriGen — 可验证任务合成

## 设计原则

「造可验证题」和「省着训」绑在同一条流水线：不是随便造一句指令，
而是把「指令 + 初始状态 + 可验证判据」三元组一起生成。

## 任务模板

| 模板 | 验证器 | 说明 |
|---|---|---|
| rename_file | file_exists | 文件管理器重命名 |
| edit_file | file_contains | 编辑器写内容并保存 |
| delete_file | file_absent | 删除文件 |
| move_file | file_exists | 终端 mv |
| echo_file | file_exists | 终端创建文件 |
| toggle_theme | state_match | 设置切换主题 |

## 可验证判定器

`file_exists` / `file_contains` / `file_absent` / `process_running` /
`ui_element` / `state_match` / `clipboard` —— 全部对 `DesktopState` 做确定性判定。

## 扩展新模板

在 `cuforge/verigen/templates.py` 里新增 `TaskTemplate`：
指令生成器 + 初始状态生成器 + 验证器生成器 + 成功判据 + 参数空间。
