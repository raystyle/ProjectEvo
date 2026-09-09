# secret-scan

密钥与隐私扫描插件。核心 skill 为 `secrets`(显示 `secret-scan:secrets`)。

用 PEP 723 零依赖 Python 扫本地工作区、git 全历史;可选 `gh` 读 GitHub Secret Scanning 告警、当前树 code search;完整远程历史须显式裸克隆。

## 安装

市场已加 `raystyle/ProjectEvo` 后:

```text
/plugin install secret-scan@projectevo
```

Codex:`codex plugin add secret-scan@projectevo`;Grok:`grok plugin install secret-scan@projectevo --trust`;Kimi(无市场):拷 `skills/secrets/` 整目录至 `~/.kimi/skills/`。

## 用法

```powershell
uv run plugins/secret-scan/skills/secrets/scripts/scan.py
uv run plugins/secret-scan/skills/secrets/scripts/scan.py --github owner/repo --no-cwd
```

入口 `skills/secrets/SKILL.md`。选型见仓内 `docs/research/S005-git密钥隐私扫描skill选型.md`。
