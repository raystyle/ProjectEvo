# Changelog

本文件记录 project-evo skill 及本仓库的所有可交付变更。格式：新增/变更/修复/移除 + 日期；先写 `[Unreleased]`，发布时转版本（git tag）。

## [Unreleased]

### 变更（2026-09-04，第三十一批：skill 改名 evo,消除插件名与 skill 名重叠）

> 用户指出市场安装后显示 Skill(project-evo:project-evo) 双名重叠;裁定:插件名、市场安装标识、`/project-evo:*` 斜杠命令前缀不动(品牌与安装兼容优先),skill 目录与 name 改为 evo,显示收敛为 project-evo:evo。

- 目录:plugins/project-evo/skills/project-evo git mv 至 plugins/project-evo/skills/evo;SKILL.md frontmatter name 同步 evo(硬规则:name 与目录名一致)
- 仓内路径引用全量同步:README(含反斜杠命令示例)、docs/README、AGENTS(规范导语/name 规则/地图/分层原则/硬规则 1)、插件 README 与三斜杠命令、hooks.json($CLAUDE_PLUGIN_ROOT 面)、.claude/settings.json、githooks/pre-commit、.tools/md-ref-scan 默认根、CI 冒烟、tests 两处路径;CHANGELOG 历史批次记载保留原路径不改
- verification 引言措辞修正:project-evo 定位为文档体系插件,核心 skill 为 evo
- 插件名、双市场清单、双 manifest、安装通道均不变;已安装用户插件更新即得新路径,无需重装

### 新增（2026-09-04，第三十批:市场分发协议沉淀,tool-cli-agents 第二节增补）

> 信源:Claude Code 官方文档原文取回(code.claude.com/docs 插件市场页)+ Codex 本机实弹(codex-cli 0.149.1:简写/SSH/HTTPS+钉版三形态逐一如实跑通)。用户问「marketplace add 应该支持 https 和 ssh 两种?」触发调研,裁定沉淀。

