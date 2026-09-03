# ProjectEvo

> 一句话定位:project-evo skill 的开发与维护仓——一个渐进知识库型 Agent skill,指导为项目建立需求驱动、留痕沉淀、持续进化的文档体系(四原语 + docs 六目录 + 五步工作流),按意图路由检索内置 references,定位内容不需要读全文。

## 快速开始

```powershell
# 1. 看 skill 本体(意图路由入口,18 行意图→参考表)
Get-Content skills\project-evo\SKILL.md

# 2. 检索参考(rg 定位文件 + mq 提取结构)
rg --files skills\project-evo\references | rg release
reader query skills\project-evo\references\base-primitives.md ".h2"

# 3. 用配套 CLI 安装骨架 / 诊断合规(uv 运行时,零依赖)
uv run project-evo init <目标项目> --name <项目名>     # 安装文档骨架(幂等不覆盖)
uv run project-evo check <目标项目>                    # 诊断 PE-01 至 PE-13(退出码 0/1/2)
# 等价 PowerShell 用例集:skills\project-evo\verification\command-test-cases.md

# 4. 项目级安装 skill 到目标项目(唯一安装通道;重装即更新)
uv run project-evo skill <目标项目>                  # 双落位 .claude/skills/ 与通用 .agents/skills/,agent 目录按惯例 gitignore
```

## 目录结构

```text
ProjectEvo/
  skills/project-evo/          唯一交付 skill 源(安装通道 = project-evo skill 命令)
    SKILL.md                   意图路由 + 体系速览 + 知识库检索法
    references/                分类扁平知识库 17 篇(前缀 base/flow/env/tool/exp)
    verification/              骨架规范检查命令(PE-01 至 PE-13,参数化目标项目)
  src/project_evo/             uv Python 工具(init/check/skill/llms;data/skill 内嵌全树受双漂移守卫)
  tests/                       pytest 11 测(含 skill 树漂移守卫、双落位安装、版本序与离线容错)
  pyproject.toml               uv 项目定义(零运行时依赖)
  docs/
    README.md                  文档地图(全部文档导航)
  AGENTS.md                    协作规则唯一权威源(硬规范/仓库地图/硬规则)
  CLAUDE.md                    一行 @AGENTS.md 桥接
  CHANGELOG.md                 变更日志(版本级里程碑粒度)
  ROADMAP.md                   阶段与里程碑状态
```

## 核心概念

- **渐进知识库**:SKILL.md 只做意图路由与速览;完整知识在 references,按「rg 定位文件名 + mq 提取节/代码块」渐进检索
- **三层检索接口**:目录名定类别、文件名定主题(类别前缀 + 主题词)、标题定节(h2 一节一事)
- **四原语**:PRD 要什么 / GOAL 要达成什么 / PLAN 怎么做 / TODO 做到哪;需求经追问链澄清,禁止静默假设
- **docs 六目录**:proven(完全成功的 plan 方案归档)/ diary / research / references(现役流程)/ guide(规范禁令)/ mistakes;分界口诀:方案进 proven、流程进 references、禁令进 guide
- **五步工作流**:登记 → 立项 → 执行 → 验收 → 归档;过程内自修正闭环,一次只推进一个目标
- **六态标记**:事实断言必标 [实证/推断/经验/记忆/假设/直觉];没验证不得写成已验证

## 常用命令

```powershell
# 检索(只读)
rg -n "<关键词>" skills\project-evo\references\README.md   # 索引导航
rg -n "<关键词>" skills\project-evo\references\            # 全文搜
reader query <文件> ".h2"                                   # 抽节目录(mq)
reader query <文件> ".code"                                 # 只抽命令块

# 诊断(对目标项目只读;退出码 0/1/2)
uv run project-evo check <目标项目>
# 等价 PowerShell 用例集:skills\project-evo\verification\command-test-cases.md

# 项目级安装(双落位 .claude/skills/ 与 .agents/skills/;重装即更新)
uv run project-evo skill <目标项目>

# 升级(参考 browser-harness 方式)
uv tool install git+https://github.com/raystyle/ProjectEvo   # 部署:git 直装(bh 同款)
uv run project-evo update -y            # git 模式:干净仓 ff-only pull;安装态:uv tool install --upgrade git+ 源
#                                        版本探测走 GitHub Releases,离线容错;PEVO_REPO/PEVO_GIT 环境变量可覆盖目标
```

## 文档导航

| 文档 | 讲什么 | 何时看 |
|------|--------|--------|
| `AGENTS.md` | 开发协作规则唯一权威源 | 写/改任何文件前 |
| `skills/project-evo/SKILL.md` | skill 本体(意图路由) | 使用/修改 skill 前 |
| `skills/project-evo/references/README.md` | 参考知识库渐进索引 | 找参考文档时先看 |
| `skills/project-evo/verification/command-test-cases.md` | 骨架规范检查命令 | 验证目标项目合规时 |
| `docs/README.md` | 全仓文档地图 | 找任何文档时 |
| `ROADMAP.md` | 阶段与里程碑状态 | 看进度时 |
| `CHANGELOG.md` | 变更日志 | 查历史时 |

## 环境前提

- skill 本体纯 Markdown,无运行时依赖;配套 CLI 零第三方依赖;部署 `uv tool install git+https://github.com/raystyle/ProjectEvo`(bh 同款 git 直装),升级走 `project-evo update`
- 检索与验证命令:PowerShell 7.6.5 实测;ripgrep 15.2.0 实测;reader 0.4.0 实测(mq 提取)
- 平台:Windows 主开发;文档与用例按三平台适配撰写(见 references/env-platform.md)
