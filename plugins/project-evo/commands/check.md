---
description: 诊断骨架合规 PE-01 至 PE-13(只读)
argument-hint: [目标项目路径]
allowed-tools: Bash
---

对 $ARGUMENTS 指定的项目(缺省当前目录)做 project-evo 骨架合规诊断。

脚本在本插件 `skills/evo/scripts/check.py`(定位不到就 rg --files 搜 check.py)。执行:

```bash
uv run <脚本路径>/check.py <目标项目>
```

输出 PASS/FAIL/SKIP 逐项表与结论行。逐项判定语义见 skill 的 `verification/command-test-cases.md`;FAIL 项按对应参考修正后复跑,直到全绿。
