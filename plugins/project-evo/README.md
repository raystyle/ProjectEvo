# project-evo

项目进化插件:一个插件四个 skill,即 `docs-evo` 文档骨架与治理、`super-research` 资料检索管线、`secret-scan` 密钥与隐私扫描、`office-pro` OfficeCLI 专业面。

状态:active。插件面客户端:Claude Code、Codex、Grok;纯 skills 面:Kimi 等手拷子集。

## 前置

- 无硬性运行时依赖;skill 本体纯 Markdown
- 脚本(`scripts/init.py`、`check.py`、`scan.py`)为零依赖 PEP 723 标准 Python(>=3.12),`uv run <脚本>` 或系统 `python` 均可
- `scan.py` 的 git 历史扫描需目标项目是 git 仓

## 安装

Claude Code:

```text
/plugin marketplace add raystyle/ProjectEvo
/plugin install project-evo@projectevo
```

Codex:

```bash
codex plugin marketplace add raystyle/ProjectEvo
```

Grok:

```bash
grok plugin marketplace add raystyle/ProjectEvo
grok plugin install project-evo@projectevo --trust
```

Kimi(无市场):把 `skills/` 下四个 skill 目录一并拷至 `~/.kimi/skills/`;斜杠命令与 hook 不随行。

本地开发(三客户端同款,路径换本地仓根)。

## 用法

安装插件后,四个 skill 按意图路由自动触发,客户端显示为 `project-evo:docs-evo` / `project-evo:super-research` / `project-evo:secret-scan` / `project-evo:office-pro`;也可用斜杠命令(Claude Code 面):

- `/project-evo:init <目标项目> [--name 项目名]` 安装文档骨架(幂等,不覆盖已有)
- `/project-evo:check [目标项目]` 诊断骨架合规 PE-01 至 PE-13(只读,退出码 0/1/2)
- `/project-evo:scan [目标项目] [--no-history]` 安全与规范扫描(token/密钥/隐私 + markdown 禁字)
- `/project-evo:secret-scan-cli [目标项目]` 密钥与隐私深扫(工作区 + git 全历史,GitHub 面加 `--github owner/repo`)
- `/project-evo:office-cli [which|smoke]` 定位本机 officecli 或跑 docx/xlsx/pptx 冒烟

脚本可独立调用(免插件):

```bash
uv run skills/docs-evo/scripts/init.py <目标项目> --name <项目名>
uv run skills/docs-evo/scripts/check.py [目标项目]
uv run skills/docs-evo/scripts/scan.py [目标项目] --no-history
uv run skills/secret-scan/scripts/scan.py [目标项目]
uv run skills/office-pro/scripts/which.py
```

示例提示词:「用 project-evo 为这个项目初始化文档骨架」「搜一下 agent skills 规范的论文和近期文章」「扫一下这个仓有没有密钥泄露」「把这份 pptx 第 3 页标题改掉并居中」。

## 输出

- init:目标项目根下 AGENTS/PRD/GOAL/PLAN/TODO/INDEX + docs 六目录 + guide 模板(已有文件跳过)
- check:PE-01 至 PE-13 逐项 PASS/FAIL/SKIP 与结论行
- scan:按严重级排序的发现清单(文件:行 + 脱敏片段 + 首见提交)
- secret-scan:同上口径的独立深扫(工作区 + git 全历史;GitHub alerts 与 code search),误报豁免走 `PEVO_SCAN_ALLOW`
- office-pro:which 打印本机 officecli 路径与版本;smoke 跑 docx/xlsx/pptx 三类读写冒烟

## 架构

四个 skill 都是渐进知识库:SKILL.md 只做意图路由与速览,完整知识在各自 `references/`(分类扁平,前缀 base/flow/env/tool/exp 分组,rg 定位 + 结构提取渐进检索)。可执行面:`skills/docs-evo/scripts/`(规则唯一权威 `mdrules.py`,check 的 PE-12 与 scan、md-guard 同源)、`skills/secret-scan/scripts/`、`skills/office-pro/scripts/`;模板在 `skills/docs-evo/assets/templates/`。PostToolUse hook(`hooks/hooks.json`)对编辑中的 markdown 做四类禁字会话内提醒。

## 敏感产物

scan 的白名单走目标项目环境变量 `PEVO_SCAN_ALLOW`(分号分隔正则,匹配 文件:行 规则);测试夹具等已知误报在此豁免,不改动扫描规则本身。

## 支持与发布

- 支持:[raystyle/ProjectEvo issues](https://github.com/raystyle/ProjectEvo/issues)
- 当前发布:0.3.1
