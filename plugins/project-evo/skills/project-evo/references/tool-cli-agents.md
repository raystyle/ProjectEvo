# agent-native CLI 设计：人与 agent 双用户契约

> 本篇 = 目标项目造 CLI（或给存量 CLI 补面）时，把 agent 当第二类用户的设计契约：发现怎么被找到、输出怎么省 token、输入怎么稳、自由代码怎么逃生、任务脚本怎么归档、多面怎么同源。与 base-init.md 的 agent-native SKILL.md 模式（骨架层：根 SKILL.md 怎么写）互补；是否引入具体框架走 tool-selection.md 稳度判据。提炼自 wevm/incur（TS 原作）与 douglance/incurs（Rust 移植）两仓 README [实证: 2026-09-04 两仓 README 原文取回核对]；契约方法论框架无关，两仓是样本实现。

## 一、双用户公理与 token 经济学

公理三条：

- **agent 是合法用户**：输出第一消费者常是管道里的 LLM 而非终端前的人；stdout 非 TTY 即 agent 视角
- **token 是 agent 的货币**：花在读输出上的 token 都从推理预算里扣；省 token 即降本提速
- **人机同源**：同一命令定义服务两面；呈现可分叉，数据契约不可分叉

经济学证据（incur 对 20 命令 CLI 的会话建模；量级示义，绝对值随模型假设变，未本仓复验 [推断]）：

| 会话环节 | MCP+JSON | 单一大 skill+JSON | agent-native CLI |
| --- | --- | --- | --- |
| 会话启动（工具可用即注入） | 6747 | 624 | 805 |
| 发现（学会命令面） | 0（启动已注入） | 11489 | 387 |
| 调用 5 次 | 110 | 65 | 65 |
| 响应 5 次 | 10940 | 10800 | 5790 |
| 全程成本 | $0.0325 | $0.0410 | $0.0131 |

三条省法对应后文三节：**发现层省**（schema 不逐轮全量注入，skill 按命令组拆分，常驻仅 frontmatter 级）、**响应层省**（默认紧凑输出）、**维护层省**（一份定义多面渲染，help/skill/schema 不各写各的）。

## 二、发现契约：三通道与渐进加载

| 通道 | 形态 | 每轮成本 | 定位 |
| --- | --- | --- | --- |
| `skills add` | 自动生成并安装 skill 文件 | 低（常驻仅 frontmatter） | 默认推荐 |
| `mcp add` | 注册为 MCP server | 高（工具 schema 注入每轮） | 需工具编排时 |
| `--llms` | 打印命令清单（markdown 或 JSON schema） | 零（按需一次） | 任何 agent 立即可用 |

要点：

- **skill 按命令组拆分**：单一大 skill 是发现层最贵形态（11489 token）；按命令组拆文件后 agent 只加载相关组（387） [实证: 信源 README 数字]
- **--llms 双形态**：markdown 给 agent 读，JSON schema 给程序消费；一族工具同构时 agent 换工具零学习
- 家族同款：browser-harness `--llms` 紧凑索引 [实证]；本仓 v0.2.0 起转插件市场形态,发现契约由 marketplace.json 承担、命令面收敛为 skill 内 scripts（旧 `project-evo llms` 随转型退役）[实证: 第二十八批]；reader `reader skill` 生成根 SKILL.md [经验: base-init 跨项目适配表]

## 三、输出契约：紧凑可解析与下一步建议

- **默认紧凑格式（TOON）**：类 YAML 但无引号无花括号；同构对象列表表格化（表头即字段，一行一对象），比 JSON 省至 60% token [实证: 信源 README 声称]

```text
friends[3]: ana,luis,sam
hikes[3]{id,name,distanceKm}:
  1,Blue Lake Trail,7.5
  2,Ridge Overlook,9.2
  3,Wildflower Loop,5.1
```

