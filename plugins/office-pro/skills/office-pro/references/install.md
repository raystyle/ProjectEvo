# 安装：钉资产，不喷 skill

> 本文件 = 本机怎么拿到 `officecli`。官方 `install.ps1` / `officecli install` 会探测 agent 目录并拷 SKILL/MCP，本通道故意不用。

## 钉 GitHub 资产

Windows x64 例（版本号换成当时 latest，非预发布）：

```powershell
$ver = 'v1.0.148'
$dir = Join-Path $env:TEMP 'pevo-officecli'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
aria2c -x 8 -s 8 -c -d $dir -o officecli-win-x64.exe "https://github.com/iOfficeAI/OfficeCLI/releases/download/$ver/officecli-win-x64.exe"
aria2c -x 8 -s 8 -c -d $dir -o SHA256SUMS "https://github.com/iOfficeAI/OfficeCLI/releases/download/$ver/SHA256SUMS"
Get-FileHash (Join-Path $dir 'officecli-win-x64.exe') -Algorithm SHA256
Get-Content (Join-Path $dir 'SHA256SUMS')
```

哈希必须与清单中 `officecli-win-x64.exe` 一行一致。再复制：

```powershell
$dstDir = Join-Path $env:LOCALAPPDATA 'OfficeCLI'
New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
Copy-Item (Join-Path $dir 'officecli-win-x64.exe') (Join-Path $dstDir 'officecli.exe') -Force
$env:OFFICECLI_SKIP_UPDATE = '1'
& (Join-Path $dstDir 'officecli.exe') --version
```

User PATH 追加 `$dstDir`。已启动的 agent 会话不会立刻看到裸命令 `officecli`，用绝对路径或新开终端。[实证: 2026-09-08]

定位：`uv run plugins/office-pro/skills/office-pro/scripts/which.py`

## 禁止

- 未读完就 `irm .../install.ps1 | iex`
- `officecli install`、`officecli skills`、`officecli mcp`（会喷到 `~\.claude\skills` 等）
- 把 `officecli.exe` 提交进 git

官方 Scoop / npm 通道存在，本 skill 不默认走。更新检查用 `OFFICECLI_SKIP_UPDATE=1` 关掉。

## 写文件前的锁与只读

| 现象 | 处理 |
| --- | --- |
| `IsReadOnly` | `attrib -R` 目标文件；`Copy-Item` 会继承只读 |
| `Access denied` / 被另一进程占用 | `Get-Process POWERPNT`；改副本，用户关掉 PowerPoint 后再覆盖原文件 |
| 第一次改用户稿 | 旁路备份一份再动手 |

[实证: 2026-09-08 攻击智能体 pptx 只读 + POWERPNT 锁]
