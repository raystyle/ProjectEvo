# reader — 本地文档阅读搜索提取指南

> 定位:**读取本地文档、电子书等文档参考资料**(用户裁定):PDF 按页、markdown 与 Word/EPUB/ODT/RTF/Office/CSV 按标题节,是读一切本地参考资料的首选,代替自写解析。本机 v0.4.0,缩写 `rr` 同入口 [实证: 2026-09-03 `reader --version`]。

## 一、三个子命令

```powershell
reader search <文件|目录> <关键词> [--regex] [-i] [-C N] [--pages 范围] [--format json] [--ocr]
reader extract <文件> [--pages 范围] [-o 文件] [--format json] [--offset N] [--limit M] [--ocr]
reader query  <文件> <mq表达式> [--format json]      # .h2 标题 / .code 代码块 / .link 链接 / select 管道
```

- 退出码 grep 语义:0 命中 / 1 无命中(search) / 2 出错 [实证: 2026-09-03]
- 目录输入 search 递归批量搜,命中行前缀文件路径
- 索引:`reader --llms` 出紧凑命令索引;`reader skill` 出完整 SKILL.md

## 二、输出契约

- text:命中行 `单元:行号:文本`;上下文 `单元-行号-文本`;extract 节头 `== page N ==` / `== section N ==`
- json:`{"ok":bool,"data":...,"meta":{command,duration_ms[,next_offset,cta]}}`;`--filter hits[].text` 点路径裁剪
- 不可靠页(扫描件/编码问题)标 `needs_ocr` 提示

## 三、OCR 兜底(扫描件/乱码文本层)

```powershell
reader extract "水印扫描版.pdf" --pages 2-4 --ocr     # PP-OCRv6 tiny,约 1 秒/页(多核并行)
```

- 首用自动下载约 6.2MB 模型;`--offline` 禁下载
- 实测量级:81 页全量 OCR 约 1-2 分钟,单页 1s 左右 [实证: 2026-09-03 安全牛 PDF 81 页全量提取]
- 水印 PDF 常见「文本层乱码」:extract 显示 `suspected_garbled_text`,直接加 `--ocr` 即可 [实证: 同上]

## 四、使用模式

| 场景 | 命令 |
| --- | --- |
| 大文档先看结构 | `reader extract <pdf> --pages 4-5`(目录页) |
| 全文落盘再分析 | `reader extract <pdf> --ocr -o fulltext.txt` |
| 定位关键词及上下文 | `reader search <文件> 关键词 -C 2` |
| 抽标题/代码块/链接 | `reader query <文件> ".h2"` / `".code"` / `".link"` |
| 批量找材料 | `reader search <目录> 关键词` |

## 五、环境变量(源码实证,2026-09-03 核对 D:\reader 仓\src)

| 变量 | 作用 | 默认 |
| --- | --- | --- |
| `READER_OCR_CACHE_DIR` | OCR 模型缓存目录(测试门控用) | 平台缓存目录下 `reader\models`(win:%LOCALAPPDATA%/%APPDATA%;mac:~/Library/Caches;linux:$XDG_CACHE_HOME 或 ~/.cache) |
| `READER_OCR_MODEL_SIZE` | OCR 模型档位,**只认 `tiny`/`small`** | `tiny`(非法值直接报错) |
| `GH_TOKEN` | `self update` 子命令的 GitHub 认证(匿名有配额,token 额度高) | 未设走匿名 |

[实证: ocr.rs:107/117/135-149、selfupdate.rs:138 逐行核对]

## 六、坑

| 坑 | 处理 | 状态 |
| --- | --- | --- |
| 中文参数在 PowerShell 被转义异常 | 路径与关键词加引号;必要时 `--%` 停止解析 | [记忆] |
| OCR 首跑慢 | 模型下载一次性成本,后续秒级 | [实证: 2026-09-03] |
| mq select 高级语法不确定 | 先 `reader skill` 查长形态文档再写表达式 | [经验: 2026-09-03 select 语法首试未命中] |

## 七、复验命令

```powershell
reader --version
reader --llms           # 索引可达
```
