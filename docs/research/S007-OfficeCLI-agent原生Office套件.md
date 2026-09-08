# OfficeCLI：给 agent 用的 Office 套件

- 状态:已完成
- 日期:2026-09-08
- 关联:https://github.com/iOfficeAI/OfficeCLI ；已沉淀 `plugins/office-pro`

> 本文件 = 这个项目是什么、怎么给 agent 用、本机钉资产安装与烟测结果。未 clone、未跑官方 `install.ps1`、未 `officecli install`（不往 agent 目录喷 SKILL/MCP）。不把「first and best」当事实。

## 背景

用户指定研究该仓，随后要求安装测试并回填。入口是 GitHub；文档在 Wiki 与根 `SKILL.md`。本轮钉 GitHub release 资产 `officecli-win-x64.exe` 到 `%LOCALAPPDATA%\OfficeCLI\`，User PATH 已追加该目录；当前 Grok 会话进程 PATH 尚未继承，须新开终端才有裸命令 `officecli`。[实证: 2026-09-08 User PATH 含该目录、本会话 `Get-Command officecli` 空]

## 关键结论

1. **这是面向 AI agent 的 OpenXML CLI，不是 Microsoft Office。** 单文件自包含二进制（.NET 运行时打进包），读写 `.docx` / `.xlsx` / `.pptx`，不要求本机装 Office。语言 C#，许可 Apache-2.0。[实证: README 与 `gh repo view` 字段]
2. **规模已经很大。** 2026-03-15 建仓，2026-09-07 仍在推；约 30286 star、2067 fork、约 6099 commit、主页 `officecli.ai`。同组织还有桌面壳 [AionUi](https://github.com/iOfficeAI/AionUi)（约 33k star）。[实证: 2026-09-08 `gh repo view`]
3. **给 agent 的接口是 CLI + 内嵌 SKILL.md + MCP，不是 Python 库。** 路径像 DOM（1-based，`/slide[1]/shape[2]`），命令支持 `--json` 与结构化错误码。`officecli install` 会往 Claude Code、Cursor、Copilot、Codex 等目录塞 skill 与 MCP；本轮故意不跑。[实证: `officecli install --help` 列出 claude/copilot/codex/cursor/...；本机 `~\.claude\skills` 与 `~\.agents\skills` 无 officecli]
4. **分层是 L1 读到 L2 DOM 到 L3 生 XML。** 另有常驻进程（named pipe，改完不立刻落盘）、batch、`merge`、`dump`、`watch`。给非 officecli 读文件前必须 `save`/`close`。本轮 `create` 会自动常驻，`close` 后落盘。[实证: 烟测 `Created: ... kept open in background` 后 `Resident closed`]
5. **本机 v1.0.148 烟测通过，未做 A/B。** pptx / docx / xlsx 的 create、add/set、view、get `--json`、validate、close 全绿；坏路径 JSON 失败码 `not_found`、退出 1。不能据此声称「比 python-docx 少 50 行」或渲染保真。未跑 `watch` / MCP。[实证: 2026-09-08 `%TEMP%\pevo-officecli\smoke2.txt`]

## 它做什么

用类 DOM 路径寻址 OpenXML 元素，增删改查，不经过 Word/Excel/PowerPoint 进程。

| 层 | 命令 | 用途 |
| --- | --- | --- |
| L1 | `view` `validate` `view issues` | 大纲/文本/HTML/截图/问题列表。`view` 第二参必填 mode |
| L2 | `get` `query` `set` `add` `remove` `move` `swap` | 结构化改元素 |
| L3 | `raw` `raw-set` `add-part` | XPath 改生 XML |

Excel 侧自称内置 350+ 函数求值与透视表写入；Word 有 i18n/RTL、LaTeX 公式、mermaid 转图；PPT 有动画/Morph/3D glb。函数求值本轮只实证了 `SUM`；其余以 README 与 Wiki 为准，未复验。[实证: `--prop formula=SUM(B1,5)` 得 `computedValue` 15]

## 安装通道

文档所述 Windows：`irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex`，或 Scoop，或 npm `@officecli/officecli`。另有镜像 `https://d.officecli.ai/install.ps1`。官方脚本会装二进制并在首次安装时拷 SKILL.md 到探测到的 agent 目录。更新默认后台检查，可 `OFFICECLI_SKIP_UPDATE=1`。[经验: 官方脚本未执行；验证路径：读完 `install.ps1` 再决定是否用]

本轮实际做法（钉资产，不喷 skill）：

1. `aria2c` 拉 `https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.148/officecli-win-x64.exe` 与同目录 `SHA256SUMS`
2. SHA256 `df91e48fa250500b05ae1043777af26857e51ed12ea75b2f7a57e3333e3813bf` 与清单一致，文件 33419176 字节
3. 复制为 `%LOCALAPPDATA%\OfficeCLI\officecli.exe`，User PATH 追加该目录
4. `--version` 打印 `1.0.148`；烟测全程 `OFFICECLI_SKIP_UPDATE=1`

[实证: 2026-09-08 `Get-FileHash` 与 `officecli.exe --version`]

