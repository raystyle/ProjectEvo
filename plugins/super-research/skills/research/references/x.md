# X 搜索

> 查已收割的本地库，不碰浏览器。现场收割是另一条命令，须用户明确要求。

## 命令

```powershell
bh x-intel search --stats
bh x-intel search "<kw>" --limit 5
bh x-intel search --recent --limit 5
bh x-intel search --since 6h --limit 5
```

返回 JSON `{_ok,_v,_ts,count,items}`。`items` 含 author、handle、text、url、posted_at。

[实证: 2026-09-08 库 1435 帖 / 666 作者；`search rust` 与 `search typescript` 各 5 条；`node:test` 0 条]

## 禁止

- `bh x-search ...`：CLI 会当成 JS 片段，报 `x is not defined`
- 把 X 搜索当 Google SERP：这是本地 `x_tweets.db`，不是 x.com 现场搜
- 未请自 `harvest`：会占用 x-intel 已有 X tab 做现场收割
- `goto_url` 到带马标记的 x.com 监控 tab

## 与 Google / Medium

| | Google / Medium | X |
| --- | --- | --- |
| 命令 | `bh google-search` / `medium-search` | `bh x-intel search` |
| 对象 | 现场 SERP | 本地库 |
| 浏览器 | 复用搜索 tab | 不碰 |
