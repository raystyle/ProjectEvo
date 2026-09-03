# 平台适配规范：Windows、Linux 与 macOS

> 项目骨架与工具链的三平台适配。**立项时问清目标平台矩阵**（见 base-init.md Step 2），按本篇落到 AGENTS、.gitattributes、CI 与工具选型。提炼自 reader 仓 三平台仓实践（CI 三系统门禁、R004/R005 接管验收、M005 行尾教训）[经验： reader 仓 P0004/R004/R005]。

## 一、shell 分平台约定（写进 AGENTS 操作规则）

| 平台 | shell | 禁止 |
| --- | --- | --- |
| Windows | PowerShell 7(`pwsh`) | `powershell.exe` 5.1、cmd |
| Linux | 该平台常规 shell(bash） | 依赖 Windows 专有命令 |
| macOS | zsh/bash | 同上 |
| WSL2 | 仓内 Linux 规则 | 与宿主 Windows 规则混用 |

[经验： reader 仓 AGENTS 规则 2 原文口径]

注意：**pwsh 7 本身跨平台**（Linux/macOS 可装），所以验证命令与工具脚本用 pwsh 写仍可三平台跑；但项目对外脚本不要假设 pwsh 存在，见「脚本载体」。

## 二、编码与行尾

- 文档与源码一律 **UTF-8**;Windows 上需兼容 PowerShell 5.1 的脚本用 **UTF-8 BOM**（无 BOM 中文 ps1 给 5.1 读会乱码） [经验： reader 仓 同款规则]
- **`.gitattributes` 钉死行尾**（`* text=auto eol=lf` 按语言细化），不靠各机 `core.autocrlf` 配置 [经验： reader 仓 P0004 实践；不做则跨平台 diff 全是行尾噪声]
- 代码中**禁止手拼路径分隔符**：用 Path API / `std::path::Path` 拼接，不写 `"a\\b"` 或 `"a/b"` 硬编码 [经验： reader 仓 M005，反斜杠 join 直接打红 linux/macOS 测试]

## 三、文档路径写法

| 场景 | 写法 |
| --- | --- |
| Windows 主开发仓的文档 | 反斜杠 `docs\proven\`（与主平台工具口径一致，reader 仓 模式） |
| 跨平台协作仓/通用文档 | 正斜杠 `docs/proven/`（所有平台 shell 与 markdown 链接都认） |
| 命令示例 | 跟目标平台 shell；跨平台示例用正斜杠 + 标注 |

原则：文档路径写法**全仓统一一种**，在 G001 声明；同仓混用两种是断链与复制粘贴事故之源。

## 四、脚本载体：跨平台优先

| 载体 | 平台面 | 用途定位 |
| --- | --- | --- |
| **uv Python(PEP 723）** | 三平台一致 | `.tools\` 项目工具**默认载体**；一处编写三处可跑 |
| pwsh 7 脚本 | 三平台（需装 pwsh） | Windows 主场项目可用；对外交付勿假设存在 |
| ps1（5.1 兼容） | 仅 Windows | Windows 内部一次性任务；带 BOM |
| bash | Linux/macOS/WSL | Unix 侧粘合；Windows 用户跑不了，勿做唯一入口 |
| Rust/Go 单二进制 | 三平台 | 高频门禁工具升级形态（参考 reader 自身） |

沉淀铁律的跨平台版：**手拼 ≥2 次的操作升级为 uv Python 脚本，而不是平台专属脚本**。

## 五、命令示例的跨平台写法

- 同一操作给两种形态时并列标注：`# PowerShell` / `# bash`，不写「等价命令自查」
- browser-harness 管道脚本：Windows 用 here-string(`@'...'@ | browser-harness`),Linux/macOS 用 heredoc(`<<'EOF' | browser-harness ... EOF`） [实证： browser-harness SKILL 双形态约定]
- 验证命令集（verification/）以 pwsh 写，首行注明「pwsh 7 跨平台；纯 bash 环境按注释转写」或附 bash 等价块

## 六、CI 三系统门禁

- 矩阵：`windows-latest` / `ubuntu-latest` / `macos-latest`（必要时加 arm64)
- 每平台跑同一套门禁（fmt/lint/test + 文档门禁），**首跑全绿才算跨平台兼容闭环** [经验： reader 仓 P0004「验收以 CI 首跑为准」]
- **CI 文档门禁**：文档机检四件套（字符/断链/标题/lint）以与本地同口径进 CI，本地过了 CI 不过的漂移立刻现形 [经验： ome 源仓 第十六批实践]
- CI 门禁上岗三坑（逐个踩过） [经验： ome 源仓 CI 三修]：
  1. runner **无预装**本地有的工具（uv 等需安装脚本引入）
  2. `GITHUB_PATH` 写入**仅后续步生效**，同步生效用 `export`
  3. Windows runner Python stdout 默认 cp1252，打印中文炸，脚本内重配 `sys.stdout` 为 UTF-8
- 平台差异吸收在代码与配置层（.gitattributes、条件编译、路径 API），不在 CI 层写 if/else 分叉逻辑
- Windows runner 随时退役更替（如 macos-13 Intel 退役） [经验： reader 仓 M004]，矩阵选型预留交叉编译退路

## 七、接管开发验收（多机协作）

换平台接管开发时，按清单验收而非口头确认（参考 reader 仓 R004 Linux / R005 mac 模式）：

```text
1. 仓已同步到目标 commit;工具链就位(rust/py/uv/rg/rumdl 按项目清单)
2. 门禁三件 + 文档门禁全绿(与移交方结果对账)
3. 真样本冒烟 N 路过(项目定义的最小真实输入)
4. 平台特有件验证(如 linux musl 预建、mac 交叉预建)
5. 推送后 CI 三系统绿
```

## 八、各工具平台注意速查

| 工具 | Windows | Linux | macOS |
| --- | --- | --- | --- |
| gh / git / aria2c | 三平台二进制，行为一致 | 同 | 同（arm64 注意资产选对） |
| reader | 三平台发布（musl 静态 linux 资产） | 同 | 同 [实证： reader 仓 P0013] |
| browser-harness | 第一优先验证 | headless 默认（无显示环境） | 支持 |
| browser-harness + WSL2 | 宿主 Windows 栈用 9223 | WSL2 镜像网络下 Linux 栈自钉端口（如 9224）避撞 | - [经验： bh SKILL 约定] |
| uv | 三平台 | 同 | 同 |
| rmux | 三平台 | 同 | 同 |

## 九、立项时的平台决策（回填 base-init.md Step 2)

初始化问关键问题时必含：**「目标平台矩阵是什么？」**，单平台内部工具（只 Windows）可裁剪跨平台开销；对外交付/CI 发布产品必须三平台门禁起步。决策记进 AGENTS 边界段与 PRD（D 编号），后续「顺便支持下 linux」类需求走 PRD 追问链，不静默扩矩阵。
