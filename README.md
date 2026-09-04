# ProjectEvo

> 一句话定位：project-evo 插件市场仓。唯一交付 project-evo 插件：一个渐进知识库型 Agent skill，指导为项目建立需求驱动、留痕沉淀、持续进化的文档体系（根原语 + docs 六目录 + 五步工作流），按意图路由检索内置 references，附 init/check/scan 零依赖脚本与 md 禁字会话挡板。

## 快速开始

```text
# 1. Claude Code 安装(推荐通道)
/plugin marketplace add raystyle/ProjectEvo
/plugin install project-evo@projectevo
# 斜杠命令 /project-evo:init|check|scan 与 PostToolUse 禁字挡板随插件生效

# 2. Codex 安装
codex plugin marketplace add raystyle/ProjectEvo
```

脚本可独立使用(免插件,PEP 723 零依赖,uv run 或系统 python 直跑):

```powershell
uv run plugins/project-evo/skills/project-evo/scripts/init.py <目标项目> --name <项目名>   # 安装骨架(幂等不覆盖)
uv run plugins/project-evo/skills/project-evo/scripts/check.py <目标项目>                  # 诊断 PE-01 至 PE-13(退出码 0/1/2)
uv run plugins/project-evo/skills/project-evo/scripts/scan.py <目标项目> [--no-history]    # secrets + md 禁字扫描
# 等价 PowerShell 用例集:plugins\project-evo\skills\project-evo\verification\command-test-cases.md
```

## 目录结构

```text
ProjectEvo/
  .claude-plugin/marketplace.json    Claude Code 市场清单
  .agents/plugins/marketplace.json   Codex 市场清单
  plugins/project-evo/               唯一交付插件(发布单元)
    .claude-plugin/plugin.json       Claude manifest
    .codex-plugin/plugin.json        Codex manifest(字段与 Claude 面同步,受测试守卫)
    README.md                        插件说明(状态/前置/安装/用法/敏感产物/发布)
    commands/                        斜杠命令 init|check|scan(Claude 面)
    hooks/hooks.json                 PostToolUse md 禁字挡板(Claude 面)
    skills/project-evo/
      SKILL.md                       意图路由 + 体系速览 + 知识库检索法
      references/                    分类扁平知识库 21 篇(前缀 base/flow/env/tool/exp)
      verification/                  骨架规范检查命令(PE-01 至 PE-13,参数化目标项目)
      assets/templates/              骨架模板(init.py 渲染源)
      scripts/                       init/check/scan/md-guard/mdrules(PEP 723 零依赖)
  .tools/                            md-ref-scan 断链扫描(仓内维护)
  githooks/                          pre-commit 挡板(md-guard --staged + md-ref-scan)
  tests/                             pytest(脚本行为 + 清单一致性守卫 + 仓内禁字回归)
  pyproject.toml                     维护环境(pytest;package=false,不分发)
  docs/README.md                     文档地图
  AGENTS.md / CLAUDE.md / CHANGELOG.md / ROADMAP.md
```

## 核心概念

- **插件市场形态**：skill 内容 100% 双客户端共享，manifest 是薄壳；定义一次多面暴露（Claude/Codex）
- **渐进知识库**：SKILL.md 只做意图路由与速览；完整知识在 references，按「rg 定位文件名 + mq 提取节/代码块」渐进检索
- **三层检索接口**：目录名定类别、文件名定主题（类别前缀 + 主题词）、标题定节（h2 一节一事）
- **四原语**：PRD 要什么 / GOAL 要达成什么 / PLAN 怎么做 / TODO 做到哪；需求经追问链澄清，禁止静默假设
- **docs 六目录**：proven（完全成功的 plan 方案归档）/ diary / research / references（现役流程）/ guide（规范禁令）/ mistakes
- **五步工作流**：登记 到 立项 到 执行 到 验收 到 归档；一次只推进一个目标
- **六态标记**：事实断言必标 [实证/推断/经验/记忆/假设/直觉]；没验证不得写成已验证

## 常用命令

```powershell
# 检索(只读)
rg -n "<关键词>" plugins\project-evo\skills\project-evo\references\README.md   # 索引导航
rg -n "<关键词>" plugins\project-evo\skills\project-evo\references\            # 全文搜
reader query <文件> ".h2"                                                      # 抽节目录(mq)

# 诊断(对目标项目只读;退出码 0/1/2)
uv run plugins/project-evo/skills/project-evo/scripts/check.py <目标项目>

# 升级:插件通道原生管理(/plugin 或 codex plugin 面更新),或重跑 marketplace add 刷新
```

## 文档导航

| 文档 | 讲什么 | 何时看 |
|------|--------|--------|
| `AGENTS.md` | 开发协作规则唯一权威源 | 写/改任何文件前 |
| `plugins/project-evo/skills/project-evo/SKILL.md` | skill 本体（意图路由） | 使用/修改 skill 前 |
| `plugins/project-evo/skills/project-evo/references/README.md` | 参考知识库渐进索引 | 找参考文档时先看 |
| `plugins/project-evo/skills/project-evo/verification/command-test-cases.md` | 骨架规范检查命令 | 验证目标项目合规时 |
| `plugins/project-evo/README.md` | 插件说明与安装 | 安装/分发插件时 |
| `docs/README.md` | 全仓文档地图 | 找任何文档时 |
| `ROADMAP.md` | 阶段与里程碑状态 | 看进度时 |
| `CHANGELOG.md` | 变更日志 | 查历史时 |

## 环境前提

- skill 本体纯 Markdown;脚本零第三方依赖（PEP 723，>=3.12，`uv run` 或系统 python）
- 安装走各客户端插件市场（Claude Code `/plugin marketplace add raystyle/ProjectEvo`；Codex `codex plugin marketplace add raystyle/ProjectEvo`）；旧 `uv tool install` 通道自 v0.2.0 退役
- 检索与验证命令：PowerShell 7.6.5 实测；ripgrep 15.2.0 实测；reader 0.4.0 实测（mq 提取）
- 平台：Windows 主开发；文档与用例按三平台适配撰写（见 references/env-platform.md）
