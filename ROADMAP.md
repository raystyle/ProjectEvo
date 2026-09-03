# Roadmap

阶段与里程碑状态。四态:未开始 / 进行中 / 已完成 / 挂起。随进展翻转,详细历史见 `CHANGELOG.md`。

## 阶段一:skill 成型(进行中)

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| 三仓文档体系提炼(家族骨架) | 已完成 | reader 仓 / PVE 仓 / browser-harness 调研归纳 [实证: 2026-09-03 三仓实地核对] |
| skill 单文件版(project-docs) | 已完成 | 已被三层布局版取代 |
| skill 规范仓 结构重构(project-evo) | 已完成 | 初版 SKILL + references/{howto,pitfalls} + verification + evals;后续演进为意图路由 SKILL + 分类扁平 references(前缀分组)并移除 evals(见 CHANGELOG 第六/七批) [实证: 2026-09-03] |
| verification 命令自验全绿 | 已完成 | PowerShell 用例集 + Python check 双实现,脚手架产物 11 PASS/0 FAIL 实测 |
| uv Python 工具成型 | 已完成 | project-evo init/check/llms/skill;7 测全绿;v0.1.0 定版 |
| 真实项目试跑(第一个用户) | 未开始 | 找一个新项目按 skill 初始化,回填 pitfalls |

## 阶段二:打磨与安装(未开始)

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| git init + 首版 tag + 远端发布 | 已完成 | 2026-09-03:公开仓 raystyle/ProjectEvo,main + v0.1.0 tag 已推,Release 已发;update 版本探测闭环实测(已是最新,exit 0)[实证] |
| 项目级安装通道验证 | 进行中 | project-evo skill 命令已实现;找真实项目首装实测 |
| 与 skill 规范仓 `project` skill 的分工说明 | 未开始 | project=元文件/文档四类规范;project-evo=结构源仓 全骨架与工作流,互补关系写清 |

## 阶段三:延伸(未开始)

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| scripts/ 沉淀 | 未开始 | 骨架生成若手拼 ≥2 次,升级为可执行脚手架脚本(沉淀铁律) |
| 断链扫描工具适配 | 未开始 | 参考 reader 仓 `.tools/md-ref-scan.py` 模式 |
