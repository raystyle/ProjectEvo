"""secret-scan 脚本:工作区/历史命中、脱敏、GitHub 参数校验。"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "plugins" / "secret-scan" / "skills" / "secrets" / "scripts"


def _load():
    spec = importlib.util.spec_from_file_location("pevo_secret_scan", SCRIPTS / "scan.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


scan_mod = _load()
TOKEN = "ghp_" + ("A" * 36)


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        env={
            **os.environ,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
        },
    )


def test_worktree_finds_github_token(tmp_path: Path):
    (tmp_path / "cfg.txt").write_text(f"token = {TOKEN}\n", encoding="utf-8")
    finds, notes = scan_mod.run_scan(tmp_path, history=False, pii=False, github=None, clone_history=False)
    assert not notes
    assert any(f["rule"] == "GitHub token" for f in finds)
    joined = " ".join(f["snippet"] for f in finds)
    assert TOKEN not in joined


def test_history_finds_deleted_token(tmp_path: Path):
    _git(tmp_path, "init", "-b", "main")
    (tmp_path / "cfg.txt").write_text(f"token = {TOKEN}\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-m", "leak")
    (tmp_path / "cfg.txt").unlink()
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-m", "remove")
    finds = scan_mod.scan_history(tmp_path, pii=False)
    assert any(f["rule"] == "GitHub token" and f["source"] == "history" for f in finds)
    joined = " ".join(f["snippet"] for f in finds)
    assert TOKEN not in joined


def test_cli_github_requires_owner_repo(tmp_path: Path):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "scan.py"), "--github", "nopath", "--no-cwd"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert r.returncode == 2
    assert "owner/repo" in r.stderr


def test_ab_matches_oracle():
    """A/B 对照脚本退出 0，且每条与 ab-cases 期望一致（对照本身不作门禁胜负）。"""
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "ab.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["cases"], "夹具不得为空"
    assert all(c["A_match_exp"] and c["B_match_exp"] for c in data["cases"]), data["cases"]


def test_cli_json_clean(tmp_path: Path):
    (tmp_path / "ok.txt").write_text("hello\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "scan.py"), str(tmp_path), "--no-history", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["findings"] == []
