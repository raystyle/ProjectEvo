# Changelog

本文件记录 project-evo skill 及本仓库的所有可交付变更。格式:新增/变更/修复/移除 + 日期;先写 `[Unreleased]`,发布时转版本(git tag)。

## [Unreleased]

### 实测(2026-09-03,v0.1.0 后)

- 真实项目首装(remotex,已有部分体系的存量仓):init 建 6 跳 5(幂等含 Windows 大小写碰撞保护)、check 诊断 8 PASS / 4 FAIL(均为存量文档真实差距:references 未登记新 INDEX、AGENTS 缺义务表、research 无六态、存量文档含 emoji)、skill 双落位安装 + gitignore 追加幂等;未触碰既有内容文件、未提交(目标仓自主裁决)

## [0.1.0] - 2026-09-03

首个版本,双形态交付:

- **渐进知识库 skill**:SKILL.md 意图路由 + references 分类扁平 17 篇 + verification 检查命令 13 条;吸收家族七仓 1148 提交的演化实践(经验分治、封版模式、平台适配、环境索引、17 条误区),全量六态标注并隐私脱敏
- **uv Python 工具**(project-evo,零运行时依赖):init 骨架安装(幂等)/ check 诊断 PE-01 至 PE-13 / skill 项目级安装(.claude/skills 与通用 .agents/skills 双落位,内嵌全树 + 双漂移守卫 + agent 目录 gitignore 惯例)/ llms 索引;pytest 8 测全绿,端到端冒烟通过

### 开发批次明细(POC 期)

### 新增(2026-09-03,第十五批:update 自更新,参考 browser-harness 方式)

- `project-evo update [-y] [--repo o/r]`:双安装模式分派——git 模式(仓内 checkout)要求工作区干净后 `git pull --ff-only`;installed 模式走 `uv tool install --upgrade`(PEVO_GIT 环境变量切 git 源)
- 版本探测:GitHub Releases API(匿名,GH_TOKEN/GITHUB_TOKEN 可注入,超时离线返回 None 不阻塞);semver 近似比较含 a/b/rc 预发布序
- 升级后 realign 提示:对已装项目重跑 `project-evo skill` 同步最新 skill 树
- pytest 增 3 测(版本序比较、离线容错、update 冒烟)至 11 测全绿;README/SKILL.md/llms 同步

### 修复(2026-09-03,第十四批:README 同步与 checker 围栏误判)

- README 四处同步:快速开始第 3 步改为 uv CLI 主入口(init/check,PowerShell 用例集降为等价)、目录树补 src/tests/pyproject、常用命令诊断组补 uv check、环境前提补 uv 运行时说明;清除全部 gh skill 表述
- checker 修复真 bug:PE-11 标题检查现**跳过围栏代码块内 # 注释行**(本仓 README 的 powershell 注释曾被误判);新增回归测试
- AGENTS 三个真违规标题去括号(解释移标题下 > 引用行);自家仓复诊 FAIL 6 降到 5,余项均为设计内(骨架仓检查项不适用于 skill 开发仓,verification 已注记 PE-01/02/03/08/09)
- pytest 9 测全绿

### 变更(2026-09-03,第十三批:README 按规范重写)

- 按标准 README 七段式重写:一句话定位(引用块)、快速开始 4 步(安装通道说明,替换过时 Copy-Item)、目录树(不含工作产物)、核心概念 6 术语、常用命令三分组(检索/验证/安装,标注副作用)、文档导航表(与 docs/README.md 同源)、环境前提(全部实测版本)
- 2.9KB,8KB 门禁内;快速开始与常用命令抽查实跑通过

### 变更(2026-09-03,第十二批:隐私脱敏)

- 用户裁定:skill 内不保留被吸收仓的名称与本机目录信息(隐私)
- 全仓脱敏:七个来源仓名替换为角色称谓(源头仓/结构源仓/ome 源仓/发布工程仓/云 CLI 仓/虚拟化仓/运行存储根等),本机路径替换为通用表述(环境根 EnvRoot/参照仓),外部调查 skill 引用去路径化
- 保留:公开工具名与接口(ome/OHMYENV_ROOT/browser-harness/reader/gh/git/aria2c)、提交哈希、日期与事实
- 经验标注降维:来源由「仓名+编号」改为「角色称谓」,六态语义不变

### 变更(2026-09-03,第十一批:家族三仓补读)