- tool-cli-agents.md 第二节新增「市场分发:add 形态与 git 协议(双客户端)」小节:双客户端 add 形态/简写默认协议(SSH vs HTTPS,相反)/私库认证(标准 git 机制,Claude 后台更新禁 helper)/钉版(@ref、#ref、--ref)/marketplace.json 插件级 source 七型(./、github、url、git-subdir、npm、archive、command;url 双协议;marketplace 级只 ref 无 sha)/裸 json 不可作分发载体
- 方法论一条:同一简写跨客户端解析不同,分发文档按客户端分别给实证 [经验]
- 同文件第八节同构表修正:双漂移守卫已在第二十八批随单源化消亡,该行改指清单一致性守卫
- README「快速开始」重写为「安装与部署」:四通道矩阵(Claude Code 插件/Codex 插件/本地市场开发态/裸脚本)+ 协议与钉版通用事实
- references/README 条目描述同步

### 修复（2026-09-04，第二十九批:init 脚手架语义,目标目录不存在则创建）

> 同日两犯升格:本地 e2e 与 CI 三系统冒烟(ubuntu/macos)各踩一次「目标目录不存在 exit 2」。裁定:init 是脚手架,建目标目录属其本性;check/scan 为只读诊断,保留存在性保护。

- scripts/init.py:目标目录 mkdir(parents) 替代报错退出;docstring 同步
- tests 增 test_init_creates_missing_target(嵌套不存在路径,期望 0 且 PRD.md 生成)
- CI 冒烟步无需预建目录,顺带即测新语义

### 变更（2026-09-04，第二十八批：插件市场转型,uv CLI 分发通道退役）

> 信源:SpecterOps/skills 市场仓组织维护形式实地调研(README/CONTRIBUTING/justfile/根双市场清单/插件双 manifest/catalog 机制原文取回核对)。用户裁定:放弃 uv CLI 分发,转插件市场仓,保留 git 历史原地重构;Codex 双面纳入;命令面全量(斜杠命令+hook)。六命令归宿:skill 安装与 update 随分发模式消亡(插件通道原生替代),init/check/scan 等价迁出,llms 降为 CI 冒烟。

- 目录:skills/project-evo 迁至 plugins/project-evo/skills/project-evo,模板迁至 skills/project-evo/assets/templates(均 git mv 保沿革)
- 双市场清单(.claude-plugin/marketplace.json 与 .agents/plugins/marketplace.json)+ 插件双 manifest(.claude-plugin/.codex-plugin,name/version/description 同步受测试守卫;Codex 面实弹验收:codex-cli 0.149.1 本机 `marketplace add` + `plugin add` 成功,缓存按 manifest 版本 0.2.0 归位,51 文件全树随装 [实证])
- 三脚本下沉 skill:scripts/{init,check,scan}.py(PEP 723 零依赖,逻辑原味迁自 CLI 模块);mdrules.py 立为禁字规则唯一权威(check PE-12/scan/md-guard 三面同源);md-guard.py 自包含化(PEP 723)随 skill 分发,plugin hook、.claude/settings.json、githooks 三处共用一份
- Claude 面:commands/{init,check,scan}.md 斜杠命令 + hooks/hooks.json PostToolUse 挡板($CLAUDE_PLUGIN_ROOT);Codex 面走 skill 本体与双 manifest
- 移除:src/project_evo 全树(六命令 CLI;update 自升级闭环、skill 双落位安装随分发模式消亡)、data/skill 内嵌副本(双漂移守卫随之取消,单源化)、.tools/md-guard.py(并入 plugin scripts)
- tests 重写:脚本按路径加载(无安装态包);新增市场清单一致性守卫(双市场收录一致/source 可达/双 manifest 字段与版本同步/命令面与脚本在位);仓内禁字回归改指 mdrules.py;10 测全绿
- 接线:AGENTS(地图/分层原则/硬规则 1/环境事实)、README(安装与结构全重写)、SKILL.md 配套面、base-writing-standards 与 tool-cli-agents 措辞、verification 引言、docs/README 路径、CI 冒烟(init+check 实跑 + 五 JSON 解析)、.tools/README、md-ref-scan 默认根、pyproject(package=false 降维护栈)
- 安装通道变化:uv tool install git+ 退役;新通道 Claude Code `/plugin marketplace add raystyle/ProjectEvo` + `/plugin install project-evo@projectevo`,Codex `codex plugin marketplace add raystyle/ProjectEvo`

### 新增（2026-09-04，第二十七批：agent-native CLI 设计指南,双用户契约、自由代码面与脚本 workspace 吸收）

> 信源:wevm/incur(TS 原作)与 douglance/incurs(Rust 移植)两仓 README 原文取回核对;叠加家族 browser-harness 与云 CLI 仓 管道代码逃生舱、browser-harness browser-workspace 脚本归档设计实证(用户裁定纳入)。契约方法论框架无关,两仓为样本实现。

- 新增 `references/tool-cli-agents.md`(第 21 篇),十节:双用户公理与 token 经济学(MCP/单 skill/agent-native 三形态会话成本对照,数字为信源建模未本仓复验);发现契约三通道(skills add/mcp add/--llms,skill 按命令组拆分,发现层 11489 到 387);输出契约(TOON 紧凑格式/--format 面/CTA/输出策略两档);输入契约(四面 schema/类型即文档一份多渲染/弃用全通道同步);**自由代码面**(管道代码逃生舱:here-string/heredoc 喂代码、内置库函数零 import 直集成运行时、helper 双通道;incurs Code Mode 为产品化形态,审批生命周期);人机分叉(agent 检测/全局 flag 契约);定义一次多面暴露(共享命令图 + Agent Plugins 1.0 三层:Prompt Artifact/Tool Binding/Tool Runtime);行为 oracle 对齐法(1062 测试 parity gate,映射黄金文件/双漂移守卫/llms 冒烟);**脚本 workspace**(browser-workspace 实证:agent 拥有的运行时目录非包源码、钉数据根与代码根解耦、两类产物两个口(browser_helpers.py merge 覆写 + apps/<名>.py 即成一级命令 APP_ARGS)、apps 与管道代码同一 exec 运行时零 import 互见、包薄核 + 插件增量供给本地永不删、domain-skills 站点知识层、包管稳定内核 workspace 管长尾演化);落地清单九问(含逃生舱与归档两问)
- 接线:SKILL.md 意图路由加行、description 加触发词、篇数 20 改 21;references/README 三层同步(全量 22 篇);AGENTS 仓库地图 references 篇数 17 改 21(滞后校正)
- data/skill 副本同步(双漂移守卫)

### 变更（2026-09-04，第二十六批：browser-harness 0.6.12 复验与事实刷新）

> 上游 D:\browser-harness 更新至 v0.6.12(装态同版本);实弹复验搜索与抓取全过(google_search 3 条、example.com 抓取、维基 Feedback 78KB 正文一次过,此前四度超时的同页,新版导航 30s 预算生效)。

- tool-browser-harness.md:版本 0.6.9 到 0.6.12;helper 面补 `wait_for_render`(渲染态判官);连接模型补任务级浏览器隔离;坑表首行按 Issue #3 修复改写(三档超时 env 可配:BH_IPC_TIMEOUT 5s/BH_NAVIGATE_TIMEOUT 30s/BH_SCREENSHOT_TIMEOUT 60s;导航三态事件判定,unknown 如实上报不伪装)
- 注记:上游修复原则「事件驱动判状态(成功/失败/未知),超时只做无事件时的死锁兜底」与本仓第二十批事件驱动模型同构 [实证: 上游 CHANGELOG 0.6.10]
- env-environment.md 版本快照同步;data/skill 副本同步

### 变更（2026-09-04，第二十五批：环环相扣收口,体系骨架显式化 + 断链工具沉淀）

> 用户验收标准:skill 要形成环环相扣的框架体系。机械层:交叉引用断链扫描 0;结构层:骨架显式化为 SKILL.md 七层环扣表。

- SKILL.md 体系速览新增「体系骨架(七层环扣)」表:认知(六态+知行合一)/对话(双向问答)/流程(五步+阶梯)/探查(选型+工具管线)/执行(事件+超时)/验证(测试门禁+PE)/沉淀(分治+集成约束),与传动句「执行产事件、验证产反馈,沉淀转资产,资产生复利;吸收即提炼是入库口径」;核心思想补代谢链一句
- exp-sedimentation 集成约束节挂 flow-testing 交叉引用(约束与门禁同源)
- 新增 `.tools/md-ref-scan.py`(PEP 723 零依赖断链扫描,断链检查手拼二犯升格,沉淀铁律);pre-commit 接入(git 提交挡板 = md-guard --staged + md-ref-scan);.tools/README 登记
- ROADMAP 阶段三「断链扫描工具适配」翻已完成
- data/skill 副本同步

### 变更（2026-09-04，第二十四批：tool-selection 增发现层,awesome 清单与官方库搜索）

> 用户裁定:补各开发环境各领域的 awesome 清单与各语言官方库、GitHub 搜索方法,即「不知道叫什么」的发现层。

- tool-selection.md 新增「三、发现层」:awesome 清单用法(总索引 sindresorhus/awesome,领域清单 gh search 拿;**扫清单拿候选名再回三通道核稳度,清单是发现不是裁决**,清单自身也看 pushedAt)与官方库搜索表(Rust docs.rs/Python docs/Node api+MDN/pwsh Get-Command+Learn/Go pkg.go.dev);原三至五节顺延,决策树首行改走 awesome 入口
- references/README 条目描述同步;data/skill 副本同步

### 新增（2026-09-04，第二十三批：依赖选型探查手册,阶梯的落地方法）

> 用户裁定:阶梯是知,「怎么查到每一档」是行,没有探查方法阶梯空转;五栈(rust/python/powershell/node/typescript)大量库与仓可搜索研究。提炼自家族选型手册四篇:结构源仓 R005(Rust crates.io+GitHub 双通道)、R008(PyPI)、R009(PowerShell Gallery)、云 CLI 仓 R004(npm),骨架同构。

- 新增 `references/tool-selection.md`(第 20 篇):阶梯 2 到 5 档数据源表(本仓 rg/标准库文档/平台原生/已装清单);五栈三通道能力对照(差异即方法:PyPI 关键词仅网页、Gallery CLI 恒带显式仓、cargo search 镜像须 --registry);稳度四信号(下载/发版/维护者/License,启发式非门禁);GitHub 通道四步;防仿冒与单锁纪律;结论落 S 文档双通道各一条证据、装后跑最小用例(反馈)
- 接线:flow-workflow 阶梯 bullet 挂指针;tool-gh 选型双通道挂指针;SKILL.md 意图路由加行、篇数 20;references/README 三层同步(全量 21 篇);data/skill 副本同步

### 变更（2026-09-04，第二十二批：吸收 ponytail 最小实现阶梯）

> 信源:DietrichGebert/ponytail README 全文(raw 取回)。其基准数字经一次社区纠偏(#126,单发基线虚高)后自我修正为诚实口径(均值 54% 减码、安全 100%),与六态实证纪律同气。

- flow-workflow.md 拆步骤标准加两行:**最小实现阶梯**(不需要就跳过/本仓已有就复用/标准库、平台原生、已装依赖有就用/一行就一行/皆否才写够用的最小;小因为必要不是高尔夫)+ **阶梯两护栏**(懒于解不懒于读=反冥行妄作;最小不削安全,验证/错误处理/安全/无障碍不上砧板)
- 与既有体系映射确认:阶梯是「验证过的直接复用」的执行形态,未新增文件;references/README flow-workflow 条目描述同步
- data/skill 副本同步

### 变更（2026-09-04，第二十一批：全库自省,残留清剿与事实复验）

> 执行第二十批「吸收即提炼」裁定的自省后续:全 20 篇参考 + SKILL 通读复查,四查(冗余/啰嗦/跨文件重复/事实过时)。

- 扁平化残留三处:tool-project「references/tools/」与 flow-release 两处「tools/tool-*」改为扁平路径(第六批扁平化漏网)
- 版本事实复验(五工具实测):browser-harness 0.6.8 到 0.6.9、reader 0.4.0 到 0.5.0 刷新;gh 2.98.0/git 2.55.0/aria2 1.37.0/ome 0.1.0 复验无变化;tool-reader 篇内细节断言按六态诚实标注「0.4.0 版实证,待复验」
- tool-browser-harness 坑表补一行:web-fetch 子命令输出过 PowerShell 管道中文塌码,处理=管道脚本写 UTF-8 文件再读(本日两踩)
- 指针补齐:base-init 追问链指向 flow-inquiry;flow-workflow「先读文档再执行」改「纪律」(硬规则编号是本仓语境,对目标项目读者悬空)
- 通读结论:base-init/base-docs-directories/base-primitives/env-platform/flow-release/exp-pitfalls 及五工具篇密度合格,不动

### 新增（2026-09-04，第二十批：事件驱动模型吸收 + 吸收即提炼裁定与全库自省）

> 用户裁定(2026-09-04):吸收是提炼,大量无用与冗余信息须剔除,保最准确精练的上下文表达;立为硬规则并对全部文档自省。信源:熔断器维基全文、let-it-crash 原文(支付服务三返回态例证);EDP 维基与超时专文四度撞冷启动超时未取正文(题录级)。

- 新增 `references/flow-events.md`(第 19 篇):三态事件(成功/失败/未知,未知最危险且不等于失败);let it crash 监督者模式(未知态处理从业务代码剥离到监督层);超时兜底三选(幂等重试一次/换路径/放弃并记录);熔断三态(Closed/Open/Half-open,防重试风暴);与六态接口(成功=实证渠道、失败=错误路径、未知=中转态)
- 接线:flow-workflow 拆步骤标准加「等待有上限」;SKILL.md 意图路由加行、篇数 19;references/README 三层同步(全量 20 篇);data/skill 副本同步
- 硬规则 7「吸收即提炼」立规(AGENTS.md);base-writing-standards 写完自查加第 6 条;全库自省瘦身(flow-events/flow-testing/base-writing-standards 四节等剔除重复表述)

### 新增（2026-09-04，第十九批：测试流程规范吸收,双轴分层与五层正名）

> 提炼源:本地九仓实测(reader 仓 G006 六层体系、ome 源仓 R004 黄金文件与真机对齐、结构源仓 R004 双轴雏形、浏览器工具仓 R003 四层、云 CLI 仓冒烟矩阵与真钥验收、虚拟化仓 Pester 结构冒烟与 DryRun、主机环境仓 verify/heal 闭环与假绿防线、PVE 仓 dryrun 闸门、远端接入仓 doctor 哨兵);四路并行调研,文档引句与测试实盘双核对。

- 新增 `references/flow-testing.md`(第 18 篇):**双轴模型**(地基层=框架原生单元/集成/文档测试,意图层=冒烟/回归/验收/A-B 目的流程,两轴正交);五层正名表(每层归属轴、回答的问题、载体、时机);断言纪律七条(期望值独立来源禁重言式、只断稳定字段、正负例成对、错误路径覆盖等,家族各仓 AGENTS 逐字一致);跨栈载体速查(Rust/Python/TS/PowerShell 四栈);门禁时机谱(本地三件到批次到 CI 三系统到发版三路到 verify/heal 收尾,含假绿防线);特色机制八项(黄金文件 oracle、快照纪律、回归生长律、防漂移、DryRun 沙箱、A-B、验收即对照、六态衔接);AGENTS「写测试时」摘要条款
- 接线:flow-workflow 验收口径加测试分层调度行;base-primitives 义务表「写测试」行指向;SKILL.md 意图路由加行、篇数 18;references/README 三层同步(全量 19 篇)
- data/skill 内嵌副本同步(双漂移守卫)

### 新增（2026-09-04，第十八批：集成约束四形态落地,禁字二犯升格）

> 用户裁定(2026-09-04):重复犯的错误除规则与文档记录外必须有集成约束:Agent 的各种 HOOK 阻断或提醒、项目强制执行的 uv 运行时 python 脚本工具、git 提交事件的 HOOK 提醒、转换的回归测试用例。规则是知,约束是行。触发案:第十六/十七批新增文本连犯破折号禁字(各被 scan 当场抓住)。

- 教义:exp-sedimentation.md 升格节加「集成约束(二犯以上必配)」四形态与验收清单第 5 条;SKILL.md 意图路由、references/README 条目同步;data/skill 副本同步
- 形态一(agent hook):`.claude/settings.json` PostToolUse hook(Edit|Write|MultiEdit 到 `.tools/md-guard.py`,违规 exit 2 回传提醒);本会话实弹验证触发;.gitignore 改为忽略 `.claude/*` 但放行 `settings.json`(约束资产入库,其余仍为运行时状态)
- 形态二(uv 脚本门禁):`.tools/md-guard.py`(stdin hook 模式与 --staged 挡板模式;规则唯一权威在 `project_evo.mdfix`,与 scan/check PE-12 同源)+ `.tools/README.md` 清单
- 形态三(git 钩子):`githooks/pre-commit` 调 md-guard --staged,不过不进库;`git config core.hooksPath githooks` 已设;实测违规模板被挡(exit 1)、干净放行
- 形态四(回归测试):`tests/test_repo_md_clean.py` 仓内全量 md 禁字清零回归,CI 常驻;安装态自动跳过
- AGENTS.md 仓库地图补 `.tools/` 与 `githooks/` 两行;提交时 githooks/pre-commit 需 `git update-index --chmod=+x`(Windows 下保 exec 位)

### 变更（2026-09-04，第十七批：双向问答协议定型,吸收 grilling 拷问机制）

> 用户裁定(2026-09-04):对话模式定型为两式:你问我答(agent 拷问用户,收敛决策)与我问你答(用户咨询 agent,以问为种子扩充整理)。信源:mattpocock/skills 的 grilling SKILL.md(raw 取回,模板占位符经 blob 渲染页核对)。

- 新增 `references/flow-inquiry.md`(第 17 篇):你问我答四机制(设计树、前沿轮次=前置已定问题整轮齐问附推荐答案、事实/决策/实验三分流、无静默假设终止判据)+ 我问你答扩充式整理(用户裁定:以问为种子不断扩充追加所有关联详情,整理三步=种子扩散/人类组织/落位回写;自检三条=先读文档再答/答必六态/信源核实)+ 闭环 mermaid(两通道汇于方案,实验类走 PoC);实验三分与落位义务为超出 grilling 原文的扩展(原文只有事实/决策二分)
- flow-workflow.md:登记步追问链挂接拷问模式;base-primitives.md:文档义务表「追问链澄清」行注记(你问我答+轮次算法指向)
- SKILL.md:description 加双向问答触发词、意图路由加行、篇数 16 改 17;references/README.md:快速路由+场景索引+全量清单 18 篇同步
- data/templates/AGENTS.md:对话节补「对话分两式」摘要行(细则唯一权威在 skill)
- data/skill 内嵌副本同步(双漂移守卫)

### 变更（2026-09-04，第十六批：知行合一植入,六态理论升级与工作纪律落地）

> 理论裁定（用户 2026-09-04）:六态是知行合一的工程化,实证=知行合一态;五态为中转态,为进入实证服务;实证与经验循环,迭代复利;阳明术语（冥行妄作/悬空思索/着实去做/事上磨炼）进正式词汇。信源:王阳明知行合一双源核对（光明日报/人民网理论频道 + 中文维基,后者参考节引前者,独立性部分打折;核心引句双源吻合）。

- base-writing-standards.md:六态节重构为「知行合一的工程化」;两级结构（实证态一/中转态五）+ mermaid 六态流转图;用法升红线级:中转态标注义务（假设/推断附验证动作、记忆附复核点,不写即未完成）与收尾处置纪律（悬空升实证/留 research/注销,禁止滞留）;写完自查同步
- flow-workflow.md:新增「三、知行合一工作纪律」（反冥行妄作=不查不验就动手、反悬空思索=研究做完不落地（PoC 必落 poc\ 目录）、着实去做、事上磨炼）,原三至八节顺延重编号;验收通用口径补两条（悬空中转态处置、研究类目标验收看 PoC 产物）
- exp-sedimentation.md:成功经验链下新增「实证与经验的循环（迭代复利）」小节（mermaid + references 为循环固化形态）
- exp-pitfalls.md:P6 六态标记滥用补第三误读（中转态长期滞留）与正解同步
- SKILL.md:description 加知行合一触发词;意图路由与体系速览同步;references/README.md 三条目描述同步;verification PE-10 加手检注记（验证路径属语义判断,机检不做）
- data/skill 内嵌副本同步（双漂移守卫）;G001 模板六态节补一行
- 不动:checker/cli 不加新 PE 检查;AGENTS 硬规则与 ROADMAP 无涉

### 实测（2026-09-03,v0.1.0 后）

- 真实项目首装（remotex，已有部分体系的存量仓）：init 建 6 跳 5（幂等含 Windows 大小写碰撞保护）、check 诊断 8 PASS / 4 FAIL（均为存量文档真实差距：references 未登记新 INDEX、AGENTS 缺义务表、research 无六态、存量文档含 emoji）、skill 双落位安装 + gitignore 追加幂等；未触碰既有内容文件、未提交（目标仓自主裁决）

## [0.1.0] - 2026-09-03

首个版本，双形态交付：

- **渐进知识库 skill**:SKILL.md 意图路由 + references 分类扁平 17 篇 + verification 检查命令 13 条；吸收家族七仓 1148 提交的演化实践（经验分治、封版模式、平台适配、环境索引、17 条误区），全量六态标注并隐私脱敏
- **uv Python 工具**（project-evo，零运行时依赖）：init 骨架安装（幂等）/ check 诊断 PE-01 至 PE-13 / skill 项目级安装（.claude/skills 与通用 .agents/skills 双落位，内嵌全树 + 双漂移守卫 + agent 目录 gitignore 惯例）/ llms 索引；pytest 8 测全绿，端到端冒烟通过

### 开发批次明细（POC 期）

### 新增（2026-09-03，第十五批：update 自更新，参考 browser-harness 方式）

- `project-evo update [-y] [--repo o/r]`：双安装模式分派，git 模式（仓内 checkout）要求工作区干净后 `git pull --ff-only`；installed 模式走 `uv tool install --upgrade`（PEVO_GIT 环境变量切 git 源）
- 版本探测：GitHub Releases API（匿名，GH_TOKEN/GITHUB_TOKEN 可注入，超时离线返回 None 不阻塞）；semver 近似比较含 a/b/rc 预发布序
- 升级后 realign 提示：对已装项目重跑 `project-evo skill` 同步最新 skill 树
- pytest 增 3 测（版本序比较、离线容错、update 冒烟）至 11 测全绿；README/SKILL.md/llms 同步

### 修复（2026-09-03，第十四批：README 同步与 checker 围栏误判）

- README 四处同步：快速开始第 3 步改为 uv CLI 主入口（init/check,PowerShell 用例集降为等价）、目录树补 src/tests/pyproject、常用命令诊断组补 uv check、环境前提补 uv 运行时说明；清除全部 gh skill 表述
- checker 修复真 bug：PE-11 标题检查现**跳过围栏代码块内 # 注释行**（本仓 README 的 powershell 注释曾被误判）；新增回归测试
- AGENTS 三个真违规标题去括号（解释移标题下 > 引用行）；自家仓复诊 FAIL 6 降到 5，余项均为设计内（骨架仓检查项不适用于 skill 开发仓，verification 已注记 PE-01/02/03/08/09)
- pytest 9 测全绿

### 变更（2026-09-03，第十三批：README 按规范重写）

- 按标准 README 七段式重写：一句话定位（引用块）、快速开始 4 步（安装通道说明，替换过时 Copy-Item）、目录树（不含工作产物）、核心概念 6 术语、常用命令三分组（检索/验证/安装，标注副作用）、文档导航表（与 docs/README.md 同源）、环境前提（全部实测版本）
- 2.9KB，8KB 门禁内；快速开始与常用命令抽查实跑通过

### 变更（2026-09-03，第十二批：隐私脱敏）

- 用户裁定：skill 内不保留被吸收仓的名称与本机目录信息（隐私）
- 全仓脱敏：七个来源仓名替换为角色称谓（源头仓/结构源仓/ome 源仓/发布工程仓/云 CLI 仓/虚拟化仓/运行存储根等），本机路径替换为通用表述（环境根 EnvRoot/参照仓），外部调查 skill 引用去路径化
- 保留：公开工具名与接口（ome/OHMYENV_ROOT/browser-harness/reader/gh/git/aria2c）、提交哈希、日期与事实
- 经验标注降维：来源由「仓名+编号」改为「角色称谓」，六态语义不变

### 变更（2026-09-03，第十一批：家族三仓补读）

> 研究对象：云 CLI 仓（09-02 立项，TS/Node,omc CLI，最新完整形态）、虚拟化仓（08-03 生，家族最老祖先，先有工程后有体系，后期反向接入）、运行存储根（非 git 仓，运行存储数据根）。至此家族七仓全读。

- base-init.md 增 **agent-native CLI 的 SKILL.md 模式**（何时用 + 命令表指向 R 文档 + 管道代码逃生舱 + helper 双通道；bh/两仓同款）与 **存量仓接入迁移路径**（plans到proven 改名、补编号、AGENTS 四段重写、六态补标、引用替换、门禁接入；虚拟化仓实证序列）
- base-docs-directories.md:mistakes 单文件形态补最新仓实证（云 CLI 仓 09-02 仍单文件）；编号规则增**跨仓不对齐是常态**（G004 三义漂移实证，稳定的是类别语义非绝对号码）
- env-environment.md 增**代码根与数据根解耦**模式（ome EnvRoot / 运行存储根 StoreRoot / bh BH_HOME 三例）

### 变更（2026-09-03，第十批：源头仓 溯源吸收）

> 研究对象：源头仓（体系总源头，458 提交，2026-08-19 至 09-03；现行体系多数发明诞生于 08-29「文档体系重构：从流水账到状态驱动的统一标准」）。另发现家族未读仓：云 CLI 仓、虚拟化仓、运行存储根。

- base-primitives.md 增 AGENTS **8KB 大小软门禁**（超限下沉 references；家族实测 8.9-16.7KB，两仓被迫瘦身重构）与 **CHANGELOG/ROADMAP 粒度纪律**（只留版本级里程碑，源头曾细碎堆积后全删收敛）
- base-docs-directories.md mistakes 节增**演化路径**（单文件 MISTAKES.md 起步合法到膨胀拆 M1xx，源头实证）与 **diary/proven 出身注记**（08-29 一个 history 拆成两目录，分界即「流水 vs 方案」）
- flow-workflow.md 验收口径增**多轮独立 review**实践（多家 agent 无头轮换至缺陷清零，缺陷家族沉淀；源头三轮 kimi/codex/claude 实证）
- exp-pitfalls.md 增 P16（CHANGELOG 记流水）、P17（AGENTS 无限膨胀）

### 变更（2026-09-03，第九批：ome 源仓 对照优化）

> 研究对象：ome 源仓（ome CLI 源码仓，103 提交，08-31 从 源头仓 结构平移；轻量变体：三原语无 PRD、无 proven、编号平移留洞）。其 AGENTS 四段与 结构源仓 一致，印证第八批模板升级。

- base-docs-directories.md diary 节升级：概貌级口径纪律（防单文件膨胀）+ **收工自省五段模板**（概貌/关键裁决/得失/明日入口/环境）
- exp-pitfalls.md 增 P13-P15:PowerShell 批改中文 md 塌行（一律编辑工具）、口径类裁决先展示再落码（taxonomy 四轮返工）、对环境想当然（runner 预装/正则先验证）
- env-platform.md CI 节增「CI 文档门禁」：四件套同口径进 CI + 上岗三坑（uv 预装/GITHUB_PATH export 语义/Windows stdout cp1252)
- flow-release.md 增「门禁与实跑互补」纪律（首跑实整抓逻辑缺口，门禁全绿下的漏网实证）
- flow-workflow.md 增「八、跨仓协作」：姊妹仓校准、ISSUE 矩阵四形态（通报/依赖/提议/上报）、对齐清单、探查先行、规范跨仓统一
- base-init.md 裁剪原则增「轻量变体合法」（ome 源仓 实证样本）

