# 项目工具：`.tools/` 约定与外部工具路由

> 项目工具分两类：**项目自有工具**（`.tools\` 下 uv 运行时 Python 脚本）与**外部标准工具**（gh/git/browser-harness/reader/aria2c 等，指南见同目录各工具文件与 `README.md` 索引）。

## 一、`.tools\`：项目自有脚本工具

### 定位

- 有复用价值的自定义脚本（检查门禁、批量处理、跑批对比）归档 `.tools\`，配 `README.md` 清单与规则
- **载体统一为 uv 运行时 Python 脚本**：PEP 723 内联依赖头 + `uv run --script` 运行，零 venv 管理、零激活、跨机可跑
- [实证： reader 仓 `.tools\` 四件门禁脚本 + ab_run.py 跑批器长期运行此模式]

### PEP 723 脚本写法

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6"]
# ///
"""一句话用途(自述与用法,归档必带)。"""
import sys, yaml  # 第三方依赖直接 import,uv 自动解析

def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

运行：`uv run --script .tools\xxx.py [args]`（首次自动建缓存环境；离线机先 `uv cache` 预热）。

### 归档规则

| 规则 | 要求 |
| --- | --- |
| 命名 | kebab-case + `.py`，名即用途（`md-ref-scan.py`、`ab-run.py`） |
| 自述 | 脚本头部 docstring 写清用途、用法、退出码语义 |
| 清单 | `.tools\README.md` 逐脚本一行：文件、职责、用法示例 |
| 退出码 | 遵循 grep 语义：0 成功/命中，1 无命中，2 出错（stderr 人读） |
| 豁免 | 门禁类脚本配显式豁免清单文件（如 `md-ref-allow.txt`），不留口头豁免 |
| 入库 | 脚本与豁免清单入 git；产物与缓存 gitignore |

### 沉淀铁律

同类手拼操作（命令序列、内联代码）重复 **≥2 次**，必须升级为 `.tools\` 脚本；反之，一次性验证留在 research 的代码块即可，不预建脚本。

### 常见 `.tools\` 脚本族（按需生长）

| 脚本族 | 用途 | 时机 |
| --- | --- | --- |
| `md-ref-scan.py` | 仓内 markdown 引用断链回归 | 文档结构大改后必跑 |
| `md-char-scan.py` / `md-heading-scan.py` | 禁用字符/标题规范机检 | guide 定了规范就配 |
| `*-run.py` | A/B 跑批、批量对比 | 有质量/性能对比需求时 |

## 二、外部标准工具路由

五工具定位（用户裁定，2026-09-03；详细操作指南见同目录各工具文件）：

| 工具 | 定位 | 何时代替默认 |
| --- | --- | --- |
| **gh** | 搜索代码和项目仓库（release 管理其次） | 代替网页搜 GitHub 与裸 curl API |
| **git** | 本地 clone 研究代码仓库（版本控制其次） | `--depth 1` + grep/log/blame 深读外来仓 |
| **browser-harness** | 搜索引擎和网页抓取 | 代替 WebSearch/curl 当结果要 JS 渲染/交互/登录态 |
| **reader** | 读取本地文档、电子书等参考资料 | 代替自写解析；`--ocr` 兜底扫描件 |
| **aria2c** | 下载任意资料（大文件/断点续传） | 代替 curl/Invoke-WebRequest 当大文件/可续传 |

五工具构成研究管线：**发现**（gh 搜仓与代码、browser-harness 搜引擎）到 **获取**（git clone、aria2c 下载）到 **研读**（reader 读本地、browser-harness 抓页面）到 结论落 `docs/research/` 标六态。

选择原则：先问「普通 HTTP 能不能直接拿」，能就用 fetch/curl；需要交互/渲染/登录态才上 browser-harness。小文件 curl，大文件/可续传 aria2c。读本地文档一律 reader。

## 三、登记与维护

- 外部工具的**版本事实**与**使用细则**沉淀在 `references/tool-<名>.md`，关键断言标六态
- 工具升级后：跑该工具指南里的「复验命令」更新 `[实证]` 日期，CHANGELOG 记一笔
- 新工具引入：先在 `references/README.md` 索引登记定位，再写指南；连续两个项目用到才值得建指南