> 研究对象:云 CLI 仓(09-02 立项,TS/Node,omc CLI,最新完整形态)、虚拟化仓(08-03 生,家族最老祖先——先有工程后有体系,后期反向接入)、运行存储根(非 git 仓,运行存储数据根)。至此家族七仓全读。

- base-init.md 增 **agent-native CLI 的 SKILL.md 模式**(何时用 + 命令表指向 R 文档 + 管道代码逃生舱 + helper 双通道;bh/两仓同款)与 **存量仓接入迁移路径**(plans→proven 改名、补编号、AGENTS 四段重写、六态补标、引用替换、门禁接入;虚拟化仓实证序列)
- base-docs-directories.md:mistakes 单文件形态补最新仓实证(云 CLI 仓 09-02 仍单文件);编号规则增**跨仓不对齐是常态**(G004 三义漂移实证——稳定的是类别语义非绝对号码)
- env-environment.md 增**代码根与数据根解耦**模式(ome EnvRoot / 运行存储根 StoreRoot / bh BH_HOME 三例)

### 变更(2026-09-03,第十批:源头仓 溯源吸收)

> 研究对象:源头仓(体系总源头,458 提交,2026-08-19 至 09-03;现行体系多数发明诞生于 08-29「文档体系重构:从流水账到状态驱动的统一标准」)。另发现家族未读仓:云 CLI 仓、虚拟化仓、运行存储根。

- base-primitives.md 增 AGENTS **8KB 大小软门禁**(超限下沉 references;家族实测 8.9-16.7KB,两仓被迫瘦身重构)与 **CHANGELOG/ROADMAP 粒度纪律**(只留版本级里程碑,源头曾细碎堆积后全删收敛)
- base-docs-directories.md mistakes 节增**演化路径**(单文件 MISTAKES.md 起步合法→膨胀拆 M1xx,源头实证)与 **diary/proven 出身注记**(08-29 一个 history 拆成两目录,分界即「流水 vs 方案」)
- flow-workflow.md 验收口径增**多轮独立 review**实践(多家 agent 无头轮换至缺陷清零,缺陷家族沉淀;源头三轮 kimi/codex/claude 实证)
- exp-pitfalls.md 增 P16(CHANGELOG 记流水)、P17(AGENTS 无限膨胀)

### 变更(2026-09-03,第九批:ome 源仓 对照优化)

> 研究对象:ome 源仓(ome CLI 源码仓,103 提交,08-31 从 源头仓 结构平移;轻量变体:三原语无 PRD、无 proven、编号平移留洞)。其 AGENTS 四段与 结构源仓 一致,印证第八批模板升级。

- base-docs-directories.md diary 节升级:概貌级口径纪律(防单文件膨胀)+ **收工自省五段模板**(概貌/关键裁决/得失/明日入口/环境)
- exp-pitfalls.md 增 P13-P15:PowerShell 批改中文 md 塌行(一律编辑工具)、口径类裁决先展示再落码(taxonomy 四轮返工)、对环境想当然(runner 预装/正则先验证)
- env-platform.md CI 节增「CI 文档门禁」:四件套同口径进 CI + 上岗三坑(uv 预装/GITHUB_PATH export 语义/Windows stdout cp1252)
- flow-release.md 增「门禁与实跑互补」纪律(首跑实整抓逻辑缺口,门禁全绿下的漏网实证)
- flow-workflow.md 增「八、跨仓协作」:姊妹仓校准、ISSUE 矩阵四形态(通报/依赖/提议/上报)、对齐清单、探查先行、规范跨仓统一
- base-init.md 裁剪原则增「轻量变体合法」(ome 源仓 实证样本)

### 新增(2026-09-03,第八批:三仓 git 史对照优化)

> 研究对象:结构源仓(203 提交,体系源头,09-03 文档体系重构)、reader 仓(97 提交)、PVE 仓(2 提交);谱系 源头仓 → 结构源仓 → reader 仓 → PVE 仓/browser-harness,姊妹仓交替演化互相校准。