### 新增（2026-09-03，第八批：三仓 git 史对照优化）

> 研究对象：结构源仓（203 提交，体系源头，09-03 文档体系重构）、reader 仓（97 提交）、PVE 仓（2 提交）；谱系 源头仓 到 结构源仓 到 reader 仓 到 PVE 仓/browser-harness，姊妹仓交替演化互相校准。

- 新增 `references/exp-sedimentation.md`（经验沉淀分治，源仓 G004 提炼）：成功/错误经验两条链、产生时机与检索路径、**二犯升格工作流**（错误经验的终点是变成正确工作流）、一条知识一个权威落位、[推断]/[假设] 禁止跳级进 references
- base-primitives.md AGENTS 模板三段 到 **四段**（加意图路由节）+ 摘要层铁律（一行摘要、细则唯一权威在 R 文档，双份并行必漂移，源仓 5 处失守实证）
- base-primitives.md INDEX 节增维护硬规则：**以磁盘为唯一事实源**、登记缺陷高发区（diary/.tools/src/编号段/断号）、断号注记、TODO 残表清退
- exp-pitfalls.md 增 P9-P12：双份并行膨胀、规范文件自违规（豁免态全绿是假象）、豁免退出顺序纪律、旧索引当重写底稿
- flow-workflow.md 归档步挂经验分治落位；SKILL.md 意图路由表增「经验沉淀/升格」行；references/README 增经验组（17 篇）

