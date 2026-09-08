---
name: office
description: >-
  用 OfficeCLI 专业读写 .docx/.xlsx/.pptx：钉 GitHub 资产安装、DOM 路径增删改查、
  既有稿几何纠偏、写入前事实核查。不跑官方 install.ps1、不 officecli install 喷 skill。
  Use when Office 文档、pptx 偏位、docx xlsx 自动化、OfficeCLI、agent 改幻灯片、
  事实核查写进 PPT、钉资产安装 officecli。
compatibility: 需本机 OfficeCLI 二进制（Windows 默认 %LOCALAPPDATA%\OfficeCLI\officecli.exe）
---

# office - OfficeCLI 专业面

本文件只做意图路由与硬规则。安装、命令契约、改稿循环、事实核查分见 `references/`。选型与烟测见仓内 `docs/research/S007-OfficeCLI-agent原生Office套件.md`。

OfficeCLI 是 OpenXML CLI，不是 Microsoft Office，不要求本机装 Word/Excel/PowerPoint。[实证: S007]

## 一、何时用

改已有或新建 `.docx` / `.xlsx` / `.pptx`，且要用可脚本化、可 `--json` 的命令而不是 GUI。客户端自带的 docx/pptx 技能仍可用；本 skill 管 OfficeCLI 通道与本仓实证过的纪律。斜杠命令 `/office-pro:office-cli [which|smoke]`。

## 二、意图路由

| 你要做的事 | 入口 |
| --- | --- |
| 本机没有 `officecli` / 要升级 | `references/install.md` |
| 查命令、路径、JSON、公式、常驻 | `references/cli.md` |
| 改已有 pptx/docx/xlsx（偏位、换文案） | `references/edit.md` |
| 把调研结论写进幻灯片前 | `references/facts.md` |
| 验证本机二进制 | `verification/smoke.md` |

## 三、硬规则

1. **钉资产，不喷 skill。** 装二进制用 GitHub release + `SHA256SUMS`。禁止未读就 `install.ps1 | iex`。禁止 `officecli install` / `officecli skills` / `officecli mcp`（会往 Claude/Cursor/Codex 等目录塞 SKILL）。[实证: S007；`officecli install --help`]
2. **先备份再写。** 目标只读则 `attrib -R`。被 PowerPoint 锁住则改副本，关闭后再覆盖。
3. **PowerShell 禁止参数名 `$args`。** 改用 `$ocArgs` 再 splat，否则子命令被吃掉、只打根 help、退出 0。[实证: S007 第一轮烟测]
4. **写进稿面的数字必须能对上官方页。** 对不上就删数字或写「未复测」，禁止星级/幻觉率/靶场分无出处留在 PPT。[经验: 2026-09-08 攻击智能体稿]
5. **改完要看见。** `view screenshot --page N --render native` 核几何与溢出；非 officecli 读盘前 `save`/`close`。
6. **图片保持纵横比。** 只改 `x`/`y` 或按原比例同时改 `width`/`height`。

全程 `OFFICECLI_SKIP_UPDATE=1`。进程 PATH 未继承 User PATH 时用绝对路径。

## 四、最小命令面

```powershell
$env:OFFICECLI_SKIP_UPDATE = '1'
$bin = "$env:LOCALAPPDATA\OfficeCLI\officecli.exe"

& $bin --version
& $bin view $file outline
& $bin view $file text --page 8
& $bin query $file '*' --find '关键词' --compact
& $bin get $file '/slide[N]' --json --depth 1
& $bin query $file '/slide[N] > *' --compact --fields x,y,width,height,name
& $bin set $file '/slide[N]/shape[@id=ID]' --prop 'text=新标题'
& $bin set $file '/slide[N]/picture[@id=ID]' --prop 'x=360pt' --prop 'width=580pt' --prop 'height=295pt'
& $bin view $file screenshot --page N --render native --screenshot-width 1600 --screenshot-height 900 -o $out.png
& $bin close $file
```

定位二进制：`uv run plugins/office-pro/skills/office/scripts/which.py`

```mermaid
flowchart TD
  备份 --> 探查
  探查 --> 改
  改 --> 截图核
  截图核 -->|还有偏位或溢出| 改
  截图核 -->|干净| 关常驻
  关常驻 --> 事实扫残留
```
