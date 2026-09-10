# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""A/B 对照:secret-scan(A) vs docs-evo scan(B)。对照不是门禁,退出码 0。

用法: uv run ab.py
在临时 git 仓种伪造密钥,跑两侧,stdout 打 JSON 对照表。
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
DOCS_EVO_SCAN = REPO / "plugins" / "project-evo" / "skills" / "docs-evo" / "scripts" / "scan.py"
GHP = "ghp_" + ("A" * 36)
STRIPE = "sk_live_" + ("B" * 24)
GLPAT = "glpat-" + ("C" * 20)
AWS_DOC = "AKIAIOSFODNN7EXAMPLE"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _git(cwd: Path, *args: str) -> None:
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t.test",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t.test",
    }
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, env=env)


def _plant(root: Path) -> None:
    _git(root, "init", "-b", "main")
    (root / "old.txt").write_text(f"token={GHP}\n", encoding="utf-8")
    (root / "old-stripe.txt").write_text(f"{STRIPE}\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "hist")
    (root / "old.txt").unlink()
    (root / "old-stripe.txt").unlink()
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "drop")
    (root / "ghp.txt").write_text(f"token={GHP}\n", encoding="utf-8")
    (root / "stripe.txt").write_text(f"{STRIPE}\n", encoding="utf-8")
    (root / "gitlab.txt").write_text(f"{GLPAT}\n", encoding="utf-8")
    (root / "ph.txt").write_text("password=changeme\n", encoding="utf-8")
    (root / "aws.txt").write_text(f"key={AWS_DOC}\n", encoding="utf-8")
    (root / ".env").write_text("x=1\n", encoding="utf-8")
    (root / "mail.txt").write_text("alice@gmail.com\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "work")


def _rules(finds: list[dict], source: str | None = None) -> set[str]:
    out = set()
    for f in finds:
        if source and f.get("source") != source:
            continue
        out.add(f"{f.get('file')}|{f.get('rule')}|{f.get('source', '-')}")
    return out


def _has(finds: list[dict], file: str, rule_sub: str, source: str | None = None) -> bool:
    for f in finds:
        if file not in str(f.get("file", "")):
            continue
        if rule_sub.lower() not in str(f.get("rule", "")).lower():
            continue
        if source and f.get("source") != source:
            continue
        return True
    return False


def _docs_evo_has(finds: list[dict], file: str, rule_sub: str, history: bool | None = None) -> bool:
    for f in finds:
        if file not in str(f.get("file", "")):
            continue
        if rule_sub.lower() not in str(f.get("rule", "")).lower():
            continue
        commit = str(f.get("commit") or "-")
        is_hist = commit not in ("-", "")
        if history is True and not is_hist:
            continue
        if history is False and is_hist:
            continue
        return True
    return False


def main() -> int:
    a_mod = _load(HERE / "scan.py", "ab_a")
    b_mod = _load(DOCS_EVO_SCAN, "ab_b")
    with tempfile.TemporaryDirectory(prefix="pevo-ab-") as td:
        root = Path(td)
        _plant(root)
        a_finds, _ = a_mod.run_scan(root, history=True, pii=True, github=None, clone_history=False)
        b_finds = b_mod.scan_worktree_secrets(root) + b_mod.scan_history_secrets(root)

        cases = [
            ("ghp-work", _has(a_finds, "ghp.txt", "GitHub token", "worktree"), _docs_evo_has(b_finds, "ghp.txt", "GitHub token", False), True, True),
            ("stripe-work", _has(a_finds, "stripe.txt", "Stripe", "worktree"), _docs_evo_has(b_finds, "stripe.txt", "Stripe", False), True, False),
            ("gitlab-work", _has(a_finds, "gitlab.txt", "GitLab", "worktree"), _docs_evo_has(b_finds, "gitlab.txt", "GitLab", False), True, False),
            ("hist-ghp", _has(a_finds, "old.txt", "GitHub token", "history"), _docs_evo_has(b_finds, "old.txt", "GitHub token", True), True, True),
            ("hist-stripe", _has(a_finds, "old-stripe.txt", "Stripe", "history"), _docs_evo_has(b_finds, "old-stripe.txt", "Stripe", True), True, False),
            ("placeholder", _has(a_finds, "ph.txt", "assigned", "worktree"), _docs_evo_has(b_finds, "ph.txt", "assigned", False), False, False),
            ("aws-example", _has(a_finds, "aws.txt", "AWS", "worktree"), _docs_evo_has(b_finds, "aws.txt", "AWS", False), True, True),
            ("env-file", _has(a_finds, ".env", "sensitive file", "worktree"), _docs_evo_has(b_finds, ".env", "sensitive file", False), True, True),
            ("email-pii", _has(a_finds, "mail.txt", "email", "worktree"), _docs_evo_has(b_finds, "mail.txt", "email", False), True, False),
        ]
        rows = []
        for cid, a_hit, b_hit, exp_a, exp_b in cases:
            rows.append({
                "id": cid,
                "A": a_hit,
                "B_docs_evo": b_hit,
                "exp_A": exp_a,
                "exp_B": exp_b,
                "A_match_exp": a_hit is exp_a,
                "B_match_exp": b_hit is exp_b,
                "A_minus_B": a_hit and not b_hit,
            })

        b2 = "SKIP:gitleaks/trufflehog 未装;detect-secrets 可选 uvx 未在本脚本默认拉取"
        report = {
            "A": "secret-scan scan.py",
            "B": "docs-evo scan.py secrets 部分",
            "B2": b2,
            "A_count": len(a_finds),
            "B_count": len(b_finds),
            "cases": rows,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
