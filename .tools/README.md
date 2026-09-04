# .tools 项目脚本工具

| 脚本 | 用途 | 调用方 |
| --- | --- | --- |
| md-ref-scan.py | skills 树交叉引用断链扫描(PEP 723 自包含,零依赖) | git pre-commit;文档结构大改后必跑 |

> md 禁字门禁 md-guard.py 自第二十八批随 skill 下沉到 `plugins/project-evo/skills/project-evo/scripts/`(规则唯一权威 `mdrules.py`,与 check PE-12、scan 同源;PEP 723 自包含),由 plugin hook、`.claude/settings.json` 与 `githooks/pre-commit` 三处调用同一份。
> 来历:禁字二犯升格(第十八批,集成约束四形态);断链检查手拼二犯升格(第二十五批,沉淀铁律)。
