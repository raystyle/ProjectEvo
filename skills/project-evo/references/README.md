# project-evo 参考知识体系(渐进索引)

> `references/` 是**分类 + 扁平**目录:文件名 = 类别前缀 + 主题词(base/flow/env/tool/exp),目录与命名以 rg 检索为先——`rg --files references | rg <主题词>` 直接命中;每篇一个主题、自包含完整参考。本 README 是唯一路由入口,三层渐进:快速路由 → 场景索引 → 全量清单;新参考文件建成后登记进第三层。

## 一、快速路由(高频场景 → 文档)

| 我要… | 看哪篇 |
| --- | --- |
| 在新项目落地骨架 | [base-init.md](base-init.md) |
| 建根原语 / 写 AGENTS | [base-primitives.md](base-primitives.md) |
| 决定文档放哪个目录 / 写方案 | [base-docs-directories.md](base-docs-directories.md) |
| 推进一个目标 / 踩坑就地纠偏 | [flow-workflow.md](flow-workflow.md) |
| 写任何文档前 | [base-writing-standards.md](base-writing-standards.md) |
| 发一个版本 | [flow-release.md](flow-release.md) |
| 落地前预警 / 踩坑对照 | [exp-pitfalls.md](exp-pitfalls.md) |

## 二、场景索引(按工作维度)

### 项目骨架与规范

- [base-primitives.md](base-primitives.md) - 根原语详解(PRD/GOAL/PLAN/TODO/INDEX/AGENTS 职责、模板头、文档义务表、分平台 shell 约定)
- [base-docs-directories.md](base-docs-directories.md) - docs 六目录精确定义、proven/references/guide 分界口诀、方案模板、编号规则
- [base-writing-standards.md](base-writing-standards.md) - 写作规范(文件名即标题、标题干净、六态完整定义、路径两制、门禁选配)
- [base-init.md](base-init.md) - 初始化五步、关键问题清单、裁剪原则、验收清单、跨项目适配参考

### 工作流与发布

- [flow-workflow.md](flow-workflow.md) - 五步工作流(登记→立项→执行→验收→归档)、拆步骤标准、优先级取舍、自修正闭环、沉淀铁律
- [flow-release.md](flow-release.md) - 封版发布模式:前置裁定、三路全平台门禁、封版件、tag 触发、发布验收(reader 仓 R008 模式)

### 平台与环境

- [env-platform.md](env-platform.md) - 平台适配:shell 分平台、编码行尾、文档路径两制、脚本载体、CI 三系统门禁、接管验收清单
- [env-environment.md](env-environment.md) - 环境依赖索引:ome(Oh My Env)三态模型、命令面速查、七域分组、依赖路由规则、换机重建

### 工具

- [tool-project.md](tool-project.md) - 项目工具:`.tools/` uv 运行时 Python 脚本约定(PEP 723)、归档规则、沉淀铁律、外部工具路由
- [tool-gh.md](tool-gh.md) - 搜索代码和项目仓库(release 管理其次):定位决策表、两级 sha 链、搜索陷阱
- [tool-git.md](tool-git.md) - 本地 clone 研究代码仓库(版本控制其次):拉取策略、pickaxe/blame/bisect、平台坑
- [tool-browser-harness.md](tool-browser-harness.md) - 搜索引擎和网页抓取:helper 面、AX 树定位、坐标点击、后台 tab 坑
- [tool-reader.md](tool-reader.md) - 读取本地文档/电子书:三子命令、OCR 兜底、mq 查询、环境变量
- [tool-aria2c.md](tool-aria2c.md) - 下载任意资料:参数表(--help=#all 实证)、断点续传、校验

### 经验

- [exp-pitfalls.md](exp-pitfalls.md) - 已知误区十七条(proven 语义、双份漂移、豁免退出、索引底稿、批改塌行、口径返工、环境想当然、CHANGELOG 流水、AGENTS 膨胀等)
- [exp-sedimentation.md](exp-sedimentation.md) - 经验沉淀分治:成功/错误两条链、产生时机与检索路径、二犯升格工作流(结构源仓 G004 模式)

> 五工具定位(用户裁定):gh=搜索代码和项目仓库;git=本地 clone 研究代码仓库;browser-harness=搜索引擎和网页抓取;reader=读取本地文档电子书参考资料;aria2c=下载任意资料。研究管线:**发现**(gh/browser-harness)→ **获取**(git/aria2c)→ **研读**(reader/browser-harness)→ 结论落 `docs/research/` 标六态。

## 三、全量清单(17 篇)

| 文件 | 主题 |
| --- | --- |
| base-init.md | 初始化流程与跨项目适配 |
| base-primitives.md | 根原语详解与模板头 |
| base-docs-directories.md | 六目录定义与方案模板 |
| flow-workflow.md | 五步工作流与自修正闭环 |
| base-writing-standards.md | 写作规范与六态 |
| flow-release.md | 封版发布模式 |
| env-platform.md | 三平台适配 |
| env-environment.md | 环境依赖索引(ome) |
| tool-project.md | 项目工具约定与路由 |
| exp-pitfalls.md | 已知误区十七条 |
| exp-sedimentation.md | 经验沉淀分治细则 |
| tool-gh.md / tool-git.md / tool-browser-harness.md / tool-reader.md / tool-aria2c.md | 五工具指南 |
| README.md | 本索引 |

另有仓内姊妹件:`../verification/command-test-cases.md`(规范检查命令)。

## 检索方法

目录与文件名为 rg 检索设计(前缀=类别词、主干=主题词);文档结构为 mq 提取设计(h2=节、code=命令、表格=键值)。

```powershell
rg --files . | rg 关键词                    # 1 文件名定位(类别词/主题词)
rg -n "关键词" README.md                    # 2 索引导航
rg -n "关键词" . --glob "!README.md"        # 3 全文搜
reader query <文件> ".h2"                    # 4 结构化提取节目录
reader query <文件> ".code"                  #    只抽命令
```
