# ProjectEvo

> 一句话定位：ProjectEvo 插件市场仓。四插件：`project-evo`（文档骨架 skill `docs-evo`）、`super-research`（资料检索 skill `research`）、`secret-scan`（密钥隐私扫描 skill `secrets`）、`office-pro`（OfficeCLI 专业面 skill `office`）。

## 安装

市场名 `projectevo`，源 `raystyle/ProjectEvo`；四个插件在任意客户端同名安装：`project-evo` / `super-research` / `secret-scan` / `office-pro`。

### Claude Code（推荐）

```text
/plugin marketplace add raystyle/ProjectEvo
/plugin install project-evo@projectevo
/plugin install super-research@projectevo
/plugin install secret-scan@projectevo
/plugin install office-pro@projectevo
```

得到 skill 本体、斜杠命令与 PostToolUse md 禁字挡板。

### Codex

```bash
codex plugin marketplace add raystyle/ProjectEvo
codex plugin add project-evo@projectevo        # 其余插件同名替换
```

也可在 Codex 的 `/plugins` 界面安装。

### Grok

```bash
grok plugin marketplace add raystyle/ProjectEvo
grok plugin install project-evo@projectevo --trust    # 其余插件同名替换
```

升级：`grok plugin marketplace update` 后 `grok plugin update`。读 Claude manifest 面，无需单独 manifest [实证: 2026-09-09 本机 grok 1.0.13 四插件装齐]。

### Kimi（无插件市场）

Kimi 只认 skills 目录（`~/.kimi-code/config.toml` 的 `extra_skill_dirs` 指向 `~/.kimi/skills`），把仓内 `plugins\<插件>\skills\<skill>` 整目录拷进去：

```powershell
Copy-Item D:\ProjectEvo\plugins\*\skills\* ~\.kimi\skills\ -Recurse
```

只有 skill 本体；斜杠命令与 hooks 不随行，插件改版后手动重拷。

### 本地开发与裸脚本

- 本地市场（开发态，指向工作树，改动即生效，免推送）：各客户端把 `marketplace add` 的源换成仓根路径，如 `/plugin marketplace add D:\ProjectEvo`
- 裸脚本（任何环境，免插件免客户端，PEP 723 零依赖）：见下文使用示例的等价命令

### 协议与钉版

- 市场客户端都收 HTTPS 与 SSH git URL；GitHub 简写默认协议相反：Claude Code 走 SSH（`CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` 切 HTTPS），Codex 走 HTTPS；Grok install 另收本地路径，支持 `@ref` 与 `#subdir`
- 钉版：Claude Code `raystyle/ProjectEvo@v0.2.3` 或 URL 尾 `#v0.2.3`；Codex `--ref v0.2.3`
- 私有仓认证走标准 git 凭据（credential helper 或 ssh-agent），与终端 git 行为一致

## 使用示例

安装后 skill 按意图路由自动触发；斜杠命令与裸脚本为等价入口（裸脚本在仓根运行，路径按需替换）。

### 文档骨架（project-evo:docs-evo）

对 agent 说：「用 project-evo 为这个项目初始化文档骨架」「check 一下这个项目符不符合骨架」。

```powershell
uv run plugins/project-evo/skills/docs-evo/scripts/init.py <目标项目> --name <项目名>   # 安装骨架(幂等,不覆盖已有)
uv run plugins/project-evo/skills/docs-evo/scripts/check.py <目标项目>                  # 诊断 PE-01 至 PE-13(只读)
uv run plugins/project-evo/skills/docs-evo/scripts/scan.py <目标项目> [--no-history]    # secrets + md 禁字扫描
```

Claude Code 斜杠命令：`/project-evo:init`、`/project-evo:check`、`/project-evo:scan`。init 后目标项目得到 AGENTS/PRD/GOAL/PLAN/TODO/INDEX 根原语与 docs 六目录；等价用例集见 `plugins\project-evo\skills\docs-evo\verification\command-test-cases.md`。

### 资料检索（super-research:research）

对 agent 说：「搜一下 agent skills 规范的论文和近期文章」「用 aria2c 下这个 pdf 再用 reader 抽要点」。管线覆盖 gh 代码与仓库搜索、Google/Medium 网页、X 本地库、aria2c 下载、reader 抽取；结论落目标项目 `docs/research` 并标六态。

### 密钥扫描（secret-scan:secrets）

对 agent 说：「扫一下这个仓有没有密钥泄露，含 git 历史」。

```powershell
uv run plugins/secret-scan/skills/secrets/scripts/scan.py                               # 工作区 + git 全历史
uv run plugins/secret-scan/skills/secrets/scripts/scan.py --github owner/repo --no-cwd  # GitHub 告警与 code search
```

误报豁免走目标项目环境变量 `PEVO_SCAN_ALLOW`（分号分隔正则，匹配 文件:行）。

### Office 读写（office-pro:office）

对 agent 说：「把这份 pptx 第 3 页标题改掉并居中」「核对稿面数字与官方页一致再写入」。

```powershell
uv run plugins/office-pro/skills/office/scripts/which.py    # 定位本机 officecli
uv run plugins/office-pro/skills/office/scripts/smoke.py    # docx/xlsx/pptx 三类冒烟
```

Claude Code 斜杠命令：`/office-pro:office-cli [which|smoke]`。

## 环境前提

- skill 本体纯 Markdown；脚本零第三方依赖（PEP 723，>=3.12，`uv run` 或系统 python）
- 检索与验证命令按 PowerShell 7、ripgrep、reader 实测
- 平台：Windows 主开发；文档与用例按三平台适配撰写（`plugins/project-evo/skills/docs-evo/references/env-platform.md`）

## 文档导航

| 文档 | 讲什么 | 何时看 |
|------|--------|--------|
| `AGENTS.md` | 开发协作规则唯一权威源 | 写/改任何文件前 |
| `plugins/<插件>/README.md` | 各插件说明与安装 | 安装/分发单个插件时 |
| `plugins/project-evo/skills/docs-evo/SKILL.md` | docs-evo skill 本体（意图路由） | 使用/修改 skill 前 |
| `docs/README.md` | 全仓文档地图 | 找任何文档时 |
| `ROADMAP.md` | 阶段与里程碑状态 | 看进度时 |
| `CHANGELOG.md` | 变更日志 | 查历史时 |
