---
name: project-evo
description: >-
  项目进化(project evolution)渐进知识库:指导建立与治理项目的文档结构和规则(家族骨架),
  并以需求驱动的循环推动项目持续进化。根原语 AGENTS/PRD/GOAL/PLAN/TODO/INDEX + docs 六目录
  (proven/diary/research/references/guide/mistakes)、P/S/R/G/M/D 编号、五步工作流、六态标记（知行合一）、双向问答（你问我答拷问/我问你答咨询）、
  三平台适配、ome 环境索引、封版发布。触发后先读本文件「意图路由」定位,再渐进检索 references/。
  Use when 初始化或治理项目文档体系/骨架/结构/规范,项目进化,需求立项到归档工作流,
  或判断文档落位、平台适配、环境依赖、发版流程、agent-native CLI 契约时。
compatibility: 通用(不限语言/平台);提炼自 Rust CLI、Python 基础设施 harness、Python CLI+daemon 三类仓实践。
---

# project-evo - 项目进化指南

**渐进知识库型 skill**：本文件只做两件事，**意图路由**（你要做的事 到 该查哪篇参考）与**体系速览**（一层概览）；完整知识在 `references/` 分类扁平目录（前缀 base/flow/env/tool/exp 分组，21 篇自包含），按「rg 定位文件 + mq 提取结构」渐进检索，不要求一次读完。

核心思想：文档是项目的操作系统，需求进 PRD、目标进 GOAL、过程留痕进 diary/research、方案归档进 proven、流程沉淀进 references、规范固化进 guide、踩坑进 mistakes。做过的不重做、踩过的不再踩、验证过的直接复用。吸收即提炼，沉淀成资产；循环迭代，复利增厚。

## 一、意图路由（按意图直达参考）

> 表未覆盖的意图：跳到「二、知识库检索」用文件名/关键字搜 references/，或查 `references/README.md` 渐进索引。

| 意图 / 你要做的事 | 参考 |
| --- | --- |
| 在新项目初始化骨架 / 已有项目补文档 | `references/base-init.md` |
| 写 PRD / GOAL / PLAN / TODO / INDEX | `references/base-primitives.md` |
| 写或改 AGENTS（定位/规则/义务表） | `references/base-primitives.md` |
| 这份文档该放哪个目录（proven/references/guide 分界） | `references/base-docs-directories.md` |
| 写方案文档（PNNNN，找模板） | `references/base-docs-directories.md` |
| 推进一个目标 / 拆步骤 / 定优先级 | `references/flow-workflow.md` |
| 立项前拷问用户（你问我答）/ 被咨询时怎么答（我问你答） | `references/flow-inquiry.md` |
| 执行中发现问题，怎么就地纠偏 | `references/flow-workflow.md`（自修正闭环） |
| 写测试 / 定测试分层与门禁（单元/集成/冒烟/回归/验收） | `references/flow-testing.md` |
| 定任务执行的事件模型 / 超时兜底防卡死 | `references/flow-events.md` |
| 写任何文档前（命名/标题/六态/门禁） | `references/base-writing-standards.md` |
| 给断言打事实标记（[实证]等）/ 理解六态与知行合一 | `references/base-writing-standards.md` |
| 发一个版本（封版/tag/资产验收） | `references/flow-release.md` |
| 定平台矩阵 / shell 行尾 / CI 三系统 / 换机接管 | `references/env-platform.md` |
| 盘点环境依赖 / ome 命令 / 换机重建 | `references/env-environment.md` |
| 建项目脚本工具（.tools / uv / PEP 723) | `references/tool-project.md` |
| 找库搜代码（gh）/ 深读外来仓（git） | `references/tool-gh.md` / `references/tool-git.md` |
| 选依赖 / 查库（五栈数据源与稳度判据） | `references/tool-selection.md` |
| 给 CLI 加 agent 用户面（agent-native 契约、管道逃生舱、脚本 workspace） | `references/tool-cli-agents.md` |
| 搜引擎/抓网页 / 读本地文档 / 下资料 | `references/tool-browser-harness.md` / `references/tool-reader.md` / `references/tool-aria2c.md` |
| 落地前预警 / 疑似踩了已知坑 | `references/exp-pitfalls.md` |
| 经验往哪沉淀 / 踩坑何时升格 / 二犯配什么约束 | `references/exp-sedimentation.md` |
| 验证某项目是否符合骨架 | `verification/command-test-cases.md` |

## 二、知识库检索（rg 定位 + mq 提取）

设计原则：目录与文件名以 **rg 检索**为先（类别前缀 base/flow/env/tool/exp + 主题词）；文档结构以 **mq 提取**为先（h2=节、code=命令、表格=键值）。

```powershell
# 1 文件名:类别词或主题词直接命中(flow-release / env-platform / tool-gh …)
rg --files references | rg 关键词

# 2 索引:先查渐进索引拿候选
rg -n "关键词" references\README.md

# 3 全文:结构关键字直搜(proven/references/guide/六态/封版/pin/PATH…)
rg -n "关键词" references\

# 4 结构化提取:进文件后按节/代码块抽取,不整篇读
reader query references\base-primitives.md ".h2"      # 节导航
reader query references\tool-aria2c.md ".code"        # 只要命令
```