- 新增 `references/exp-sedimentation.md`(经验沉淀分治,源仓 G004 提炼):成功/错误经验两条链、产生时机与检索路径、**二犯升格工作流**(错误经验的终点是变成正确工作流)、一条知识一个权威落位、[推断]/[假设] 禁止跳级进 references
- base-primitives.md AGENTS 模板三段 → **四段**(加意图路由节)+ 摘要层铁律(一行摘要、细则唯一权威在 R 文档,双份并行必漂移——源仓 5 处失守实证)
- base-primitives.md INDEX 节增维护硬规则:**以磁盘为唯一事实源**、登记缺陷高发区(diary/.tools/src/编号段/断号)、断号注记、TODO 残表清退
- exp-pitfalls.md 增 P9-P12:双份并行膨胀、规范文件自违规(豁免态全绿是假象)、豁免退出顺序纪律、旧索引当重写底稿
- flow-workflow.md 归档步挂经验分治落位;SKILL.md 意图路由表增「经验沉淀/升格」行;references/README 增经验组(17 篇)

### 变更(2026-09-03,第七批:渐进知识库定型)

- 用户裁定三原则落地:**目录与文件名为 rg 检索设计;文档结构为 mq 提取设计;SKILL.md 只做意图路由与速览**
- 移除 `evals/` 层:本 skill 为渐进知识库型,不做用例评估;AGENTS 布局/索引/硬规则、README、docs/README、references/README、ROADMAP 同步
- SKILL.md 重写为「意图路由前置」:18 行意图→参考路由表、rg 定位 + mq 提取四层检索法、体系速览压缩;frontmatter description 改为渐进知识库语义
- references 分类 + 扁平化:文件名加类别前缀(base-/flow-/env-/tool-/exp-),16 篇前缀分组自然排序;全部交叉引用同步
- base-writing-standards.md 重构为「命名三层标准」:定位模型(目录名→文件名→标题三层检索接口,定位内容不需要读全文)、文件名标准、标题结构标准(mq 自检)、反模式清单
- 硬规则更新:「双层机器可读」(rg 检索 + mq 提取)替换原两类评估规则

### 变更(2026-09-03,第六批:references 扁平化)

- 用户裁定:去掉 howto/pitfalls/tools 分类子目录,`references/` 为扁平目录,README 即渐进索引路由
- `references/` 扁平为 16 篇(9 howto + 5 工具指南 + pitfalls.md + README);pitfalls/README.md 改 pitfalls.md,tools/ 索引并入主 README
- references/README.md 重写为三层渐进索引:快速路由(高频场景)→ 场景索引(四维度分组)→ 全量清单;含五工具定位与研究管线、检索方法
- 全部交叉引用同步(SKILL.md 详细参考、AGENTS.md 布局与索引、docs/README.md、project-tools/environment/pitfalls 内链);代码调查 skill 外部路径保持原样
- 新参考文件登记义务改为「登记进 README 第三层全量清单」

### 新增(2026-09-03,第五批:环境索引与封版模式)

- `references/howto/environment.md`:环境依赖索引——ome(Oh My Env,全平台 Agent 依赖环境管理 CLI,v0.1.0 未封板)三态模型(locked/installed/path)、七域分组、命令面速查(query/pin/install/deploy/update/status/daily/verify/heal/doctor)、环境根布局、项目依赖路由规则(status 盘点→AGENTS 环境事实登记→verify/doctor 进门禁)、browser-harness 走 uv tool 的例外说明
- `references/howto/release.md`:封版发布模式——提炼自 reader 仓 R008 四轮发布实证:前置裁定(版本必前进/Unreleased 有货才封/semver 取舍)、三路全平台门禁(主开发机+各平台实机+CI,含阶段标记串与吞退出码纪律)、封版件五步一次提交、tag 触发(一致性闸)、发布验收(资产件数/sha256 抽查/self update 首验/收尾义务)
- workflow.md 归档步挂接 release.md;SKILL.md、references/README、docs/README 索引同步

### 新增(2026-09-03,第四批:平台适配维度)

- `references/howto/platform.md`:平台适配规范九节——shell 分平台约定(pwsh7/bash/zsh 与禁项)、编码与行尾(UTF-8/BOM/.gitattributes 钉 LF/禁手拼分隔符)、文档路径写法两制(Windows 主场反斜杠 vs 跨平台正斜杠,全仓统一)、脚本载体跨平台优先级(uv Python 默认)、命令双形态写法、CI 三系统门禁、接管开发验收清单(R004/R005 模式)、八工具平台速查、立项平台决策
- init.md:Step 2 增「目标平台矩阵」必问项;Step 5 验收清单增平台决策落地检查
- primitives.md:AGENTS 模板操作规则段补分平台 shell 约定(reader 仓 规则 2 口径)
- writing-standards.md:路径写法规则由 Windows 单制改为两制全仓统一
- git.md:「Windows 专项坑」扩为「平台坑」八条(补 macOS 大小写不敏感、exec bit、文件锁、二进制行尾误伤)
- browser-harness.md:脚本模式补 Linux/macOS heredoc 形态
- verification:复验前提注明 pwsh 7 跨平台 + bash 转写口径
- SKILL.md、references/README、docs/README 索引同步

