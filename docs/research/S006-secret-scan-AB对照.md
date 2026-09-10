# secret-scan 与 docs-evo scan A/B 对照

- 状态:已完成
- 日期:2026-09-08
- 关联:[S005](S005-git密钥隐私扫描skill选型.md)；夹具 `plugins/secret-scan/skills/secrets/verification/ab-cases.md`

> 对照不是门禁。A = `secret-scan` `scan.py`；B = `docs-evo` `scan.py` 的 secrets 部分。人裁决。伪造密钥，无真实凭据。

## 背景

S005 只做了文献对照，没有同夹具实跑。`flow-testing` 规定 A/B 是对比、结论回填 S 文档。用户指出 secret-scan 缺这一步。

本机无 gitleaks、无 trufflehog，B2 跳过。未默认 `uvx detect-secrets`（会拉第三方包）。

## 关键结论

1. **九条夹具期望两侧全中。** `uv run scripts/ab.py` 对每条 `A_match_exp` 与 `B_match_exp` 均为 true。[实证: 2026-09-08 本机 ab.py]
2. **A 比 B 多抓的是规则面，不是历史能力。** 共有的 GitHub token（工作区与已删提交）、`.env` 文件、AWS 文档示例假阳、`password=changeme` 占位，两边一致。A 独有：Stripe `sk_live_`、GitLab `glpat-`、以及 `--pii` 邮箱。[实证: 对照表 A_minus_B]
3. **两边都把 AWS 文档示例 `AKIAIOSFODNN7EXAMPLE` 当真密钥。** 这是假阳，不因此否定 A；要消须单独加示例白名单，本轮不加。[实证: aws-example 两侧 true]
4. **B2 未跑，不能声称优于 gitleaks。** 规则库仍窄于 gitleaks。[记忆: 本机未装；要进实证需装后重跑 ab 夹具]

## 对照表

脚本输出：A 16 条发现，B 9 条（含规则重叠与历史去重差异，不以条数论胜负）。

| id | A | B | 期望 A/B | 裁决 |
| --- | --- | --- | --- | --- |
| ghp-work | 是 | 是 | 是/是 | 共有能力 |
| stripe-work | 是 | 否 | 是/否 | A 增补 |
| gitlab-work | 是 | 否 | 是/否 | A 增补 |
| hist-ghp | 是 | 是 | 是/是 | 历史能力共有 |
| hist-stripe | 是 | 否 | 是/否 | A 增补覆盖已删提交 |
| placeholder | 否 | 否 | 否/否 | 占位未误报 |
| aws-example | 是 | 是 | 是/是 | 共有假阳 |
| env-file | 是 | 是 | 是/是 | 敏感文件共有 |
| email-pii | 是 | 否 | 是/否 | 仅 A `--pii` |

## 裁决

继续用 A 做密钥/隐私深挖，B 留在 docs-evo 做浅密钥加 markdown 禁字。不把 gitleaks 绑进运行时。GitHub alerts/`--clone-history` 本轮夹具未覆盖，仍是 S005 的推断，不算本对照实证。

复跑：`uv run plugins/secret-scan/skills/secrets/scripts/ab.py`
