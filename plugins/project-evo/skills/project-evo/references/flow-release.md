# 封版发布模式：全平台门禁验收与 tag 触发

> 从「CHANGELOG Unreleased 有货」到「Release 资产验收」的封版操作手册。提炼自 reader 仓 R008（四轮发布实证：v0.1.0 至 v0.4.0）[经验： reader 仓 R008 及其验收记录]。

## 一、前置裁定

- **封版 = 发布一个新版本**：版本号必前进，不存在不改版本号的封版；封版件、tag 与 Release 资产同属一次发布
- **Unreleased 有条目才封版**；空则不发布
- 版本号取舍：能力新增或行为变化取次版本号（`0.x.0`），修复取补丁号（`0.x.y`）；与 ROADMAP 阶段对照
- 发布通道只走 stable；不做自动更新（self update 同口径）

## 二、全平台门禁验收（三路全绿才进封版）

按项目平台矩阵（env-platform.md）组织三路：

1. **主开发机**：代码门禁（lint/test 全 target，外部真样本缺失自动跳过）+ 文档门禁（lint/断链/规范机检）+ release 构建
2. **各平台实机**（每平台一台，ssh 接管）：`git pull --ff-only` 后同套门禁 + release 构建 + 真样本冒烟
3. **CI**：main 推送后平台矩阵 run 全绿

纪律 [经验： reader 仓 M006 等]：
- 验收命令**不接吞退出码的管道**（`| tail` 之类）
- 实机远程命令用**阶段标记串**逐段确认（`&& echo STAGE-OK`）
- 实机工具链与 CI 对齐（如 `rustup run stable`），防本机默认工具链差异
- **门禁与实跑互补，缺一不可**：门禁抓格式与回归，首跑实整抓逻辑缺口，源仓 heal all 首跑抓出两真缺口、CI 首跑抓限流、停栈实测抓单实例守卫缺口，全是门禁全绿下的漏网 [经验： ome 源仓 2026-09-03 得失]

## 三、封版件（一次提交）

1. **产物内版本号**改目标版本（CI 有 tag 一致性闸，不一致 job 直接红）
2. **CHANGELOG**：`[Unreleased]` 转为 `[<版本>] - <日期>`，正文只留版本级里程碑
3. **自动生成物重生**：含版本号的生成文件（SKILL.md、快照等）重生；注意 test 不重建产物，须先 build [实证： reader 仓 SKILL 重生坑]
4. **快照复审**：版本号入快照的，`.snap.new` 逐个人工审后入库
5. **门禁复跑**（本机全件）全绿后一次提交：`chore: 封版 v<版本>`

## 四、tag 触发发布

```powershell
git tag v<版本>
git push origin main v<版本>      # tag 推送即触发 release 流水线
```

流水线要点：tag 与产物版本一致性闸；`--locked`/可复现构建；每平台打包（二进制 + README/LICENSE/SKILL + `.sha256` 校验件）上传 Release [经验： reader 仓 release.yml 五 job 模式]。

## 五、发布验收

- release run 各 job 全绿（重依赖平台的构建是风险点）
- **资产件数齐**：平台数 ×（压缩包 + `.sha256`)
- 抽查三件：`.sha256` 校验过、解包 `--version` 冒烟过、self update（如有）报已最新
- 本机与 CI 资产 sha 不一致属预期（构建机差异），一致性以官方 `.sha256` 为准 [实证： reader 仓 v0.3.0 轮]
- **收尾义务**（对齐 AGENTS 义务表「发布」行）：CHANGELOG 已定版、ROADMAP 阶段状态翻转、diary 当天钩子

## 六、验收入壳（随验收回填）

验收记录落在本文档尾部或 proven 方案内：各路退出码/阶段标记、run id、资产清单、抽查结果、当轮发现的新坑（进 mistakes）。reader 仓 模式：每次发布一段验收记录，含实测量级与首验项 [经验： R008 验收记录两轮]。

## 七、与体系其它件的衔接

| 环节 | 依据 |
| --- | --- |
| Unreleased 起步与转版 | flow-workflow.md 归档步 + base-primitives.md 义务表「发布」行 |
| tag 纪律与一致性闸 | tool-git.md 二节 |
| release 资产上传/验收 | tool-gh.md 二节 |
| 平台矩阵与实机接管 | env-platform.md 六/七节 |
| 环境依赖（实机工具链） | env-environment.md(ome status 盘点） |