### 变更(2026-09-03,第三批:工具指南实证深化)

- reader.md 新增「环境变量」节:全量 env 面源码实证(READER_OCR_CACHE_DIR 含三平台默认值逻辑、READER_OCR_MODEL_SIZE 只认 tiny/small、GH_TOKEN for self update;ocr.rs/selfupdate.rs 逐行核对),消除上一批遗留的 [经验] 待验项
- gh.md 零节重写:吸收 代码调查 skill 五轮实测速查表(定位决策表、两级 sha 链机制、六条搜索陷阱),标注经验来源
- git.md 零节重写:吸收 git-forensics-guide(pickaxe -S/-G 分工、blame -L/log -L、bisect、ls-remote 与浅/稀疏克隆、五工具搜索边界表)
- aria2c.md 参数表全部实证重写(`aria2c --help=#all` 1767 行核对,含默认值);新增帮助命令技巧(裸 --help 只出第一页)
- browser-harness.md 新增「零点五、脚本 helper 面」(源码 helpers.py def 清单实证);定位改为搜索引擎与网页抓取优先
- 素材来源:代码调查 skill skill howto(gh-search-cheatsheet/git-forensics-guide)、D:\reader 仓 与 浏览器工具仓 源码、gh 与 aria2c 命令帮助

### 新增(2026-09-03,第二批:项目工具维度)

- `skills/project-evo/references/howto/project-tools.md`:项目工具约定——`.tools/` uv 运行时 Python 脚本(PEP 723 头、`uv run --script`、归档规则、沉淀铁律)+ 外部工具路由表
- `skills/project-evo/references/tools/`:外部标准工具指南五篇(gh 2.98.0 / git 2.55.0 / browser-harness 0.6.8 / reader 0.4.0 / aria2 1.37.0,版本均本机实证)+ README 索引与快速路由
- 五工具定位按用户裁定对齐:gh=搜索代码和项目仓库、git=本地 clone 研究代码仓库、browser-harness=搜索引擎和网页抓取、reader=读取本地文档电子书参考资料、aria2c=下载任意资料;gh/git/browser-harness 增设「零节」承载首要场景,README 与 project-tools 路由表增研究管线视角(发现→获取→研读)
- 自验修正:browser-harness.md 移除 emoji 违规(马形标记改文字描述)
- SKILL.md、references/README.md、docs/README.md 同步登记

### 新增(2026-09-03,第一批:骨架成型)

- `skills/project-evo/SKILL.md`:skill 概览层(定位与进化闭环、文件地图、编号体系、六目录、五步工作流、六态标记)
- `skills/project-evo/references/`:howto 五篇(primitives / docs-directories / workflow / writing-standards / init)+ pitfalls(已知误区)+ README 索引
- `skills/project-evo/verification/command-test-cases.md`:骨架规范检查命令(参数化 `$ProjectRoot`)
- `skills/project-evo/evals/evals.json`:skill 质量评估用例 4 条
- 仓库层:AGENTS.md(唯一权威源)、CLAUDE.md(一行桥接)、README.md、ROADMAP.md、.gitignore、docs/README.md(文档地图)

### 变更(2026-09-03)

- skill 由单文件 `SKILL.md` 重构为 skill 规范仓 三层布局(SKILL.md 概览 + references/howto 详参 + verification/evals 两类评估)
- skill 命名 `project-docs` → `project-evo`(项目进化),description 增加进化闭环触发词
- proven 语义修正:明确为**完全成功的 plan 方案归档**(立项建方案、完成回填),非里程碑/成果列表 [经验: 用户裁定]

### 移除(2026-09-03)

- 撤回用户级安装副本(`~/.claude/skills/project-evo`)与项目内 `.claude/skills/` 副本;源码唯一位置改为 `skills/project-evo/`
