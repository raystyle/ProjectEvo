# project-evo 命令行为验证用例集（（1） 工具/命令行为评估）

> project-evo 是文档体系 skill，无外部命令；本文件用「规范检查命令」验证一个项目是否遵守 project-evo 骨架。
> 用例均参数化 `$ProjectRoot`（默认指向本仓库自身，也能指向任意目标项目复用）。
> 每条可直接复制复验。

---

## 一、骨架结构验证

```powershell
# 前置:设定目标项目根(须为采用 project-evo 骨架的项目)
# 注意:本 skill 的开发仓(D:\ProjectEvo)自身是 skill 规范仓 布局,不适用 PE-01/02/03/09
$ProjectRoot = "D:\目标项目"
Set-Location $ProjectRoot

# [PE-01] 根六原语齐全(AGENTS/PRD/GOAL/PLAN/TODO/INDEX)
"AGENTS.md","PRD.md","GOAL.md","PLAN.md","TODO.md","INDEX.md" | Where-Object { -not (Test-Path $_) }
# 预期: 空结果(六件全在)

# [PE-02] docs 六目录齐全
"proven","diary","research","references","guide","mistakes" | ForEach-Object { "docs\$_" } | Where-Object { -not (Test-Path $_) }
# 预期: 空结果

# [PE-03] 方案模板在位
Test-Path "docs\guide\template.md"
# 预期: True

# [PE-04] CLAUDE.md 一行桥接
(Get-Content CLAUDE.md).Count
# 预期: 1(仅 @AGENTS.md)
```

## 二、编号与登记验证

```powershell
# [PE-05] 编号文件名规范(编号目录无空格/括号/冒号)
Get-ChildItem docs -Recurse -File -Filter *.md | Where-Object { $_.Name -match '[()\s:]' -and $_.Name -ne "template.md" } | Select-Object Name
# 预期: 空结果

# [PE-06] P 编号连续且四位(proven 有文档时)
Get-ChildItem docs\proven -File | ForEach-Object { if ($_ -notmatch '^P\d{4}-') { $_.Name } }
# 预期: 空结果(或目录为空)

# [PE-07] docs 编号文档均已登记 INDEX
$indexed = (Get-Content INDEX.md -Raw); Get-ChildItem docs -Recurse -File | Where-Object { $_.Name -ne "template.md" -and $_.Name -notmatch '^\d{4}-\d{2}-\d{2}-' -and -not $indexed.Contains($_.Name) } | Select-Object Name
# 预期: 空结果(所有编号文档名出现在 INDEX 中)
```

## 三、内容规范验证

```powershell
# [PE-08] AGENTS 含文档义务表
rg -c "义务" AGENTS.md
# 预期: ≥ 1

# [PE-09] PRD 与 GOAL 互指(D01 出现在两文件)
rg -c "D01" PRD.md; rg -c "D01|建立" GOAL.md
# 预期: 各 ≥ 1

# [PE-10] 六态标记在研究/方案文档中出现(有此类文档时)
rg -l "\[实证:|\[推断:|\[经验:|\[假设:" docs
# 预期: 非空(research/proven 至少一篇带标记)

# [PE-11] 标题禁括号(正文 markdown 标题行)
rg -n "^#+ .*[()]" docs AGENTS.md README.md
# 预期: 空结果(引用块 > 与正文不算)

# [PE-12] 四类禁字(emoji/破折号/箭头;豁免区感知)
rg -n "[\x{2600}-\x{27BF}\x{1F000}-\x{1FAFF}\x{2705}\x{26A0}]" AGENTS.md README.md CHANGELOG.md ROADMAP.md docs skills -g "*.md"
# 预期: 空结果
```

## 四、断链验证

```powershell
# [PE-13] INDEX 提到的本仓文件真实存在(粗检:提取反引号路径逐个 Test-Path)
$misses = Select-String -Path INDEX.md -Pattern '`([\w\-\\/\.]+\.(?:md|rs|py|toml))`' -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique | Where-Object { -not (Test-Path $_) }
$misses
# 预期: 空结果(INDEX 中引用的文件全部在位;有扫描脚本则优先用脚本)
```

---

## 复验前提

- **pwsh 7 跨平台**（Windows/Linux/macOS 均可装）；rg（ripgrep）在 PATH。本用例集以 pwsh 书写，三平台同跑；纯 bash 环境按语义转写（`Test-Path`到`test -f`，数组遍历到`for`，rg 用法不变）
- 用例对「最小集」项目：PE-06/PE-10 在对应目录为空时跳过不算失败
- 目标项目若裁剪（如 research 缓建）：PE-02 相应目录豁免，须在项目 AGENTS 注明裁剪决定
- 平台差异（路径分隔符、大小写敏感文件系统）以目标项目 G001 声明的路径写法为准（见 env-platform.md 三节）
