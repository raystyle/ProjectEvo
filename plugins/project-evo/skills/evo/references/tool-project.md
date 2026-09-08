# 项目工具：`.tools/` 约定与外部工具路由

> 项目工具分两类：**项目自有工具**（`.tools\` 下 uv 运行时 Python 脚本）与**外部标准工具**（gh/git/browser-harness/reader/aria2c 等，指南见同目录各工具文件与 `README.md` 索引）。Node/TS 仓的 tsc、node:test、npm pack 工程合同见 [tool-typescript.md](tool-typescript.md)，不在本篇重复。

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

## 二、外部检索不在本篇

搜代码、搜网页、读电子书、下论文与种子，走市场技能 `super-research:research`。本篇只约定项目仓内 `.tools/`。

## 三、登记与维护

- 项目脚本升级后：更新 `.tools/README.md` 清单
- 新脚本：同类手拼 >=2 次才建；连续两个项目用到才值得抽公共约定
