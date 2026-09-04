# project-evo

项目进化插件:为项目建立需求驱动、留痕沉淀、持续进化的文档体系(家族骨架)。

状态:active。支持客户端:Claude Code 与 Codex。

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

本地开发(两客户端同款,路径换本地仓根)。

## 用法

安装插件后,skill `project-evo` 按意图路由自动触发;也可用斜杠命令(Claude Code 面):

- `/project-evo:init <目标项目> [--name 项目名]` 安装文档骨架(幂等,不覆盖已有)
- `/project-evo:check [目标项目]` 诊断骨架合规 PE-01 至 PE-13(只读,退出码 0/1/2)
- `/project-evo:scan [目标项目] [--no-history]` 安全与规范扫描(token/密钥/隐私 + markdown 禁字)

脚本可独立调用(免插件):

```bash
uv run skills/project-evo/scripts/init.py <目标项目> --name <项目名>
uv run skills/project-evo/scripts/check.py [目标项目]
uv run skills/project-evo/scripts/scan.py [目标项目] --no-history
```

示例提示词:「用 project-evo 为这个项目初始化文档骨架」「check 一下这个项目符不符合骨架」。

## 输出

- init:目标项目根下 AGENTS/PRD/GOAL/PLAN/TODO/INDEX + docs 六目录 + guide 模板(已有文件跳过)
- check:PE-01 至 PE-13 逐项 PASS/FAIL/SKIP 与结论行
- scan:按严重级排序的发现清单(文件:行 + 脱敏片段 + 首见提交)

## 架构

skill 为渐进知识库:SKILL.md 只做意图路由与体系速览,完整知识在 `skills/project-evo/references/`(分类扁平,前缀 base/flow/env/tool/exp 分组,rg 定位 + 结构提取渐进检索)。可执行面在 `skills/project-evo/scripts/`(规则唯一权威 `mdrules.py`,check 的 PE-12 与 scan、md-guard 同源);模板在 `assets/templates/`。PostToolUse hook(`hooks/hooks.json`)对编辑中的 markdown 做四类禁字会话内提醒。

## 敏感产物

scan 的白名单走目标项目环境变量 `PEVO_SCAN_ALLOW`(分号分隔正则,匹配 文件:行 规则);测试夹具等已知误报在此豁免,不改动扫描规则本身。

## 支持与发布

- 支持:[raystyle/ProjectEvo issues](https://github.com/raystyle/ProjectEvo/issues)
- 当前发布:0.2.0
