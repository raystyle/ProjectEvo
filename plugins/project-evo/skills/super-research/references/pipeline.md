# 研究管线

> 发现到获取到研读到落盘。本篇是编排；各工具命令见同目录分篇。

## 一、四段

| 段 | 工具 | 产出 |
| --- | --- | --- |
| 发现 | `gh search`、`bh google-search`、`bh medium-search`、`bh x-intel search`、arxiv API | 标题、URL、仓库 |
| 获取 | `aria2c` HTTP/种子文件；`git clone` 仅深读源码 | 本地文件 |
| 研读 | `reader extract/search/query` | 节、命中行 |
| 落盘 | 目标项目 `docs/research/SNNN` | 六态结论 |

## 二、论文

1. 发现：`bh google-search "site:arxiv.org <题>" --top 5` 后 `pluck gs_search`；或 `aria2c` 拉 `http://export.arxiv.org/api/query?search_query=...&max_results=3`
2. 直链：Google 的 `/html/<id>` 改 `https://arxiv.org/pdf/<id>`
3. 下载：`aria2c -x 8 -s 8 -c -d <dir> -o <id>.pdf "https://arxiv.org/pdf/<id>"`
4. 核对：`reader extract <pdf> --pages 1-2`

[实证: 2026-09-08 NodeSRT arXiv:2104.00142，108268 字节，reader 抽出标题与摘要]

## 三、种子

1. 发现：Google 官方发行页（如 `site:releases.ubuntu.com`）或 `bh web-fetch` 该页，找 `.torrent`
2. **只下种子文件**：`aria2c --follow-torrent=false -d <dir> -o name.torrent <url>`
3. 列载荷：`aria2c -S name.torrent`（看体积再决定要不要下 ISO）
4. 禁止对多 GB 载荷默默 `aria2c name.torrent`：默认会 `follow-torrent` 并 `file-allocation=prealloc`，立刻占满磁盘

[实证: 2026-09-08 下 Ubuntu 24.04.4 desktop `.torrent` 508158 字节；未加 `--follow-torrent=false` 时预分配 6.1GiB ISO，已杀掉并删]

## 四、浏览器面

研究任务默认无头：`bh engine start` 到 `bh web-fetch --engine` 到 `bh engine stop`。临时 profile，杀进程即净。用户已开搜索页才复用 tab。详见 web.md。