### 变更（2026-09-03，第七批：渐进知识库定型）

- 用户裁定三原则落地：**目录与文件名为 rg 检索设计；文档结构为 mq 提取设计；SKILL.md 只做意图路由与速览**
- 移除 `evals/` 层：本 skill 为渐进知识库型，不做用例评估；AGENTS 布局/索引/硬规则、README、docs/README、references/README、ROADMAP 同步
- SKILL.md 重写为「意图路由前置」：18 行意图到参考路由表、rg 定位 + mq 提取四层检索法、体系速览压缩；frontmatter description 改为渐进知识库语义
- references 分类 + 扁平化：文件名加类别前缀（base-/flow-/env-/tool-/exp-），16 篇前缀分组自然排序；全部交叉引用同步
- base-writing-standards.md 重构为「命名三层标准」：定位模型（目录名到文件名到标题三层检索接口，定位内容不需要读全文）、文件名标准、标题结构标准（mq 自检）、反模式清单
- 硬规则更新：「双层机器可读」（rg 检索 + mq 提取）替换原两类评估规则

### 变更（2026-09-03，第六批：references 扁平化）

- 用户裁定：去掉 howto/pitfalls/tools 分类子目录，`references/` 为扁平目录，README 即渐进索引路由
- `references/` 扁平为 16 篇（9 howto + 5 工具指南 + pitfalls.md + README);pitfalls/README.md 改 pitfalls.md,tools/ 索引并入主 README
- references/README.md 重写为三层渐进索引：快速路由（高频场景）到 场景索引（四维度分组）到 全量清单；含五工具定位与研究管线、检索方法
- 全部交叉引用同步（SKILL.md 详细参考、AGENTS.md 布局与索引、docs/README.md、project-tools/environment/pitfalls 内链）；代码调查 skill 外部路径保持原样
- 新参考文件登记义务改为「登记进 README 第三层全量清单」