- **格式面可切**：`--format` 支持 toon/json/yaml/md/jsonl，`--json` 为速记；流式命令每 chunk 一行，jsonl 形态逐行包 type 字段
- **CTA（下一步建议）**：输出尾部列「接下来可跑什么」（命令 + 一句话理由），成功与失败都带；agent 链式推进不反问用户
- **输出策略两档**：`agent-only`（人面隐藏数据，agent 面全给）与 `all`；组级声明可被子命令继承或覆写

## 四、输入契约：schema 化 I/O

- **四面 schema**：args/options/env/output 全声明；入口先验证后执行，格式错误不进业务
- **类型即文档，一份多渲染**：字段 describe 同时进 --help、skill 文档、JSON schema；改一处三面同步（单一事实源的命令面版）
- **弃用全通道同步**：一个 deprecated 标记同时体现为 help 中 [deprecated]、skill 文档提示、schema 布尔字段、TTY 使用时 stderr 警告；四处只见一处即漂移

## 五、自由代码面：管道代码逃生舱

固定命令覆盖高频与稳定操作；长尾与组合逻辑靠**管道代码面**：CLI 无参 + 管道喂代码即执行，代码跑在运行时上下文里，agent 自由写自由执行。

```powershell
# browser-harness:helpers 预导入,零 import 直接写
@'
info = new_tab("https://example.com")   # 任务首个导航用 new_tab
wait_for_load()
print(page_info())
'@ | browser-harness
```

```bash
# Linux/macOS heredoc 形态
browser-harness <<'EOF'
print(google_search("rust web framework", limit=5))
EOF
```

设计要点：

- **内置库函数零 import**：运行时预导入 helper 面（导航/页面读写/抓取等），函数名即 API；agent 不猜模块路径 [实证: browser-harness helpers.py def 清单，见 tool-browser-harness.md]
- **直接集成运行时**：代码跑在 CLI 常驻上下文（daemon 连接、tab 状态、配置），不是每次起冷进程；helper 双通道（全量命名空间 + 顶层解包常用名）兼顾全量与顺手 [经验: 云 CLI 仓 omc 同款 TS 片段管道]
- **产品化形态是 Code Mode**（incurs）：codemode_execute 启动 JS 执行、直接调 tool catalog，配审批生命周期（codemode_decide 逐动作批/拒、codemode_cancel 取消）；本地只读工具免批、远程与破坏性工具须批 [实证: 信源 README]
- 分工：固定命令管高频与稳定（schema 保障），自由代码管长尾与组合（逃生舱保障）；两者同源一个运行时，脚本产物归档见「九、脚本 workspace」

## 六、人机分叉契约

| 机制 | 语义 |
| --- | --- |
| agent 检测 | stdout 非 TTY 即 agent；分叉的是呈现（进度/装饰），不变的是数据契约 |
| 全局 flag 契约 | --help/-h、--version、--llms、--mcp、--json、--format、--verbose 每命令免费自带，不逐命令设计 |

## 七、定义一次多面暴露

incurs 把「一份命令定义」扩成共享命令图，全部暴露面从同一 schema 源生成 [实证: 信源 README]：

```mermaid
flowchart TD
    def[typed command definitions] --> graph[shared command graph + schemas]
    graph --> cli[CLI]
    graph --> http[HTTP]
    graph --> mcp[MCP]
    graph --> art[generated artifacts: openapi / skills / completions / codegen]
```

- **Agent Plugins 1.0 三层打包**：Prompt Artifact（skills/<名>/SKILL.md，教 agent 怎么用）+ Tool Binding（mcp.json，怎么连工具）+ Tool Runtime（bin/，可执行本体）；根 plugin.json 声明三层，支持 skills-only 精简包
- 与本仓硬规则「单一权威源」同构：定义只有一份，其余全是产物；产物再生成拒绝静默覆盖（须显式 force）

## 八、行为对齐与验证

incurs 方法：vendored 上游 TS 实现为**行为 oracle**，其 1062 条测试分类入册；parity gate 让双实现跑同输入、比结构化输出 [实证: 信源 README]。

