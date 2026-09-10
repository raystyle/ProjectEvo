# git 密钥与隐私扫描 skill 选型

- 状态:已完成
- 日期:2026-09-08
- 关联:用户要用超级研究技能调研「扫描 SKILL + uv Python 扫本地仓与 GitHub 历史」

> 本文件 = 选型依据。落地插件是 `plugins/secret-scan`（skill `secrets`）。不复述真实密钥。

## 背景

本仓 `docs-evo` 的 `scan.py` 已扫工作区 + 本地 `git log -p --all`，并混扫 markdown 禁字。用户要的是**独立扫描 skill**：密钥/密码/隐私，脚本走 uv，对象含本地仓与 GitHub 历史提交。

## 关键结论

1. **成熟引擎是 Go 二进制，不是 uv Python。** `gitleaks/gitleaks` 约 29k star、`trufflesecurity/trufflehog` 约 28k star，扫 git 历史与（TruffleHog）远程 GitHub/验证存活密钥。agent skill 市场上大量 SKILL.md 只是「去跑 gitleaks/trufflehog」的说明书。[实证: 2026-09-08 `gh search repos`]
2. **最接近「uv run scripts/scan.py」的现成 skill 是 akaihola/secrets-scan。** 它编排 `uvx detect-secrets` + npm `secretlint`，扫的是**当前 git 跟踪文件**，不是全历史，也不是 GitHub API。[实证: agent-skills.md 该 skill 正文]
3. **GitHub 历史不能靠 `gh search code` 单独完成。** code search 只索引默认分支当前树；已删提交里的密钥要 `git log -p` 或平台 Secret Scanning alerts。alerts 需仓库打开 secret scanning 且 token 有 `security_events`。[推断: 对照 GitHub 文档与本仓 docs-evo 已用 `git log -p`；alerts 权限未在本机复验]
4. **本仓应自带 PEP 723 零依赖脚本，不绑 gitleaks。** 与 docs-evo 脚本合同一致、Windows 无 brew、无 Docker。规则比 docs-evo 现网正则更全，但比 gitleaks 规则库窄；GitHub 面用 `gh api` alerts + 可选 `--clone-history` 拉裸仓再扫历史。活密钥探测（对第三方发请求）不做。[经验: 本仓 v0.2.0 零依赖门禁；用户明确 uv Python]。与 docs-evo scan 的同夹具实跑见 [S006](S006-secret-scan-AB对照.md)。
5. **报告必须脱敏。** 安全审计 skill 把 scanner snippet 写进仓内报告会二次泄露（claude-security-audit v2.6.1 踩过）。本 skill 片段只留前缀。[实证: velimattiv/claude-security-audit README]

## 现成 skill 对照

| 形态 | 代表 | 扫什么 | 运行时 | 与需求差 |
| --- | --- | --- | --- | --- |
| 说明书绑二进制 | git-secret-scanner / secrets-gitleaks / GitGuardian ggshield skill | 工作区+历史；GG 还可扫机 | gitleaks / trufflehog / ggshield | 非 uv Python；Windows 安装重 |
| uv 编排第三方 | akaihola secrets-scan | 当前跟踪文件 | `uvx detect-secrets` + secretlint | 无全历史、无 GitHub 史 |
| 进攻面 OSINT | Claude-OSINT secret_scan.py | 80 条正则 + 在线校验器 | stdlib Python | 含对外验证，超出本仓防御口径 |
| 扫 agent 会话史 | agentsweep | `~/.claude` 等 JSONL | `uv tool install` | 不是 git 仓 |
| 本仓 docs-evo scan | `skills/docs-evo/scripts/scan.py` | 工作区+本地历史+md 禁字 | PEP 723 零依赖 | 无 GitHub 面；规则少；与文档禁字绑死 |

Yelp `detect-secrets`（约 4.6k star）是 Python 熵检测，`uvx` 即跑，但历史要另接 git。GitGuardian `ggshield`（约 2k star）Python CLI，技能教 agent 先扫再修，依赖其云/CLI。

## GitHub 三层

1. **当前树**：`gh search code --repo owner/repo` 对已知前缀（`ghp_` `AKIA` 等）。漏已删文件。
2. **平台告警**：`gh api repos/owner/repo/secret-scanning/alerts`。有则最省；无私有权或未开功能则 404/403，当 SKIP 不是失败。
3. **完整历史**：`gh repo clone owner/repo -- --bare` 后对裸仓 `git log -p --all`。体积与时间随仓涨，必须显式 `--clone-history`，禁止默认克隆。

本地已是 git 远程跟踪仓时，第 3 层等于 `git fetch --all` 再扫本地历史，不必再 clone。

## 处置口径（写入 skill，不写入扫描器）

HIGH：视为已泄露，先轮换再考虑 `git filter-repo` / BFG。公开远程清史也清不掉已被爬的副本。
误报：白名单环境变量，不改规则。
不把完整密钥写进 issue、diary、研究笔记。

## 落地

插件 `secret-scan`，skill 名 `secrets`。docs-evo 的 `scan` 斜杠命令保留（文档禁字 + 浅密钥）。本 skill 专责密钥/隐私挖掘。
