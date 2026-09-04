# ProjectEvo 开发协作规则

> project-evo skill 开发规范。

> 唯一权威源。`CLAUDE.md` 仅一行 `@AGENTS.md` 桥接，不重复维护。
> 本仓库规范以 [agentskills 官方 spec](https://agentskills.io/specification) 为**硬标准**。

## 一、SKILL 硬性规范

> 以 agentskills 官方 spec 为硬标准。

evo 是一个 skill 目录（位于 `plugins/project-evo/skills/`），至少含一个 `SKILL.md`（YAML frontmatter + Markdown 正文）。

### frontmatter 字段

| 字段 | 是否必填 | 约束 |
|------|------|------|
| `name` | 必填 | ≤64 字符；小写字母/数字/连字符；**必须与目录名一致**（`evo`) |
| `description` | 必填 | 1-1024 字符；「做什么 + 何时用」兼具；含触发关键词 |
| `license` / `compatibility` / `metadata` / `allowed-tools` | 可选 | 见官方 spec |
| `version` / `argument-hint` 等非官方字段 | **禁止** | 版本由 git tag / release 管理 |

### 正文与目录

- `SKILL.md` ≤500 行；只留**原语概览 + 详细参考入口**；详细操作移 `references/`
- 标准布局：`SKILL.md`（意图路由+速览） + `references/`（分类+扁平，前缀分组） + `verification/`（命令行为）；无 evals 层（渐进知识库型 skill，不做用例评估）
- **分层原则**：SKILL.md 只留原语概览；references/ 每篇一主题自包含完整参考；实现代码唯一来源是插件内 `skills/evo/scripts/`（PEP 723 零依赖；禁字规则唯一权威 `mdrules.py`，check PE-12/scan/md-guard 三面同源）

### 写作约束

- **禁止 emoji**；流程图用 mermaid，禁止 box-drawing 手拼伪流程图
- 事实性断言标六态：`[实证]/[推断]/[经验]/[记忆]/[假设]/[直觉]`
- 中文为主；命令/代码/专有名词保原文

## 二、仓库地图

```
ProjectEvo/
├── .claude-plugin/marketplace.json   # Claude Code 市场清单
├── .agents/plugins/marketplace.json  # Codex 市场清单
├── plugins/
│   └── project-evo/     # 唯一交付插件:项目进化(结构源仓 文档骨架)
│       ├── .claude-plugin/plugin.json   # Claude manifest
│       ├── .codex-plugin/plugin.json    # Codex manifest(与 Claude 面字段同步,测试守卫)
│       ├── README.md    # 插件说明(状态/前置/安装/用法/敏感产物/发布)
│       ├── commands/    # 斜杠命令 init|check|scan(Claude 面)
│       ├── hooks/       # hooks.json:PostToolUse md 禁字挡板(Claude 面)
│       └── skills/evo/
│           ├── SKILL.md     # 意图路由 + 体系速览 + 知识库检索方法
│           ├── references/  # 分类扁平参考目录(前缀分组 21 篇,README 渐进索引路由)
│           ├── verification/# 命令行为验证用例(规范检查命令,参数化 ProjectRoot)
│           ├── assets/templates/  # 骨架模板(scripts/init.py 渲染源)
│           └── scripts/   # init/check/scan/md-guard/mdrules(PEP 723 零依赖)
├── .tools/              # uv 运行时门禁脚本(md-ref-scan:断链扫描)
├── githooks/            # git 提交钩子(pre-commit 挡板,形态三;git config core.hooksPath githooks)
├── tests/               # pytest(脚本行为 + 清单一致性守卫 + 仓内禁字回归)
├── pyproject.toml       # 维护环境定义(pytest;package=false,不分发)
├── docs/                # 本仓库自身文档(地图见 docs/README.md)
├── AGENTS.md            # 本文件:唯一权威源(硬规则+地图+索引)
├── CLAUDE.md            # 一行 @AGENTS.md
├── CHANGELOG.md         # 变更日志([Unreleased] 起步)
├── ROADMAP.md           # 路线图(阶段/里程碑/状态)
├── README.md            # 标准入口
```

> skill 源码唯一位置是 `plugins/project-evo/skills/evo/`；分发走插件市场（根双清单 + 插件双 manifest），无内嵌副本（双漂移守卫已随单源化取消，清单一致性守卫接棒）。

## 三、文档索引

> 去哪里找什么。

| 文档 | 讲什么 | 何时看 |
|------|--------|--------|
| `plugins/project-evo/skills/evo/SKILL.md` | skill 本体概览 | 使用/修改 skill 前 |
| `plugins/project-evo/skills/evo/references/README.md` | 参考知识体系渐进索引（快速路由到场景到全量） | 找参考文档时 |
| `plugins/project-evo/skills/evo/verification/command-test-cases.md` | 规范检查命令 | 验证某项目是否符合骨架 |
| `docs/README.md` | 文档地图 | 找文档时 |
| `ROADMAP.md` | 阶段与里程碑状态 | 看进度时 |
| `CHANGELOG.md` | 变更日志 | 查历史时 |

## 四、硬规则速查

> 每条硬规则带六态来源标注。

1. **单一权威源**：skill 内容只在 `plugins/project-evo/skills/evo/` 维护；引用其项目的文档体系规则以该 skill 为准，本文件不重复。[经验： 双份漂移踩坑]
2. **proven 语义**：proven = **完全成功的 plan 方案归档**（立项建方案、完成回填），不是里程碑/成果列表，用户 2026-09-03 明确裁定，写入 skill。[经验： 用户纠正]
3. **双层机器可读**：目录与文件名以 rg 检索为先（类别前缀+主题词）；文档内部结构以 mq 提取为先（标题层级/代码块/表格）。[经验： 用户裁定 2026-09-03]
4. **变更完整性**：只改 skill 不同步 SKILL.md 索引/references/CHANGELOG = 变更不完整。[经验]
5. **禁止 emoji**;mermaid 画流程图。[经验： 渲染错乱踩坑]
6. **先读文档再执行**：操作前先查 references/索引，禁止凭记忆重写删减版。[经验： 「文档在、执行者没查」踩坑]
7. **吸收即提炼**：外部信源与家族实践进库前剔除无用与冗余，只留最准确精练的可复用表达；新增不是堆料，每篇自省可再删。[经验： 用户裁定 2026-09-04]

## 五、环境事实

- 平台：Windows · PowerShell 7（禁 powershell.exe 5.1 与 cmd）
- skill 提炼源：D：\reader 仓、D：\PVE 仓、浏览器工具仓（家族骨架三仓）
- 当前阶段：v0.2.0 插件市场形态（2026-09-04 转型，第二十八批；SpecterOps/skills 组织形式既证模式）；部署 = Claude Code `/plugin marketplace add raystyle/ProjectEvo` 或 Codex `codex plugin marketplace add raystyle/ProjectEvo`；旧 `uv tool install` 通道已退役
- 项目状态与待办见 `ROADMAP.md`，不再在本文维护
