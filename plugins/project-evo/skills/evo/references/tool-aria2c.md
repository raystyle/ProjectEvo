# aria2c - 多线程下载指南

> 定位：**下载任意资料**（用户裁定）：大文件/断点续传/多协议（HTTP/FTP/BitTorrent/Metalink）。小文件直接 curl/Invoke-WebRequest，不必动用。本机 aria2 1.37.0 [实证： 2026-09-03 `aria2c --version`]。

## 一、与 curl 的分界

| 场景 | 用 |
| --- | --- |
| 小文件、一次性 API 响应 | curl / fetch |
| 大文件（模型、release 资产、数据集） | aria2c |
| 断点续传、多连接加速 | aria2c(`-c` + `-s`) |
| 种子 / Metalink | aria2c（唯一解） |

## 二、核心用法

```powershell
# 标准下载:多连接 + 断点续传 + 指定目录与文件名
aria2c -x 16 -s 16 -c -d D:\downloads -o model.zip "https://example.com/model.zip"

# 校验和验证(下载完自动核对,不匹配即失败)
aria2c --checksum=sha-256=<hash> -d . -o asset.zip "https://.../asset.zip"

# 认证与重试
aria2c --header="Authorization: Bearer <token>" -m 5 --retry-wait=3 -d . -o f.bin "<url>"

# 批量:从文件读 URL 清单,并行 N 个
aria2c -i urls.txt -j 3
```

## 三、参数表（全部实证自 `aria2c --help=#all`，2026-09-03)

| 参数 | 含义 | 默认 |
| --- | --- | --- |
| `-x, --max-connection-per-server=N` | 每服务器最大连接 | 4 |
| `-s, --split=N` | 分片下载数 | 5 |
| `-k, --min-split-size=SIZE` | 小于此不切分 | 1M |
| `-c, --continue` | 断点续传（续 `.aria2` 控制文件） | false |
| `-d, --dir=DIR` / `-o, --out=FILE` | 目录 / 文件名 | - |
| `-V, --check-integrity` | 按分片哈希校验（配合 torrent/metalink) | false |
| `--checksum=TYPE=DIGEST` | 下载后校验，失败退出非 0 | - |
| `-m, --max-tries=N` | 重试次数，0=无限 | 5 |
| `--retry-wait=SEC` | 重试间隔秒 | 0 |
| `-U, --user-agent=UA` | HTTP UA | aria2/$VERSION |
| `--header=HEADER` | 追加请求头（可多次） | - |
| `--all-proxy=PROXY` | 全协议代理 | - |
| `--allow-overwrite` / `--auto-file-renaming` | 同名覆盖 / 自动改名（配合 `-c` 幂等：关改名开覆盖） | false / true |
| `--check-certificate` | 证书校验 | true |
| `-i, --input-file=FILE` / `-j, --max-concurrent-downloads=N` | URL 清单批量 / 并行数 | - / 5 |
| `--file-allocation=METHOD` | 预分配（none/prealloc/falloc) | prealloc |
| `--summary-interval=SEC` / `--console-log-level=LEVEL` | 进度输出频率 / 日志级别 | 60 / notice |

> **帮助命令**：`aria2c --help` 只出第一页；**`aria2c --help=#all` 出全量 1767 行**（2026-09-03 实测） [实证]。

## 四、在项目工作流中的位置

- **模型/大资产拉取**：配 sha256 钉死（与 reader 的 OCR 模型三件 SHA-256 钉死同款思路 [经验： reader 仓 P0014])
- **release 资产验收**：gh 拿 URL 到 aria2c 带 checksum 下载 到 本地复算哈希对账
- 下载产物一律进 gitignore 目录；需要入库的小资产走 git lfs 或直接入库按项目规则定

## 五、坑

| 坑 | 处理 | 状态 |
| --- | --- | --- |
| 某些服务器拒绝多连接（429/403） | 降 `-x 4` 或 `-x 1`；`-U` 伪装 UA | [记忆] |
| `.aria2` 控制文件残留 | 正常完成自动删；中断后续传靠它，勿手删 | [记忆] |
| PowerShell 引号吞 URL 参数 | URL 加引号；含 `&` 必须引号 | [经验] |
| GitHub release 私有资产 401 | `--header="Authorization: Bearer $(gh auth token)"` | [记忆] |
| `-k 1M` 默认值导致小文件不分片 | 大文件显式 `-s 16 -k 1M` 以上 | [实证： 默认值出自 --help=#all] |

## 六、复验命令

```powershell
aria2c --version
aria2c --help=#all | Select-String "checksum"    # 参数面可达
```
