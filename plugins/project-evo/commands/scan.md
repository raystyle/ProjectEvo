---
description: 安全与规范扫描:secrets 与 markdown 禁字,告警提示修改
argument-hint: [目标项目路径] [--no-history]
allowed-tools: Bash
---

对 $ARGUMENTS 指定的项目(缺省当前目录)做安全与规范扫描。

脚本在本插件 `skills/evo/scripts/scan.py`(定位不到就 rg --files 搜 scan.py)。执行:

```bash
uv run <脚本路径>/scan.py <目标项目>          # 全量:工作区+git 历史+md 禁字
uv run <脚本路径>/scan.py <目标项目> --no-history   # 只扫工作区
```

处置口径:HIGH(密钥疑似入库)先轮换凭据再清史(git filter-repo / BFG);md 禁字按告警逐行修正(破折号用冒号/括号/拆句,箭头改文字);已知误报走环境变量 PEVO_SCAN_ALLOW 白名单,不改规则。
