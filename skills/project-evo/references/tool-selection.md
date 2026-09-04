# 依赖选型与探查：数据源与搜索研究方法

> 最小实现阶梯的落地方法：阶梯是知，探查是行。第 2 到 5 档（本仓已有/标准库/平台原生/已装依赖）怎么查、生态库怎么选怎么核。提炼自家族选型手册四篇（结构源仓 R005 Rust 双通道、R008 PyPI、R009 Gallery、云 CLI 仓 R004 npm） [实证: 2026-09-04 四篇原文核对]。

## 一、先查仓内，再出仓（阶梯 2 到 5 档）

| 档 | 数据源 | 查法 |
| --- | --- | --- |
| 本仓已有 | 代码库 + INDEX | `rg` 搜函数名/功能词；INDEX 索引；proven 找先例 |
| 标准库 | 官方文档 | Rust std 与 docs.rs、Python docs、Node 与 MDN、pwsh `Get-Command`/`About_*` |
| 平台原生 | 平台文档 | 如浏览器原生控件（ponytail 首例：日期选择器就是 `<input type="date">`） |
| 已装依赖 | 清单与锁文件 | `Cargo.toml`/lock、`pyproject.toml`+`uv.lock`、`package.json`、`modules.psd1`；必要时 rg 进依赖源码目录 |

出仓前必答「真的没有吗」：仓内 rg 一遍、已装清单过一遍，再出仓。

## 二、生态选型：三通道与稳度四信号

### 三通道能力对照（差异即方法）

| 生态 | 网站搜索 | CLI 搜索 | API |
| --- | --- | --- | --- |
| Rust crates.io | 有 | `cargo search --registry crates-io`（镜像源必须显式） | 有（反向依赖 1 req/s 须带 UA） |
| Python PyPI | 有（**唯一关键词入口**） | 无（`pip search` 已永久关闭） | 元数据有（`/pypi/<名>/json`），关键词无 |
| PowerShell Gallery | 有 | `Find-PSResource`（**恒带 `-Repository PSGallery`**，裸调抖动） | v2 |
| Node/TS npm | 有 | `npm search [--json]` | `/-/v1/search` + 下载量 API |

### 稳度四信号（各生态同构）

下载量级、最近发版（近 6 到 12 月）、维护者/反向依赖、License。阈值是启发式不是门禁：窄领域新库会被误杀，人工核仓库与文档再定。

### GitHub 通道（评估质量与找真实用法，与注册中心通道互补）

`gh search repos`（星数与 pushedAt 并看，新秀加 created 限定）到 `gh repo view` 定点核证（isArchived/license/issues）到 releases 看发布节奏 到 `gh search code` 找签名片段的真实用法 到 深读用 `--filter=blob:none --no-checkout` 先行。细则见 tool-gh.md。

## 三、发现层：awesome 清单与官方库搜索

### awesome 清单（社区策展的领域地图）

- 总索引 `sindresorhus/awesome`；领域清单用搜法拿：`gh search repos "awesome <栈或领域>" --sort=stars --limit 5`（限定词与关键词同在引号内，语言另用 `--language`）
- 各栈常青清单（名称稳定数年）：awesome-rust / awesome-python / awesome-powershell / awesome-nodejs / awesome-go 及领域细分（awesome-react、awesome-cli 等） [经验]
- 用法：**不知道叫什么时先扫清单拿候选名**，再回三通道核稳度；清单是发现不是裁决：策展新鲜度不齐，清单自身也看 pushedAt，四信号仍是门

### 官方库（标准库）搜索

| 语言 | 入口 |
| --- | --- |
| Rust | docs.rs 与 std 文档站内搜索；本地 `cargo doc --open` |
| Python | docs.python.org 站内搜；本地 `pydoc <模块>` |
| Node/TS | nodejs.org/api；平台原生查 MDN；TS 查 Handbook |
| PowerShell | `Get-Command` 与 `About_*` 主题；Microsoft Learn 站内搜 |
| Go | pkg.go.dev（标准库与生态统一入口） |

## 四、防坑与锁定

- **名字防仿冒**：各生态均有仿冒前缀与热门名仿冒，装前与官方文档一字不差核对
- **锁定单一**：一仓一锁（`Cargo.lock`/`uv.lock`/`package-lock.json`/`modules.psd1`），CI 冻结安装（`--locked`/`uv sync --frozen`/`npm ci`）
- PowerShell 模块经 psmodule 版本加 SHA256 双锁，不散装 Install-Module
- **稳妥梯队优先**：名称稳定、小版本演进的库优先（各栈手册列有清单，如 PyPI 的 httpx/pytest/ruff、npm 的 typescript/zod/vitest）

## 五、结论落位与验收

- 选型结论落 research（S 文档），断言标六态；**双通道至少各一条证据**（注册中心稳度字段 + GitHub 质量信号）
- 引入的依赖有 pin 或版本理由；窄领域新库写明复核依据
- 装后即跑一个最小用例验证（反馈），不是装完即信

## 六、决策树

| 目标 | 做法 |
| --- | --- |
| 不知道叫什么 | awesome 清单扫候选（`gh search repos "awesome <领域>"`），或注册中心网站搜索 |
| 已知名字 | 注册中心 API/CLI 核元数据 + 下载量 |
| 评估质量 | GitHub 通道四步 |
| 生产可复现 | 单锁 + CI 冻结安装 |
