# TypeScript/Node 项目工程

> 本文件 = Node/TS 仓怎么建、怎么验（运行时、tsc、测试、依赖、打包）；与 tool-project.md（Python `.tools`）分栈；与 tool-selection.md（出仓选型）分工：本篇是落地后的工程合同。浏览器检索见 `super-research:research`；agent 脚本 workspace 见 tool-cli-agents.md。提炼自 D:\browser-harness-ts 的 package.json、tsconfig、R001、M101 至 M103、P0001 [实证: 2026-09-08 对照源仓]。

## 一、运行时合同

- `"type": "module"`；`engines.node` 钉 `>=22`（源仓本机 Node 24.20）
- 先用 Node 内置：WebSocket、fetch、`node:sqlite`、child_process、path、test。内置能做的不进 dependencies
- 入口面一次定义：`bin`（CLI）、`main` / `types` / `exports`（库）、`files` 白名单（只出 dist、技能、资产、README、LICENSE；不出 src 与 tsconfig）

## 二、tsc 合同

家族默认编译器选项（按项目可裁，砍严选项须写理由）：

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "declaration": true,
    "incremental": true,
    "skipLibCheck": true,
    "types": ["node"]
  }
}
```

含义速记：

- NodeNext 加 verbatimModuleSyntax：`.ts` 里 import 写 `.js` 扩展名
- isolatedModules：禁跨文件 const enum 一类只靠 tsc 的技巧，给以后换打包器留退路
- noUncheckedIndexedAccess：索引访问当可能 undefined

核心包用 `tsc -p tsconfig.json` 出 dist/（含 .d.ts）。不要把 CLI 或库打成单文件 bundle。

## 三、运行时依赖白名单

- dependencies 白名单制：新增 runtime 依赖走 PRD 采纳。家族实证现役仅 commander（CLI 解析）与 zod（环境变量与选项校验）[实证: browser-harness-ts D29]
- devDependencies 从宽：typescript、`@types/node`、esbuild（仅浏览器 IIFE 产物需要时）
- 出仓前再问「Node 内置有没有」（接 tool-selection 阶梯 2 到 5 档）

## 四、构建分面

| 面 | 工具 | 产物 | 约束 |
| --- | --- | --- | --- |
| 核心包 / CLI | tsc | dist/*.js 加 .d.ts | 类型面与运行面同源 |
| 浏览器侧车 SDK | esbuild（devDependency） | 自包含 IIFE，进 git | 产物零 runtime 依赖 |
| 协议 / IDL 生成 | 仓内 gen 脚本 | `src/generated.ts` 一类 | 禁止手改；换源后 gen 再测 |

保真判据（有上游生成物时）：与上游 diff 只允许头注释差异 [实证: 2026-09-04 源仓首次生成对账]。

## 五、测试

家族 TypeScript 默认载体是 **node:test**（Node 内置），不是 vitest [实证: browser-harness-ts `npm test`]。

```powershell
npm test   # build + typecheck:apps + node --test "dist/*.test.js"
```

硬规则：

1. 先 tsc 再测编译产物；测试与源码同目录 `src/*.test.ts`，邻模块 import 写 `.js`
2. glob **必须带引号**：`node --test "dist/*.test.js"`。Windows git-bash 裸 glob 把目录当参数解析会炸 [实证: M002，已固化进 package.json]
3. 测试钉临时 HOME / 数据根，禁止碰安装态与开发态家目录 [实证: paths.test.ts sandbox]
4. 混有 `.mjs` 插件或应用时另立 `tsconfig.apps.json`：`allowJs` + `checkJs` + `noEmit`，纳入 `npm test`（`typecheck:apps`）[实证: D32]
5. 外部依赖缺失 skip，不失败不伪造（与 flow-testing 闸门同构）

vitest 可作意图层替代；新仓无理由不跟 node:test。

## 六、路径

一律 `node:path` API 拼接，禁止手拼 `\` 或 `/`（env-platform 同款，TS 落点是 `node:path`）。

## 七、开发态 vs 安装验收

npm CLI 包有两套家，禁止混用 [实证: M014]。

判定：包根有没有 `tsconfig.json`（`files` 不含此文件）。有 = 开发态，没有 = 安装态。

| | 开发 | 安装验收 |
| --- | --- | --- |
| 入口 | `node dist/cli.js` 或 `npm link` | `npm pack` 再 `npm install -g ./<name>-*.tgz`，只用 PATH 上的命令 |
| 数据根 | 仓内 `.xxx-dev` | 用户配置目录 |
| 禁 | 从仓库起看板或守护去看安装态数据 | `npm install -g .` 与把 link 当安装验收（包根仍能看见 tsconfig，会被判成开发态） |

给人看的验收走 pack tgz，不要 link。

## 八、环境解析与空串

坏的配置值不得在 import 时把进程打死：缺省、非法、`<=0` 回落到默认。zod `safeParse`，不 throw [实证: src/env.ts D29]。

空串不是缺省：失败时 `ErrorEvent.message` 一类字段给 `""`，`?? fallback` 不触发。取值用 truthiness，不用 `??` 链 [实证: M001]。

## 九、Windows 进程与锁

- fnm 下 `Get-Command npm` 是 `npm.ps1`，`spawnSync('npm.cmd')` 无 PATH 直调失败（status null）。改走与 `node.exe` 同目录的 `node npm-cli.js` [实证: M016]
- 无内核锁时，时间维抢占（`stealAfterMs: 30s`）会偷活锁。只认 pid 死亡，不要用超时当锁失效 [实证: M007]
- 事件匹配键只用稳定必填字段，不用协议里 deprecated 且 optional 的字段 [实证: M018]

## 十、CI 与封版

CI：`fail-fast: false`；矩阵 os（ubuntu / windows / macos）乘 node（22、24）；步骤 `npm ci` + `npm test` [实证: browser-harness-ts `.github/workflows/ci.yml`]。本地过了 CI 不过，以 CI 为准修。

封版（接 flow-release.md）：

1. `package.json` 与 `package-lock.json` 两处 version 同步
2. `npm test` 全绿
3. `npm pack` 到 `npm install -g ./<name>-*.tgz` 到 `--version` 对版 到 安装态冒烟
4. tag

`prepack` 钩子跑 build，保证 tgz 含最新 dist。

## 十一、架构经验一条

语义层对传输无关的 Host 接口编程，CLI / 插件 / worker 复用同一套 helpers，不产生第二套语义实现 [经验: P0001 源仓移植最有价值的一条]。脚本 workspace 的落位与增量供给见 tool-cli-agents.md。

## 十二、验收清单

- engines.node 与 CI 矩阵下限一致
- tsc 合同就位；import 扩展名 `.js`
- runtime 依赖白名单外无暗增
- `npm test` glob 带引号；测试不碰真实家目录
- 安装验收走 pack tgz，不走 link
- 路径只经 `node:path`
- 生成物禁手改
