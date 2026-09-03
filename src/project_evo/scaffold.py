"""init 子命令:向目标项目生成文档骨架。

模板即家族体系的最小集(四原语 + INDEX/AGENTS + docs 六目录 + 方案模板 + 初始 G001)。
纪律:已有文件一律跳过不覆盖(幂等);每份文件带真实初始内容,不产空壳。
"""

from __future__ import annotations

import datetime
from pathlib import Path

DIRS = [
    "docs/proven",
    "docs/diary",
    "docs/research",
    "docs/references",
    "docs/guide",
    "docs/mistakes",
    "poc",
]

_T = {

"AGENTS.md": """# {name}:开发协作规则

> 唯一权威源。`CLAUDE.md` 仅一行 `@AGENTS.md` 桥接,不重复维护。

## 一、项目定位

> 本项目的本质与边界。根为定位,下分本质、边界、交互对象。

1. **本质**:<一句话:本项目是什么>
2. **边界**:<做什么、不做什么、质量承诺到哪>
3. **交互对象**:<谁通过什么面使用本项目>

## 二、工作规则

> 四类场景:对话、操作、编码、文档。先列动作清单,再定规则(可以/禁止/参考)。

### 对话

- 每轮先核对四原语(PRD/GOAL/PLAN/TODO);新需求先入 PRD 走追问链,禁止静默假设
- 一次只推进一个目标;踩坑当场落 docs/mistakes

### 操作

- Windows 用 PowerShell 7(pwsh);Linux/macOS/WSL 用该平台常规 shell
- 未经指示不做 commit/push/reset 等变更操作;提交一事一提交(fix:/feat:/docs:/chore:/test: 前缀)

### 编码

- <按本项目技术栈补充:选型细则、测试分层、脚本归档 .tools 等>

### 文档

| 动作 | 时机 | 义务 |
| --- | --- | --- |
| 新需求提出 | 提出时 | PRD 登记新行 |
| 目标立项 | 开工前 | GOAL 起点/锚点、PLAN 方案、TODO 清单 |
| 选型与调研 | 研究完成 | S 文档(六态)+ INDEX 研究节 |
| 踩坑 | 当场 | mistakes 接编一行;INDEX 错误节同步 |
| 方案达成 | 验收全绿 | proven 回填、GOAL 历史行、INDEX 归档节 |
| 每次提交 | 提交后 | diary 当天记钩子 |
| 发布 | tag 后 | CHANGELOG 封版、ROADMAP 阶段状态 |

## 三、意图路由

> 需求意图到文档/命令的映射摘要层;细则唯一权威见对应 R 文档。

- <示例:构建问题 → docs/references/Rxxx>

## 四、资源索引

> 配合 INDEX 的搜索方法与分析路径。

```powershell
rg -n "关键词" INDEX.md
rg -n "关键词" docs\\mistakes\\
```
""",

"CLAUDE.md": """@AGENTS.md
""",

"PRD.md": """# PRD:需求清单管理

> 角色:需求清单,四原语之首:需求驱动目标。GOAL 的每个目标应能回指本清单条目。
> 分工:PRD=要什么;GOAL=要达成什么;PLAN=怎么做;TODO=做到哪。

## 生命周期

```text
新需求 到 待澄清 到 已澄清 到 已采纳 到 已交付
拒绝路径:任一状态 到 已拒绝(记原因防复问)
```

## 需求清单

| 编号 | 需求 | 状态 | 澄清轮次 | 派生去向 |
| --- | --- | --- | --- | --- |
| D01 | 建立项目文档体系(本骨架由 project-evo init 生成) | 已采纳 | 第 0 轮 | GOAL 起点 |
""",

"GOAL.md": """# GOAL:任务目标管理

> 角色:工作任务管理,四个部分:起点、锚点、进程、历史。随工作实时更新。

## 起点

- **日期**:{date}
- **起点**:D01 建立文档体系;骨架已由 project-evo init 生成,首个目标自定。

## 锚点

- **锚定的目标**:D01 文档体系运转(待细化)

### 推进时间线

| 日期 | 进展 |
| --- | --- |
| {date} | 骨架生成,四原语与 docs 六目录就位 |

## 进程

- 当前目标:D01(进行中)

## 历史

| 日期 | 目标 | 结果 |
| --- | --- | --- |
""",

"PLAN.md": """# PLAN:当前目标实施计划

> 角色:当前目标方案文档:基于 research(为什么)与 references(怎么做)的执行计划;每条挂依据来源,不存历史目标。

## 当前目标

D01 文档体系运转

## 完成的定义

- [ ] 第一个真实需求走完五步(登记 到 立项 到 执行 到 验收 到 归档)
- [ ] 第一次踩坑当场落 mistakes
""",

"TODO.md": """# TODO:当前目标任务进度清单

> 角色:当前目标的任务进度清单。目标完成后回填 docs/proven 对应方案,起新清单。

## 任务进度清单

| 任务项 | 进度 | 说明 | 日期 |
| --- | --- | --- | --- |
| 细化首个目标 | 未开始 | 在 GOAL 锚点登记 | |
""",

"INDEX.md": """# INDEX:项目总索引

> 角色:全仓唯一索引:只做定位。规则权威源见 AGENTS.md。

## 一、编号体系

前缀:`P`(proven,已完成方案归档,4 位);`S`(research,研究,3 位);`R`(references,现役流程,3 位);`G`(guide,规范禁令,3 位);`M`(mistakes,M1xx 分类文件、M0xx 行级)。退役编号不复用。

## 二、目录结构

| 类别 | 目录 | 说明 |
| --- | --- | --- |
| 文档 | docs(proven/diary/research/references/guide/mistakes) | 方案归档/日记/研究/流程/规范/错误 |
| 代码 | src | <按项目实际填写,逐文件职责> |

## 三、方案归档

| 编号 | 文件 | 主题 |
| --- | --- | --- |

## 四、项目日记

## 五、研究文档

| 编号 | 文件 | 主题 |
| --- | --- | --- |

## 六、references 现役流程

| 编号 | 文件 | 用途 |
| --- | --- | --- |

## 七、guide 规范

| 编号 | 文件 | 用途 |
| --- | --- | --- |
| G001 | `docs\guide\G001-文档标准细则.md` | 命名/写作/六态/门禁 |

## 八、错误速查

| 编号 | 分类文件 | 覆盖关键词 | 行级编号段 |
| --- | --- | --- | --- |

## 九、阶段与版本

- ROADMAP.md:阶段路线
- CHANGELOG.md:版本里程碑
""",

"CHANGELOG.md": """# Changelog

本文件记录可交付变更。粒度纪律:只留版本级里程碑(定位变更/发布/阶段完成/核心能力整体落地)。

## [Unreleased]
""",

"ROADMAP.md": """# Roadmap

阶段与里程碑状态。四态:未开始 / 进行中 / 已完成 / 挂起。

## 阶段一:{date} 起

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| 文档体系建立 | 已完成 | project-evo init 生成 |
| 首个目标闭环 | 未开始 | 五步走完一次 |
""",

"docs/guide/template.md": """# 方案模板:新方案文档的写作骨架

> 新方案照此写。落点:docs/proven/PNNNN-短名.md。进行中与否以 TODO.md 为准。

- 状态:草案 / 进行中 / 已完成 / 搁置
- 日期:YYYY-MM-DD
- 关联:TODO 待办项 / 相关方案 / 研究

## 背景与问题

## 目标与非目标

## 方案

## 备选方案

## 实施步骤

## 风险与回滚

## 实施过程与经验

> 完成时回填,不是留空:实际怎么做、踩了什么坑、沉淀的经验。

## 验收标准
""",

"docs/guide/G001-文档标准细则.md": """# G001:文档标准细则

> 本仓文档的命名、结构与事实标记标准(精简起步版,按需扩充)。

## 命名

- 文件名即标题;编号目录文件名以编号开头(PNNNN/SNNN/RNNN/GNNN-短名.md)
- 不含空格、括号、冒号;research/diary 用 `-` 断句的博客式长标题

## 结构

- 标题干净(不带括号/口号/破折号),解释放标题下一行 `>` 引用
- 树形分层;h2 = 一节一事;命令进代码块;关键事实用表格

## 六态标记

事实性断言必标:`[实证: ...]` / `[推断: ...]` / `[经验: ...]` / `[记忆: ...]` / `[假设: ...]` / `[直觉: ...]`。关键结论必标;禁止把没验证写成已验证。

## 登记与门禁

- 新文档建成登记 INDEX 对应节
- 建议接入 markdown lint 与断链扫描(按项目选配)
""",
}


def generate(target: Path, name: str) -> tuple[list[str], list[str]]:
    """在 target 下生成骨架。返回 (created, skipped) 相对路径列表。幂等:已有文件跳过。"""
    date = datetime.date.today().isoformat()
    created: list[str] = []
    skipped: list[str] = []
    for d in DIRS:
        (target / d).mkdir(parents=True, exist_ok=True)
    for rel, tpl in _T.items():
        path = target / rel
        if path.exists():
            skipped.append(rel)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(tpl.format(name=name, date=date), encoding="utf-8")
        created.append(rel)
    return created, skipped
