# git — 版本控制操作规范

> 定位:**本地 clone 研究代码仓库**(用户裁定)+ 项目版本控制的协作约定(提交规范、tag 发布、Windows 坑)。本机 git 2.55.0.windows.4 [实证: 2026-09-03 `git --version`]。

## 零、clone 研究代码仓库(首要场景)

### 拉取策略

```powershell
git clone --depth 1 https://github.com/owner/repo.git     # 最新快照(只要现状)
git clone --depth 50 <url>                                 # 浅历史(要近期脉络)
git clone --filter=blob:none --no-checkout <url>           # 只拿历史结构,按需取 blob
git clone --depth 1 --branch v0.4.0 <url>                  # 只要某分支/Tag
git sparse-checkout set src/ocr                            # 稀疏检出某目录
git ls-remote --tags <url>                                 # 不 clone 先看远程 tag
```

> 提醒:`--filter=blob:none` 拿不到文件内容,此时用 gh 的 contents/blob API 按需反查;**要跑 pickaxe/blame 溯源必须完整历史**。 [经验: 代码调查 skill git-forensics-guide 同款结论]

### 研究姿势(摸底 → 溯源)

```powershell
# 摸底
git log --oneline -15                     # 近期演进脉络
git ls-files / git ls-tree -r --name-only HEAD   # 文件清单/版本树
git grep -n "needs_ocr"                   # 仓内全文检索(比 gh search code 更全、无配额)
git grep -n "<symbol>" <rev>              # 指定历史版本的内容搜索

# 溯源(何时引入/谁改的/怎么演变)
git log -S"<symbol>" --oneline -- <path>  # pickaxe:该字符串出现次数变化的 commit
git log -G"<regex>" --oneline -- <path>   # diff 内容匹配(更全但更吵)
git blame -L 120,140 <path>               # 关键行归属(附 commit/作者/日期)
git blame -w -C -C <path>                 # 忽略空白,追踪跨文件移动
git log -L 120,140:<path> --oneline       # 整段代码的完整演进(高级 blame)
git show --stat <sha>                     # 某提交改了哪些文件
git tag --contains <sha> / git describe --tags <sha>   # release 边界定位
git log --all --oneline --grep="<kw>"     # 全分支按 message 搜
git bisect start / bad / good <sha> / reset   # 二分定位「哪次改坏的」
```

**-S 与 -G 分工**:`-S` 数出现次数变化(净增/删才入史,重构换行可能漏);`-G` 按 diff 内容匹配(更全)。查符号名或重构,两者都跑再对答案。[经验: 代码调查 skill 实测结论]

### 工具边界(clone 前后用什么搜)

| 诉求 | 工具 |
| --- | --- |
| 远程/跨仓库,还没 clone | gh search(见 tool-gh.md 零节) |
| 本地工作区,最快、任意正则、无配额 | `rg` |
| 历史版本内容搜索 | `git grep <rev>` |
| 何时引入/演变 | `git log -S/-G`(pickaxe) |
| 结构级(免疫大小写/注释噪声) | `ast-grep run/outline` |

接力:**gh 定位(拿 blob/commit 双 sha)→ git clone → rg 锁文件 → git -S/blame 验历史**。结论落 `docs/research/` 标六态;研究用 clone 放临时区,用完即删。深挖全量命令见 外部调查 skill 的 git 取证指南 [经验: 外部代码调查 skill]。

## 一、提交规范

```powershell
git add <files>
git commit -m "feat: OCR 兜底落地 --ocr 进 extract 与 search"
```

| 前缀 | 用途 |
| --- | --- |
| `feat:` | 新功能 |
| `fix:` | 缺陷修复 |
| `docs:` | 纯文档变更 |
| `test:` | 测试变更 |
| `chore:` | 构建/配置/杂项 |

硬规则 [经验: reader 仓/PVE 仓 AGENTS 同款]:
- **一事一提交**:一次提交只做一件事;多事混一是审计污染
- **未经指示不做** `git commit` / `push` / `reset` / `rebase` / `force` 等变更操作(agent 协作场景)
- 提交信息中文描述 + 前缀;正文可多行(动机、影响面)

## 二、tag 发布流

```powershell
# 版本一致性:先改产物内版本号(Cargo.toml/pyproject 等),CI 有闸
git tag v0.4.0
git push origin v0.4.0        # tag 推送触发 release 流水线
```

- tag 名 = 版本号(`v` + semver),与产物内版本一致性由 CI 闸校验 [经验: reader 仓 release.yml]
- 打错 tag:本地 `git tag -d v0.4.0`;已推远端需 `git push origin :refs/tags/v0.4.0` 后重打——**已发 release 的 tag 不回退,发新补丁版** [经验]

## 三、平台坑(Windows / Linux / macOS)

| 坑 | 平台 | 根因 | 处理 |
| --- | --- | --- | --- |
| 行尾 CRLF/LF 混乱 | 全平台协作 | 各机 autocrlf 不一 | `.gitattributes` 钉死(`* text=auto eol=lf` 按语言细化),不靠个人配置 [经验: reader 仓 P0004] |
| 中文文件名显示成 `\xxx` 转义 | Windows | quotePath 默认 | `git config core.quotepath false` |
| 反斜杠路径进脚本打红远端测试 | Windows 惯性 | 分隔符硬编码 | 代码用 Path API;脚本参数化 [经验: reader 仓 M005] |
| Git Bash 落出 `nul` 保留名文件 | Windows | 保留名 | 避免重定向到 nul;误产文件用 `\\?\` 路径删 [经验: reader 仓 M008] |
| 文件系统大小写不敏感 | macOS(Windows 亦然) | HFS+/NTFS | 改名只变大小写要两步(`a.md`→`b.md`→`A.md`);import 路径按大小写敏感写(linux CI 会抓) [记忆] |
| 可执行位丢失 | Windows 提交 | NTFS 无 exec bit | 脚本加 shebang + `git update-index --chmod=+x`;或统一走解释器调用 [记忆] |
| 文件占用锁 | Windows | 句柄独占 | 关掉占用进程再操作;构建产物目录加 gitignore [记忆] |
| 行尾自动转换致二进制损坏 | 全平台 | autocrlf 误伤 | `.gitattributes` 对二进制后缀标 `-text` [经验] |

## 四、常用排查

```powershell
git log --oneline -10                     # 近期提交
git log --oneline v0.3.0..v0.4.0          # 两版之间的提交
git diff --stat HEAD~1                    # 上次提交改动面
git status -sb                            # 工作区 + 分支跟踪状态
git tag --sort=-creatordate | select -First 5   # 最新 tag
git remote -v                             # 远端配置
```

## 五、多机/接管协作

- 接管新机:`git clone` → 跑项目门禁 → 对照 `ROADMAP.md` 确认进度(不从对话记忆续接)
- 未推送的本地提交是单点风险:收工前确认 `git status -sb` 无 ahead 遗留

## 六、复验命令

```powershell
git --version
git config core.quotepath   # 应为 false(中文仓)
git status -sb              # 当前仓状态
```