薄 SDK：`pip install officecli-sdk`、`npm install @officecli/sdk`，走常驻管道，缺二进制时会自行拉。[经验: 未装 SDK]

## 本机烟测

工作目录 `%TEMP%\pevo-officecli\smoke2`。PowerShell 封装函数参数名必须避开保留变量 `$args`，改用 `$ocArgs` 再 splat，否则子命令被吃掉、只打印根 help、退出 0、不建文件。[实证: 第一轮 `$args` 全失败；改名后下表全绿]

| 文件 | 操作 | 结果 |
| --- | --- | --- |
| `deck.pptx` 9831 字节 | `create`；`add / --type slide --prop title=Hello Agent`；`view outline`；`get /slide[1] --json`；`validate`；`close` | 大纲 `Slide 1: "Hello Agent"`；JSON `success: true`；validate 通过 |
| `report.docx` 5309 字节 | `create`；`add /body` 两段（Heading1 + 正文）；`view text`；`get /body --json`；`validate`；`close` | 文本两段可见；Heading1 告警但仍写入；validate 通过 |
| `data.xlsx` 4460 字节 | `create`；A1/A2/B1 设值；B2 `--prop formula=SUM(B1,5)`；`get /Sheet1/B2 --json`；`validate`；`close` | `computedValue` 15、`evaluated: true` |
| 坏路径 | `get deck.pptx /slide[99] --json` | `{success:false,error:{code:not_found,...}}` 退出 1 |

locale 从 OS 推断为 `zh-SG`。docx 默认 Times New Roman / 等线 11pt；pptx 标题 Calibri Light / 等线。未指定 `--locale`。[实证: create 提示与 get JSON `effective.font`]

xlsx 公式写法对照（同一会话）：

| `--prop` | 单元格类型 | 求值 |
| --- | --- | --- |
| `formula=SUM(B1,5)` | Number | 15 |
| `value==SUM(C1,5)`（Excel 前置 `=`） | Number / formula | 15 |
| `value=SUM(D1,5)`（无前置 `=`） | String | 文本 `SUM(D1,5)`，不求值 |

[实证: smoke2 `get B2` / `get C2` / `get D2`]

`create` 会保持常驻；`view` 必须带 mode（`text` / `outline` / ...），缺参打印 help 非默读全文。

## 和本仓的位置

| | OfficeCLI | 本仓 / Grok 现成面 |
| --- | --- | --- |
| 形态 | 自包含 C# 二进制 + SKILL.md + MCP | Grok 捆绑 `docx`/`pptx`/`pdf` 技能；Python 生态 python-docx/openpyxl |
| 改文档 | 路径寻址、JSON、常驻 | 库 API / 技能流程 |
| 看见版面 | 内置 HTML/PNG（自称；本轮未跑 screenshot/watch） | 一般看不到排版 |
| 依赖 | 无 Office、无 Python | 视技能/库而定 |

它不是 ProjectEvo 的替代品：evo 管文档骨架，OfficeCLI 管 Office 文件。不进 evo `references/`（第三方工具调研，不是本仓工作流）。2026-09-08 用户裁定吸收为独立市场插件 `office-pro`（skill `office-pro`）。操作面在 `plugins/office-pro/`；本文件仍是选型与烟测底稿，不复述改稿纪律。未与 python-pptx 做 A/B，未跑 `watch`。[经验: 既有稿纠偏、native 截图核、事实核查进稿面已在同日实弹]

## 风险与坑

- 常驻不落盘：别的程序读文件前必须 `save`/`close`
- shell 方括号要引号；`--prop` 不是 `--name`
- PPT `shape[1]` 常是标题占位
- 打开着的 Word/PPT 会锁文件
- 默认 docx 样式部件没有 `Heading1`：`style=Heading1` 会告警「not found in styles part, will be referenced as-is」，段落仍在、validate 仍过，Word 里样式是否生效未用 Word 打开核验 [实证: smoke2 add h1 告警；验证：用 Word 打开 `report.docx`]
- xlsx：`value=SUM(...)` 是字符串；公式用 `formula=` 或 `value==...` [实证: 上表]
- PowerShell 函数参数不要叫 `$args` [实证: 第一轮烟测]
- 远程 `install.ps1 | iex` 与 `officecli install` 会喷 skill/MCP；本机若只需二进制，钉 GitHub 资产即可
- 营销句「world's first and best」不作选型依据
- User PATH 追加后，已启动的 agent 会话不会立刻看到 `officecli`，用绝对路径或新开终端

## 未做

- 未 clone 源码、未跑 `install.ps1`、未 `officecli install` / `skills` / `mcp`
- 未读 Wiki 全文与 `skills/` 各子技能
- 未 `watch`、未 html、未 batch/merge/dump、未 L3 raw（native 截图在后续改稿实弹已做，见沉淀）
- 未与 python-docx / Grok `docx`/`pptx` 技能做 A/B
- 未装 SDK

## 沉淀

2026-09-08 吸收为 `plugins/office-pro`。入口 `plugins/office-pro/skills/office-pro/SKILL.md`。后续既有稿纠偏、截图核、事实核查进稿面见该 skill 的 `references/edit.md` 与 `facts.md`。
