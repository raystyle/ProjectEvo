# A/B 夹具与期望

> 对照不是门禁。期望值写在本文件，不从扫描器抄。脚本 `scripts/ab.py` 种夹具、跑 A/B、打印对照表；人裁决回填 `docs/research/S006`。

夹具全是伪造值，禁止换成真实密钥。

| id | 位置 | 种入 | 期望 A secret-scan | 期望 B docs-evo scan |
| --- | --- | --- | --- | --- |
| ghp-work | 工作区 `ghp.txt` | `ghp_` + 36 字母 | 命中 GitHub token | 命中 GitHub token |
| stripe-work | 工作区 `stripe.txt` | `sk_live_` + 24 字母 | 命中 Stripe key | 不命中密钥规则 |
| gitlab-work | 工作区 `gitlab.txt` | `glpat-` + 20 字母 | 命中 GitLab token | 不命中密钥规则 |
| hist-ghp | 历史已删 `old.txt` | 同 ghp | 历史命中 GitHub token | 历史命中 GitHub token |
| hist-stripe | 历史已删 `old-stripe.txt` | 同 stripe | 历史命中 Stripe key | 不命中 |
| placeholder | 工作区 `ph.txt` | `password=changeme` | 不命中 assigned | 不命中 assigned |
| aws-example | 工作区 `aws.txt` | `AKIAIOSFODNN7EXAMPLE` | 命中 AWS（文档示例假阳） | 命中 AWS（假阳） |
| env-file | 工作区 `.env` | 任意文本 | 命中 sensitive file | 命中 sensitive file |
| email-pii | 工作区 `mail.txt` | `alice@gmail.com` | `--pii` 才命中 email | 不命中 |

B2 `uvx detect-secrets` 本机有网才跑；缺则 SKIP，不失败。gitleaks/trufflehog 本机未装则 SKIP。