### 新增（2026-09-03，第五批：环境索引与封版模式）

- `references/howto/environment.md`：环境依赖索引，ome（Oh My Env，全平台 Agent 依赖环境管理 CLI，v0.1.0 未封板）三态模型（locked/installed/path）、七域分组、命令面速查（query/pin/install/deploy/update/status/daily/verify/heal/doctor）、环境根布局、项目依赖路由规则（status 盘点到AGENTS 环境事实登记到verify/doctor 进门禁）、browser-harness 走 uv tool 的例外说明
- `references/howto/release.md`：封版发布模式，提炼自 reader 仓 R008 四轮发布实证：前置裁定（版本必前进/Unreleased 有货才封/semver 取舍）、三路全平台门禁（主开发机+各平台实机+CI，含阶段标记串与吞退出码纪律）、封版件五步一次提交、tag 触发（一致性闸）、发布验收（资产件数/sha256 抽查/self update 首验/收尾义务）
- workflow.md 归档步挂接 release.md;SKILL.md、references/README、docs/README 索引同步

### 新增（2026-09-03，第四批：平台适配维度）

- `references/howto/platform.md`：平台适配规范九节，shell 分平台约定（pwsh7/bash/zsh 与禁项）、编码与行尾（UTF-8/BOM/.gitattributes 钉 LF/禁手拼分隔符）、文档路径写法两制（Windows 主场反斜杠 vs 跨平台正斜杠，全仓统一）、脚本载体跨平台优先级（uv Python 默认）、命令双形态写法、CI 三系统门禁、接管开发验收清单（R004/R005 模式）、八工具平台速查、立项平台决策
- init.md:Step 2 增「目标平台矩阵」必问项；Step 5 验收清单增平台决策落地检查
- primitives.md:AGENTS 模板操作规则段补分平台 shell 约定（reader 仓 规则 2 口径）
- writing-standards.md：路径写法规则由 Windows 单制改为两制全仓统一
- git.md：「Windows 专项坑」扩为「平台坑」八条（补 macOS 大小写不敏感、exec bit、文件锁、二进制行尾误伤）
- browser-harness.md：脚本模式补 Linux/macOS heredoc 形态
- verification：复验前提注明 pwsh 7 跨平台 + bash 转写口径
- SKILL.md、references/README、docs/README 索引同步