检索原则：先窄后宽（文件名到索引到正文）；命中多篇时以 README 场景分组定主从；进文件先 `.h2` 抽目录再定点读。

## 三、体系速览（一层概览，细节均在 references)

### 体系骨架（七层环扣）

| 层 | 承载件 | 衔接 |
| --- | --- | --- |
| 认知 | 六态（base-writing-standards）+ 知行合一（flow-workflow 三节） | 知行合一给方向，六态给状态；实证与经验循环 |
| 对话 | 双向问答（flow-inquiry） | 你问我答收决策入 PRD，我问你答核知识出 S 文档 |
| 流程 | 五步工作流与最小实现阶梯（flow-workflow） | 登记到归档主线；阶梯管写码前，探查是其落地 |
| 探查 | 依赖选型（tool-selection）+ 五工具管线（tool-\*） | 阶梯 2 到 5 档的数据源与稳度判据 |
| 执行 | 事件三态与超时兜底（flow-events） | 任务运行模型；未知必处置，反馈即事件 |
| 验证 | 测试双轴与门禁（flow-testing）+ verification PE 检查 | 反馈的工程化；测试绿是实证最强依据 |
| 沉淀 | 经验分治与集成约束（exp-sedimentation）+ exp-pitfalls | 错误反馈转资产；二犯升格并配机器约束 |

环的传动：执行产事件、验证产反馈，沉淀把反馈转资产，资产让下一轮更快（复利）；吸收即提炼是入库口径。

### 文件地图

```text
<项目根>\
  PRD.md / GOAL.md / PLAN.md / TODO.md    四原语(需求→目标→计划→进度)
  INDEX.md    唯一索引(编号表、目录结构、代码位置)
  AGENTS.md   协作规则唯一权威源(CLAUDE.md 一行桥接)
  README.md / CHANGELOG.md / ROADMAP.md / LICENSE
  SKILL.md    (仅 agent-native 工具)供 Agent 发现接入
  docs\
    proven\     PNNNN  完全成功的 plan 方案归档(封存,不再更新)
    diary\      YYYY-MM-DD-*.md  项目日记,一天一篇
    research\   SNNN   研究原型过程(为什么;六态;PoC 落 poc\)
    references\ RNNN   现役做事的流程(操作手册,持续更新)
    guide\      GNNN   做事的规范(标准与禁令)+ template.md
    mistakes\   M1xx 分类文件 / M0xx 行级条目
  .tools\      项目脚本工具(带 README 清单)
  poc\         (有研究的项目)PoC 产物,S 编号子目录
```

### 编号体系

| 前缀 | 含义 | 位数 | 目录 |
| --- | --- | --- | --- |
| `P` | proven，完全成功的 plan 方案归档 | 4 位（P0001) | `docs\proven\` |
| `S` | research，研究原型过程 | 3 位（S001） | `docs\research\` |
| `R` | references，做事的流程（现役） | 3 位（R001） | `docs\references\` |
| `G` | guide，做事的规范（标准禁令） | 3 位（G001） | `docs\guide\` |
| `M` | mistakes；M1xx=分类文件，M0xx=行级 | 全局递增 | `docs\mistakes\` |
| `D` | PRD 需求条目 | 2 位（D01） | `PRD.md` |

接当前最大号；退役编号不复用。

### 六目录分界口诀（易错）

**方案做成归档进 proven（历史）；可复用流程提炼进 references（现役）；标准禁令进 guide。**

### 五步工作流

登记（追问链澄清）到 立项（proven 建 PNNNN 方案）到 执行（留痕）到 验收（对照完成定义）到 归档（回填+diary+反哺）。一次只推进一个目标；问题不留在对话里。底层纪律知行合一：知落行、行返知（见 flow-workflow.md 第三节）。

### 六态事实标记

`[实证: ...]`（已验证，附依据）/ `[推断: ...]`（逻辑推出）/ `[经验: ...]`（历史惯例）/ `[记忆: ...]`（建议复核）/ `[假设: ...]`（待验证）/ `[直觉: ...]`（无据倾向）。关键结论必标；禁止把「没验证」写成「已验证」。五态为进入实证服务（标注写清验证路径与复核点）；实证与经验循环复利；悬空中转态收尾必处置（升实证、留 research 或注销）。

## 四、参考知识库索引

完整渐进索引（快速路由到场景到全量）见 `references/README.md`；姊妹件：`verification/command-test-cases.md`（骨架规范检查命令）。

配套脚本（`scripts/`，PEP 723 零依赖，uv run 或系统 python 直跑；模板在 `assets/templates/`）：`init.py <path> [--name 名]` 安装文档骨架（幂等）/ `check.py [path]` 诊断合规（PE-01 至 PE-13)/ `scan.py [path] [--no-history]` 安全与规范扫描；禁字规则唯一权威 `scripts/mdrules.py`（check 的 PE-12、scan、md-guard 三面同源）。安装通道：Claude Code `/plugin marketplace add raystyle/ProjectEvo` 后装 project-evo 插件（`/project-evo:*` 斜杠命令与 PostToolUse 禁字挡板随插件生效）；Codex `codex plugin marketplace add raystyle/ProjectEvo`。
