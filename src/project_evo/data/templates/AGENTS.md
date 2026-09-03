# {name}：开发协作规则

> 唯一权威源。`CLAUDE.md` 仅一行 `@AGENTS.md` 桥接，不重复维护。

## 一、项目定位

> 本项目的本质与边界。根为定位，下分本质、边界、交互对象。

1. **本质**：<一句话：本项目是什么>
2. **边界**：<做什么、不做什么、质量承诺到哪>
3. **交互对象**：<谁通过什么面使用本项目>

## 二、工作规则

> 四类场景：对话、操作、编码、文档。先列动作清单，再定规则（可以/禁止/参考）。

### 对话

- 每轮先核对四原语（PRD/GOAL/PLAN/TODO）；新需求先入 PRD 走追问链，禁止静默假设
- 一次只推进一个目标；踩坑当场落 docs/mistakes

### 操作

- Windows 用 PowerShell 7(pwsh);Linux/macOS/WSL 用该平台常规 shell
- 未经指示不做 commit/push/reset 等变更操作；提交一事一提交（fix：/feat:/docs:/chore:/test： 前缀）

### 编码

- <按本项目技术栈补充：选型细则、测试分层、脚本归档 .tools 等>

### 文档

| 动作 | 时机 | 义务 |
| --- | --- | --- |
| 新需求提出 | 提出时 | PRD 登记新行 |
| 目标立项 | 开工前 | GOAL 起点/锚点、PLAN 方案、TODO 清单 |
| 选型与调研 | 研究完成 | S 文档（六态）+ INDEX 研究节 |
| 踩坑 | 当场 | mistakes 接编一行；INDEX 错误节同步 |
| 方案达成 | 验收全绿 | proven 回填、GOAL 历史行、INDEX 归档节 |
| 每次提交 | 提交后 | diary 当天记钩子 |
| 发布 | tag 后 | CHANGELOG 封版、ROADMAP 阶段状态 |

## 三、意图路由

> 需求意图到文档/命令的映射摘要层；细则唯一权威见对应 R 文档。

- <示例：构建问题 到 docs/references/Rxxx>

## 四、资源索引

> 配合 INDEX 的搜索方法与分析路径。

```powershell
rg -n "关键词" INDEX.md
rg -n "关键词" docs\mistakes\
```