映射到本仓既有机制（同构，非移植）：

| oracle 法组件 | 本仓同构 |
| --- | --- |
| 行为 oracle（参考实现即标准） | 黄金文件（flow-testing.md） |
| parity gate（双实现比输出） | 双漂移守卫（data/skill 与 skills/ 逐文件一致） |
| 清单与 schema 溯源 | llms 冒烟（CI 门禁） |

## 九、脚本 workspace：集中归档与同运行时复用

按需求写的自定义任务脚本要有一个围绕 CLI 的集中维护点（browser-harness 的 browser-workspace 实证 [实证: bh SKILL.md 与 run.py，2026-09-04 核对]），且 workspace 脚本命令与管道代码共用同一运行时。

### 定位与落位

- workspace 是 **agent 拥有的运行时目录**，不是包源码：只放任务专属 helper、任务脚本与数据，装好的包永不被改
- 落位钉在数据根（BH_HOME，默认 ~/.config/browser-harness），git checkout 安装也不例外；仓内 browser-workspace/ 只放受版控的参考内容（代码根与数据根解耦）
- 位置可 env 覆写（BH_BROWSER_WORKSPACE）；目录改名走整树自动迁移（搬走全部用户数据，不孤儿化）

### 两类产物两个口

| 产物 | 落位 | 出口 |
| --- | --- | --- |
| 可复用函数 | browser_helpers.py | 自动并入 helper 面（merge 语义：包内填默认，workspace 副本按函数覆写；缺省总用最新包内） |
| 独立任务脚本 | apps/<名>.py | 即成一级命令：browser-harness <名> [args...]，位置参数进 APP_ARGS |

- **同一 exec 运行时**：apps 脚本与管道/heredoc 代码走同一条执行路径（预导入 helpers、合并 workspace helper 后 exec）；workspace 新写的函数，下一次管道脚本直接调用，零 import [实证: run.py 单入口 exec(code, globals())]
- 长跑插件配 rmux 会话（`browser-harness rmux ensure ...`），不占前台；任务数据（db、心跳、supervisor 日志）同归 workspace，脚本与数据同址

### 供给与演化

- **包是薄核**（daemon、helpers、rmux、诊断），应用全是 workspace 插件；`--update`/`skills sync` 增量供给，本地新增永不删 [实证: bh SKILL.md]
- **领域技能层**：workspace/domain-skills/<host>/ 归档站点操作知识（目录名 = 去掉 www. 后的首段），做该站任务前必读；workspace 不只归档脚本，还归档「这个站点怎么操作」的知识
- 设计公理：**包管稳定内核，workspace 管长尾演化**；升级包不动 workspace，删 workspace 不伤包

## 十、落地清单

| 项 | 自问 | 不满足的代价 |
| --- | --- | --- |
| 发现 | 有 --llms 清单或可安装的 skill 文件吗 | agent 每会话重学命令面 |
| 拆分 | skill 按命令组拆了吗 | 一次加载全量，发现层翻倍 |
| 输出 | 默认输出紧凑且结构稳定吗 | 响应 token 膨胀，解析靠猜 |
| CTA | 尾部有下一步建议吗 | agent 停下反问用户 |
| schema | args/options/env/output 有声明吗 | 参数格式靠试错 |
| 逃生舱 | 固定命令覆盖不了时能管道喂代码吗 | agent 被迫求加新命令或绕开工具 |
| 归档 | 按需求写的任务脚本有集中 workspace 吗（还是散落在对话里） | 复用靠重写，演化无痕迹 |
| 弃用 | 弃用四处（help/skill/schema/警告）同步吗 | agent 持续调用死参数 |
| 同源 | help/skill/llms 出自一份定义吗 | 三面漂移，agent 学到旧契约 |

样本实现选型提示：incur（TS，npm）与 incurs（Rust，crates.io）均为 MIT；活跃度与稳度未深查，引入前按 tool-selection.md 四信号核 [推断]。
