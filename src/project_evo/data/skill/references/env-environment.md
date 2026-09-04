# 环境依赖索引：ome（Oh My Env）模式

> 本机工具链由 **ome**(Oh My Env）管理：全平台 Agent 工具及运行时依赖环境的部署、管理、验收与诊断 CLI。环境根 EnvRoot（可用 `--env-root` 或 `OHMYENV_ROOT` 覆盖）。**当前 v0.1.0，尚未封板**，命令面可能变化，以 `ome --help` 实测为准，升级后对照刷新本篇 [实证： 2026-09-03 ome 0.1.0 实测]。

## 一、ome 管理模型

### 三态 + 域分组

每个工具由三态刻画（见 `ome status`）：**locked**（锁定版本，pin 管理）到 **installed**（已装版本）到 **path**（是否注册用户 PATH）。工具按七个域分组 [实证： status 输出实测]：

| 域 | 工具数 | 内容（代表性） |
| --- | --- | --- |
| 操作编排依赖 | 2 | ome 自身、herdr |
| 运行时依赖 | 8 | pwsh、wsl、python、uv、fnm… |
| 编译器依赖 | 4 | rustup、go、zig、dotnet… |
| 运行时衍生依赖 | 1 | cargo/gopath 类运行时衍生物 |
| 多路复用依赖 | 1 | rmux |
| 远程服务依赖 | 2 | claude 类 |
| 命令工具依赖 | 19 | reader、gh、git、aria2、rg、jq、yq、mq、ast-grep、rumdl、7z… |

### 环境根布局

```text
环境根\
  <工具名>\    自包含安装(reader\reader.exe;portable git 布局…)
  uv-tools\    uv tool 安装的 Python CLI(browser-harness)+ bin\ 垫片
  modules\     PowerShell 模块(omp/Pester/Posh-SSH)
  cache\ logs\ images\ deploy\   支撑目录
ome 自身:C:\Users\<u>\AppData\Local\Programs\ome\ome.exe(ome init 装入用户程序目录)
各仓内:ome 本地状态目录,gitignore 之 [经验: reader 仓 066bdec 同款处理]
```

**代码根与数据根解耦**（家族通用模式）：工具仓只放代码与文档，大体量运行数据（镜像/模型/缓存/实例）放独立数据根，环境变量指路（ome 的 `OHMYENV_ROOT`、browser-harness 的 `BH_HOME` 等，数据根各自以环境变量指路）；数据根不是 git 仓库，README 即清单 [实证： 运行存储根「运行存储」README 明示解耦约定]

## 二、ome 命令面速查（v0.1.0 实测）

| 命令 | 用途 | 备注 |
| --- | --- | --- |
| `ome query` | 解析工具版本与下载资产，不落盘 | 干跑探测 |
| `ome pin`(alias `lock`） | 查看/设置版本锁定 | 未锁定的工具自动锁定最新版 |
| `ome install` | 按锁定版本安装到环境目录 | **不注册 PATH** |
| `ome deploy` | 安装 + 注册用户 PATH | 对外可用形态 |
| `ome update` | 更新到最新版并重新锁定 | |
| `ome status` | **依赖权威索引**：三态 + 域分组逐工具 | 项目盘点入口 |
| `ome daily` | 日常更新：同主版本自动升，跨主版本保留待确认 | 语义化版本安全更新 |
| `ome init` | 自装到用户程序目录 + catalog 同步 + PATH，幂等 | 换机重建环境 |
| `ome package` | 打包工具为可分发目录 | 不注册 PATH、不回写锁定 |
| `ome verify` | 按部署维度验收环境一致性 | 失败返回非零（可进门禁） |
| `ome heal` | 幂等自愈指定部署维度 | |
| `ome doctor` | 诊断：版本漂移、PATH 死链重复、锁定缺失、缓存孤儿 | 失败返回非零 |
| `ome self` | ome 自身管理 | |
| 全局 | `--env-root <dir>`、`--format kv/json/jsonl`、`--json` | 脚本化友好 |

## 三、项目五工具在 ome 中的位置

| 工具 | 域 | 安装形态 | 环境根位置 | 指南 | 版本快照 |
| --- | --- | --- | --- | --- | --- |
| reader | 命令工具 | 自包含（reader.exe + rr.exe + SKILL.md) | `环境根\reader\` | [tool-reader.md](tool-reader.md) | 0.5.0 [实证: 2026-09-04] |
| gh | 命令工具 | 自包含 | `环境根\gh\` | [tool-gh.md](tool-gh.md) | 2.98.0 [实证] |
| git | 命令工具 | 自包含（portable) | `环境根\git\` | [tool-git.md](tool-git.md) | 2.55.0 [实证] |
| aria2 | 命令工具 | 自包含 | `环境根\aria2\` | [tool-aria2c.md](tool-aria2c.md) | 1.37.0 [实证] |
| browser-harness | - | **uv tool**（非 ome 直管） | `环境根\uv-tools\browser-harness\` | [tool-browser-harness.md](tool-browser-harness.md) | 0.6.12 [实证: 2026-09-04] |

> browser-harness 走 uv tool 安装（`uv tool install browser-harness`），升级用 `uv tool upgrade`，不在 ome 锁定面内；其余四工具由 ome 三态管理。

## 四、依赖路由规则（项目初始化时执行）

1. **盘点**：初始化项目先跑 `ome status` 拿权威索引；按「平台矩阵 + 技术栈」勾出本项目依赖，登记进项目 AGENTS「环境事实」节：工具 + 安装形态（ome 域/uv tool/系统）+ 版本获取命令（**版本号不硬编码，防漂移**）
2. **验收**：`ome verify` / `ome doctor` 失败返回非零，可直接进项目门禁或接管验收清单（env-platform.md 七节第 2 步）
3. **换机重建**：`ome init` 幂等装自身 到 `ome install`（按锁定）到 `ome status` 对账
4. **日常**：跨主版本升级经 `ome daily` 保留待确认，**升级依赖是显式决策**，不静默跳主版本 [实证： daily 语义出自 --help]
5. **版本快照**：关键工具版本在项目 ROADMAP/diary 记「快照 + 日期」，升级后复验刷新
6. **新增工具**：先查 `ome status` 防重复安装；Python CLI 一律 `uv tool install`；能被 ome 管的优先进 ome 锁定面

## 五、复验命令

```powershell
ome --version                 # 0.1.0(未封板,升级后对照 --help 刷新本篇)
ome status                    # 全量依赖三态索引(权威来源)
ome status --format json      # 脚本化消费
ome doctor                    # 环境健康(漂移/死链/孤儿)
uv tool list                  # uv-tools 面(browser-harness 等)
```
