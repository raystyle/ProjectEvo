---
description: 安装文档骨架(幂等,不覆盖已有)
argument-hint: <目标项目路径> [--name 项目名]
allowed-tools: Bash
---

为 $ARGUMENTS 指定的项目安装 project-evo 文档骨架。

脚本在本插件 `skills/evo/scripts/init.py`(定位不到就 rg --files 搜 init.py)。执行:

```bash
uv run <脚本路径>/init.py <目标项目> --name <项目名>
```

纪律:已有文件一律跳过不覆盖;装完按输出提示补两处:AGENTS 定位段、GOAL 起点回指 D01。骨架结构与各文件义务详见 skill 的 `references/base-init.md`。
