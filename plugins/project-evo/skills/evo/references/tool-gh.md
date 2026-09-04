# gh - GitHub CLI 操作指南

> 定位：**搜索代码和项目仓库**（用户裁定）：找库、找实现、找用法的第一入口；亦覆盖 release 管理与全部 GitHub 操作，代替网页与裸 API curl。本机 gh 2.98.0 [实证： 2026-09-03 `gh --version`]。

## 零、代码与仓库搜索（首要场景）

### 定位决策表（按目标选命令）

| 目标 | 命令 |
| --- | --- |
| 定义处（首选） | `gh search code "<kw>" --repo <o/r> --filename "<f>" --json path,repository,sha,textMatches,url` |
| 搜仓库（选型看星/活跃/license) | `gh search repos "pdf extraction rust" --limit 10 --json fullName,stargazersCount,updatedAt,license` |
| 只知道符号 | 小项目直接关键词；大项目加 `--language`；不确定名先泛词扫目录再二次定向 |
| fork 仓库 | 内联 `"fork:true"`（`is:fork` 在 code search 无效） |
| 完整仓库元数据 | `gh api "search/code?q=<q>&per_page=<n>"`(gh search code 的 repository 裁剪仅 5 字段） |
| 变更上下文 | `gh api repos/<o>/<r>/commits/<sha> --jq '.files'` |
| web 定位 | `gh browse -R <o/r> <path:行号> --blame -n` |

> 以上定位决策与陷阱来自 代码调查 skill skill 五轮实测速查表 [经验： 外部代码调查 skill 五轮实测速查表]。

### 关键机制：两级 sha 链

`gh search code --json` 返回的 `items[].sha` = **blob sha**（到文件内容）；`html_url` 中的 sha = **commit sha**（到变更历史）。这是 gh 与 git 互查的咬合点：gh 定位拿双 sha 到 git clone 后 `git show <commit_sha>:<path>` 对账。[经验： 同上速查表一级结论]

### 搜索陷阱（实测）

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 大小写敏感 | `Executer` 搜空 | 搜词与源码一致；或改 ast-grep 结构匹配 |
| bool flag 空格传值 | `--archived true` 到 `[]` | `--archived=true` |
| `--filename "*.glob"` 通配 | `[]` | 用具体文件名（`--filename sched.h`） |
| 内联多 qualifier 互斥 | `language:go repo:x` 到 `[]` | 独立 flag `--language` + `--repo` |
| `--json` 字段硬校验 | `--json nope` 到 exit 1 | 用 `--help` 列出的字段 |
| search 与 view 字段名不同 | `stargazerCount`(view)/`stargazersCount`(search） | 区分命令 |

选型双通道口径：gh search（code 实证）+ crates.io/PyPI 元数据，结论标六态（五栈数据源与稳度判据见 tool-selection.md） [经验： reader 仓 R002 选型细则同款]。定位后 `gh repo clone` 本地深读（交给 tool-git.md 零节）。

## 一、认证与状态

```powershell
gh auth status          # 认证状态与账号
gh auth login           # 交互登录(浏览器/device 两种)
```

- 认证一次后，git 对 github.com 的 push/pull 也会走 gh 凭据（`gh auth setup-git` 显式接通）
- 环境变量 `GH_TOKEN` 可注入 token（无交互场景：CI、脚本内调用）；带 token 时 `gh api` 限流额度更高 [经验： reader 仓 self-update 用 GH_TOKEN 加 gh api 兜底]

## 二、Release 管理（项目封版核心流）

```powershell
# 查最新与列表
gh release list --repo <owner>/<repo> --limit 5
gh release view v0.4.0 --repo <owner>/<repo>

# 创建 release(笔记文件 + 资产)
gh release create v0.4.0 --title "v0.4.0 — 主题" --notes-file notes.md asset1.zip asset2.zip

# 上传资产到已有 release(幂等,重复上传会报已存在)
gh release upload v0.4.0 asset.zip --clobber   # --clobber 覆盖同名
```

要点：
- **先打 git tag 再 create release**（或 `gh release create` 自动建 tag）
- 上传后验收：`gh release view v0.4.0 --json assets --jq ".assets[].name"` 逐一对资产名与 sha256 [经验： reader 仓 R008 封版流程]
- tag 名与产物版本一致性闸放 CI，不靠人眼

## 三、gh api（兜底一切）

```powershell
gh api repos/{owner}/{repo}/releases/latest --jq .tag_name
gh api repos/{owner}/{repo}/releases/latest --jq .assets[].browser_download_url
```

- 带 `--jq` 直接出字段，省 jq 管道
- 限流时回退策略：匿名 curl `api.github.com` 到 gh api（认证）到 重试退避 [经验： 同上]

## 四、日常操作速查

```powershell
gh repo view --web                    # 仓库概览/打开网页
gh pr list / gh pr view / gh pr create --fill
gh issue list / gh issue view 12
gh run list / gh run watch <id>       # Actions 运行状态
gh workflow run release.yml           # 手动触发工作流
```

## 五、坑

| 坑 | 处理 |
| --- | --- |
| 匿名 API 限流 403 | 注入 `GH_TOKEN` 或确认 `gh auth status` |
| 资产上传竞态（并发 job） | release 上传加锁或 `--clobber`；CI 里串行化上传步 [经验： reader 仓 M004] |
| Windows 路径含空格/中文 | 资产路径加引号；必要时先 copy 到短路径 [记忆] |

## 六、复验命令

```powershell
gh --version                 # 版本事实
gh auth status               # 认证可用性
gh release list --limit 3    # release 面可达性
```
