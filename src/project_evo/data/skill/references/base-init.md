# 初始化流程：在目标项目落地骨架

> 五步执行指南 + 裁剪原则 + 验收清单 + 跨项目适配。在目标项目执行 project-evo 时照此走。

## Step 1：判断项目状态

- **空项目/新项目** 到 全量骨架（Step 3 最小集起步）
- **已有项目补文档** 到 先盘点现有文档（README/docs/wiki/issue），问清：哪些保留、哪些迁移、哪些废弃；现有内容按六目录分界归类安置，**不推倒重来**
- 判断依据：git 历史、现有文档规模、团队协作约定

## Step 2：问关键问题（禁止静默假设）

| 问题 | 用途 |
| --- | --- |
| 项目一句话定位是什么？ | 写进 AGENTS 项目定位段（本质/边界/交互对象） |
| 技术栈与形态？（CLI/服务/库/前端） | 决定 tests 分层规范、CI 门禁选型、目录树代码区 |
| **目标平台矩阵？**（仅 Windows / 三平台 / 特定 OS） | 决定 CI 矩阵、脚本载体、行尾策略（详见 env-platform.md) |
| 交互对象是谁？（agent-native 工具？人？） | agent-native 需根 SKILL.md 与稳定输出契约 |
| 有没有研究/选型场景？ | 无则 research/ 与 poc/ 缓建 |
| 文档语言与 lint 工具偏好？ | 中文为主？rumdl/markdownlint? |

追问链模式：一次问清一批，逐条澄清后才动手；用户的裁定记进 PRD 澄清轮次。

## Step 3：生成骨架（最小可用集）

1. **根六件**：`AGENTS.md` `PRD.md` `GOAL.md` `PLAN.md` `TODO.md` `INDEX.md`
   - 模板头见 `base-primitives.md`；AGENTS 填入本项目定位与文档义务表
   - `CLAUDE.md` 一行 `@AGENTS.md`
2. **docs 六目录** + `docs\guide\template.md`（方案模板）+ 初始 G001（文档标准细则：命名/写作/检查，内容见 `base-writing-standards.md`）
3. `CHANGELOG.md`（`[Unreleased]` 起步）、`ROADMAP.md`（阶段四态）；README 缺则一并建
4. **首条需求 D01 登记**（通常是「建立文档体系」本身），GOAL 起点写明发起日期与原因，PRD 与 GOAL 互指
5. 按项目类型追加：agent-native 工具加根 `SKILL.md`；有脚本积累建 `.tools\` + README；有研究规划建 `poc\` + README 登记表

**agent-native CLI 的 SKILL.md 模式**（browser-harness / 两仓同款）：「何时用」（什么场景一律走本 CLI，不裸调 API 不手拼 curl）+ 命令全表指向 R 文档（唯一权威）+ **管道代码逃生舱**（无参 + 管道即执行，如 `@'...TS 片段...'@ | omc`；helper 双通道：全量命名空间 + 顶层解包常用名）+ 可复用脚本 apps 目录约定 [经验： 云 CLI 仓 SKILL.md 明示参照 browser-harness 模式]

**存量仓接入的迁移路径**（虚拟化仓实证，08-03 老工程仓反向接入体系）：旧目录改名归位（`plans` 到 `proven`）到 research 补 S 编号 到 AGENTS 四段重写 到 六态补标 到 全仓引用字面替换 到 文档门禁接入。不推倒重来，逐件迁移逐件对账 [实证： 虚拟化仓 迁移提交序列 d269c9c / 1ba5119 / 0bd9843]

## Step 4：裁剪原则

- 最小集 = 六原语 + docs 六目录 + template + G001；**其余按需生长，不一次建全**
- 小型/短期项目可合并：PRD+GOAL 可先合流（文件头注明），diary 可选
- **轻量变体是合法形态**（实证样本：ome 源仓 = 三原语无 PRD、无 proven 目录、references 编号平移留洞加注记），裁剪后在 INDEX 注明裁剪决定即可，不必补齐全套
- **禁止为凑结构建空文档**：每个文件建立时必须有真实初始内容（哪怕是首条需求）
- 已有团队约定（如 CONTRIBUTING、ADR）保留原位，在 INDEX 登记并写明与本体系的关系

## Step 5：验收清单

- [ ] 每份新文档已登记 INDEX 对应节，编号无冲突、无跳号
- [ ] 文件名即标题，无括号/空格/冒号
- [ ] AGENTS 含：项目定位三段 + 文档义务表（按本项目裁剪）
- [ ] PRD D01 与 GOAL 起点互相回指
- [ ] 仓内引用无断链（有扫描脚本则跑；无则人工抽查 INDEX 链接）
- [ ] 平台矩阵决策落地：单平台项目 AGENTS 注明；跨平台项目 `.gitattributes` 钉行尾、CI 三系统矩阵起步（见 env-platform.md)
- [ ] diary 记录初始化当天一笔
- [ ] （可选）`git init` + 首提交；`.gitignore` 三类齐全（智能体配置/密钥/衍生垃圾）

## 跨项目适配参考（三个实证样本）

| 来源项目 | 形态 | 特有增量 |
| --- | --- | --- |
| reader 仓 | Rust CLI(agent-native） | 根 SKILL.md 由 `reader skill` 生成 + 双漂移守卫；六层测试体系规范（G006）;`.tools\` md 门禁四件；`poc\` S 编号登记表 |
| PVE 仓 | Python（基础设施 harness) | references 增「意图路由」（需求意图到命令面映射）；research 混硬件调研（S001 硬件选型） |
| browser-harness | Python CLI + daemon | skill 双入口（SKILL.md + `--llms` 紧凑索引）；插件开发规范；agent-workspace 约定 |

适配原则：**结构照搬、内容重写、门禁选配**。每个项目的 AGENTS 边界段必须是该项目自己的定位，禁止样本仓原文照抄。

## 初始化之后（首次运转）

1. 第一个真实需求走完整五步（登记到立项到执行到验收到归档），验证体系转得动
2. 第一次踩坑当场落 mistakes，这是体系可信度的第一块试金石
3. 一周后回看：哪些文档没人写、哪些规则守不住，裁剪或降级，再固化进 guide
