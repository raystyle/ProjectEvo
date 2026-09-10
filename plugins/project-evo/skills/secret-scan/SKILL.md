---
name: secret-scan
description: >-
  扫描 git 仓库与 GitHub 历史中的密钥、密码、Token、私钥与可选隐私字段。uv 运行 PEP 723 零依赖 Python:
  工作区、git log 全历史、gh secret-scanning alerts、gh search code;可选裸克隆再扫历史。
  Use when 密钥泄露、密码入库、token 扫描、隐私扫描、git history secret、gitleaks 替代、
  GitHub secret scanning、.env 提交、凭据轮换。
compatibility: 需 Python >=3.12 或 uv;GitHub 面需 gh 已登录
---

# secret-scan - 密钥与隐私扫描

本文件只做意图路由与命令面。规则在 `scripts/rules.py`，GitHub 细节在 `references/github.md`，处置在 `references/remediate.md`。

## 一、何时用

本地仓疑似提交过密钥、要挖已删除提交、或要对 `owner/repo` 做 GitHub 侧告警/当前树检索。文档禁字仍走 `project-evo:scan`。

## 二、命令

脚本:`plugins/project-evo/skills/secret-scan/scripts/scan.py`

```powershell
uv run <脚本> [目标项目]                  # 工作区 + 本地 git 全历史
uv run <脚本> [目标项目] --no-history     # 只扫工作区
uv run <脚本> --pii                       # 加扫邮箱与大陆手机号(误报多)
uv run <脚本> --github owner/repo --no-cwd
uv run <脚本> --github owner/repo --clone-history --no-cwd
uv run <脚本> --json
```

退出码:0 干净 / 1 有发现 / 2 出错。白名单:`SECRET_SCAN_ALLOW="正则;正则"`。

`--clone-history` 会 `gh repo clone -- --bare` 到 `%TEMP%\pevo-secrets\`，仓大时先问用户。禁止默认克隆。

## 三、三层 GitHub

| 层 | 开关 | 覆盖 |
| --- | --- | --- |
| 平台告警 | `--github` | Secret Scanning alerts;未开或无权限则 SKIP |
| 当前树检索 | `--github` | `gh search code` 已知前缀;漏已删文件 |
| 完整历史 | `--clone-history` 或本地已 fetch 的 git 仓 | `git log -p --all` |

本地已是该远程的 clone 时,`git fetch --all` 后扫本地历史即可,不必再 clone。

## 四、报告纪律

- 片段脱敏,禁止把完整密钥写进 issue、diary、研究笔记
- HIGH:先轮换再清史(见 `references/remediate.md`)
- 不做对第三方的活密钥探测

选型依据:`docs/research/S005-git密钥隐私扫描skill选型.md`。A/B 夹具:`verification/ab-cases.md`；实跑回填 `docs/research/S006-secret-scan-AB对照.md`。

```powershell
uv run plugins/project-evo/skills/secret-scan/scripts/ab.py
```