### 变更（2026-09-03，第三批：工具指南实证深化）

- reader.md 新增「环境变量」节：全量 env 面源码实证（READER_OCR_CACHE_DIR 含三平台默认值逻辑、READER_OCR_MODEL_SIZE 只认 tiny/small、GH_TOKEN for self update;ocr.rs/selfupdate.rs 逐行核对），消除上一批遗留的 [经验] 待验项
- gh.md 零节重写：吸收 代码调查 skill 五轮实测速查表（定位决策表、两级 sha 链机制、六条搜索陷阱），标注经验来源
- git.md 零节重写：吸收 git-forensics-guide(pickaxe -S/-G 分工、blame -L/log -L、bisect、ls-remote 与浅/稀疏克隆、五工具搜索边界表）
- aria2c.md 参数表全部实证重写（`aria2c --help=#all` 1767 行核对，含默认值）；新增帮助命令技巧（裸 --help 只出第一页）
- browser-harness.md 新增「零点五、脚本 helper 面」（源码 helpers.py def 清单实证）；定位改为搜索引擎与网页抓取优先
- 素材来源：代码调查 skill skill howto(gh-search-cheatsheet/git-forensics-guide）、D：\reader 仓 与 浏览器工具仓 源码、gh 与 aria2c 命令帮助

### 新增（2026-09-03，第二批：项目工具维度）

- `skills/project-evo/references/howto/project-tools.md`：项目工具约定，`.tools/` uv 运行时 Python 脚本（PEP 723 头、`uv run --script`、归档规则、沉淀铁律）+ 外部工具路由表
- `skills/project-evo/references/tools/`：外部标准工具指南五篇（gh 2.98.0 / git 2.55.0 / browser-harness 0.6.8 / reader 0.4.0 / aria2 1.37.0，版本均本机实证）+ README 索引与快速路由
- 五工具定位按用户裁定对齐：gh=搜索代码和项目仓库、git=本地 clone 研究代码仓库、browser-harness=搜索引擎和网页抓取、reader=读取本地文档电子书参考资料、aria2c=下载任意资料；gh/git/browser-harness 增设「零节」承载首要场景，README 与 project-tools 路由表增研究管线视角（发现到获取到研读）
- 自验修正：browser-harness.md 移除 emoji 违规（马形标记改文字描述）
- SKILL.md、references/README.md、docs/README.md 同步登记

### 新增（2026-09-03，第一批：骨架成型）

- `skills/project-evo/SKILL.md`:skill 概览层（定位与进化闭环、文件地图、编号体系、六目录、五步工作流、六态标记）
- `skills/project-evo/references/`:howto 五篇（primitives / docs-directories / workflow / writing-standards / init)+ pitfalls（已知误区）+ README 索引
- `skills/project-evo/verification/command-test-cases.md`：骨架规范检查命令（参数化 `$ProjectRoot`）
- `skills/project-evo/evals/evals.json`:skill 质量评估用例 4 条
- 仓库层：AGENTS.md（唯一权威源）、CLAUDE.md（一行桥接）、README.md、ROADMAP.md、.gitignore、docs/README.md（文档地图）

### 变更（2026-09-03)

- skill 由单文件 `SKILL.md` 重构为 skill 规范仓 三层布局（SKILL.md 概览 + references/howto 详参 + verification/evals 两类评估）
- skill 命名 `project-docs` 到 `project-evo`（项目进化），description 增加进化闭环触发词
- proven 语义修正：明确为**完全成功的 plan 方案归档**（立项建方案、完成回填），非里程碑/成果列表 [经验： 用户裁定]

### 移除（2026-09-03)

- 撤回用户级安装副本（`~/.claude/skills/project-evo`）与项目内 `.claude/skills/` 副本；源码唯一位置改为 `skills/project-evo/`
