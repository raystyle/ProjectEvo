# bh 与 reader 使用过程技巧

- 状态:已完成
- 日期:2026-09-08
- 关联:用户裁定「只复用 1 到 2 个 tab、不重复附着」；信源为本会话对 `bh` 0.5.2 与 `reader` 0.6.0 的实弹

> 本文件 = 为什么这么用、验证了什么、别再踩什么。下次照着做的操作已抽进 `super-research` 的 research 技能（web.md / reader.md）。

## 背景

连续两轮用 browser 技能做 Google / Medium / 网页抓取，又用 reader 技能研读 `E:\研究资料` 电子书。过程里反复出现：新开 tab 导致 Chrome Allow 再授权、daemon 重启丢附着、EPUB 打不开、扫描 PDF 空页、大目录列举卡死。用户当场裁定工位复用。

## 关键结论

1. **附着一次、工位复用**：Chrome Allow 按 WebSocket 连接弹，不按 tab 弹。`--new-tab` 与 `bh --restart` 会再连一次，等于再授权。钉 1 到 2 个已有 tab，只 `switch_tab(id, false)`。[实证: 2026-09-08 复用 Google 与 Medium 既有 SERP tab，不再弹 Allow]
2. **应用走 ensure_app_tab，片段走 switch_tab**：`bh google-search` / `medium-search` 按 host 复用应用 tab；`bh '<js>'` 默认工位未附着时是 `cdp_disconnected`。禁止为求值再 `--new-tab`。[实证: 默认 `list_tabs` 无 await 得 `{}`；await 后报 not attached；`--new-tab` 能求值但 close_tab 判定非 bh-owned]
3. **HTTP 抓取优先，失败如实报**：`web-fetch` 能 HTTP 就不要开浏览器页。DNS/错误页不得当正文成功。[实证: `example.org` HTTP 绿；`example.com` Chrome `ERR_NAME_NOT_RESOLVED` 仍 exit 0 且 title 留马标记]
4. **pluck 不是现场**：`google-search pluck` 可能吐上一轮缓存。以当前 SERP 页 `js` 抽取为准。[实证: pluck 3 条旧结果，页内刮到 8 条 `node:test TypeScript ESM`]
5. **reader 对坏书跳过、对扫描页标 needs_ocr**：目录 search 遇 malformed EPUB 跳过继续；扫描 PDF 要 `--ocr`。PowerShell 里 `--filter 'results[]'` 会被吃空，改 `--filter results`。[实证: 2026-09-08 `E:\研究资料\EPUB` 与 `Command-Line Rust` PDF]
6. **大资料盘先顶层、禁盲目递归**：`Get-ChildItem -Recurse` 对 `E:\研究资料` 会挂死。先 `dir /b` 顶层，再进 `EPUB` / `书籍作品`。[实证: 两轮递归列举超时被杀]

## 一、bh 搜索与抓取过程

### 工位表（本会话钉死）

| 工位 | 既有 tab | 用途 |
| --- | --- | --- |
| Google | 已在 SERP 的 page target | 搜索、页内刮结果 |
| Medium | 已在 medium.com 搜索或文章的 page target | 站内搜、grab、HTTP 补全文 |
| HTTP | 无 tab | `bh web-fetch` 默认 HTTP |

看板 `http://127.0.0.1:9870` 禁止当工作 tab。用户正在看的页禁止 `goto_url`。

### 命令顺序

```powershell
bh doctor --json          # healthy 且 default cdp:true 才继续
bh sessions               # 从 JSON 读 targetId，禁止猜
# 复用，不新建
bh google-search "<q>" --top 5
bh google-search ready
bh google-search pluck gs_search
# 与当前 SERP 不一致时，switch_tab 到 Google 工位用 js 刮 a>h3
bh medium-search "<q>" --top 5
bh medium-search pluck ms_search
bh web-fetch "<url>" --text     # HTTP 优先
```

`medium-search grab` 本轮 25s 超时；`ready` 已在目标文且 `challenged: false` 时改 HTTP `web-fetch`，不重试硬闯。[实证: ashusk 文 grab 超时、HTTP 拿到全文]

### 禁止

- `bh --new-tab`（本轮已开过 example.org，守卫不让关）
- `bh --restart --yes`（为自愈再连，必再弹 Allow）
- 不 `await` 的 `list_tabs()` / `current_tab()`（得到空对象，像没 tab）
- 关用户 tab、关看板、关 X 工位

## 二、reader 电子书过程

### 库地图（未全盘递归）

| 分区 | 观察 |
| --- | --- |
| 根 | 约 90 份会议 PDF 加 *Command-Line Rust* |
| `EPUB\` | 7 本；3 本 `malformed document: no chapter` |
| `书籍作品\` | PDF 成书：Black Hat Rust、Command-Line Rust、Clean Code 多语言 |
| `技术资料\` | 有目录，列举超时，本轮未进 |

坏 EPUB 的 PDF 副本在 `书籍作品\blackhat rust\`：`black_hat_rust.pdf` 文本层可读。

### 命令顺序

```powershell
reader --version                 # 本机 0.6.0，rr 同入口
reader extract <epub> --offset 0 --limit 6
reader query <epub> ".h2"
reader search <目录或文件> "<词>" -i
reader extract <pdf> --pages 1-8
# 节头 needs_ocr 再:
reader extract <pdf> --pages 7-12 --ocr
```

参数必须是 `reader extract <文件> --pages …`，不要把 `--pages` 写在文件前面（clap 会当成未知参数）。[实证]

### 书内可复用线索（研读摘，不是全书）

- *Cybersecurity Ops with bash*：选 bash 因为跨平台、目标机常无需另装解释器；Windows 列 Git Bash / Cygwin / WSL / cmd 与 PowerShell；每章 Workshop。[实证: query .h2 与 search Why bash]
- *Command-Line Rust*：clap 2.33 项目制复刻 Unix 工具；测试先行。扫描页漏检，OCR 能补目录。[实证: search clap]
- *Black Hat Rust* PDF：第 4 章同时讲 clap、日志、测试，与上一本互补。[实证: extract p2-8 目录]
- *PowerShell for Sysadmins*：能抽封面与 workflow 命中，偏云编排示例。

## 三、待办

- `技术资料\` 未进，需用户指定子树再读
- *Data Science at the Command Line* EPUB 几乎只有封面，换 PDF 或重打包后再验
- `example.org` 残留 tab 不能由 agent 关，需用户手关
- Python `browser-harness` 0.6.12 与 TS `bh` 0.5.2 是两套 CLI，过程技巧按客户端分开写，禁止混 oracle
