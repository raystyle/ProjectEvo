---
description: 扫描本地 git 与 GitHub 的密钥/隐私泄露
argument-hint: [目标项目] [--github owner/repo] [--clone-history] [--pii] [--no-history] [--json]
allowed-tools: Bash
---

对 $ARGUMENTS 做密钥与隐私扫描。脚本在本插件 `skills/secret-scan/scripts/scan.py`。

```bash
uv run <脚本>/scan.py $ARGUMENTS
```

缺省扫当前目录工作区 + git 全历史。`--github owner/repo` 加 GitHub alerts 与 code search;完整远程历史必须显式 `--clone-history`。HIGH 先轮换凭据再清史。
