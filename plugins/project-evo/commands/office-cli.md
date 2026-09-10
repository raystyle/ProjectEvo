---
description: 定位本机 OfficeCLI，或跑三类文件冒烟
argument-hint: [which|smoke]
allowed-tools: Bash
---

对 OfficeCLI 做定位或冒烟。脚本在本插件 `skills/office-pro/scripts/`（定位不到就 rg --files 搜 which.py）。

$ARGUMENTS 缺省或为 `which`：跑 `which.py`（找到退出 0，未找到退出 2）。
$ARGUMENTS 为 `smoke`：跑 `smoke.py`（无二进制退出 2）。

```bash
uv run <脚本路径>/which.py
uv run <脚本路径>/smoke.py
```

安装、改稿、事实核查纪律见 skill `references/`。禁止 `officecli install`。
