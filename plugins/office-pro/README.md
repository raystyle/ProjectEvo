# office-pro

OfficeCLI 专业面插件。核心 skill 为 `office`（显示 `office-pro:office`）。

用钉过的 GitHub 资产读写 `.docx` / `.xlsx` / `.pptx`：DOM 路径增删改查、既有稿几何纠偏、写入前事实核查。不跑官方 `install.ps1`，不 `officecli install`（会往 agent 目录喷 SKILL/MCP）。不把 `officecli.exe` 提交进 git。

选型与烟测底稿：仓内 `docs/research/S007-OfficeCLI-agent原生Office套件.md`。

## 前置

- 本机 OfficeCLI 二进制。Windows 默认 `%LOCALAPPDATA%\OfficeCLI\officecli.exe`
- 全程 `OFFICECLI_SKIP_UPDATE=1`
- 脚本 PEP 723 零依赖（`>=3.12`），`uv run` 或系统 python

## 安装

市场已加 `raystyle/ProjectEvo` 后：

```text
/plugin install office-pro@projectevo
```

Codex：在 `/plugins` 里装 `office-pro`。二进制另按 `skills/office/references/install.md` 钉资产，插件不代装。

## 用法

技能按意图路由自动触发（改 pptx/docx/xlsx、OfficeCLI、幻灯片偏位、稿面事实核查）。入口 `skills/office/SKILL.md`。

斜杠命令（Claude Code 面）：

- `/office-pro:office-cli [which|smoke]` 定位二进制或三类文件冒烟

```powershell
uv run plugins/office-pro/skills/office/scripts/which.py
uv run plugins/office-pro/skills/office/scripts/smoke.py
```
