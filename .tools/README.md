# .tools 项目脚本工具

| 脚本 | 用途 | 调用方 |
| --- | --- | --- |
| md-guard.py | markdown 四类禁字门禁(规则同源 `project_evo.mdfix`,与 scan/check PE-12 一致) | Claude Code PostToolUse hook(集成约束形态一)与 git pre-commit(形态三),见 `githooks/pre-commit` |
| md-ref-scan.py | skills 树交叉引用断链扫描(PEP 723 自包含,零依赖) | git pre-commit;文档结构大改后必跑 |

> md-guard 为薄适配不带 PEP 723 头(需项目环境导入 project_evo),仓外等价命令 `project-evo scan <path>`;md-ref-scan 自包含可直接 `uv run --script`。
> 来历:禁字二犯升格(第十八批,集成约束四形态);断链检查手拼二犯升格(第二十五批,沉淀铁律)。
